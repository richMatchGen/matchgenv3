from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import viewsets, permissions
from .models import Club, SocialAccount, Player
from .serializers import UserSerializer, ClubSerializer, SocialAccountSerializer, PlayerSerializer, MatchSerializer
from rest_framework.permissions import IsAuthenticated
from .utils import generate_caption
from django.http import JsonResponse
from .image_utils import add_text_to_image,overlay_logo, generate_fulltime, generate_halftime,generate_starting_xi,generate_post,generate_goal_alert,get_template_path
from django.conf import settings
from PIL import Image, ImageDraw, ImageFont
from rest_framework.parsers import MultiPartParser, FormParser
from .social_posting import post_to_twitter, post_to_facebook
from rest_framework import status
from django.contrib.auth.hashers import make_password
import os

from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user_profile(request):
    """
    API to fetch user profile information.
    """
    user = request.user
    return Response({
        "username": user.username,
        "email": user.email,
    })

@api_view(["GET"])
@permission_classes([IsAuthenticated])  # ✅ Requires JWT Token
def get_protected_message(request):
    return Response({"message": f"Hello {request.user.username}, this is a protected route!"})

@api_view(['GET'])
@permission_classes([AllowAny])
def get_message(request):
    return Response({"message": "Hello from Django API!"})

@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_starting_xi(request):
    """
    API to update the Starting XI of a club.
    """
    try:
        club = Club.objects.get(owner=request.user)
    except Club.DoesNotExist:
        return Response({"error": "Club not found"}, status=status.HTTP_404_NOT_FOUND)

    selected_players = request.data.get("starting_xi", [])

    # Reset all players to not be in Starting XI
    Player.objects.filter(club=club).update(is_starting_xi=False)

    # Mark selected players as Starting XI
    Player.objects.filter(id__in=selected_players, club=club).update(is_starting_xi=True)

    return Response({"message": "Starting XI updated successfully!"})



# User Authentication API
@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user:
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })
    return Response({'error': 'Invalid Credentials'}, status=400)


@api_view(['POST'])
def register_user(request):
    """
    API endpoint to register new users.
    """
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')

    if not username or not email or not password:
        return Response({'error': 'All fields are required'}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(email=email).exists():
        return Response({'error': 'Email already in use'}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(username=username, email=email, password=password)
    return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    if request.method == 'GET':
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_user_profile(request):
    """
    API to update user profile details (username & email).
    """
    user = request.user
    data = request.data

    if "username" in data:
        if User.objects.filter(username=data["username"]).exclude(id=user.id).exists():
            return Response({"error": "Username already taken."}, status=status.HTTP_400_BAD_REQUEST)
        user.username = data["username"]

    if "email" in data:
        if User.objects.filter(email=data["email"]).exclude(id=user.id).exists():
            return Response({"error": "Email already in use."}, status=status.HTTP_400_BAD_REQUEST)
        user.email = data["email"]

    user.save()
    return Response({"message": "Profile updated successfully!"})

@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def change_password(request):
    """
    API to change user password.
    """
    user = request.user
    data = request.data

    old_password = data.get("old_password")
    new_password = data.get("new_password")

    if not old_password or not new_password:
        return Response({"error": "Both old and new passwords are required."}, status=status.HTTP_400_BAD_REQUEST)

    if not user.check_password(old_password):
        return Response({"error": "Incorrect old password."}, status=status.HTTP_400_BAD_REQUEST)

    user.password = make_password(new_password)
    user.save()
    return Response({"message": "Password updated successfully!"})

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_club(request):
    """
    API to create a club for the logged-in user.
    """
    if Club.objects.filter(owner=request.user).exists():
        return Response({"error": "User already has a club."}, status=status.HTTP_400_BAD_REQUEST)

    data = request.data.copy()
    data["owner"] = request.user.id
    serializer = ClubSerializer(data=data)

    if serializer.is_valid():
        serializer.save(owner=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_club(request):
    """
    API to fetch the logged-in user's club details.
    """
    print(request.user.id)

    try:
        club = Club.objects.get(owner_id=request.user.id)
        serializer = ClubSerializer(club)
        return Response(serializer.data)
    except Club.DoesNotExist:
        return Response({"error": "Club not found."}, status=status.HTTP_404_NOT_FOUND)

@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_club(request):
    """
    API to update club details, including logo.
    """
    try:
        club = Club.objects.get(owner=request.user)
    except Club.DoesNotExist:
        return Response({"error": "Club not found."}, status=status.HTTP_404_NOT_FOUND)

    serializer = ClubSerializer(club, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def upload_club_logo(request):
    """
    API to upload a new club logo.
    """
    parser_classes = [MultiPartParser, FormParser]

    try:
        club = Club.objects.get(owner=request.user)
    except Club.DoesNotExist:
        return Response({"error": "Club not found."}, status=status.HTTP_404_NOT_FOUND)

    if "logo" not in request.FILES:
        return Response({"error": "No file uploaded."}, status=status.HTTP_400_BAD_REQUEST)

    club.logo = request.FILES["logo"]
    club.save()

    return Response({"message": "Club logo uploaded successfully!", "logo_url": club.logo.url})



@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_squad(request):
    """ Fetch squad for logged-in user's club """
    try:
        club = Club.objects.get(owner=request.user)
        players = Player.objects.filter(club=club)
        serializer = PlayerSerializer(players, many=True)
        return Response(serializer.data)
    except Club.DoesNotExist:
        return Response({"error": "Club not found"}, status=status.HTTP_404_NOT_FOUND)



@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_player(request):
    """ Add a player to the squad """
    try:
        club = Club.objects.get(owner=request.user)
    except Club.DoesNotExist:
        return Response({"error": "Club not found"}, status=status.HTTP_404_NOT_FOUND)

    data = request.data.copy()
    data["club"] = club.id
    serializer = PlayerSerializer(data=data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_match(request):
    """ Create a new match fixture """
    try:
        club = Club.objects.get(owner=request.user)
    except Club.DoesNotExist:
        return Response({"error": "Club not found"}, status=status.HTTP_404_NOT_FOUND)

    data = request.data.copy()
    data["club"] = club.id
    serializer = MatchSerializer(data=data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Club ViewSet
class ClubViewSet(viewsets.ModelViewSet):
    queryset = Club.objects.all()
    serializer_class = ClubSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)  # ✅ Allow file uploads

    def get_queryset(self):
        return Club.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class SocialAccountViewSet(viewsets.ModelViewSet):
    serializer_class = SocialAccountSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Return only the logged-in user's social accounts"""
        return SocialAccount.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Automatically associate the logged-in user with the social account"""
        serializer.save(user=self.request.user)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generate_ai_caption(request):
    """
    API to generate an AI-powered caption for a match.
    """
    match_info = request.data
    caption = "testing captions"
    return Response({"caption": caption})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generate_graphic(request):

    """
    API to generate match graphics dynamically based on user selection.
    """
    try:
        # User selects club and post type
        club = request.data.get("club", "modern")  # Default template pack
        template_type = request.data.get("template_type")  # fulltime, halftime, goal_alert, starting_xi

        # Generate the correct filename
        output_filename = f"{template_type}_{club}.png"
        output_image = os.path.join(settings.MEDIA_ROOT, "generated", output_filename)

        # Handle each post type separately
        if template_type == "fulltime":
            score = request.data.get("score", "0-0")
            generate_fulltime(club, score, output_image)

        elif template_type == "halftime":
            score = request.data.get("score", "0-0")
            generate_halftime(club, score, output_image)

        elif template_type == "goal_alert":
            goal_scorer = request.data.get("goal_scorer", "Unknown Player")
            team = request.data.get("team", "Unknown Team")
            minute = request.data.get("minute", "90")
            generate_goal_alert(club, goal_scorer, team, minute, output_image)

        elif template_type == "starting_xi":

            team_name = request.data.get("team_name", "Unknown Team")
            players = request.data.get("players", [])
            generate_starting_xi(club, team_name, players, output_image)

            print(players)
            print("players above")
        else:
            return Response({"error": "Invalid template type."}, status=400)

        return Response({
            "image_url": f"http://127.0.0.1:8000/media/generated/{output_filename}",
            "message": "✅ Graphic successfully created!"
        })

    except Exception as e:
        return Response({"error": str(e)}, status=400)



# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def generate_graphic(request):
#     """
#     API to overlay text onto a final whistle graphic.
#     """
#     try:
#         text = request.data.get("text", "FULL TIME")
#         position = request.data.get("position", [50, 50])
#         font_size = request.data.get("font_size", 40)
#         club_logo = request.data.get("club_logo", None)
#
#         # Ensure position is a tuple
#         position = tuple(map(int, position))
#
#         # Define paths (Make sure MEDIA_ROOT is used)
#         input_image = os.path.join(settings.STATICFILES_DIRS[0], "templates/final_whistle.png")
#         output_filename = f"final_whistle_{text.replace(' ', '_')}.png"
#         output_image = os.path.join(settings.MEDIA_ROOT, output_filename)
#
#         # Debugging
#         print(f"🔹 Saving image at: {output_image}")
#
#         # Process image
#         add_text_to_image(input_image, text, output_image, position, font_size)
#
#         # Overlay club logo if provided
#         if club_logo:
#             logo_path = os.path.join(settings.MEDIA_ROOT, "club_logos", club_logo)
#             overlay_logo(output_image, logo_path, output_image)
#
#         # Get posting preferences
#         post_twitter = request.data.get("post_twitter", False)
#         # post_facebook = request.data.get("post_facebook", False)
#
#         twitter_result = None
#         # facebook_result = None
#
#         # Post to Twitter
#         if post_twitter:
#             caption = f"🔥 {text} 🔥 #MatchGen"
#             print(caption)
#             twitter_result = post_to_twitter(request.user,output_image, caption)
#
#         # # Post to Facebook
#         # if post_facebook:
#         #     caption = f"🚨 Match Update: {text} 🚨"
#         #     facebook_result = post_to_facebook(output_image, caption)
#
#         # Verify file existence after saving
#         if os.path.exists(output_image):
#             print("✅ Image successfully saved!")
#         else:
#             print("❌ Image NOT saved!")
#
#         # return Response({
#         #     "image_url": f"http://127.0.0.1:8000/media/{output_filename}",
#         #     "twitter_post": twitter_result,
#         #     # "facebook_post": facebook_result
#         # })
#
#         return Response({
#             "image_url": f"http://127.0.0.1:8000/media/{output_filename}",
#             "message": "✅ Graphic successfully created."
#         })
#
#         # return Response({"image_url": f"{settings.MEDIA_URL}{output_filename}"})
#
#     except Exception as e:
#         print(f"⚠️ Error: {str(e)}")
#         return Response({"error": str(e)}, status=400)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def link_twitter(request):
    """
    API to save a user's Twitter access token.
    """
    access_token = request.data.get("access_token")
    access_token_secret = request.data.get("access_token_secret")

    if not access_token or not access_token_secret:
        return Response({"error": "Missing access tokens"}, status=400)

    # Save or update the Twitter access token
    social_account, created = SocialAccount.objects.update_or_create(
        user=request.user,
        platform="twitter",
        defaults={"access_token": access_token, "access_token_secret": access_token_secret},
    )

    return Response({"status": "success", "message": "Twitter account linked successfully."})

# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def update_twitter_token(request):
#     """
#     API to update the Twitter access token.
#     """
#     access_token = request.data.get("access_token")
#     access_token_secret = request.data.get("access_token_secret")
#
#     if not access_token or not access_token_secret:
#         return Response({"error": "Missing access tokens"}, status=400)
#
#     # Save or update the Twitter access token
#     social_account, created = SocialAccount.objects.update_or_create(
#         user=request.user,
#         platform="twitter",
#         defaults={"access_token": access_token, "access_token_secret": access_token_secret},
#     )
#
#     return Response({"status": "success", "message": "Twitter token updated successfully."})

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def generate_starting_xi_graphic(request):
    """
    API to generate a Starting XI graphic based on the selected lineup.
    """
    try:
        club = Club.objects.get(owner=request.user)
        players = request.data.get("players", [])  # Expecting a list of player names
        output_filename = f"starting_xi_{club.name.replace(' ', '_')}.png"
        output_image = os.path.join(settings.MEDIA_ROOT, output_filename)

        # Debugging Information
        print(f"🔍 Club: {club.name}")
        print(f"🔍 Players: {players}")
        print(f"🔍 Output Image: {output_image}")

        # Get Template Path
        template_path = get_template_path(club.name, "starting_xi")
        print(f"✅ Template Path: {template_path}")

        generate_starting_xi(club.name, players, output_image)

        return Response({
            "image_url": f"http://127.0.0.1:8000/media/{output_filename}",
            "message": "✅ Starting XI graphic successfully created."
        })
    except Club.DoesNotExist:
        return Response({"error": "Club not found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print(f"❌ API Error: {e}")  # Debugging
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter
from .views import generate_starting_xi_graphic,login_user, register_user, user_profile, ClubViewSet, SocialAccountViewSet, generate_ai_caption, generate_graphic, link_twitter, get_message, get_protected_message, get_user_profile, update_user_profile, change_password, create_club,get_club,update_club,upload_club_logo, get_squad, add_player, create_match,update_starting_xi

router = DefaultRouter()
router.register(r'clubs', ClubViewSet, basename='club')
router.register(r'social-accounts', SocialAccountViewSet, basename='socialaccount')

urlpatterns = [
    path('message/', get_message, name="get_message"),
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),  # ✅ Get JWT Token
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),  # ✅ Refresh Token
    path('register/', register_user, name="register_user"),
    path('profile/', user_profile, name='profile'),
    path('', include(router.urls)),  # Includes `/api/clubs/`
    path('generate-caption/', generate_ai_caption, name='generate_caption'),
    path("generate-graphic/", generate_graphic, name="generate_graphic"),
    path('link-twitter/', link_twitter, name='link_twitter'),
    path("protected/", get_protected_message, name="protected"),
    path("profile/", get_user_profile, name="user-profile"),
    path("profile/update/", update_user_profile, name="update-profile"),
    path("change-password/", change_password, name="change-password"),
    path("club/", create_club, name="create-club"),
    path("club/details/", get_club, name="get-club"),
    path("club/update/", update_club, name="update-club"),
    path("club/upload-logo/", upload_club_logo, name="upload-club-logo"),
    path("squad/", get_squad, name="get-squad"),
    path("squad/add/", add_player, name="add-player"),
    path("match/", create_match, name="create-match"),
    path("squad/update-starting-xi/", update_starting_xi, name="update-starting-xi"),
    path("generate-starting-xi/", generate_starting_xi_graphic, name="generate-starting-xi"),

]

import tweepy
import requests
import os
from django.conf import settings
from .models import SocialAccount


def post_to_twitter(user, image_path, caption):
    """
    Posts the final whistle graphic to Twitter using the user's access token.
    """
    try:
        # Retrieve user's Twitter access token
        social_account = SocialAccount.objects.filter(user=user, platform="twitter").first()
        if not social_account:
            return {"status": "error", "message": "User has not linked their Twitter account."}

        # Authenticate with Twitter API using the stored token
        auth = tweepy.OAuth1UserHandler(
            settings.TWITTER_API_KEY,
            settings.TWITTER_API_SECRET,
            social_account.access_token,
            social_account.access_token_secret
        )
        api = tweepy.API(auth)

        # Upload image
        media = api.media_upload(image_path)

        # Post tweet with caption
        tweet = api.update_status(status=caption, media_ids=[media.media_id])
        return {"status": "success", "tweet_id": tweet.id_str}

    except Exception as e:
        return {"status": "error", "message": str(e)}


def post_to_facebook(image_path, caption):
    """
    Posts the final whistle graphic to a Facebook page.
    """
    try:
        url = "https://graph.facebook.com/v12.0/me/photos"
        params = {
            "caption": caption,
            "access_token": settings.FACEBOOK_PAGE_ACCESS_TOKEN
        }
        files = {'source': open(image_path, 'rb')}

        response = requests.post(url, files=files, data=params)
        return response.json()

    except Exception as e:
        return {"status": "error", "message": str(e)}

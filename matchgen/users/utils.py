import openai
from django.conf import settings

import openai
from django.conf import settings

def generate_caption(match_info):
    """
    Generate AI-powered sports captions based on match details.
    """
    client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)  # New OpenAI Client

    prompt = f"Generate a Twitter-style sports update for {match_info['team1']} vs {match_info['team2']} at {match_info['stadium']}. Score: {match_info['score']}."

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # Use the latest GPT-4 Turbo model
        messages=[{"role": "system", "content": prompt}],
        temperature=0.7,
        max_tokens=100
    )

    return response.choices[0].message.content.strip()

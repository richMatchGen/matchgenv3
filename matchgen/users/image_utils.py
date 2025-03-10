from PIL import Image, ImageDraw, ImageFont
import os
from django.conf import settings

import cv2
import numpy as np

def ensure_png_format(image_path):
    """
    Converts the image to PNG if it's not already in PNG format.
    """
    if not image_path.lower().endswith(".png"):
        img = Image.open(image_path)
        new_path = image_path.replace(".jpg", ".png").replace(".jpeg", ".png")
        img.save(new_path, "PNG")
        print(f"✅ Converted to PNG: {new_path}")
        return new_path  # Return the new PNG path
    return image_path  # If already PNG, return original


def remove_background_opencv(image_path):
    """
    Removes background using OpenCV and makes the image transparent.
    """
    try:
        img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)

        # Convert to grayscale and apply threshold
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, mask = cv2.threshold(gray, 230, 255, cv2.THRESH_BINARY)

        # Create an alpha channel (transparency)
        alpha = cv2.bitwise_not(mask)
        b, g, r = cv2.split(img)
        rgba = [b, g, r, alpha]

        # Merge into an RGBA image (with transparency)
        transparent_img = cv2.merge(rgba)

        # Save with transparent background
        output_path = image_path.replace(".png", "_transparent.png")
        cv2.imwrite(output_path, transparent_img)
        print(f"✅ Background removed with OpenCV: {output_path}")

        return output_path
    except Exception as e:
        print(f"❌ Error removing background: {e}")
        return image_path  # Return original image if error occurs


def add_text_to_image(input_image, text, output_image, position, font_size, font_path=None, color=(255, 255, 255), shadow=False):
    """
    Adds text to an image with optional shadow for better visibility.
    """
    try:
        img = Image.open(input_image).convert("RGBA")
        draw = ImageDraw.Draw(img)

        # Load font
        if not font_path:
            font_path = os.path.join(settings.BASE_DIR, "users/fonts/comicbd.ttf")
        font = ImageFont.truetype(font_path, font_size)

        if shadow:
            shadow_offset = 2
            shadow_position = (position[0] + shadow_offset, position[1] + shadow_offset)
            draw.text(shadow_position, text, font=font, fill=(0, 0, 0, 128))

        draw.text(position, text, font=font, fill=color)

        img.save(output_image)
        print(f"✅ Image saved: {output_image}")
    except Exception as e:
        print(f"❌ Error processing image: {e}")


def overlay_logo(background_image, logo_image, output_image, position=(50, 50), scale=0.2):
    """
    Overlays a club logo on the match graphic.
    """
    try:
        print(f"🔹 Background Image Path: {background_image}")
        print(f"🔹 Logo Image Path: {logo_image}")
        print(f"🔹 Output Image Path: {output_image}")

        if not os.path.exists(logo_image):
            raise FileNotFoundError(f"❌ Logo file not found: {logo_image}")

        # ✅ Convert to PNG if not already
        logo_image = ensure_png_format(logo_image)

        # ✅ Remove background before processing
        logo_image = remove_background_opencv(logo_image)

        bg = Image.open(background_image).convert("RGBA")
        logo = Image.open(logo_image).convert("RGBA")


        # Resize logo using LANCZOS (replacing ANTIALIAS)
        logo_size = (int(bg.width * scale), int(bg.width * scale))
        logo = logo.resize(logo_size, Image.LANCZOS)

        # Paste logo onto background
        bg.paste(logo, position, logo)
        bg.save(output_image)
        print(f"✅ Logo overlay saved: {output_image}")

    except Exception as e:
        print(f"❌ Error overlaying logo: {e}")


def get_template_path(club, template_type):
    """
    Returns the correct template path based on the club's assigned template pack.
    """
    template_packs = {
        "modern": {
            "fulltime": "templates/modern/final_whistle.png",
            "halftime": "templates/modern/halftime.png",
            "goal_alert": "templates/modern/goal_alert.png",
            "starting_xi": "templates/modern/starting_xi.png"
        },
        "classic": {
            "fulltime": "templates/classic/final_whistle.png",
            "halftime": "templates/classic/halftime.png",
            "goal_alert": "templates/classic/goal_alert.png",
            "starting_xi": "templates/classic/starting_xi.png"
        }
    }
    return os.path.join(settings.STATICFILES_DIRS[0], template_packs[club][template_type])

def generate_post(club, template_type, text, output_image, position=(300, 400), font_size=50):
    """
    Generates a graphic based on the club's preset template pack and selected post type.
    """
    position_mapping = {
        "fulltime": (400, 800),
        "halftime": (550, 350),
        "goal_alert": (500, 300),
        "starting_xi": (300, 400)
    }
    position = position_mapping.get(template_type, (100, 200))
    base_template = get_template_path(club, template_type)
    add_text_to_image(base_template, text, output_image, position, font_size, shadow=False)

def generate_fulltime(club, score, output_image):
    """
    Generates a full-time score graphic.
    """
    text = f"{score}"
    generate_post(club, "fulltime", text, output_image)

def generate_halftime(club, score, output_image):
    """
    Generates a halftime score graphic.
    """
    text = f"HALF TIME\n{score}"
    generate_post(club, "halftime", text, output_image)

def generate_goal_alert(club, goal_scorer, team, minute, output_image):
    """
    Generates a goal alert graphic based on club template.
    """
    text = f"GOAL!\n{goal_scorer} ({minute}')\n{team}"
    generate_post(club, "goal_alert", text, output_image)

import os
from PIL import Image, ImageDraw, ImageFont
from django.conf import settings

def get_template_path(club_name, template_type):
    """
    Returns the correct template path based on the club's assigned template pack.
    """
    template_packs = {
        "modern": {
            "starting_xi": "templates/modern/starting_xi.png"
        },
        "classic": {
            "starting_xi": "templates/classic/starting_xi.png"
        }
    }

    # Example: Assign a default template pack if not specified (modify as needed)
    template_pack = "modern"

    # ✅ Construct the full template path
    template_path = os.path.join(settings.STATICFILES_DIRS[0], template_packs[template_pack][template_type])

    print(f"✅ Using Template: {template_path}")  # Debugging
    return template_path


def generate_starting_xi(club_name, players, output_image):
    """
    Generates a Starting XI graphic based on the selected lineup.
    """
    try:
        base_template = get_template_path(club_name, "starting_xi")

        if not os.path.exists(base_template):
            raise FileNotFoundError(f"❌ Template not found: {base_template}")

        # Generate Text
        players_text = "\n".join(players)
        add_text_to_image(base_template, f"{club_name} STARTING XI\n{players_text}", output_image, position=(300, 400), font_size=50)

        print(f"✅ Starting XI graphic saved: {output_image}")
    except Exception as e:
        print(f"❌ Error generating Starting XI graphic: {e}")


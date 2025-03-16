from django.contrib.auth.models import User
from django.db import models

def club_logo_path(instance, filename):
    return f"club_logos/{instance.id}/{filename}"

class Club(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, unique=False)
    logo = models.ImageField(upload_to=club_logo_path, null=True, blank=True)
    primary_color = models.CharField(max_length=7, default="#000000")  # Hex color code
    secondary_color = models.CharField(max_length=7, default="#FFFFFF")
    template_pack = models.CharField(
        max_length=50,
        choices=[("classic", "Modern"), ("classic", "Classic"), ("minimal", "Minimal")],
        default="classic"
    )

    def __str__(self):
        return self.name

class SocialAccount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    platform = models.CharField(max_length=50, choices=[
        ('twitter', 'Twitter'),
        ('facebook', 'Facebook'),
        ('instagram', 'Instagram')
    ])
    access_token = models.CharField(max_length=500)
    access_token_secret = models.CharField(max_length=500, null=True, blank=True)  # Only for Twitter
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.platform}"


class Player(models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name="players")
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=50)  # Example: Goalkeeper, Defender, Midfielder, Forward
    jersey_number = models.IntegerField(null=True, blank=True)
    is_starting_xi = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} ({self.position})"

class Match(models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name="matches")
    opponent = models.CharField(max_length=100)
    match_date = models.DateTimeField()
    location = models.CharField(max_length=100)
    home_or_away = models.CharField(max_length=10, choices=[("Home", "Home"), ("Away", "Away")])
    score = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return f"{self.club.name} vs {self.opponent} - {self.match_date.strftime('%Y-%m-%d')}"

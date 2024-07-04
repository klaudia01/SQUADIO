from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from taggit.managers import TaggableManager

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    bio = models.TextField(null=True, default="")
    avatar = models.ImageField(null=True, default='default_avatar.png', upload_to='profile_pictures')
    background = models.ImageField(null=True, default='default_background.png', upload_to='profile_backgrounds')
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    followed_users = models.ManyToManyField('self', through='Follow', symmetrical=False, related_name='followers',
                                            blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'username']

    objects = UserManager()

    def __str__(self):
        return self.email


class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following_set')
    followed_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers_set')

    class Meta:
        unique_together = ('follower', 'followed_user')


contact_form_choice = (
    ('discord', 'Discord'),
    ('steam', 'Steam'),
    ('epic', 'Epic Games'),
    ('battlenet', 'Battle.net'),
    ('xboxlive', 'Xbox Live'),
    ('psnetwork', 'PlayStation Network'),
    ('nintendo', 'Nintendo Switch'),
    ('ubisoftconnect', 'Ubisoft Connect'),
    ('twitter', 'Twitter'),
    ('instagram', 'Instagram'),
    ('facebook', 'Facebook'),
)


class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    contact_form = models.CharField(max_length=50, choices=contact_form_choice, null=True)
    contact_username = models.CharField(max_length=100, null=True)
    contact_link = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.user.email

    class Meta:
        unique_together = ('user', 'contact_form')


game_choice = (
    ('fortnite', 'Fortnite'),
    ('apexlegends', 'Apex Legends'),
    ('warzone', 'Call of Duty: Warzone'),
    ('apexlegends', 'Apex Legends'),
    ('csgo', 'Counter-Strike 2'),
    ('overwatch2', 'Overwatch 2'),
    ('lol', 'League of Legends'),
    ('dota2', 'Dota 2'),
    ('pubg', 'PlayerUnknown\'s Battlegrounds'),
    ('rocketleague', 'Rocket League'),
    ('rainbowsixsiege', 'Rainbow Six Siege'),
    ('minecraft', 'Minecraft'),
    ('worldofwarcraft', 'World of Warcraft'),
    ('genshinimpact', 'Genshin Impact'),
    ('amongus', 'Among Us'),
    ('fallguys', 'Fall Guys: Ultimate Knockout'),
    ('valorant', 'Valorant'),
    ('fifa', 'FIFA'),
    ('gtav', 'Grand Theft Auto V'),
    ('baldursgate3', 'Baldur\'s Gate 3'),
    ('forza', 'Forza Horizon'),
    ('rust', 'Rust'),
    ('roblox', 'ROBLOX')
)


class Game(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game_name = models.CharField(max_length=50, choices=game_choice, null=True)

    class Meta:
        unique_together = ('user', 'game_name')


platform_choice = (
    ('pc', 'PC'),
    ('xbox', 'Xbox'),
    ('playstation', 'PlayStation'),
    ('nintendo', 'Nintendo Switch'),
    ('mobile', 'Mobilne'),
    ('vr', 'VR'),
)


class Platform(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    platform_name = models.CharField(max_length=50, choices=platform_choice, null=True)

    class Meta:
        unique_together = ('user', 'platform_name')


play_style_choice = (
    ('relax', 'Relaks'),
    ('competitive', 'Rywalizacja'),
    ('ranked', 'Gra rankingowa'),
    ('tournament', 'Gra turniejowa'),
    ('weekday', 'W tygodniu'),
    ('weekend', 'Weekend'),
    ('morning', 'Poranek'),
    ('afternoon', 'Popołudnie'),
    ('evening', 'Wieczór'),
    ('night', 'Noc'),
    ('mic_on', 'Włączony mikrofon'),
    ('mic_off', 'Wyłączony mikrofon'),
)


class PlayStyle(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    play_style_name = models.CharField(max_length=50, choices=play_style_choice, null=True)

    class Meta:
        unique_together = ('user', 'play_style_name')


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    tag = TaggableManager()

    def __str__(self):
        return f'{self.user.username} - {self.created_at}'





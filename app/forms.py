from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model

from .models import Contact, Game, Platform, PlayStyle, Post
from .models import contact_form_choice, game_choice, platform_choice, play_style_choice

User = get_user_model()


class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Adres e-mail'}),
        error_messages={'unique': 'Istnieje już użytkownik z tym adresem e-mail.'},
    )
    name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Wyświetlana nazwa'}),
    )
    username = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nazwa użytkownika'}),
        error_messages={'unique': 'Istnieje już użytkownik z tą nazwą użytkownika.'},
    )
    password1 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Hasło'}),
    )

    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Powtórz hasło'}),
    )

    class Meta:
        model = User
        fields = ['email', 'name', 'username', 'password1', 'password2']


class EditUserForm(UserChangeForm):
    avatar = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control'}),
    )
    background = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control'}),
    )
    name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    bio = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Napisz coś o sobie'}),
    )

    class Meta:
        model = User
        fields = ['avatar', 'background', 'name', 'bio']


class ContactForm(forms.ModelForm):
    choices_with_empty = [('', 'Wybierz formę kontaktu')] + list(contact_form_choice)

    contact_form = forms.ChoiceField(
        choices=choices_with_empty,
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    contact_username = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nazwa użytkownika'}),
    )
    contact_link = forms.URLField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Link'}),
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ContactForm, self).__init__(*args, **kwargs)

        existing_contacts = Contact.objects.filter(user=user)
        existing_choices = [contact.contact_form for contact in existing_contacts]
        available_choices = [(key, value) for key, value in contact_form_choice if key not in existing_choices]

        self.fields['contact_form'].choices = [('', 'Wybierz formę kontaktu')] + available_choices

    class Meta:
        model = Contact
        fields = ['contact_form', 'contact_username', 'contact_link']


class EditContactForm(forms.ModelForm):
    contact_username = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nazwa użytkownika'}),
    )
    contact_link = forms.URLField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Link'}),
    )

    class Meta:
        model = Contact
        fields = ['contact_username', 'contact_link']


class GameForm(forms.ModelForm):
    choices_with_empty = [('', 'Wybierz grę')] + list(game_choice)

    game_name = forms.ChoiceField(
        choices=choices_with_empty,
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(GameForm, self).__init__(*args, **kwargs)

        existing_games = Game.objects.filter(user=user)
        existing_choices = [game.game_name for game in existing_games]
        available_choices = [(key, value) for key, value in game_choice if key not in existing_choices]

        self.fields['game_name'].choices = [('', 'Wybierz grę')] + available_choices

    class Meta:
        model = Game
        fields = ['game_name']


class PlatformForm(forms.ModelForm):
    choices_with_empty = [('', 'Wybierz platformę')] + list(platform_choice)

    platform_name = forms.ChoiceField(
        choices=choices_with_empty,
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(PlatformForm, self).__init__(*args, **kwargs)

        existing_platforms = Platform.objects.filter(user=user)
        existing_choices = [platform.platform_name for platform in existing_platforms]
        available_choices = [(key, value) for key, value in platform_choice if key not in existing_choices]

        self.fields['platform_name'].choices = [('', 'Wybierz platformę')] + available_choices

    class Meta:
        model = Platform
        fields = ['platform_name']


class PlayStyleForm(forms.ModelForm):
    choices_with_empty = [('', 'Wybierz styl gry')] + list(play_style_choice)

    play_style_name = forms.ChoiceField(
        choices=choices_with_empty,
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(PlayStyleForm, self).__init__(*args, **kwargs)

        existing_play_styles = PlayStyle.objects.filter(user=user)
        existing_choices = [play_style.play_style_name for play_style in existing_play_styles]
        available_choices = [(key, value) for key, value in play_style_choice if key not in existing_choices]

        self.fields['play_style_name'].choices = [('', 'Wybierz styl gry')] + available_choices

    class Meta:
        model = PlayStyle
        fields = ['play_style_name']


class FilterForm(forms.Form):
    game_choices = Game._meta.get_field('game_name').choices
    platform_choices = Platform._meta.get_field('platform_name').choices
    play_style_choices = PlayStyle._meta.get_field('play_style_name').choices

    selected_games = forms.MultipleChoiceField(choices=game_choices, widget=forms.CheckboxSelectMultiple,
                                               required=False)
    selected_platforms = forms.MultipleChoiceField(choices=platform_choices, widget=forms.CheckboxSelectMultiple,
                                                   required=False)
    selected_play_styles = forms.MultipleChoiceField(choices=play_style_choices, widget=forms.CheckboxSelectMultiple,
                                                     required=False)


class FollowForm(forms.Form):
    user_id = forms.IntegerField(widget=forms.HiddenInput())
    next = forms.CharField(widget=forms.HiddenInput(), required=False)


class PostForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'W co dzisiaj grasz?'}))
    tag = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Możesz dodać tagi oddzielając je przecinkami'}))

    class Meta:
        model = Post
        fields = ['text', 'tag']

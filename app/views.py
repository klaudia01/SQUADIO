from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q, Value, Case, When, IntegerField, F, Subquery, Sum
from django.db.models.functions import Coalesce
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.cache import never_cache
from taggit.models import Tag

from .forms import RegisterForm, EditUserForm, GameForm, ContactForm, PlatformForm, PlayStyleForm, FilterForm, \
    FollowForm, PostForm, EditContactForm
from .models import User, Game, Contact, Platform, PlayStyle, Post, Follow


@never_cache
def start_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    context = {}

    return render(request, 'app/start.html', context)


@login_required(login_url='login')
def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    follow_form = FollowForm(initial={'next': request.path})
    contacts = Contact.objects.filter(user=user)
    games = Game.objects.filter(user=user)
    platforms = Platform.objects.filter(user=user)
    play_styles = PlayStyle.objects.filter(user=user)

    user = get_object_or_404(User, username=username)
    user_posts = Post.objects.filter(user=user).order_by('-created_at')

    context = {
        'user': user,
        'contacts': contacts,
        'games': games,
        'platforms': platforms,
        'play_styles': play_styles,
        'follow_form': follow_form,
        'user_posts': user_posts,
        'active_page': 'profile'
    }

    return render(request, 'app/profile.html', context)


@never_cache
def login_view(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
            user = authenticate(request, email=email, password=password)

            if user:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Nieprawidłowy adres email lub hasło.')

        except User.DoesNotExist:
            messages.error(request, 'Podany adres email nie jest powiązany z żadnym kontem. Sprawdź swoje dane '
                                    'logowania lub utwórz nowe konto.')

    context = {
        'page': page,
    }

    return render(request, 'app/login.html', context)


def logout_view(request):
    logout(request)

    return redirect('start')


@never_cache
def register_view(request):
    form = RegisterForm(request.POST)

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            if any(form.errors):
                form_errors = '\n'.join([' '.join(errors) for errors in form.errors.values()])
                messages.error(request, form_errors)
            else:
                messages.error(request, 'Rejestracja nieudana. Sprawdź wprowadzone dane i spróbuj ponownie.')

            context = {'form': form}
            return render(request, 'app/register.html', context)
    else:
            form = RegisterForm()

    if request.user.is_authenticated:
            return redirect('home')

    context = {'form': form}
    return render(request, 'app/register.html', context)


@login_required(login_url='login')
def edit_user_view(request):
    user = request.user
    form = EditUserForm(instance=user)

    if request.method == 'POST':
        form = EditUserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile', username=user.username)

    context = {
        'form': form,
        'active_page': 'profile'
    }

    return render(request, 'app/edit_user.html', context)


@login_required(login_url='login')
def edit_contacts_list_view(request):
    user = request.user
    contacts = Contact.objects.filter(user=user)

    if request.method == 'POST':
        form = ContactForm(request.POST, user)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.user = user
            contact.save()
            return redirect('edit_contacts_list')
        else:
            messages.error(request, 'Dodanie kontaktu nie powiodło się. Oba pola są wymagane.')
    else:
        form = ContactForm(user=user)

    context = {
        'user': user,
        'contacts': contacts,
        'form': form,
        'active_page': 'profile'
    }

    return render(request, 'app/edit_contacts_list.html', context)


def delete_contact_view(request, contact_id):
    contact = Contact.objects.get(id=contact_id)
    user = request.user

    if contact.user == request.user:
        contact.delete()

    return redirect('edit_contacts_list')


@login_required(login_url='login')
def edit_contact_view(request, contact_id):
    user = request.user
    contact = get_object_or_404(Contact, id=contact_id)

    if request.method == 'POST':
        form = EditContactForm(request.POST, instance=contact)
        if form.is_valid():
            form.save()
            return redirect('edit_contacts_list')
    else:
        form = EditContactForm(instance=contact)

    context = {
        'user': user,
        'contact': contact,
        'form': form,
        'active_page': 'profile'}

    return render(request, 'app/edit_contact.html', context)


@login_required(login_url='login')
def edit_games_view(request):
    user = request.user
    games = Game.objects.filter(user=user)

    if request.method == 'POST':
        form = GameForm(request.POST, user)
        if form.is_valid():
            game = form.save(commit=False)
            game.user = user
            game.save()
            return redirect('edit_games')
    else:
        form = GameForm(user=user)

    context = {
        'user': user,
        'games': games,
        'form': form,
        'active_page': 'profile'
    }

    return render(request, 'app/edit_games.html', context)


def delete_game_view(request, game_id):
    game = Game.objects.get(id=game_id)
    user = request.user

    if game.user == request.user:
        game.delete()

    return redirect('edit_games')


@login_required(login_url='login')
def edit_platforms_view(request):
    user = request.user
    platforms = Platform.objects.filter(user=user)

    if request.method == 'POST':
        form = PlatformForm(request.POST, user)
        if form.is_valid():
            platform = form.save(commit=False)
            platform.user = user
            platform.save()
            return redirect('edit_platforms')
    else:
        form = PlatformForm(user=user)

    context = {
        'user': user,
        'platforms': platforms,
        'form': form,
        'active_page': 'profile'
    }

    return render(request, 'app/edit_platforms.html', context)


def delete_platform_view(request, platform_id):
    platform = Platform.objects.get(id=platform_id)
    user = request.user

    if platform.user == request.user:
        platform.delete()

    return redirect('edit_platforms')


@login_required(login_url='login')
def edit_play_styles_view(request):
    user = request.user
    play_styles = PlayStyle.objects.filter(user=user)

    if request.method == 'POST':
        form = PlayStyleForm(request.POST, user)
        if form.is_valid():
            play_style = form.save(commit=False)
            play_style.user = user
            play_style.save()
            return redirect('edit_play_styles')
    else:
        form = PlayStyleForm(user=user)

    context = {
        'user': user,
        'play_styles': play_styles,
        'form': form,
        'active_page': 'profile'
    }

    return render(request, 'app/edit_play_styles.html', context)


def delete_play_style_view(request, play_style_id):
    play_style = PlayStyle.objects.get(id=play_style_id)
    user = request.user

    if play_style.user == request.user:
        play_style.delete()

    return redirect('edit_play_styles')


@login_required(login_url='login')
def find_partner_view(request):
    user = request.user
    users = User.objects.all()
    follow_form = FollowForm(initial={'next': request.path})
    user_games = Game.objects.filter(user=user).values_list('game_name', flat=True)
    user_platforms = Platform.objects.filter(user=user).values_list('platform_name', flat=True)
    user_play_styles = PlayStyle.objects.filter(user=user).values_list('play_style_name', flat=True)

    base_query = User.objects.annotate(
        score=Coalesce(
            Sum(Case(
                When(playstyle__play_style_name__in=user_play_styles, then=Value(2)),
                default=Value(0),
                output_field=IntegerField()
            )) +
            Sum(Case(
                When(platform__platform_name__in=user_platforms, then=Value(2)),
                default=Value(0),
                output_field=IntegerField()
            )),
            Value(0)
        )
    ).filter(
        game__game_name__in=user_games,
        score__gt=0
    ).exclude(id=user.id).order_by('-score')

    form = FilterForm(request.GET)

    if form.is_valid():
        selected_games = form.cleaned_data.get('selected_games')
        selected_platforms = form.cleaned_data.get('selected_platforms')
        selected_play_styles = form.cleaned_data.get('selected_play_styles')

        if selected_games:
            for game in selected_games:
                base_query = base_query.filter(game__game_name=game)

        if selected_platforms:
            for platform in selected_platforms:
                base_query = base_query.filter(platform__platform_name=platform)

        if selected_play_styles:
            for play_style in selected_play_styles:
                base_query = base_query.filter(playstyle__play_style_name=play_style)

    for matched_user in base_query:
        matched_user.has_all_preferences = (
                set(matched_user.game_set.values_list('game_name', flat=True)) == set(user_games) and
                set(matched_user.platform_set.values_list('platform_name', flat=True)) == set(user_platforms) and
                set(matched_user.playstyle_set.values_list('play_style_name', flat=True)) == set(user_play_styles)
        )

        matched_user.has_similar_preferences = (
                set(user_games).issubset(set(matched_user.game_set.values_list('game_name', flat=True))) and
                set(user_platforms).issubset(set(matched_user.platform_set.values_list('platform_name', flat=True))) and
                set(user_play_styles).issubset(
                    set(matched_user.playstyle_set.values_list('play_style_name', flat=True)))
        )

    context = {
        'users': users,
        'matched_users': base_query,
        'form': form,
        'follow_form': follow_form,
        'active_page': 'find_partner'
    }

    return render(request, 'app/find_partner.html', context)


@login_required(login_url='login')
def follow_view(request, user_id):
    user_to_follow = get_object_or_404(User, id=user_id)

    is_following = request.user.followed_users.filter(id=user_to_follow.id).exists()

    if request.method == 'POST':
        follow_form = FollowForm(request.POST)
        if follow_form.is_valid():
            if is_following:
                request.user.followed_users.remove(user_to_follow)
            else:
                request.user.followed_users.add(user_to_follow)

    next_path = request.POST.get('next', request.META.get('HTTP_REFERER', '/'))

    return redirect(next_path)


@login_required(login_url='login')
def friends_view(request):
    following = Follow.objects.filter(follower=request.user)
    followers = Follow.objects.filter(followed_user=request.user)
    friends = following.filter(followed_user__in=followers.values('follower'))
    friends_users = User.objects.filter(id__in=friends.values_list('followed_user', flat=True))

    context = {
        'friends': friends_users,
        'active_page': 'friends'
    }

    return render(request, 'app/friends.html', context)


@login_required(login_url='login')
def following_view(request):
    following = request.user.following_set.all()

    context = {
        'following': following,
        'active_page': 'friends'
    }

    return render(request, 'app/following.html', context)


@login_required(login_url='login')
def followers_view(request):
    followers = request.user.followers_set.all()
    context = {
        'followers': followers,
        'active_page': 'friends'
    }
    return render(request, 'app/followers.html', context)


@login_required(login_url='login')
def feed_view(request):
    posts = Post.objects.all().order_by('-created_at')

    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.user = request.user
            new_post.save()

            tags = form.cleaned_data.get('tag')
            if tags:
                tag_list = [tag.strip().capitalize() for tag in tags.split(',')]
                new_post.tag.add(*tag_list)

            return redirect('home')
    else:
        form = PostForm()

    tag_filter = request.GET.get('tag', None)
    if tag_filter:
        posts = posts.filter(tag__name__iexact=tag_filter)

    tags = Tag.objects.annotate(num_posts=Count('taggit_taggeditem_items')).order_by('-num_posts')

    context = {
        'posts': posts,
        'form': form,
        'tags': tags,
        'active_page': 'home'
    }

    return render(request, 'app/home.html', context)


def delete_post_view(request, post_id):
    post = Post.objects.get(id=post_id)
    user = request.user

    if post.user == request.user:
        post.delete()

    next_path = request.POST.get('next', request.META.get('HTTP_REFERER', '/'))

    return redirect(next_path)

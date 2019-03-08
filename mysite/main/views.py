from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import NewUserForm
from django.contrib import messages
from .models import Story, Genre, Series
from django.http import HttpResponse


def single_slug(request, single_slug):
    genres = [g.slug for g in Genre.objects.all()]
    if single_slug in genres:
        matching_series = Series.objects.filter(genre__slug=single_slug)
        series_urls = {}

        for m in matching_series.all():
            part_one = Story.objects.filter(series__series=m.series).earliest("publish_date")
            series_urls[m] = part_one.slug

        context = {
            "series": matching_series,
            "part_ones": series_urls
        }
        return render(request, 'main/genre.html', context)

    stories = [s.slug for s in Story.objects.all()]
    if single_slug in stories:
        this_story = Story.objects.get(slug=single_slug)
        stories_from_series = Story.objects.filter(series__series=this_story.series).order_by('publish_date')
        this_story_idx = list(stories_from_series).index(this_story)

        context = {
            'story': this_story,
            'sidebar': stories_from_series,
            'this_story_idx': this_story_idx
        }
        return render(request, 'main/story.html', context)

    return HttpResponse(f"<h1>'{single_slug}' does not correspond to anything!</h1>")


def index(request):
    context = {
        'genres': Genre.objects.all
    }
    return render(request, 'main/genres.html', context)


def about(request):
    return render(request, 'main/about.html')


def register(request):
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'New account created: {username}')
            login(request, user)
            return redirect('main:index')
        else:
            for msg in form.error_messages:
                messages.error(request, f'{msg}: {form.error_messages[msg]}')

            context = {
                'form': form
            }
            return render(request, 'main/register.html', context)

    form = NewUserForm()
    context = {
        'form': form
    }
    return render(request, 'main/register.html', context)


def logout_request(request):
    logout(request)
    messages.info(request, 'Logged out successfully.')
    return redirect('main:index')


def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f'You are now logged in as {username}')
                return redirect('/')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')

    form = AuthenticationForm()
    context = {
        "form": form
    }
    return render(request, 'main/login.html', context)

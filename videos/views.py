from django.shortcuts import render


def landing(request):
    # Displays videos app home page
    return render(request, 'videos/videos_landing.html')

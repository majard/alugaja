from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

from catalog.forms import SignUpForm, ProfileForm

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        pform = ProfileForm(request.POST)
        if form.is_valid() and pform.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.profile.contact = pform.cleaned_data.get('contact')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('houses')
    else:
        form = SignUpForm()        
        pform = ProfileForm()
    return render(request, 'signup.html', {'form': form, 'pform': pform})
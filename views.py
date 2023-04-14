from django.shortcuts import render, redirect
from django.contrib.auth import login, logout,authenticate
from django.contrib import messages
from .form import SignUpForm

# Create your views here.
def HomePageView(request):
    # check to see if logged in user
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # To authenticate
        user = authenticate(request, username=username, password =password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Hello {username}!')
            return redirect('home')
        else:
            messages.info(request, 'login failed! Please try again...')            
    return render(request, 'home.html', {})

def register_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # Authenticate and login
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'You have Successful registered! {username}')
            return redirect('home')
    else:
            form = SignUpForm()   
            return render(request, 'register.html', {'form': form})
    return render(request, 'register.html', {'form': form})



def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out!')
    return redirect('home')

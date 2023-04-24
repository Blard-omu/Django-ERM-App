from django.shortcuts import render, redirect
from django.contrib.auth import login, logout,authenticate
from django.contrib import messages
from .form import SignUpForm, AddRecordForm
from .models import Record

# Create your views here.
def HomePageView(request):
    # Populating the Record on homepage
    records = Record.objects.all()
    # check to see if logged in user
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # To authenticate
        user = authenticate(request, username=username, password =password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome {username}! 👋')
            return redirect('home')
        else:
            messages.error(request, 'login failed! Please try again...')            
    return render(request, 'home.html', {'records': records})

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
    messages.info(request, 'You have been logged out!')
    return redirect('home')

def customer_record(request, pk):
	if request.user.is_authenticated:
		# Look Up Records
		customer_record = Record.objects.get(id=pk)
		return render(request, 'record.html', {'customer_record':customer_record})
	else:
		messages.warning(request, "You Must Be Logged In To View That Page...")
		return redirect('home')

def delete_record(request, pk):
    if request.user.is_authenticated:
        try:
            record = Record.objects.get(id=pk)
            record_id = record.id
            record.delete()
            messages.info(request, f"Record no: {record_id} Deleted Successfully...")
        except Record.DoesNotExist:
            messages.error(request, "Record does not exist.")
        return redirect('home')
    else:
        messages.warning(request, "You must be logged in to do that.")
        return redirect('home')

def add_record(request):
	form = AddRecordForm(request.POST or None)
	if request.user.is_authenticated:
		if request.method == "POST":
			if form.is_valid():
				add_record = form.save()
				messages.success(request, "New Record Added...")
				return redirect('home')
		return render(request, 'add_record.html', {'form':form})
	else:
		messages.warning(request, "You Must Be Logged In...")
		return redirect('home')

def update_record(request, pk):
	if request.user.is_authenticated:
		current_record = Record.objects.get(id=pk)
		form = AddRecordForm(request.POST or None, instance=current_record)
		if form.is_valid():
			form.save()
			messages.success(request, "Record Has Been Updated!")
			return redirect('home')
		return render(request, 'update_record.html', {'form':form})
	else:
		messages.warning(request, "You Must Be Logged In...")
		return redirect('home')
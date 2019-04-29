from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import auth
from contacts.models import Contact


# Create your views here.
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password'] 

        user = auth.authenticate(username = username, password = password)

        if user is not None:
            auth.login(request,user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid Credentials')
            return redirect('login')

    else:
        return render(request, 'accounts/login.html')

def logout(request):
    if request.method == "POST":
        auth.logout(request)
        return redirect('index')

def register(request):
    #Get post values
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        #password validation

        if password == password2:
            if User.objects.filter(username = username).exists():
                messages.error(request, 'That USername is Taken')
                return redirect('register')
            else:
                if User.objects.filter(email = email).exists():
                    messages.error(request, 'That Email is been used')
                    return redirect('register')
                else:
                    user = User.objects.create_user(username=username,first_name=first_name,last_name=last_name,password=password,email=email)
                    user.save()
                    messages.success(request, 'Welcome to BTRE')
                    return redirect('login')
        else:
            messages.error(request, 'Passwords do not match')
            return redirect('register')
    else:
        return render(request, 'accounts/register.html')

def dashboard(request):
    user_contact = Contact.objects.order_by('-contact_date').filter(user_id = request.user.id)
    context = {
        'contacts' : user_contact,
    }
    return render(request, 'accounts/dashboard.html', context)
from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from .forms import UserProfileForm
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import UserProfile
from .forms import ExpenseForm
from decimal import Decimal

@login_required(login_url='login')
def update_savings(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.cleaned_data['expense']
            
            # Check if expense is a valid Decimal value
            if expense is not None:
                user_profile = UserProfile.objects.get(user=request.user)
                user_profile.current_savings -= Decimal(expense)
                user_profile.save()
                return redirect('dashboard')  # Change 'dashboard' to your actual dashboard URL
    else:
        form = ExpenseForm()

    return render(request, 'update_savings.html', {'form': form})

class DialogflowWebhook(APIView):
    # ...

    def post(self, request, *args, **kwargs):
        # Assuming Dialogflow sends data in JSON format
        data = request.data

        # Extract relevant information from the Dialogflow payload
        username = data.get('username')
        income = data.get('income')
        current_savings = data.get('current_savings')
        goal = data.get('goal')

        # Get the user profile based on the username
        user = get_object_or_404(User, username=username)
        user_profile, created = UserProfile.objects.get_or_create(user=user)

        # Update the user profile with Dialogflow data
        user_profile.income = income
        user_profile.current_savings = current_savings
        user_profile.goal = goal
        user_profile.save()

        return Response({"message": "Data successfully updated"}, status=status.HTTP_200_OK)

@login_required(login_url='login')  # Requires the user to be logged in to access this view
def create_profile(request):
    # Check if the user already has a profile
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        # If the form is submitted, update the user profile with the form data
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
    else:
        # If it's a GET request, initialize the form with the current user profile data
        form = UserProfileForm(instance=user_profile)

    return render(request, 'create_profile.html', {'form': form, 'user_data': user_profile})
# Create your views here.
@login_required(login_url='login')
def HomePage(request):

    return render(request,'home.html')

def SignupPage(request):
    if request.method=='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')
        income = request.POST.get('income')
        current_savings = request.POST.get('current_savings')
        goal = request.POST.get('goal')
        user = User.objects.create_user(uname, email, pass1)
        if pass1==pass2:
            return redirect('login')
        else:
            return HttpResponse("Your passwords do not match")
    return render(request,'signup.html')


def LoginPage(request):
    pass
    if request.method=='POST':
        username=request.POST.get('username')
        pass3=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass3)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            return HttpResponse("Username or password is incorrect")
    return render(request,'login.html')

def LogoutPage(request):
    logout(request)
    return redirect('login')

def BotPage(request):
    return render(request,'bot.html')

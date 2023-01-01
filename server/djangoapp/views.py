from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
#from django.views.decorators.csrf import csrf_exempt
from .models import *
from .restapis import *
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def about(request):
    context = {}
    return render(request, 'djangoapp/about.html', context)


# Create a `contact` view to return a static contact page
def contact(request):
    context = {}
    return render(request, 'djangoapp/contact.html', context)

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/user_login.html', context)
    else:
        return render(request, 'djangoapp/user_login.html', context)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    context = {}
    logout(request)
    return render(request, 'djangoapp/index.html', context)

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'djangoapp/registration.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        url = "https://au-syd.functions.appdomain.cloud/api/v1/web/0126338a-2b94-4c58-8db4-d6f932482271/dealership-package/get-dealership"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        context['dealership_list'] = dealerships        
        return render(request, 'djangoapp/index.html', context)

def get_dealerships_by_id(dealer_id):
    url = "https://au-syd.functions.appdomain.cloud/api/v1/web/0126338a-2b94-4c58-8db4-d6f932482271/dealership-package/get-dealership?dealerId=" + dealer_id.__str__()
    # Get dealers from the URL
    dealerships = get_dealers_by_id(url,dealerId=dealer_id)
    return dealerships[0]

def get_dealerships_by_state(request,state):
    if request.method == "GET":
        url = "https://au-syd.functions.appdomain.cloud/api/v1/web/0126338a-2b94-4c58-8db4-d6f932482271/dealership-package/get-dealership"
        # Get dealers from the URL
        dealerships = get_dealers_by_state(url,statename=state)
        # Concat all dealer's short name
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        return HttpResponse(dealer_names)


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...
def get_dealer_details(request,dealer_id):
    context = {}
    if request.method == "GET":
        url = "https://au-syd.functions.appdomain.cloud/api/v1/web/0126338a-2b94-4c58-8db4-d6f932482271/dealership-package/get-review"
        # Get dealers from the URL
        reviews = get_dealer_reviews_from_cf(url,dealerid=dealer_id)
        context['review_list'] = reviews
        context['dealer_id'] = dealer_id
        current_dealer = get_dealerships_by_id(dealer_id)
        context['dealer_name'] = current_dealer.full_name
        return render(request, 'djangoapp/dealer_details.html', context)

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...
#@csrf_exempt
def add_review(request, dealer_id):
    context = {}
    user = request.user
    if request.method == "POST":
        if user.is_authenticated:
            url = "https://au-syd.functions.appdomain.cloud/api/v1/web/0126338a-2b94-4c58-8db4-d6f932482271/dealership-package/post-review"
            review = {
                "name": "seke",
                "dealership": 23,
                "review": "It sucks always have an issue class modules are always outdated!!!",
                "purchase": False,
                "another": "field",
                "purchase_date": "02/16/2021",
                "car_make": "Audi",
                "car_model": "Car",
                "car_year": 1964
            }

            car = CarModel.objects.get(pk=int(request.POST['car']))
            review["name"] = user.username
            review["dealership"] = dealer_id
            review["review"] = request.POST['reviewcontent']
            review["purchase"] = request.POST['purchasecheck']
            review["another"] = "field"
            review["purchase_date"] = request.POST['purchasedate']
            review["car_make"] = car.carmake.name
            review["car_model"] = car.cartype
            review["car_year"] = car.year
            json_payload = {
                "review" : {}
            }
            json_payload["review"] = review
            response = post_request(url, json_payload, dealerId=dealer_id)
            return get_dealer_details(request,dealer_id)
            #return HttpResponse(response)
        else:
            return render(request, 'djangoapp/index.html', context)
    else:
        cars = CarModel.objects.all()
        current_dealer = get_dealerships_by_id(dealer_id)
        context['dealer_name'] = current_dealer.full_name
        context['cars'] = cars
        context['dealer_id'] = dealer_id
        return render(request, 'djangoapp/add_review.html', context)

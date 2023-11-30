from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

from .resapis import get_dealers_from_cf
from .resapis import get_dealer_reviews_from_cf
from .resapis import analyze_review_sentiments
from .resapis import post_request

# Get an instance of a logger
logger = logging.getLogger(__name__)



# Create an `about` view to render a static about page
def about(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)


# Create a `contact` view to return a static contact page
def contact(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)

# Create a `login_request` view to handle sign in request.
def login_request(request):
    context = {}
    # Handles POST request
    if request.method == "POST":
        # Get username and password from request.POST dictionary
        username = request.POST['username']
        password = request.POST['psw']
        # Try to check if provide credential can be authenticated
        user = authenticate(username=username, password=password)
        if user is not None:
            # If user is valid, call login method to login current user
            login(request, user)
            return render(request, 'djangoapp/index.html', context)
        else:
            # If not, return to login page again
            return render(request, 'djangoapp/contact.html', context)
    else:
        return render(request, 'djangoapp/index.html', context)


# Create a `logout_request` view to handle sign out request
def logout_request(request):
    # Get the user object based on session id in request
    print("Log out the user `{}`".format(request.user.username))
    # Logout user in the request
    logout(request)
    # Redirect user back to course list view
    # return redirect('djangoapp/index.html')
    return render(request, 'djangoapp/index.html')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    # If it is a GET request, just render the registration page (OJO: Sign up link from index.html to access to registration page):
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    # If it is a POST request
    elif request.method == 'POST':
        # Get user information from request.POST
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            # Check if user already exists
            User.objects.get(username=username)
            user_exist = True
        except:
            # If not, simply log this is a new user
            logger.debug("{} is new user".format(username))
        # If it is a new user
        if not user_exist:
            # Create user in auth_user table
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            # Login the user and redirect to course list page
            login(request, user)
            #return redirect("djangoapp/index.html")
            return render(request, 'djangoapp/index.html')
        else:
            return render(request, 'djangoapp/registration.html', context)



# To view Home test (to be deleted)

def get_home(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/index.html', context)
    

# To view to add POST test (to be deleted)

def review_form(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/add_review.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships

def get_dealerships(request):
    if request.method == "GET":
        url = "http://127.0.0.1:3000/dealerships/get"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        return HttpResponse(dealer_names)
    


# Create a `get_dealer_details` view to render the reviews of a dealer
# Según las pruebas, 'request' corresponde a 'url' y 'id' al parámetro id en urls.py (path(route='dealer/<int:id>').
def get_dealer_details(request, id):
    if request.method == "GET":
        # Data retrived from Cloudant through Web API in get_and_post-reviews.py
        url = "http://127.0.0.1:5000/api/get_reviews"

# Code by one resulta at time*******************
        # reviewsByid = get_dealer_reviews_from_cf(url, id)
        # textReview = reviewsByid[1]
        # print(textReview)
        # return HttpResponse(analyze_review_sentiments(textReview))
#   *****************************************

    # Obtener las revisiones del concesionario
    reviewsByid = get_dealer_reviews_from_cf(url, id)

    # Inicializar una lista para almacenar los resultados de sentimiento
    results = []

    # Iterar sobre cada revisión y procesarla con la función NLU sentiment
    for review in reviewsByid:
        textReview = review
        mySentiment = analyze_review_sentiments(textReview)

        # Agregar el resultado al lista de resultados
        results.append(f"{textReview} : {mySentiment}")
        
            # Devolver la lista de resultados como una cadena
    return HttpResponse("\n".join(results))

# ************************************************


# Create a `add_review` view to submit a review (version Week 3 by POSTAMAN)

# def add_review(request, id):
def add_review(request):
    
    if request.method == 'POST':
            # print(request.POST)
        # if request.user.is_authenticated:
            # print(csrf_token)
            # car_id = request.POST["car"]
            # car = CarModel.objects.get(pk=car_id)
            review_post_url = "http://127.0.0.1:5000/api/post_review"
            review = {
                "id": request.POST['id'],
                "time": request.POST["time"],
                "name": request.POST["name"],
                "dealership": request.POST['id'],                
                "review": request.POST["review"],
                "purchase": True,
                "another": request.POST["another"],
                "purchase_date":request.POST["purchase_date"],
                "car_make": request.POST["car_make"],  
                "car_model": request.POST["car_model"],
                "car_year": request.POST["car_year"]  
            }



            # review = {
            #     "id":id,
            #     # "time":datetime.utcnow().isoformat(),
            #     "time":["time"],
            #     "name":["name"],
            #     "dealership" :id,                
            #     "review": ["content"],
            #     "purchase": True,
            #     "another": ["another"],
            #     "purchase_date":["purchase_date"],
            #     "car_make": ["car_make"],  
            #     "car_model": ["car_model"],
            #     "car_year": ["car_year"],  
            # }

            # review=json.dumps(review,default=str)
            new_payload1 = {}
            new_payload1["review"] = review
            # print("\nREVIEW:",review)
            post_request(review_post_url, review)
    return redirect ("djangoapp:get_home")
        # return render(request, 'djangoapp/index.html')





# Create a `add_review` view to submit a review (final presentation):

# def add_review(request, id):
#     context = {}
#     url = "3000-URL/dealerships/get"
#     dealer = get_dealer_by_id_from_cf(url, id)
#     context["dealer"] = dealer    
#     if request.method == 'GET':
#         # Get cars for the dealer
#         cars = CarModel.objects.all()
#         print(cars)
#         context["cars"] = cars
#         return render(request, 'djangoapp/add_review.html', context)
    
#     elif request.method == 'POST':
#         if request.user.is_authenticated:
#             car_id = request.POST["car"]
#             car = CarModel.objects.get(pk=car_id)
#             review_post_url = "5000-url/api/post_review"
#             review = {
#                 "id":id,
#                 "time":datetime.utcnow().isoformat(),
#                 "name":request.user.username,  # Assuming you want to use the authenticated user's name
#                 "dealership" :id,                
#                 "review": request.POST["content"],  # Extract the review from the POST request
#                 "purchase": True,  # Extract purchase info from POST
#                 "purchase_date":request.POST["purchasedate"],  # Extract purchase date from POST
#                 "car_make": car.car_make.name,  # Extract car make from POST
#                 "car_model": car.name,  # Extract car model from POST
#                 "car_year": int(car.year.strftime("%Y")),  # Extract car year from POST
#             }
#             review=json.dumps(review,default=str)
#             new_payload1 = {}
#             new_payload1["review"] = review
#             print("\nREVIEW:",review)
#             post_request(review_post_url, review, id = id)
#         return redirect("djangoapp:dealer_details", id = id)

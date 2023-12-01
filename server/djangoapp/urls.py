from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'
urlpatterns = [
    # route is a string contains a URL pattern
    # view refers to the view function
    # name the URL

    # path for about view
    path(route='about/', view=views.about, name='about'),

    # path for contact us view
    path(route='contact/', view=views.contact, name='contact'), 

    # path for registration
    path(route='registration/', view=views.registration_request, name='registration'),

    # path for login
    path(route='login/', view=views.login_request, name='login'),
    # path('login/', views.login_request, name='login'), //((other option))
 

    # path for logout
    path('logout/', views.logout_request, name='logout'),


    # path for home test (to be deleted)
    path(route='home/', view=views.get_home, name='get_home'),
    
    # path for all dealer names view tests
    path(route='', view=views.get_dealerships, name='index'),


    # Dealer name by id
    path(route='dealerbyid/<int:id>',view=views.get_name, name='dealer_name'),

    # path for dealer reviews view
    path(route='reviewdealer/<int:id>', view=views.get_dealer_details, name='dealer_details'),
 

    # path for add a review view (function)
    path(route='addreview/', view=views.add_review, name='addreview'),

    # path for add a review view
    path(route='post/<int:id>', view=views.review_form, name='reviewform')
    

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
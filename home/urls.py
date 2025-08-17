
from django.contrib import admin
from django.urls import path
from home import views 
from . import views #this is used for ajax only and it is stored inside the context_processor.py for the cart items to be updated and showed in each template 

urlpatterns = [
    path("", views.index, name='home'), #the blank space "" which is given must not have space between the quotes it must be same as urls.py in Hello
    path("about", views.about, name='about'),
    path("services", views.services, name='services'),
    path("contact", views.contact, name='contact'),
    #cart urls start
    path("cart/", views.view_cart,  name = 'cart'),
    path('add_to_cart', views.add_to_cart, name='add_to_cart'),
    path('remove/<str:name>/', views.remove_from_cart, name='remove_from_cart'),
    path('update/<str:name>/<str:action>/', views.update_quantity, name='update_quantity'),
    path('update-quantity-ajax/', views.update_quantity_ajax, name='update_quantity_ajax'), #here the paths are added so it is connected with the cart page where it gets updated and removed 
    path('remove-from-cart-ajax/', views.remove_from_cart_ajax, name='remove_from_cart_ajax'),
    path("checkout/", views.checkout, name="checkout"),   # <--- Add this  for checkout views
    #auth urls 
    path('register/', views.register, name='register'), #added this link for registering 
    path('login/', views.loginUser, name='login'),  #link for login users 
    path('logout/', views.logoutUser, name='logout'),  #link for the logout user which will be redirected to the login page 
    #forgot password urls 
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('reset-password/<uidb64>/<token>/', views.reset_password, name='reset_password'),
    # in home/urls.py (only while you’re testing)
    path('debug-session/', views.some_view, name='debug_session'),
    path('clear-session/', views.clear_session, name='clear_session'),
    
    #this here resets the password by which is quick reset taken the token ,uid number and sending directly to the hange password page 
    path('password-reset-sent/<str:email>/', views.password_reset_sent, name='password_reset_sent'),
    #here this is the url for services page 
    path('book-services/', views.book_services, name='book_services'),
    path('activity/', views.my_activity, name='my_activity'), 
]


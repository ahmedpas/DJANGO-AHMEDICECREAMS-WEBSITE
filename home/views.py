from django.shortcuts import render, HttpResponse , redirect
from datetime import datetime
from django.utils import timezone
import pytz
from home.models import Contact , Order , ServiceBooking
from django.contrib import messages #here the alert message will be shown in the website after the details have been submitted or not taken from 'django messages framework'
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt #used for faster cart item count inside the profile
from .models import Order #this model is created for checkout page for taking orders 
from django.contrib.auth.models import User 
from django.contrib.auth import logout,authenticate,login 
from django.contrib.auth.decorators import login_required  #to protect pages 

#all the below imports are used for forgout password and reset password 
from django.contrib.auth.tokens import default_token_generator 
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.conf import settings
 
from itertools import chain #for checking my_activity 
from operator import attrgetter


#this is my_activity page 

@login_required(login_url='/login/')
def my_activity(request):
    # Get and sort each model separately
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    bookings = ServiceBooking.objects.filter(user=request.user).order_by('-date')
    messages = Contact.objects.filter(user=request.user).order_by('-date')
    
    # Add type identifiers
    for o in orders: o.activity_type = 'order'
    for b in bookings: b.activity_type = 'service'  
    for m in messages: m.activity_type = 'message'
    
    # Simple concatenation (not perfectly sorted by date, but works)
    timeline = list(orders) + list(bookings) + list(messages)
    
    return render(request, 'my_activity.html', {
        'timeline': timeline,
        'total_orders': orders.count(),
        'total_bookings': bookings.count(),
        'total_messages': messages.count()
    })



#this is the registration page 

def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')

        if password != password_confirm:
            messages.error(request, "Passwords do not match.")
            return redirect('/register')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, f"Username '{username}' is already taken.")
            return redirect('/register')

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        messages.success(request, f"Account created for {username}! You can now log in.")
        return redirect('/login')
    
    return render(request, 'register.html')

# --- NEW: Login View ---

def loginUser(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {username}!")
            next_page = request.GET.get('next')
            return redirect(next_page) if next_page else redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('/login')
    
    return render(request, "login.html")

# --- NEW: Logout View ---

def logoutUser(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('/login')


def index(request):
    # All products with categories
    all_products = [
        # Regular flavors
        {'name': 'Chocolate Fudge', 'price': 140, 'img': 'th1.jpg', 'desc': 'Dive into the ultimate chocolate fantasy! Our rich chocolate fudge ice cream is a creamy dream for every choco-lover.', 'category': 'premium'},
        {'name': 'Alphonso Mango', 'price': 100, 'img': 'th2.jpg', 'desc': 'Experience royalty with every bite! Made from the finest Alphonso mangoes, this flavor bursts with tropical sweetness.', 'category': 'fruit'},
        {'name': 'Black Currant', 'price': 80, 'img': 'th3.jpg', 'desc': 'Tangy, bold, and refreshingly unique! Black currant ice cream offers a vibrant burst of fruity flavor in every scoop.', 'category': 'fruit'},
        {'name': 'Pista Fudge', 'price': 130, 'img': 'th4.jpg', 'desc': 'A nutty sensation with a smooth fudge finish! Pista fudge ice cream blends crunchy pistachios with creamy decadence.', 'category': 'premium'},
        {'name': 'Hazel Fudge', 'price': 140, 'img': 'th5.jpg', 'desc': 'A smooth blend of roasted hazelnuts and velvety cream. Pure indulgence in every bite of our hazelnut delight.', 'category': 'premium'},
        {'name': 'French Vanilla', 'price': 70, 'img': 'th6.jpg', 'desc': 'Elegant, timeless, and luxuriously creamy. Our French Vanilla is a classic done to perfection.', 'category': 'classic'},
        
        # Fruit flavors
        {'name': 'Banana', 'price': 90, 'img': 'th7.jpg', 'desc': 'Smooth and creamy banana ice cream that captures the tropical sweetness of ripe bananas in every spoonful.', 'category': 'fruit'},
        {'name': 'Black Raspberry', 'price': 110, 'img': 'th8.jpg', 'desc': 'Bold and tangy black raspberry with a deep, rich flavor that delivers an intense berry experience.', 'category': 'fruit'},
        {'name': 'Cherry', 'price': 105, 'img': 'th9.jpg', 'desc': 'Sweet and tart cherry ice cream bursting with juicy cherry pieces and natural fruit flavor.', 'category': 'fruit'},
        {'name': 'Black Cherry', 'price': 115, 'img': 'th10.jpg', 'desc': 'Rich black cherry ice cream with chunks of sweet dark cherries for an indulgent fruit experience.', 'category': 'fruit'},
        {'name': 'Cinnamon Apple', 'price': 95, 'img': 'th11.jpg', 'desc': 'Warm spiced apple ice cream with cinnamon that tastes like apple pie in a scoop.', 'category': 'fruit'},
        {'name': 'Grape', 'price': 85, 'img': 'th12.jpg', 'desc': 'Fresh grape ice cream with a vibrant purple color and authentic grape flavor that kids love.', 'category': 'fruit'},
        {'name': 'Lúcuma', 'price': 130, 'img': 'th13.jpg', 'desc': 'Exotic Peruvian lúcuma with its unique orange color and sweet, nutty flavor - a rare treat!', 'category': 'fruit'},
        {'name': 'Mamey', 'price': 125, 'img': 'th14.jpg', 'desc': 'Tropical mamey fruit ice cream with its distinctive salmon color and sweet, creamy texture.', 'category': 'fruit'},
        {'name': 'Moon Mist', 'price': 100, 'img': 'th15.jpg', 'desc': 'A magical blend of grape, banana, and blue raspberry creating a colorful, fruity adventure.', 'category': 'fruit'},
        {'name': 'Passion Fruit', 'price': 140, 'img': 'th16.jpg', 'desc': 'Intensely flavored passion fruit ice cream with tropical tartness and exotic aroma.', 'category': 'fruit'},
        {'name': 'Pumpkin', 'price': 85, 'img': 'th17.jpg', 'desc': 'Seasonal pumpkin spice ice cream perfect for autumn with warm spices and creamy pumpkin.', 'category': 'fruit'},
        {'name': 'Raspberry Ripple', 'price': 110, 'img': 'th18.jpg', 'desc': 'Classic vanilla ice cream swirled with tart raspberry sauce for the perfect balance of flavors.', 'category': 'fruit'},
        {'name': 'Rum Raisin', 'price': 135, 'img': 'th19.jpg', 'desc': 'Premium rum-soaked raisins in rich vanilla ice cream - an adult favorite with Caribbean flair.', 'category': 'fruit'},
        {'name': 'Strawberry', 'price': 75, 'img': 'th20.jpg', 'desc': 'Classic strawberry ice cream made with real strawberry pieces and natural fruit flavor.', 'category': 'fruit'},
        {'name': 'Sberry Cake', 'price': 145, 'img': 'th21.jpg', 'desc': 'Creamy cheesecake ice cream with strawberry swirl and graham cracker pieces.', 'category': 'fruit'},
        {'name': 'Teaberry', 'price': 90, 'img': 'th22.jpg', 'desc': 'Unique wintergreen-flavored ice cream with a refreshing minty taste and pink color.', 'category': 'fruit'},
        {'name': 'Tiger Tail', 'price': 95, 'img': 'th23.jpg', 'desc': 'Orange-flavored ice cream with black licorice swirls creating a striking striped appearance.', 'category': 'fruit'},
        {'name': 'Tutti Frutti', 'price': 105, 'img': 'th24.jpg', 'desc': 'Colorful mix of candied fruits and nuts in vanilla ice cream - a carnival of flavors!', 'category': 'fruit'},
        {'name': 'Watermelon', 'price': 80, 'img': 'th25.jpg', 'desc': 'Refreshing watermelon ice cream perfect for summer with authentic melon taste.', 'category': 'fruit'},
        {'name': 'Bananas Foster', 'price': 150, 'img': 'th26.jpg', 'desc': 'Gourmet banana ice cream with caramelized banana pieces and a hint of rum flavoring.', 'category': 'fruit'},
        {'name': 'Lemon', 'price': 70, 'img': 'th27.jpg', 'desc': 'Zesty lemon ice cream with bright citrus flavor that refreshes and energizes.', 'category': 'fruit'},
        {'name': 'Lime', 'price': 70, 'img': 'th28.jpg', 'desc': 'Tangy lime ice cream with vibrant green color and sharp citrus kick.', 'category': 'fruit'},
        {'name': 'Orange', 'price': 75, 'img': 'th29.jpg', 'desc': 'Bright orange ice cream with natural citrus oils and refreshing orange zest.', 'category': 'fruit'},
        {'name': 'Apricot', 'price': 100, 'img': 'th30.jpg', 'desc': 'Delicate apricot ice cream with subtle sweetness and velvety smooth texture.', 'category': 'fruit'},
        {'name': 'Blueberry', 'price': 110, 'img': 'th31.jpg', 'desc': 'Fresh blueberry ice cream packed with real blueberry pieces and antioxidant goodness.', 'category': 'fruit'},
        {'name': 'Blackberry', 'price': 115, 'img': 'th32.jpg', 'desc': 'Rich blackberry ice cream with deep purple color and intense berry flavor.', 'category': 'fruit'},
        {'name': 'Apple', 'price': 80, 'img': 'th33.jpg', 'desc': 'Crisp apple ice cream with fresh apple chunks and a hint of natural sweetness.', 'category': 'fruit'},
        {'name': 'Spumoni', 'price': 160, 'img': 'th34.jpg', 'desc': 'Authentic Italian molded ice cream layered with candied fruits, nuts, and rich flavors - a true European delicacy.', 'category': 'premium'},
        {'name': 'Hokey Pokey', 'price': 150, 'img': 'th35.jpg', 'desc': 'Traditional New Zealand vanilla ice cream studded with crunchy honeycomb toffee pieces - a sweet Kiwi classic.', 'category': 'premium'},
        {'name': 'Stracciatella', 'price': 145, 'img': 'th36.jpg', 'desc': 'Classic Italian vanilla gelato with delicate chocolate chips - the elegant simplicity of authentic Italian craftsmanship.', 'category': 'premium'},
        {'name': 'Moose Tracks', 'price': 155, 'img': 'th37.jpg', 'desc': 'Rich vanilla ice cream swirled with peanut butter cups and chocolate fudge tracks - an indulgent American favorite.', 'category': 'classic'},
        {'name': 'Superman', 'price': 95, 'img': 'th38.jpg', 'desc': 'Colorful tri-colored ice cream featuring blue, red, and yellow swirls - a fun childhood favorite that brings out the superhero in everyone.', 'category': 'classic'},
        {'name': 'Cotton Candy', 'price': 90, 'img': 'th39.jpg', 'desc': 'Sweet and airy cotton candy flavored ice cream that melts on your tongue - bringing carnival magic to every scoop.', 'category': 'classic'},
        {'name': 'Red Velvet Cake', 'price': 170, 'img': 'th40.jpg', 'desc': 'Decadent red velvet cake flavored ice cream with cream cheese swirls and cake pieces - luxury dessert reimagined as ice cream.', 'category': 'premium'},
        {'name': 'Tiramisu', 'price': 140, 'img': 'th41.jpg', 'desc': 'Rich coffee-flavored ice cream layered with mascarpone and ladyfinger cookie pieces - the beloved Italian dessert in frozen form.', 'category': 'classic'},
        {'name': 'S\'mores', 'price': 125, 'img': 'th42.jpg', 'desc': 'Campfire classic recreated as ice cream with chocolate, marshmallow swirls, and graham cracker pieces - outdoor adventure in every bite.', 'category': 'classic'},

    
    ]
    

    # Filter products by category
    fruit_products = [product for product in all_products if product['category'] == 'fruit']
    premium_products = [product for product in all_products if product['category'] == 'premium']
    classic_products = [product for product in all_products if product['category'] == 'classic']

    # Search functionality
    query = request.GET.get('q', '')
    if query:
        products = [product for product in all_products 
                   if query.lower() in product['name'].lower() or 
                   query.lower() in product['desc'].lower()]
        return render(request, 'index.html', {'products': products, 'query': query})
    else:
        return render(request, 'index.html', {
            'fruit_products': fruit_products,
            'premium_products': premium_products,
            'classic_products': classic_products,
            'all_products': all_products
        })

def about(request):
    return render(request,'about.html')
    # return HttpResponse("this is about page ")

def services(request):
    return render(request,'services.html')
    # return HttpResponse("this is services page ")

def contact(request): #to 'add logic' to the form from the website itself the information we need to give the logic here 
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        desc = request.POST.get("desc")
        contact_entry = Contact(name = name , email = email , phone = phone , desc = desc , 
                          date = datetime.today()) #make and object of contact and it will take the data from the models and post it into the database if the information is filled from the website 
        if request.user.is_authenticated: #link the contact with the logged in user with the contact 
            contact_entry.user = request.user
        contact_entry.save()
        messages.success(request, "Your message has been sent !!")  #here is the display words used 
        return redirect("/contact")
    
    # Pre-fill form for logged-in users
    context = {}
    if request.user.is_authenticated:
        context['user_name'] = request.user.username
        context['user_email'] = request.user.email
    
    return render(request,'contact.html', context)
    # return HttpResponse("this is contact page ")

#starting the add to cart logic page 
def add_to_cart(request):
    name = request.GET.get('name')
    price = int(request.GET.get('price'))
    img = request.GET.get('img')
    
    cart = request.session.get('cart', [])
    
    # Check if item already in cart
    for item in cart:
        if item['name'] == name:
            item['quantity'] += 1
            break
    else:
        cart.append({'name': name, 'price': price, 'img': img, 'quantity': 1})
    
    request.session['cart'] = cart
    request.session.modified = True  # Already there, good!
    
    return redirect('/cart')


def view_cart(request):
    cart = request.session.get('cart', [])
    
    # Add subtotal calculation for each item
    for item in cart:
        item['subtotal'] = item['price'] * item['quantity']
    
    total = sum(item['price'] * item['quantity'] for item in cart)
    total_items = sum(item['quantity'] for item in cart)
    
    return render(request, 'cart.html', {
        'cart': cart, 
        'total': total, 
        'total_items': total_items,
        'cart_count': len(cart)  # This could be changed to total_items for consistency
    })



def remove_from_cart(request, name):
    cart = request.session.get('cart', [])
    cart = [item for item in cart if item['name'] != name]
    request.session['cart'] = cart
    request.session.modified = True  # Add this line
    return redirect('/cart')


def update_quantity(request, name, action):
    cart = request.session.get('cart', [])
    for item in cart:
        if item['name'] == name:
            if action == 'plus':
                item['quantity'] += 1
            elif action == 'minus':
                item['quantity'] -= 1
                if item['quantity'] <= 0:  # Remove item if quantity becomes 0
                    cart.remove(item)
                    break
            break
    request.session['cart'] = cart
    request.session.modified = True  # Add this line
    return redirect('/cart')


#here we are using the ajax to prevent the whole page from reloading making smooth user experience 
def remove_from_cart_ajax(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        item_name = data.get('item_name')
        cart = request.session.get('cart', [])
        
        # Remove the item from cart
        cart = [item for item in cart if item['name'] != item_name]
        
        request.session['cart'] = cart
        request.session.modified = True
        
        # Calculate cart totals
        cart_total = sum(item['price'] * item['quantity'] for item in cart)
        total_items = sum(item['quantity'] for item in cart)
        
        return JsonResponse({
            'success': True, 
            'cart_total': cart_total,     # Changed from 'total' to 'cart_total'
            'total_items': total_items
        })
    
    return JsonResponse({'success': False})


def update_quantity_ajax(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        item_name = data.get('item_name')
        action = data.get('action')
        cart = request.session.get('cart', [])
        
        # Store the current item's subtotal
        item_subtotal = 0
        current_quantity = 0
        
        for item in cart:
            if item['name'] == item_name:
                if action == 'plus':
                    item['quantity'] += 1
                elif action == 'minus':
                    item['quantity'] -= 1
                    if item['quantity'] <= 0:
                        cart.remove(item)
                        current_quantity = 0
                        item_subtotal = 0
                        break
                
                # Calculate item subtotal and store current quantity
                current_quantity = item['quantity']
                item_subtotal = item['price'] * item['quantity']
                break
        
        request.session['cart'] = cart
        request.session.modified = True
        
        # Calculate cart totals
        cart_total = sum(item['price'] * item['quantity'] for item in cart)
        total_items = sum(item['quantity'] for item in cart)
        
        return JsonResponse({
            'success': True, 
            'quantity': current_quantity,
            'subtotal': item_subtotal,        # Individual item subtotal
            'cart_total': cart_total,         # Overall cart total
            'total_items': total_items
        })
    
    return JsonResponse({'success': False})


#ending of the add to cart logic page 

#checkout page logic 

@login_required(login_url='/login') 
def checkout(request):
    cart = request.session.get('cart', [])
    if not cart:
        messages.info(request, "Your cart is empty!")
        return redirect('cart')

    total = sum(item['price'] * item['quantity'] for item in cart)
    total_items_count = sum(item['quantity'] for item in cart)

    ist_timezone = pytz.timezone('Asia/Kolkata')
    current_time_ist = timezone.now().astimezone(ist_timezone)

    summary_lines = [
        "AHMED ICE CREAMS",
        "Order Receipt",
        f"Date: {current_time_ist.strftime('%d/%m/%Y %H:%M')}",
        "-" * 35
    ]

    for item in cart:
        subtotal = item['price'] * item['quantity']
        summary_lines.append(f"{item['name']}")
        summary_lines.append(f" ₹{item['price']} × {item['quantity']} = ₹{subtotal}")

    summary_lines.append("-" * 35)
    summary_lines.append(f"TOTAL: ₹{total}")
    summary_lines.append(f"Items: {total_items_count}")
    summary_lines.append("Thank you for your order!")

    items_summary = '\n'.join(summary_lines)

    # Calculate next order number for this user
    order_number = get_next_order_number(request.user)

    # Save the order with user-specific order number
    order = Order.objects.create(
        user=request.user,
        order_number=order_number,
        total_amount=total,
        items_summary=items_summary
    )

    request.session['cart'] = []
    request.session.modified = True

    display_items = [{
        'name': item['name'],
        'price': item['price'],
        'quantity': item['quantity'],
        'img': item['img'],
        'subtotal': item['price'] * item['quantity']
    } for item in cart]

    return render(request, 'checkout.html', {
        'items': display_items,
        'total': total,
        'brand': 'AHMED ICE CREAMS',
        'order': order,
        'current_time_ist': current_time_ist,
    })



#ending of checkout page 

#starting of the forgot password 

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            
            # Generate token and store in session temporarily
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            
            # Store in session for quick access
            request.session['reset_user_id'] = user.pk
            request.session['reset_token'] = token
            request.session['reset_uid'] = uid
            
            # Pass uid and token to template
            return render(request, 'password_reset_sent.html', {
                'email': email,
                'uid': uid,
                'token': token
            })
            
        except User.DoesNotExist:
            messages.error(request, "No account found with this email address.")
            return redirect('/forgot-password/')
    
    return render(request, 'forgot_password.html')

#ending 

def password_reset_sent(request, email): #this is to check with the email which will directly send you to the reset password page 
    return render(request, 'password_reset_sent.html', {'email': email})

#starting of the reset password 
def reset_password(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            password = request.POST.get('password')
            password_confirm = request.POST.get('password_confirm')
            
            if password != password_confirm:
                messages.error(request, "Passwords do not match.")
                return render(request, 'reset_password.html', {'valid_link': True})
            
            # Update user's password
            user.set_password(password)
            user.save()
            
            messages.success(request, "Your password has been reset successfully! You can now login.")
            return redirect('/login/')
        
        return render(request, 'reset_password.html', {'valid_link': True})
    else:
        messages.error(request, "The password reset link is invalid or has expired.")
        return render(request, 'reset_password.html', {'valid_link': False})
#ending of the reset password 

#services page 

# Add to home/views.py
def book_services(request):
    if request.method == "POST":
        # Get form data
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        address = request.POST.get("address")
        service_type = request.POST.get("service_type")
        event_date = request.POST.get("event_date")
        guest_count = request.POST.get("guest_count")
        budget_range = request.POST.get("budget_range")
        special_requirements = request.POST.get("special_requirements")
        
        # Create service booking entry
        service_booking = ServiceBooking(
            name=name, 
            email=email, 
            phone=phone,
            address=address,
            service_type=service_type,
            event_date=event_date,
            guest_count=guest_count,
            budget_range=budget_range,
            special_requirements=special_requirements,
            date=datetime.today()
        )

        # Link to the logged-in user, if they exist
        if request.user.is_authenticated:
            service_booking.user = request.user
        
        service_booking.save()
        messages.success(request, "Your service booking request has been submitted! We'll contact you soon.")
        return redirect('/book-services/')
    
    # Pre-fill form for logged-in users
    context = {}
    if request.user.is_authenticated:
        context['user_name'] = request.user.username
        context['user_email'] = request.user.email

    return render(request, 'book_services.html', context)

def get_next_order_number(user):  #here inside the views the order of that user will be incremented by 1 for each next order and for the existing it will continue +1
    last_order = Order.objects.filter(user=user).order_by('-order_number').first()
    if last_order:
        return last_order.order_number + 1
    else:
        return 1


# In your views.py - Add this to any view for debugging and remove it when it is used for production 
#this is used to solve the issue for admin and a website or a user seperate when the admin logs into the database the user name will not change to the admin 
def some_view(request):
    print(f"Current user: {request.user}")
    print(f"Is authenticated: {request.user.is_authenticated}")
    print(f"Is superuser: {request.user.is_superuser}")
    
# Add this to views.py for testing only
def clear_session(request):
    request.session.flush()  # Clears all session data
    return redirect('/')







# '''shell - if you run with this command inside your terminal and if you give any import model and check the objects it will 
# show the name of each and every contact given inside the form and the table name which is saved inside the database 
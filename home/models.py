from django.db import models
from django.contrib.auth.models import User #this imports the user 


#only make changes if you are about to connect the page with the database by making classes 
#makemigrations - create changes and store in a file 
#migrate - apply the pending changes created by makemigrations to go inside the dbsqlite and make the changes 

#create your models here 


class Contact (models.Model):  #make a class contact model so that when you type inside the form it will take the information or amound of words which is given inside this class model
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True) #added the user field 
    name = models.CharField(max_length=122)  #here the name,email..etc are called as objects inside a class
    email = models.CharField(max_length=122)
    phone = models.CharField(max_length=12)
    desc = models.TextField()
    date = models.DateField()
    status = models.CharField(max_length=20, default='Received')  # NEW - Added status tracking
    
    def __str__(self):  #here the data inside the table of contact will get saved with the name 
        return f"Message from {self.name}"
    
#whatever changes have been made inside the models and then if we run it using makemigrations it will be visible example:-model contact created 


#it creates a new folder for order and the files will be arranged according to the number of orders placed 
from django.db import models

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True) #added user field and this on_delete=null is given when a user delets the account the data will be stored in the database but it will be null and it cannot be used again by the user with that account 
    order_number = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    total_amount = models.PositiveIntegerField()
    items_summary = models.TextField(default="")  # Contains everything including total items
    status = models.CharField(max_length=20, default='Delivered')  # NEW - Added status tracking

    class Meta:
        unique_together = ('user','order_number') #this here is added for every new user the order will start from the 1st as he is ordering it for the first time 
        ordering = ['-order_number'] 
    
    def __str__(self):
        return f"Order #{self.order_number} - {self.user.username if self.user else 'Guest'}"  #here the order will be shown by the name of the user in the database 

#this is to view the services and whatever is selected is taken inside the database
class ServiceBooking(models.Model):
    SERVICE_CHOICES = [
        ('custom_orders', 'Custom Ice Cream Orders'),
        ('bulk_orders', 'Franchise and Bulk Orders'),
        ('event_catering', 'Event Catering'),
        ('birthday_parties', 'Birthday Parties'),
        ('corporate_events', 'Corporate Events'),
        ('wedding_catering', 'Wedding Catering'),
    ]
    
    BUDGET_CHOICES = [
        ('under_5000', 'Under ₹5,000'),
        ('5000_15000', '₹5,000 - ₹15,000'),
        ('15000_30000', '₹15,000 - ₹30,000'),
        ('30000_50000', '₹30,000 - ₹50,000'),
        ('above_50000', 'Above ₹50,000'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=122)
    email = models.CharField(max_length=122)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    service_type = models.CharField(max_length=50, choices=SERVICE_CHOICES)
    event_date = models.DateField()
    guest_count = models.PositiveIntegerField()
    budget_range = models.CharField(max_length=20, choices=BUDGET_CHOICES)
    special_requirements = models.TextField(blank=True, null=True)
    date = models.DateField()
    status = models.CharField(max_length=20, default='Pending')  # NEW - Added status tracking
    
    def __str__(self):
        return f"Service Booking - {self.name} ({self.service_type})"




#idea taken from 'django query framework'
# >>> ins = Contact.objects.filter(name = "AHMED PASHA", phone = "2354122222")[0]
# >>> ins.phone = "8123516298"
# >>> ins.save()  here this is an instance from where you can change the name or phone no. etc.. of the database 
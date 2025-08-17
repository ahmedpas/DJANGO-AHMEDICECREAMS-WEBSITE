from django.contrib import admin
from home.models import Contact,Order,ServiceBooking
# Register your models here.


admin.site.register(Contact) #here register the contact because you want it to  be stored inside the database
admin.site.register(Order)  #here inside the admin database the order folder is registered 
admin.site.register(ServiceBooking)

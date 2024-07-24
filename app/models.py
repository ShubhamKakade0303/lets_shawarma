from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Item(models.Model):
    i_image = models.ImageField(upload_to = 'Images', default = 1)
    i_name = models.CharField(max_length = 50)
    CAT = ((1, "veg"),(2, "non-veg"))
    i_category = models.IntegerField(choices = CAT, verbose_name="category")
    i_desc = models.TextField()
    i_price = models.FloatField()
    
    def __str__(self):
        return self.i_name

class Platter(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    product = models.ForeignKey(Item, on_delete = models.CASCADE)
    qty = models.PositiveIntegerField(default = 0)

    @property
    def total_cost(self):
        return self.qty * self.product.i_price

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=15)
    otp = models.CharField(max_length=6) 

STATE_CHOICES = (
    ('Andhra Pradesh', 'Andhra Pradesh'),
    ('Arunachal Pradesh','Arunachal Pradesh'),  
    ('Assam','Assam'), 
    ('Bihar', 'Bihar'), 
    ('Chhattisgarh', 'Chhattisgarh'), 
    ('Goa', 'Goa'), 
    ('Gujarat', 'Gujarat'), 
    ('Haryana','Haryana'), 
    ('Himachal Pradesh','Himachal Pradesh'), 
    ('Jharkhand', 'Jharkhand'), 
    ('Karnataka', 'Karnataka'), 
    ('Kerala','Kerala'), 
    ('Madhya Pradesh','Madhya Pradesh'),
    ('Maharashtra','Maharashtra'), 
    ('Manipur', 'Manipur'), 
    ('Meghalaya', 'Meghalaya'),
    ('Mizoram', 'Mizoram'), 
    ('Nagaland', 'Nagaland'), 
    ('Odisha', 'Odisha'), 
    ('Punjab', 'Punjab'), 
    ('Rajasthan', 'Rajasthan'), 
    ('Sikkim', 'Sikkim'), 
    ('Tamil Nadu', 'Tamil Nadu'),
    ('Telangana', 'Telangana'), 
    ('Tripura', 'Tripura'), 
    ('Uttar Pradesh', 'Uttar Pradesh'),
    ('Uttarakhand', 'Uttarakhand'), 
    ('West Bengal', 'West Bengal'),
    )

class Customer(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    name = models.CharField(max_length=200)
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    mobile = models.IntegerField(default=0)
    pincode = models.IntegerField()
    state = models.CharField(choices=STATE_CHOICES, max_length=100)
    def __str__(self):
        return self.name


STATUS_CHOICES = (
    ('Accepted', 'Accepted'),
    ('Packed', 'Packed'),
    ('On the way', 'On the way'),
    ('Delivered', 'Delivered'),
    ('Cancel', 'Cancel'),
    ('Pending', 'Pending'),
)

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField()
    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_payment_status = models.CharField(max_length=100, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
    paid = models.BooleanField(default=False)

class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')
    payments = models.ForeignKey(Payment, on_delete=models.CASCADE, default="")

    @property
    def total_cost(self):
        return self.quantity * self.product.i_price
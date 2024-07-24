from django.contrib import admin
from .models import Item, Platter, Profile, OrderPlaced, Payment
# Register your models here.

admin.site.register(Item)
admin.site.register(Profile)

@admin.register(Platter)
class PlatterModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','product','qty']

@admin.register(Payment)
class PaymentModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','amount','razorpay_order_id', 'razorpay_payment_status', 'razorpay_payment_id', 'paid']

@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','customer','product', 'quantity', 'ordered_date', 'status', 'payments']

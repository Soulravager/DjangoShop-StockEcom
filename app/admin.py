from django.contrib import admin
from . models import Cart,Customer,Product,Payment,OrderPlaced,Wishlist

# Register your models here.

@admin.register(Product)

class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id' , 'title' , 'discounted_price' , 'category','product_image','stock']

@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','locality','city','state','zipcode']

@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','product','quantity']

@admin.register(Payment)
class PaymentModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','amount','razorpay_order_id','razorpay_payment_status','razorpay_payment_id','paid']


'''@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','customer','product','quantity','ordered_date','status','payment']
'''

@admin.register(Wishlist)
class WishlistModeAdmin(admin.ModelAdmin):
    list_display = ['id','user','product']
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

class CustomAdminSite(admin.AdminSite):
    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        custom_urls = [
            path('app/', self.admin_view(admin_dashboard), name='admin-dashboard'),
        ]
        return custom_urls + urls

admin.site.site_header = "E-Commerce Admin"
admin.site.site_title = "E-Commerce Dashboard"
admin.site.index_title = format_html('<a href="/admin-dashboard/">Go to Admin Dashboard</a>')


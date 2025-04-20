from django.db import models
from django.contrib.auth.models import User

# Create your models here.
STATE_CHOICES = (
        ('Kerala', ' Kerala'),
    ('hydrabad','hydrabad'),
    ('karanataka','banglaor'),
    ('Tmail Nadu','chennai'),


)

CATEGORY_CHOICES=(
    ('HO', 'LapTop'),
    ('HS', 'Mobile Phone'),
    ('HM', 'Tablet'),
    ('HC', 'Smartwatch'),
    ('SH', 'Camera'),
    ('HB', 'ear pods'),
)


class Product(models.Model):
    title = models.CharField(max_length=100)
    selling_price = models.FloatField()
    discounted_price = models.FloatField()
    description = models.TextField()
    stock = models.IntegerField(null=True, blank=True)   
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2, null=True)
    product_image = models.ImageField(upload_to='product')
    average_rating = models.FloatField(default=0.0)

    def __str__(self):
        return self.title

    def update_average_rating(self):
        reviews = self.reviews.all()
        if reviews.exists():
            self.average_rating = sum([review.rating for review in reviews]) / reviews.count()
        else:
            self.average_rating = 0.0
        self.save()


class Customer(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    mobile = models.CharField(max_length=10)  
    mail=models.EmailField(blank= True)
    zipcode= models.IntegerField()
    state = models.CharField(choices=STATE_CHOICES,max_length=100)
    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    

    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price


STATUS_CHOICES = (
    ('Accepted','Accepted'),
    ('Packed','Packed'),
    ('On The Way','On The Way'),
    ('Delivered','Delivered'),
    ('Cancel','Cancel'),
    ('Pending','Pending'),
)

class Payment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    amount = models.FloatField()
    razorpay_order_id = models.CharField(max_length=100,blank=True,null=True)
    razorpay_payment_status = models.CharField(max_length=100,blank=True,null=True)
    razorpay_payment_id = models.CharField(max_length=100,blank=True,null=True)
    paid = models.BooleanField(default=True)




class OrderPlaced (models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50,choices= STATUS_CHOICES,default='Pending')
    payment = models.ForeignKey(Payment,on_delete=models.CASCADE,default="")
    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price
    

from django.db import models
from django.contrib.auth.models import User
ORDER_CHOICE = (
    ('Accepted','Accepted'),
    ('Packed','Packed'),
    ('On The Way','On The Way'),
    ('Delivered','Delivered'),
    ('Cancel','Cancel'),
    ('Pending','Pending'),
)

class OrderStatus(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)  # Can be null if no customer
    quantity = models.PositiveIntegerField(default=1)                             # This is fine, but can be dynamic
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True)    # Payment info for the order
    delivery_status = models.CharField(max_length=20,choices= ORDER_CHOICE, default='pending')  # Default to 'pending'
    ordered_date = models.DateTimeField()
    order_id = models.CharField(max_length=100, unique=True)  # Ensure this is unique for each order

    def __str__(self):
        return f"Order {self.order_id} - {self.product.name}"


class Wishlist(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)





from django.db import models
from django.contrib.auth.models import User

#product review and rating         #product review and rating  #product review and rating 
               
class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review_text = models.TextField()
    rating = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Review by {self.user.username} - {self.rating} Stars'


#product review and rating         #product review and rating         #product review and rating         









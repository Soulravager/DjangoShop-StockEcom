from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render,redirect,HttpResponseRedirect,get_object_or_404
from django.http import HttpResponse
from django.views import View 
import razorpay
from .models import Product ,Cart,Payment,Customer,OrderPlaced,Wishlist
from . forms import CustomerRegistrationForm,CustomerProfileForm,Customer
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
from django.db.models import Q 
from django.contrib.auth.models import User
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import AnonymousUser


# Create your views here.

def home(request):
    if request.user.is_authenticated:
        totalitem = 0
        wishlist_count = 0
        totalitem = len(Cart.objects.filter(user=request.user))
        wishlist_count = Wishlist.objects.filter(user=request.user).count()
        return render(request,'app/home.html',locals())
    else:
        return HttpResponseRedirect('login/')

def about(request):
    totalitem = 0
    wishlist_count = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishlist_count = Wishlist.objects.filter(user=request.user).count()
    return render(request,'app/about.html',locals())

def error404(request):
    return render(request, 'app/error404.html')


def contact(request):
    totalitem = 0
    wishlist_count = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishlist_count = Wishlist.objects.filter(user=request.user).count()
    return render(request,'app/contact.html',locals())
#updated category view   #updated category view   #updated category view   #updated category view   #updated category view   #updated category view   

class CategoryView(View):
    def get(self, request, val):
        totalitem = wishlist_count = 0

        if request.user.is_authenticated:
            totalitem = Cart.objects.filter(user=request.user).count()
            wishlist_count = Wishlist.objects.filter(user=request.user).count()

        product = Product.objects.filter(category=val)

        # Filters
        sort_by = request.GET.get('sort_by')
        rating_filter = request.GET.get('rating')  # specific rating
        stock_filter = request.GET.get('stock')    # 'in' or 'out'
        discount_only = request.GET.get('discount')  # 'true'

        if sort_by == 'price_lh':
            product = product.order_by('discounted_price')
        elif sort_by == 'price_hl':
            product = product.order_by('-discounted_price')
        elif sort_by == 'rating_hl':
            product = product.order_by('-average_rating')
        elif sort_by == 'rating_lh':
            product = product.order_by('average_rating')

        if rating_filter:
            product = product.filter(average_rating__gte=rating_filter)

        if stock_filter == 'in':
            product = product.filter(stock__gt=0)
        elif stock_filter == 'out':
            product = product.filter(stock__lte=0)

        if discount_only == 'true':
            product = product.filter(discounted_price__lt=models.F('selling_price'))

        title = Product.objects.filter(category=val).values('title')

        return render(request, 'app/category.html', locals())
#updated category view   #updated category view   #updated category view   #updated category view   #updated category view   #updated category view   
class CategoryTitle(View):
    def get(self,request,val):
        totalitem = 0
        wishlist_count = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishlist_count = Wishlist.objects.filter(user=request.user).count()
        product = Product.objects.filter(title=val)
        title = Product.objects.filter(category=product[0].category).values('title')
        return render(request,'app/category.html',locals())




class CustomerRegistrationView(View):
    def get(self,request):
        form = CustomerRegistrationForm()
        totalitem = 0
        wishlist_count = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishlist_count = Wishlist.objects.filter(user=request.user).count()
        return render(request, 'app/customerregistration.html',locals())
    def post(self,request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Congralution! User Register Successfully')
        else:
            messages.warning(request,'Invalid Input Data')
        return render(request, 'app/customerregistration.html',locals())

class ProfileView(View):
    def get(self,request):
        form = CustomerProfileForm()
        totalitem = 0
        wishlist_count = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishlist_count = Wishlist.objects.filter(user=request.user).count()
        return render(request,'app/profile.html',locals())
    def post(self,request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            mail = form.cleaned_data['mail']

            reg = Customer(user=user,name=name,locality=locality,mobile=mobile,city=city,state=state,zipcode=zipcode,mail=mail)
            reg.save()
            messages.success(request,'Congralutions! Profile save Successfully')
        else:
            messages.warning(request,'Invalid Input Data')
        return render(request,'app/profile.html',locals())

def address(request):
    add = Customer.objects.filter(user=request.user)
    totalitem = 0
    wishlist_count=0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishlist_count = Wishlist.objects.filter(user=request.user).count()
    return render(request,'app/address.html',locals())


class updateAddress(View):
    def get(self,request,pk):
        add = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance=add)
        totalitem = 0
        wishlist_count = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishlist_count = Wishlist.objects.filter(user=request.user).count()
        return render(request,'app/updateAddress.html',locals())
    def post(self,request,pk):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            add = Customer.objects.get(pk=pk)
            add.name = form.cleaned_data['name']
            add.locality = form.cleaned_data['locality']
            add.city = form.cleaned_data['city']
            add.mobile = form.cleaned_data['mobile']
            add.state = form.cleaned_data['state']
            add.zipcode = form.cleaned_data['zipcode']
            add.save()
            messages.success(request,'Congratulations! profile update successfully')
        else:
            messages.warning(request,'Invalid Input Data')
        return redirect('address')

def Logout(request):
    return HttpResponseRedirect('/login/')

def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = get_object_or_404(Product, id=product_id)

    if product.stock > 0:
        # Check if the product is already in the user's cart
        cart_item = Cart.objects.filter(user=user, product=product).first()

        if cart_item:
            # If the item exists, you might want to increase the quantity here
            # based on your application's logic.
            # For now, let's assume you don't want to add a duplicate.
            # You could optionally show a message to the user that the item is already in the cart.
            pass # Do nothing, item is already in the cart
        else:
            # If the item doesn't exist, create a new cart item
            Cart(user=user, product=product, quantity=1).save()
            product.stock -= 1
            product.save() # Decrease stock upon adding to cart
    else:
        # Optionally handle the case where the product is out of stock
        # You could redirect back to the product page with an error message
        pass # For now, we'll just not add it

    return redirect('/cart/')



def show_cart(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0
    for p in cart:
        value = p.quantity * p.product.discounted_price
        amount = amount + value
    totalamount = amount + 40
    totalitem = 0
    wishlist_count = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishlist_count = Wishlist.objects.filter(user=request.user).count()
    return render(request,'app/addtocart.html',locals())

def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        try:
            cart_item = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
            product = cart_item.product
            if product.stock > cart_item.quantity:
                cart_item.quantity += 1
                cart_item.save()
                product.stock -= 1
                product.save()
                user = request.user
                cart = Cart.objects.filter(user=user)
                amount = 0
                for p in cart:
                    value = p.quantity * p.product.discounted_price
                    amount = amount + value
                totalamount = amount + 40
                data = {
                    'quantity': cart_item.quantity,
                    'amount': amount,
                    'totalamount': totalamount
                }
                return JsonResponse(data)
            else:
                return JsonResponse({'error': 'Stock limit reached'}, status=400) # Or handle this in your frontend
        except Cart.DoesNotExist:
            return JsonResponse({'error': 'Item not found in cart'}, status=404)

def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        try:
            cart_item = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
                cart_item.product.stock += 1
                cart_item.product.save()
            else:
                # If quantity is 1, removing the item is usually the expected behavior
                cart_item.product.stock += 1
                cart_item.product.save()
                cart_item.delete()
                user = request.user
                cart = Cart.objects.filter(user=user)
                amount = 0
                for p in cart:
                    value = p.quantity * p.product.discounted_price
                    amount = amount + value
                totalamount = amount + 40
                data = {
                    'quantity': 0, # Indicate quantity after decrement
                    'amount': amount,
                    'totalamount': totalamount
                }
                return JsonResponse(data)

            user = request.user
            cart = Cart.objects.filter(user=user)
            amount = 0
            for p in cart:
                value = p.quantity * p.product.discounted_price
                amount = amount + value
            totalamount = amount + 40
            data = {
                'quantity': cart_item.quantity,
                'amount': amount,
                'totalamount': totalamount
            }
            return JsonResponse(data)
        except Cart.DoesNotExist:
            return JsonResponse({'error': 'Item not found in cart'}, status=404)


def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        try:
            cart_item = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
            product = cart_item.product
            product.stock += cart_item.quantity  # Increase stock by the quantity in the cart
            product.save()
            cart_item.delete()
            user = request.user
            cart = Cart.objects.filter(user=user)
            amount = 0
            for p in cart:
                value = p.quantity * p.product.discounted_price
                amount = amount + value
            totalamount = amount + 40
            data = {
                'amount': amount,
                'totalamount': totalamount
            }
            return JsonResponse(data)
        except Cart.DoesNotExist:
            return JsonResponse({'error': 'Item not found in cart'}, status=404)
from django.views import View
from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Cart, Customer, Payment, OrderStatus, Wishlist
import razorpay
from django.conf import settings
from datetime import datetime

class CheckoutView(View):
    def get(self, request):
        totalitem = 0
        wishlist_count = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishlist_count = Wishlist.objects.filter(user=request.user).count()
        
        user = request.user
        add = Customer.objects.filter(user=user)
        cart_items = Cart.objects.filter(user=user)

        famount = 0
        for p in cart_items:
            value = p.quantity * p.product.discounted_price
            famount += value
        
        totalamount = famount + 40
        razorpayamount = int(totalamount * 100)

        # Fake payment order simulation
        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
        data = {"amount": razorpayamount, "currency": "INR", "receipt": "order_rcptid_12"}
        payment_response = client.order.create(data=data)
        
        order_id = payment_response['id']
        order_status = payment_response['status']

        if order_status == 'created':
            # Save fake payment
            # Generate readable fake payment_id


            # Reduce stock of each product in the cart
            for item in cart_items:
                product = item.product
                product.stock -= item.quantity
                product.save()

            # Get latest customer for user
            try:
                customer = Customer.objects.filter(user=user).latest('id')
            except Customer.DoesNotExist:
                customer = None

            now = datetime.now()
            time_str = now.strftime("%M%H")  # MinuteHour (e.g., 1523)
            fake_payment_id = f"{time_str}-{order_id}-{customer.id if customer else '0'}"

            # Save fake payment with fake_payment_id
            payment = Payment.objects.create(
                user=user,
                amount=totalamount,
                razorpay_order_id=order_id,
                razorpay_payment_status=order_status,
                razorpay_payment_id=fake_payment_id
            )
            # Generate readable fake payment_id
            now = datetime.now()
            time_str = now.strftime("%M%H")  # MinuteHour (e.g., 1523)
            fake_payment_id = f"{time_str}-{order_id}-{customer.id if customer else '0'}"

            # Create OrderStatus entries
            for item in cart_items:
                order_id_combined = f"{fake_payment_id}_{item.product.id}"
                OrderStatus.objects.create(
                    user=user,
                    product=item.product,
                    customer=customer,
                    quantity=item.quantity,
                    payment=payment,
                    ordered_date=timezone.now(),
                    order_id=order_id_combined,
                    delivery_status='pending'
                )
                OrderPlaced.objects.create(
                    user=user,
                    product=item.product,
                    customer=customer,
                    quantity=item.quantity,
                    payment=payment,
                    ordered_date=timezone.now(), 
                )

      
        return render(request, 'app/checkout.html', locals())


from django.contrib.auth import login
from django.shortcuts import redirect
from django.contrib import messages
from .models import OrderStatus, Customer, Cart, Payment
from django.utils import timezone
import uuid
from datetime import datetime

def payment_done(request):
    if not request.user.is_authenticated:
        # Try to get user from session
        user_id = request.session.get('_auth_user_id')
        if user_id:
            user = User.objects.get(pk=user_id)
            login(request, user)  # Re-authenticate user
        else:
            return redirect('login')  # Redirect to login if session is lost

    order_id = request.GET.get('order_id')
    payment_id = str(uuid.uuid4())  # For testing purposes; you can use a custom payment_id format
    cust_id = request.GET.get('cust_id')

    user = request.user  # Ensure user is authenticated

    try:
        customer = Customer.objects.get(id=cust_id)
        payment = Payment.objects.get(razorpay_order_id=order_id)
        payment.paid = True  # Mark payment as successful
        payment.razorpay_payment_id = payment_id
        payment.save()

        # Loop through the cart items
        cart = Cart.objects.filter(user=user)
        for c in cart:
            # Create OrderStatus entry immediately
            order_id_combined = f"{payment_id}_{c.product.id}"  # Generate a unique order ID combining payment_id and product_id
            OrderStatus.objects.create(
                user=user,
                product=c.product,
                customer=cust_id,  # Reference the customer
                quantity='1',  # Ensure the quantity is passed correctly
                payment=payment_id,  # Link to the payment
                delivery_status='pending',  # Default to pending
                ordered_date=timezone.now(),  # Use the current date and time
                order_id=order_id_combined  # The unique order ID
            ).save()

        return redirect('orders')  # Redirect to orders page

    except Customer.DoesNotExist:
        messages.error(request, "Customer not found.")
        return redirect('home')

    except Payment.DoesNotExist:
        messages.error(request, "Payment details not found.")
        return redirect('home')



def order_confirmation(request):
    cart_items=Cart.objects.filter(user=request.user)
    famount = 0
    for p in cart_items:
        value = p.quantity * p.product.discounted_price
        famount = famount + value
    totalamount = famount + 40
    razorpayamount = int(totalamount * 100)
    client = razorpay.Client(auth=("rzp_test_9BZyJ3buu1pncT", "6QKQl4eZL8qSwxmeZy02o4tv"))
    data = { "amount": razorpayamount, "currency": "INR", "receipt": "order_rcptid_11" }
    payment = client.order.create(data=data)
    context={
        'amt': razorpayamount,'user':request.user
    }

    return render(request,'app/pay.html',context)

from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from .models import Cart, Wishlist, OrderPlaced

from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from .models import Cart, Wishlist, OrderPlaced
from datetime import datetime, timedelta

from .models import Customer

def send_order_confirmation_email(user, order_placed):
    # Get Customer instance for this user
    try:
        customer = Customer.objects.get(user=user)
        recipient = customer.mail
    except Customer.DoesNotExist:
        print(f"❌ No customer record found for user: {user}")
        return

    delivery_date = datetime.now() + timedelta(days=5)
    email_subject = "🧾 Your Order Receipt - Rapunzel's Roots"
    email_body = f"Hi {customer.name},\n\nThank you for your order! Here is your receipt:\n\n"

    total_amount = 0
    for order in order_placed:
        item_total = order.product.discounted_price * order.quantity
        total_amount += item_total
        email_body += (
            f"Product: {order.product.name}\n"
            f"Quantity: {order.quantity}\n"
            f"Price per item: ₹{order.product.discounted_price}\n"
            f"Total for this item: ₹{item_total}\n\n"
        )

    email_body += (
        f"----------------------------------\n"
        f"Total Amount: ₹{total_amount}\n"
        f"Expected Delivery Date: {delivery_date.strftime('%d %B %Y')}\n"
        f"----------------------------------\n"
        f"\nIf you have any questions, feel free to contact us.\n"
        f"\nThanks for shopping with us!\nTeam Rapunzel's Roots"
    )

    sender = settings.EMAIL_HOST_USER

    # # Debug logs including receiver's email
    # print("\n========== EMAIL DEBUG LOG ==========")
    # print(f"📤 Sender:    {sender}")
    # print(f"📩 Recipient: {recipient}")
    # print(f"📝 Subject:   {email_subject}")
    # print(f"💰 Total:     ₹{total_amount}")
    # print(f"📦 Delivery:  {delivery_date.strftime('%d %B %Y')}")
    # print(f"📨 Email Body Preview:\n{email_body[:300]}{'...' if len(email_body) > 300 else ''}")
    # print("=====================================\n")

    try:
        send_mail(
            email_subject,
            email_body,
            sender,
            [recipient],
            fail_silently=False
        )
        print(f"✅ Email sent successfully to {recipient}\n")
    except Exception as e:
        print(f"❌ Failed to send email to {recipient}: {str(e)}\n")



@csrf_exempt
def orders(request):
    totalitem = 0
    wishlist_count = 0
    order_placed = []

    if request.user.is_authenticated:
        totalitem = Cart.objects.filter(user_id=request.user).count()
        wishlist_count = Wishlist.objects.filter(user=request.user).count()
        order_placed = OrderPlaced.objects.filter(user=request.user)
        user = request.user

        # 📬 Send email immediately when the orders page is accessed
        #send_order_confirmation_email(user, order_placed)@@@@@@@@@@@@@@@

    context = {
        'totalitem': totalitem,
        'wishlist_count': wishlist_count,
        'order_placed': order_placed
    }
    return render(request, 'app/orders.html', context)

def plus_wishlist(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        product = Product.objects.get(id=prod_id)
        user = request.user
        if not Wishlist.objects.filter(user=user, product=product).exists():
            Wishlist(user=user, product=product).save()

        data = {'message': 'Wishlist Added Successfully'}
        return JsonResponse(data)

def minus_wishlist(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        product = Product.objects.get(id=prod_id)
        user = request.user
        Wishlist.objects.filter(user=user, product=product).delete()

        data = {'message': 'Wishlist Removed Successfully'}
        return JsonResponse(data)

        

def search(request):
    query=request.GET['search']
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    product = Product.objects.filter(Q(title__icontains=query))
    return render(request,'app/search.html',locals())



from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import models
from .models import Product, OrderPlaced, Customer, Payment
from .forms import ProductForm

# Ensure only admin users can access the dashboard
def admin_required(user):
    return user.is_staff  # Only allow staff members (admin) to access

@user_passes_test(admin_required)
def admin_dashboard(request):
    total_products = Product.objects.count()
    total_orders = Payment.objects.count()
    total_customers = Customer.objects.count()
    total_revenue = Payment.objects.filter(paid=True).aggregate(total_amount=models.Sum('amount'))['total_amount'] or 0
    pending_orders = OrderPlaced.objects.filter(status='Pending').count()

    # Product form for adding a product
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')  # Redirect to refresh the dashboard
    else:
        form = ProductForm()

    context = {
        'total_products': total_products,
        'total_orders': total_orders,
        'total_customers': total_customers,
        'total_revenue': total_revenue,
        'pending_orders': pending_orders,
        'form': form,  # Pass form to template
    }
    
    return render(request, 'app/admin_dashboard.html', context)


from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .models import Cart

@login_required
def clear_cart(request):
    # Delete all cart items for the logged-in user
    Cart.objects.filter(user=request.user).delete()
    return redirect('orders')  # Redirect to cart or any desired page


from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Cart, Wishlist, Review
from .forms import ReviewForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
#Updated WIshlist and others   #Updated WIshlist and others   #Updated WIshlist and others   #Updated WIshlist and others   
class ProductDetail(View):
    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        totalitem = 0
        wishlist_count = 0
        form = ReviewForm()
        reviews = product.reviews.all().order_by('-created_at')

        # Check if this product is in the user's wishlist
        wishlist = False
        if request.user.is_authenticated:
            totalitem = Cart.objects.filter(user=request.user).count()
            wishlist_count = Wishlist.objects.filter(user=request.user).count()
            wishlist = Wishlist.objects.filter(user=request.user, product=product).exists()

        return render(request, 'app/productdetail.html', {
            'product': product,
            'totalitem': totalitem,
            'wishlist_count': wishlist_count,
            'form': form,
            'reviews': reviews,
            'wishlist': wishlist  # <== Pass it to the template
        })

#Updated WIshlist and others   #Updated WIshlist and others   #Updated WIshlist and others   
#BUY NOW BTN  #BUY NOW BTN  #BUY NOW BTN  #BUY NOW BTN  #BUY NOW BTN  #BUY NOW BTN  #BUY NOW BTN  #BUY NOW BTN  
from django.shortcuts import redirect
from .models import Cart, Product

def buy_now(request):
    if request.method == 'POST':
        prod_id = request.POST.get('prod_id')
        product = Product.objects.get(id=prod_id)
        if request.user.is_authenticated:
            cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
        return redirect('showcart')  # This is your cart page
    return redirect('/')
#BUY NOW BTN  #BUY NOW BTN  #BUY NOW BTN  #BUY NOW BTN  #BUY NOW BTN  #BUY NOW BTN  #BUY NOW BTN  #BUY NOW BTN  
#product review and rating         #product review and rating         

@login_required
def submit_review(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    
    # Get existing review if any
    review = Review.objects.filter(product=product, user=request.user).first()
    
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            product.update_average_rating()
            return redirect('product-detail', pk=product.pk)
    else:
        form = ReviewForm(instance=review)

    # Pass form + reviews for display
    reviews = Review.objects.filter(product=product).order_by('-created_at')
    return render(request, 'app/product_detail.html', {
        'product': product,
        'form': form,
        'reviews': reviews,
    })

#product review and rating         #product review and rating         #product review and rating         

#admin dashboard editing option   #admin dashboard editing option   #admin dashboard editing option   

@user_passes_test(admin_required)
def manage_products(request):
    products = Product.objects.all()

    if request.method == 'POST':
        pk = request.POST.get('product_id')
        product = get_object_or_404(Product, pk=pk)
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('manage_products')
    else:
        form = ProductForm()

    return render(request, 'app/manage_products.html', {'products': products, 'form': form})


@user_passes_test(admin_required)
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    return redirect('manage_products')
#admin dashboard editing option   #admin dashboard editing option   #admin dashboard editing option   

#ADD WiSh LIST PAGE    #ADD WiSh LIST PAGE   #ADD WiSh LIST PAGE   #ADD WiSh LIST PAGE   #ADD WiSh LIST PAGE   

from django.shortcuts import render, redirect, get_object_or_404
from .models import Wishlist, Product, Cart  # and other required models
from django.contrib.auth.decorators import login_required

@login_required
def show_wishlist(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    totalitem = Cart.objects.filter(user=request.user).count()
    wishlist_count = wishlist_items.count()
    return render(request, 'app/wishlist.html', locals())

@login_required
def remove_from_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    Wishlist.objects.filter(user=request.user, product=product).delete()
    return redirect('showwishlist')

#ADD WiSh LIST PAGE   #ADD WiSh LIST PAGE   #ADD WiSh LIST PAGE   #ADD WiSh LIST PAGE   

from django.shortcuts import render
from .models import Product
from django.db.models import Q

def category_view(request, category_slug=None):
    products = Product.objects.all()

    # Example: category filtering
    if category_slug:
        products = products.filter(category=category_slug)

    # Rating Filter
    min_rating = request.GET.get('min_rating')
    if min_rating:
        products = products.filter(average_rating__gte=min_rating)

    # Favourites Filter (assuming you have user favorites logic)
    if request.GET.get('favourites') == '1' and request.user.is_authenticated:
        products = products.filter(favourite_users=request.user)

    # Sorting
    sort = request.GET.get('sort')
    if sort == 'low_to_high':
        products = products.order_by('discounted_price')
    elif sort == 'high_to_low':
        products = products.order_by('-discounted_price')
    elif sort == 'high_rating':
        products = products.order_by('-average_rating')

    context = {
        'product': products,
        'category_name': category_slug,
    }

    return render(request, 'app/category.html', context)

#ADD WiSh LIST PAGE   #ADD WiSh LIST PAGE   #ADD WiSh LIST PAGE   #ADD WiSh LIST PAGE   
#order History #order History #order History #order History #order History #order History 




# In your views.py
from django.shortcuts import render
from .models import OrderStatus

from django.shortcuts import render
from .models import OrderStatus

def get_progress_percentage(status):
    progress_map = {
        "Pending": 10,
        "Accepted": 30,
        "Packed": 50,
        "On The Way": 70,
        "Delivered": 100
    }
    return progress_map.get(status, 0)

def order_history(request):
    orders = OrderStatus.objects.filter(user=request.user)
    
    for order in orders:
        order.progress = get_progress_percentage(order.delivery_status)
        
    return render(request, 'app/order_history.html', {'orders': orders})

from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import OrderStatus



def cancel_order(request, order_id):
    order = get_object_or_404(OrderStatus, id=order_id)
    order.delivery_status = 'Cancel'  # Set status to 'Cancel'
    order.save()
    return redirect('order_history')  # Ensure this points to the correct view for order history


from django.shortcuts import render, redirect, get_object_or_404
from .models import OrderStatus
from django.contrib.auth.decorators import login_required, user_passes_test

from .models import OrderStatus, ORDER_CHOICE

from datetime import timedelta
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from .models import OrderStatus

ORDER_CHOICE = [
    ('Pending', 'Pending'),
    ('Accepted', 'Accepted'),
    ('Packed', 'Packed'),
    ('On The Way', 'On The Way'),
    ('Delivered', 'Delivered'),
    ('Cancel', 'Cancel'),
]

@login_required
def manage_orders(request):
    # Get orders with related fields
    orders = OrderStatus.objects.select_related('user', 'product', 'payment')

    # Filter by status if provided
    status_filter = request.GET.get('status')
    if status_filter:
        orders = orders.filter(delivery_status=status_filter)

    # Filter by time range if provided
    time_range_filter = request.GET.get('time_range')
    if time_range_filter:
        if time_range_filter == 'last_7_days':
            start_date = timezone.now() - timedelta(days=7)
            orders = orders.filter(ordered_date__gte=start_date)
        elif time_range_filter == 'last_30_days':
            start_date = timezone.now() - timedelta(days=30)
            orders = orders.filter(ordered_date__gte=start_date)
        elif time_range_filter == 'this_month':
            start_date = timezone.now().replace(day=1)
            orders = orders.filter(ordered_date__gte=start_date)
        elif time_range_filter == 'last_month':
            start_date = timezone.now().replace(day=1) - timedelta(days=1)
            start_date = start_date.replace(day=1)
            orders = orders.filter(ordered_date__gte=start_date)

    # Sort orders by time if selected
    sort_by = request.GET.get('sort_by', 'latest')
    if sort_by == 'oldest':
        orders = orders.order_by('ordered_date')  # Oldest first
    else:
        orders = orders.order_by('-ordered_date')  # Latest first

    # Handle status update on POST
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        new_status = request.POST.get('delivery_status')
        order = get_object_or_404(OrderStatus, id=order_id)
        order.delivery_status = new_status
        order.save()
        return redirect('manage_orders')

    return render(request, 'app/manage_orders.html', {
        'orders': orders,
        'status_choices': ORDER_CHOICE
    })


#order History #order History #order History #order History #order History #order History #order History 


import os
from django.conf import settings

def banner_images(request):
    banner_dir = os.path.join(settings.STATICFILES_DIRS[0], 'images/banner')
    try:
        images = [
            f'images/banner/{f}' 
            for f in os.listdir(banner_dir) 
            if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))
        ]
    except FileNotFoundError:
        images = []
    return {'banner_images': images}

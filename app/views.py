from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import Item, Platter, Profile, Customer, Payment, OrderPlaced
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
import random, http.client, json, razorpay
from django.conf import settings

# Create your views here.

def home(request):
    return render(request, "home.html")

def xlogin(request):
    context = {}
    if request.method == "POST":
        eemail = request.POST.get("email")
        epassword = request.POST.get("password")
        if epassword == "" or eemail == "":
            context["error_message"] = "Fields cannot be empty"
            return render(request, "xlogin.html", context)
        else:
            u = authenticate(username=eemail, password=epassword)
            print(u)
            if u is not None:
                login(request, u)
                return redirect("/home")
            else:
                context["error_message"] = "Invalid username or password"
                return render(request, "xlogin.html", context)
    
    return render(request, "xlogin.html")

'''def phone_login(request):
    context = {}
    if request.method == "POST":
        mobile = request.POST.get("mobile")
        user = Profile.objects.filter(mobile = mobile).first()
        if user is None:
            context["error_message"] = "User not found"
            return render(request,"xlogin.html",context)
        
        otp = str(random.randint(1000, 9999))
        user.otp = otp
        user.save()
        send_otp(mobile, otp)
        request.session['mobile'] = mobile
        return redirect("/xlogin_otp")
    return render(request, "phone_login.html")'''



'''def xlogin_otp(request):
    context = {}
    if request.method == 'POST':
        mobile = request.session.get("mobile")
        if mobile:
            otp = str(random.randint(1000, 9999))
            profile = Profile(user = User, mobile = mobile, otp = otp)
            profile.save()
            #profile = Profile.objects.filter(mobile = mobile).first()
            if otp == profile.otp:
                user = User.objects.get(id = profile.user.id)
                login(request, user)
            #send_otp(mobile, otp)
            request.session["mobile"] = mobile
            return redirect("/otp")
            #otp = request.POST.get('otp')
            #send_otp(mobile, otp)
            #profile = Profile.objects.filter(mobile = mobile).first()
            #if otp == profile.otp:
                #user = User.objects.get(id = profile.user.id)
                #login(request, user)
            return redirect('/home')
        else:
            context = {'message' : 'Incorrect otp', 'class' : 'alert alert-danger', 'mobile' : mobile}
            return render (request, "xlogin_otp.html", context)

    return render (request, "xlogin_otp.html", context)'''

def xlogout(request):
    logout(request)
    print("Session deleted")
    return redirect("/home")

def signup(request):
    context = {}
    if request.method == "POST":
        ename = request.POST.get("name")
        eemail = request.POST.get("email")
        epassword = request.POST.get("password")
        econfirm_password = request.POST.get("confirm_password")
        emobile = request.POST.get("mobile")

        check_user = User.objects.filter(email = eemail).first()
        check_profile = Profile.objects.filter(mobile = emobile).first()

        if check_user or check_profile:
            context["error_message"] = "Already registered" 
            return  render(request, "signup.html",context)

        if not all([ename, eemail, epassword, econfirm_password, emobile]):
            context["error_message"] = "Fields cannot be empty"
            return render(request, "signup.html", context)
        elif epassword != econfirm_password:
            context["error_message"] = "Passwords don't match!"
            return render(request, "signup.html", context)
        
        '''if ename == "" or eemail == "" or epassword == "" or econfirm_password == "" or emobile == "":
            context["error_message"] = "Fields cannot be empty"
            return render(request, "signup.html", context)
        elif epassword != econfirm_password:
            context["error_message"] = "Password dosen't match!"
            return render(request, "signup.html", context)
        elif check_user or check_profile:
            context["error_message"] = "Already exists"
            return render(request, "signup.html", context)
        else:
            if User.objects.filter(username=eemail).exists():
                context["error_message"] = "Already taken."
            else:
                u = User.objects.create_user(
                    username = eemail,
                    email = eemail,
                    password = epassword,
                    first_name = ename,
                    mobile = emobile,
                )
                context["success"] = "Registration successful"
                return redirect("/xlogin")'''

        user = User(email = eemail, first_name = ename, username = eemail)
        user.set_password(epassword)
        user.save()    

        otp = str(random.randint(1000, 9999))
        profile = Profile(user = user, mobile = emobile, otp = otp)
        profile.save()

        send_otp(emobile, otp)
        request.session["mobile"] = emobile
        return redirect("/otp")
    else:    
        return render(request, "signup.html")

def send_otp(mobile, otp):
    conn = http.client.HTTPSConnection("control.msg91.com")
    headers = {
        'Content-Type': "application/JSON", 
        'authkey': settings.AUTH_KEY 
        }
    payload = {
        "sender": "ABC",
        "message": f"Your OTP is {otp}",
        "mobile": mobile,
        "country": "91"
        }
    payload_json = json.dumps(payload)

    conn.request("POST", "/api/v5/otp", payload_json, headers = headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))
    #return redirect('/home')

def otp(request):
    mobile = request.session["mobile"]
    context = {"mobile": mobile}
    if request.method == 'POST':
        otp = request.POST.get('otp')
        profile = Profile.objects.filter(mobile = mobile).first()

        if otp == profile.otp:
            return redirect('/xlogin')
        else:
            context = {'message' : 'Wrong otp', 'class' : 'alert alert-danger', 'mobile' : mobile}
            return render (request, "otp.html", context)

    return render (request, "otp.html", context)

def menu(request):
    c = Item.objects.all()
    context = {}
    context["Item"] = c
    print(c)
    return render(request, "menu.html", context)


def catfilter(request, cid):
    c = Item.objects.filter(i_category = cid)
    context = {}
    context['Item'] = c
    return render(request, 'menu.html', context)

def sortby(request, sid):
    if sid == '0':
        c = Item.objects.order_by('i_price').all()
    else:
        c = Item.objects.order_by('-i_price').all()
    context = {}
    context['Item'] = c
    return render(request, 'menu.html', context)

def add_to_platter(request):
    #return render(request,"add_to_platter.html")
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Item.objects.get(id = product_id)
    platter_item, created = Platter.objects.get_or_create(user = user, product = product)
    if created:
        platter_item.qty = 1
    else:
        platter_item.qty += 1
    platter_item.save()
    return redirect('/platter')

def platter(request):
    user = request.user
    platter = Platter.objects.filter(user = user)
    amount = 0
    for p in platter:
        value = p.qty * p.product.i_price
        amount = amount + value
    totalamount = amount + 40
    context = {
        'platter': platter,
        'amount': amount,
        'totalamount' : totalamount
    }
    return render(request, "platter.html", context)


def checkout(request):
    user = request.user
    add = Customer.objects.filter(user = user)
    cart_items = Platter.objects.filter(user = user)
    famount = 0
    for p in cart_items:
        value = p.qty * p.product.i_price
        famount = famount + value
    totalamount = famount + 40
    razoramount = int(totalamount * 100)
    client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_SECRET_ID))
    data = {
        "amount": razoramount,
        "currency": "INR",
        "receipt": "order_rcptid_11"
    }
    payment_response = client.order.create(data = data)
    print(payment_response)
    {'amount': 103000, 'amount_due': 103000, 'amount_paid': 0, 'attempts': 0, 'created_at': 1721559473, 'currency': 'INR', 'entity': 'order', 'id': 'order_ObG1AkAKUdHXKW', 'notes': [], 'offer_id': None, 'receipt': 'order_rcptid_11', 'status': 'created'}
    order_id = payment_response['id']
    order_status = payment_response['status']
    if order_status == 'created':
        payment = Payment(
            user = user,
            amount = totalamount,
            razorpay_order_id = order_id,
            razorpay_payment_status = order_status
        )
        payment.save()
    return render(request, 'checkout.html', locals())

def payment_done(request):
    order_id = request.GET.get('order_id')
    payment_id = request.GET.get('payment_id')
    cust_id = request.GET.get('cust_id')
    user = request.user
    customer = Customer.objects.get(id = cust_id)

    #To update payment status and payment id
    payment = Payment.objects.get(razorpay_order_id = order_id)
    payment.paid = True
    payment.razorpay_payment_id = payment_id
    payment.save()

    #To save order details
    cart = Platter.objects.filter(user = user)
    for c in cart:
        OrderPlaced(
            user = user,
            customer = customer,
            product = c.product,
            quantity = c.qty,
            payment = payment
        ).save()
    return redirect("/orders")

from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from .models import *
from django.contrib import messages
from django.db import transaction
from django.utils import timezone
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import render, get_object_or_404
from django.template.loader import select_template
from home_service.models import Customer
from django.db import IntegrityError
from django.http import JsonResponse
from .models import Service_Man, City, Service_Category, Status, User, Customer, ID_Card
from django.contrib.auth.decorators import login_required
from .models import Customer, Service_Man, Service_Category
import datetime
from django.views.decorators.http import require_POST
from .models import Feedback
from .models import Order

# Create your views here.
def notification():
    try:
        status = Status.objects.get(status='pending')
        new = Service_Man.objects.filter(status=status)
        count = new.count()  # Use .count() to directly get the count of the queryset
    except Status.DoesNotExist:
        new = Service_Man.objects.none()  # Returns an empty queryset
        count = 0
    d = {'count': count, 'new': new}
    return d

def Home(request):
    try:
        user = User.objects.get(id=request.user.id)
        error = "Logged in"
        try:
            sign = Customer.objects.get(user=user)
        except Customer.DoesNotExist:
            print("No customer found for user.")
    except User.DoesNotExist:
        error = "User not found"
        print("User not found")

    service_men = Service_Man.objects.all()
    service_categories = Service_Category.objects.all()

    for category in service_categories:
        category.total = service_men.filter(service_name=category.category).count()
        category.save()  # Consider if this save is necessary, might slow down response

    context = {
        'error': error,
        'services': service_categories
    }
    return render(request, 'home.html', context)


@login_required
def payment_success(request):
    # Assuming 'payment_id' and 'order_id' are passed back as query parameters from PayPal
    payment_id = request.GET.get('payment_id', None)
    order_id = request.GET.get('order_id', None)

    if not payment_id or not order_id:
        # Handle the case where payment information is not provided
        return HttpResponse("Invalid payment details provided.", status=400)

    # Retrieve the order from the database or perform necessary checks
    # order = Order.objects.get(id=order_id)
    
    # Optional: Save payment details to your database
    # payment = Payment.objects.create(order=order, payment_id=payment_id, status='Completed')

    # Update order status or perform other business logic
    # order.status = 'Paid'
    # order.save()

    # Redirect to a confirmation page or render a detailed success message
    # context = {'order': order, 'payment': payment}
    # return render(request, 'payment_success.html', context)

    # For simplicity, just returning a basic response for now
    return HttpResponse(f"Payment was successful! Payment ID: {payment_id}, Order ID: {order_id}")

def your_booking_submission_view(request):
    if request.method == 'POST':
        # Handle your form submission logic here
        return redirect('success_page')  # Redirect to a success page after handling
    return render(request, 'form_page.html')

def contact(request):
    error = False
    status_error = False
    if request.method == "POST":
        n = request.POST['name']
        e = request.POST['email']
        m = request.POST['message']
        
        try:
            status = Status.objects.get(status="unread")
        except Status.DoesNotExist:
            status_error = True
        else:
            Contact.objects.create(status=status, name=n, email=e, message1=m)
            error = True

    d = {'error': error, 'status_error': status_error}
    return render(request, 'contact.html', d)

def Admin_Home(request):
    dic = notification()
    cus = Customer.objects.all()
    ser = Service_Man.objects.all()
    cat = Service_Category.objects.all()
    count1=0
    count2=0
    count3=0
    for i in cus:
        count1+=1
    for i in ser:
        count2+=1
    for i in cat:
        count3+=1
    d = {'new':dic['new'],'count':dic['count'],'customer':count1,'service_man':count2,'service':count3}
    return render(request,'admin_home.html',d)


@require_POST
def process_refund(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
        
        # Placeholder for refund logic
        # In a real application, you would implement the actual refund process here
        # This could involve calling a PayPal API or your payment processor's refund API
        
        # For now, we'll just mark the order as refunded
        order.refunded = True
        order.save()
        
        return JsonResponse({"success": True, "message": "Refund processed successfully"})
    
    except Order.DoesNotExist:
        return JsonResponse({"success": False, "error": "Order not found"})
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})
    

def about(request):
    return render(request,'about.html')

def Login_User(request):
    error = ""
    if request.method == "POST":
        u = request.POST['uname']
        p = request.POST['pwd']
        user = authenticate(username=u, password=p)
        sign = ""
        if user:
            try:
                sign = Customer.objects.get(user=user)
            except:
                pass
            if sign:
                login(request, user)
                error = "pat1"
            else:
                stat = Status.objects.get(status="Accept")
                pure=False
                try:
                    pure = Service_Man.objects.get(status=stat,user=user)
                except:
                    pass
                if pure:
                    login(request, user)
                    error = "pat2"
                else:
                    login(request, user)
                    error="notmember"

        else:
            error="not"
    d = {'error': error}
    return render(request, 'login.html', d)

def Login_admin(request):
    error = ""
    if request.method == "POST":
        u = request.POST['uname']
        p = request.POST['pwd']
        user = authenticate(username=u, password=p)
        if user is not None:
            if user.is_staff:
                login(request, user)
                error = "pat"
            else:
                error = "notmember"
        else:
            error = "not"
    d = {'error': error}
    return render(request, 'admin_login.html', d)

def Signup_User(request):
    error = ""
    if request.method == 'POST':
        f = request.POST['fname']
        l = request.POST['lname']
        u = request.POST['uname']
        e = request.POST['email']
        p = request.POST['pwd']
        con = request.POST['contact']
        add = request.POST['address']
        type = request.POST['type']
        im = request.FILES['image']
        dat = datetime.date.today()
        user = User.objects.create_user(email=e, username=u, password=p, first_name=f,last_name=l)
        if type=="customer":
            Customer.objects.create(user=user,contact=con,address=add,image=im)
        else:
            stat = Status.objects.get(status='pending')
            Service_Man.objects.create(doj=dat,image=im,user=user,contact=con,address=add,status=stat)
        error = "create"
    d = {'error':error}
    return render(request,'signup.html',d)

def User_home(request):
    user= User.objects.get(id=request.user.id)
    error=""
    try:
        sign = Customer.objects.get(user=user)
        error = "pat"
    except:
        pass
    d = {'error':error}
    return render(request,'user_home.html',d)

def Service_home(request):
    user= User.objects.get(id=request.user.id)
    error=""
    try:
        sign = Customer.objects.get(user=user)
        error = "pat"
    except:
        sign = Service_Man.objects.get(user=user)
        pass
    terro=""
    if None == sign.service_name:
        terro = "message"
    else:
        if sign.status.status == "pending":
            terro="message1"
    d = {'error':error,'terro':terro}
    return render(request,'service_home.html',d)

def Service_Order(request):
    user= User.objects.get(id=request.user.id)
    error=""
    try:
        sign = Customer.objects.get(user=user)
        error = "pat"
    except:
        sign = Service_Man.objects.get(user=user)
        pass
    terro=""
    if None == sign.service_name:
        terro = "message"
    else:
        if sign.status.status == "pending":
            terro="message1"
    order = Order.objects.filter(service=sign)
    d = {'error':error,'terro':terro,'order':order}
    return render(request,'service_order.html',d)

def Admin_Order(request):
    dic = notification()
    order = Order.objects.all()
    d = {'order':order,'new': dic['new'], 'count': dic['count']}
    return render(request,'admin_order.html',d)

def Customer_Order(request):
    user= User.objects.get(id=request.user.id)
    error=""
    try:
        sign = Customer.objects.get(user=user)
        error = "pat"
    except:
        sign = Service_Man.objects.get(user=user)
        pass
    order = Order.objects.filter(customer=sign)
    d = {'error':error,'order':order}
    return render(request,'customer_order.html',d)

@transaction.atomic
def Customer_Booking(request, pid):
    if not request.user.is_authenticated:
        return redirect('login')
    
    user = User.objects.get(id=request.user.id)
    try:
        sign = Customer.objects.get(user=user)
        error = "pat"
    except Customer.DoesNotExist:
        sign = get_object_or_404(Service_Man, user=user)
        error = ""
    
    ser1 = get_object_or_404(Service_Man, id=pid)
    
    if request.method == "POST":
        booking_date = request.POST.get('date')
        if ser1.is_available(booking_date):
            if ser1.book_slot(booking_date):
                n = request.POST['name']
                c = request.POST['contact']
                add = request.POST['add']
                da = request.POST['day']
                ho = request.POST['hour']
                st = Status.objects.get(status="pending")
                
                Order.objects.create(
                    status=st, 
                    service=ser1, 
                    customer=sign, 
                    book_date=booking_date, 
                    book_days=da, 
                    book_hours=ho
                )
                
                messages.success(request, "Booking successful!")
                return redirect('customer_order')
            else:
                messages.error(request, "Booking failed. Please try again.")
        else:
            messages.error(request, "No slots available for the selected date.")
    
    ser1.reset_past_slots()
    
    d = {'error': error, 'ser': sign, 'service_man': ser1}
    return render(request, 'booking.html', d)

def check_availability(request, service_man_id):
    service_man = get_object_or_404(Service_Man, id=service_man_id)
    date = request.GET.get('date')
    if date:
        available_slots = service_man.get_available_slots(date)
        return JsonResponse({
            'available_slots': available_slots,
            'is_available': available_slots > 0
        })
    return JsonResponse({'error': 'Date not provided'}, status=400)

def feedback(request):
    return render(request, 'feedback.html')


def submit_feedback(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        rating = request.POST.get('rating')
        message = request.POST.get('message')
        
        # Basic validation
        if not all([name, email, rating, message]):
            messages.error(request, 'All fields are required.')
            return render(request, 'feedback.html', {'error': 'All fields are required.'})
        
        try:
            rating = int(rating)
            if not 1 <= rating <= 5:
                raise ValueError
        except ValueError:
            messages.error(request, 'Rating must be a number between 1 and 5.')
            return render(request, 'feedback.html', {'error': 'Invalid rating.'})
        
        # Create feedback object
        Feedback.objects.create(name=name, email=email, rating=rating, message=message)
        messages.success(request, 'Thank you for your feedback!')
        return redirect('home')
    
    return render(request, 'feedback.html')


def admin_feedback(request):
    feedbacks = Feedback.objects.all().order_by('-submitted_at')
    return render(request, 'admin_feedback.html', {'feedbacks': feedbacks})

def Booking_detail(request,pid):
    user= User.objects.get(id=request.user.id)
    error=""
    try:
        sign = Customer.objects.get(user=user)
        error = "pat"
    except:
        sign = Service_Man.objects.get(user=user)
        pass
    order = Order.objects.get(id=pid)
    d = {'error':error,'order':order}
    return render(request,'booking_detail.html',d)

def All_Service(request):
    user = ""
    error = ""
    try:
        user = User.objects.get(id=request.user.id)
        try:
            sign = Customer.objects.get(user=user)
            error = "pat"
        except:
            pass
    except:
        pass
    ser1 = Service_Man.objects.all()
    ser = Service_Category.objects.all()
    for i in ser:
        count=0
        for j in ser1:
            if i.category==j.service_name:
                count+=1
        i.total = count
        i.save()
    d = {'error': error,'ser':ser}
    return render(request,'services.html',d)

def Explore_Service(request, pid):
    if not request.user.is_authenticated:
        return redirect('login')

    user = ""
    error = ""
    try:
        user = User.objects.get(id=request.user.id)
        try:
            sign = Customer.objects.get(user=user)
            error = "pat"
        except:
            pass
    except:
        pass

    ser = get_object_or_404(Service_Category, id=pid)

    # Get or create the "Accept" status object
    status, created = Status.objects.get_or_create(status="Accept")
    if created:
        print("'Accept' status object created.")

    order = Service_Man.objects.filter(service_name=ser.category, status=status)
    d = {'error': error, 'ser': ser, 'order': order}
    return render(request, 'explore_services.html', d)

def Logout(request):
    logout(request)
    return redirect('home')

def Edit_Profile(request):
    user = User.objects.get(id=request.user.id)
    error = ""
    try:
        sign = Customer.objects.get(user=user)
        error = "pat"
    except:
        sign = Service_Man.objects.get(user=user)
    terror = False
    ser = Service_Category.objects.all()
    if request.method == 'POST':
        f = request.POST['fname']
        l = request.POST['lname']
        u = request.POST['uname']
        try:
            i = request.FILES['image']
            sign.image=i
            sign.save()
        except:
            pass
        ad = request.POST['address']
        e = request.POST['email']
        con = request.POST['contact']
        sign.address = ad
        sign.contact=con
        user.first_name = f
        user.last_name = l
        user.email = e
        user.save()
        sign.save()
        terror = True
    d = {'terror':terror,'error':error,'pro':sign,'ser':ser}
    return render(request, 'edit_profile.html',d)

def Edit_Service_Profile(request):
    user = request.user
    try:
        sign = Customer.objects.get(user=user)
    except Customer.DoesNotExist:
        sign = Service_Man.objects.get(user=user)
    
    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        address = request.POST.get('address', '')  # Use a default or empty string if not provided
        contact = request.POST.get('contact')
        service = request.POST.get('service')
        card = request.POST.get('card')
        city_name = request.POST.get('city')
        exp = request.POST.get('exp')
        dob = request.POST.get('dob')

        try:
            city = City.objects.get(city=city_name)
        except City.DoesNotExist:
            city = None  # You might want to handle this case appropriately

        sign.address = address
        sign.contact = contact
        sign.city = city
        sign.dob = dob if dob else sign.dob
        sign.id_type = card
        sign.experience = exp
        sign.service_name = service
        
        user.first_name = fname
        user.last_name = lname
        user.email = email
        
        # Handling file uploads safely
        image = request.FILES.get('image')
        if image:
            sign.image = image

        id_card = request.FILES.get('image1')
        if id_card:
            sign.id_card = id_card
        
        # Save all changes to the database
        user.save()
        sign.save()
        
        messages.success(request, 'Profile updated successfully.')
        return redirect('service_profile')  # Assuming 'service_profile' is the correct redirect location

    else:
        # GET request logic
        ser = Service_Category.objects.all()
        car = ID_Card.objects.all()
        city = City.objects.all()
        context = {
            'city': city,
            'pro': sign,
            'car': car,
            'ser': ser
        }
        return render(request, 'edit_service_profile.html', context)

@login_required
def Edit_Admin_Profile(request):
    dic = notification()
    error = False
    user = request.user
    
    # Check if the Customer object exists for the user
    try:
        pro = Customer.objects.get(user=user)
    except Customer.DoesNotExist:
        return redirect('create_customer_profile')  # Redirect to a page where the admin can create a profile
    
    if request.method == 'POST':
        f = request.POST.get('fname')
        l = request.POST.get('lname')
        u = request.POST.get('uname')
        ad = request.POST.get('address')
        e = request.POST.get('email')
        con = request.POST.get('contact')
        
        if 'image' in request.FILES:
            pro.image = request.FILES['image']
        
        pro.address = ad
        pro.contact = con
        user.first_name = f
        user.last_name = l
        user.username = u
        user.email = e
        user.save()
        pro.save()
        error = True

    d = {'error': error, 'pro': pro, 'new': dic['new'], 'count': dic['count']}
    return render(request, 'edit_admin_profile.html', d)

def profile(request):
    user = User.objects.get(id=request.user.id)
    error = ""
    try:
        sign = Customer.objects.get(user=user)
        error = "pat"
    except:
        sign = Service_Man.objects.get(user=user)
    terror = False
    d = {'pro':sign,'error':error}
    return render(request,'profile.html',d)

def service_profile(request):
    user = User.objects.get(id=request.user.id)
    error = ""
    try:
        sign = Customer.objects.get(user=user)
        error = "pat"
    except:
        sign = Service_Man.objects.get(user=user)
    terror = False
    d = {'pro':sign,'error':error}
    return render(request,'service_profile.html',d)

def admin_profile(request):
    dic = notification()
    user = User.objects.get(id=request.user.id)
    try:
        pro = Customer.objects.get(user=user)
    except Customer.DoesNotExist:
        # Handle the case where the Customer does not exist.
        # Depending on application logic, redirect or handle the error appropriately.
        # For example, redirect to the homepage with a message.
        from django.http import HttpResponse
        return HttpResponse("Customer profile not found.", status=404)
    
    d = {'pro': pro, 'new': dic['new'], 'count': dic['count']}
    return render(request, 'admin_profile.html', d)

def Change_Password(request):
    user = User.objects.get(id=request.user.id)
    error = ""
    try:
        sign = Customer.objects.get(user=user)
        error = "pat"
    except:
        pass
    terror = ""
    if request.method=="POST":
        n = request.POST['pwd1']
        c = request.POST['pwd2']
        o = request.POST['pwd3']
        if c == n:
            u = User.objects.get(username__exact=request.user.username)
            u.set_password(n)
            u.save()
            terror = "yes"
        else:
            terror = "not"
    d = {'error':error,'terror':terror}
    return render(request,'change_password.html',d)

def Admin_Change_Password(request):
    terror = ""
    if request.method=="POST":
        n = request.POST['pwd1']
        c = request.POST['pwd2']
        o = request.POST['pwd3']
        if c == n:
            u = User.objects.get(username__exact=request.user.username)
            u.set_password(n)
            u.save()
            terror = "yes"
        else:
            terror = "not"
    d = {'terror':terror}
    return render(request,'admin_change_password.html',d)

def New_Service_man(request):
    dic = notification()
    status, created = Status.objects.get_or_create(status="pending")
    if created:
        print("'pending' status object created.")
    ser = Service_Man.objects.filter(status=status)
    d = {'ser': ser, 'new': dic['new'], 'count': dic['count']}
    return render(request, 'new_service_man.html', d)

def All_Service_man(request):
    dic = notification()
    ser = Service_Man.objects.all()
    d = {'ser': ser, 'new': dic['new'], 'count': dic['count']}
    return render(request, 'all_service_man.html', d)

def All_Customer(request):
    dic = notification()
    ser = Customer.objects.all()
    d = {'ser':ser,'new': dic['new'], 'count': dic['count']}
    return render(request,'all_customer.html',d)

def Add_Service(request):
    dic = notification()
    error=False
    if request.method == "POST":
        n = request.POST['cat']
        i = request.FILES['image']
        de = request.POST['desc']
        Service_Category.objects.create(category=n,image=i,desc=de)
        error=True
    d = {'error':error,'new': dic['new'], 'count': dic['count']}
    return render(request,'add_service.html',d)

def Add_City(request):
    dic = notification()
    error=False
    if request.method == "POST":
        n = request.POST['cat']
        City.objects.create(city=n)
        error=True
    d = {'error':error,'new': dic['new'], 'count': dic['count']}
    return render(request,'add_city.html',d)

def Edit_Service(request,pid):
    dic = notification()
    error=False
    ser = Service_Category.objects.get(id=pid)
    if request.method == "POST":
        n = request.POST['cat']
        try:
            i = request.FILES['image']
            ser.image = i
            ser.save()
        except:
            pass
        de = request.POST['desc']
        ser.category = n
        ser.desc = de
        ser.save()
        error=True
    d = {'error':error,'ser':ser,'new': dic['new'], 'count': dic['count']}
    return render(request,'edit_service.html',d)

def View_Service(request):
    dic = notification()
    ser = Service_Category.objects.all()
    d = {'ser':ser,'new': dic['new'], 'count': dic['count']}
    return render(request,'view_service.html',d)

def View_City(request):
    dic = notification()
    ser = City.objects.all()
    d = {'ser':ser,'new': dic['new'], 'count': dic['count']}
    return render(request,'view_city.html',d)

def accept_confirmation(request,pid):
    ser = Order.objects.get(id=pid)
    sta = Status.objects.get(status='Accept')
    ser.status = sta
    ser.save()
    return redirect('service_order')

def confirm_message(request,pid):
    ser = Contact.objects.get(id=pid)
    sta = Status.objects.get(status='read')
    ser.status = sta
    ser.save()
    return redirect('new_message')

def delete_service(request,pid):
    ser = Service_Category.objects.get(id=pid)
    ser.delete()
    return redirect('view_service')

def delete_city(request,pid):
    ser = City.objects.get(id=pid)
    ser.delete()
    return redirect('view_city')

def delete_admin_order(request,pid):
    ser = Order.objects.get(id=pid)
    ser.delete()
    return redirect('admin_order')

def delete_Booking(request,pid):
    ser = Order.objects.get(id=pid)
    ser.delete()
    return redirect('customer_order')

def delete_service_man(request,pid):
    ser = Service_Man.objects.get(id=pid)
    ser.delete()
    return redirect('all_service_man')

def delete_customer(request,pid):
    ser = Customer.objects.get(id=pid)
    ser.delete()
    return redirect('all_customer')

def Change_status(request,pid):
    dic = notification()
    error = False
    pro1 = Service_Man.objects.get(id=pid)
    if request.method == "POST":
        stat = request.POST['stat']
        sta = Status.objects.get(status=stat)
        pro1.status=sta
        pro1.save()
        error=True
    d = {'pro':pro1,'error':error,'new': dic['new'], 'count': dic['count']}
    return render(request,'status.html',d)

def Order_status(request,pid):
    dic = notification()
    error = False
    pro1 = Order.objects.get(id=pid)
    if request.method == "POST":
        stat = request.POST['stat']
        sta = Status.objects.get(status=stat)
        pro1.status=sta
        pro1.save()
        error=True
    d = {'pro':pro1,'error':error,'new': dic['new'], 'count': dic['count']}
    return render(request,'order_status.html',d)

def Order_detail(request,pid):
    dic = notification()
    pro1 = Order.objects.get(id=pid)
    d = {'pro':pro1,'new': dic['new'], 'count': dic['count']}
    return render(request,'order_detail.html',d)

def service_man_detail(request, pid):
    dic = notification()
    pro1 = get_object_or_404(Service_Man, id=pid)
    d = {'pro': pro1, 'new': dic['new'], 'count': dic['count']}
    return render(request, 'service_man_detail.html', d)

def search_cities(request):
    error = ""
    try:
        user = User.objects.get(id=request.user.id)
        try:
            sign = Customer.objects.get(user=user)
            error = "pat"
        except Customer.DoesNotExist:
            pass
    except User.DoesNotExist:
        pass

    dic = notification()
    terror = False
    pro = []
    car = City.objects.all()
    count1 = 0
    car1 = Service_Category.objects.all()
    c = ""
    c1 = ""

    if request.method == "POST":
        c = request.POST.get('city', '')
        c1 = request.POST.get('cat', '')
        if c and c1:
            try:
                ser = City.objects.get(city=c)
                ser1 = Service_Category.objects.get(category=c1)
                pro = Service_Man.objects.filter(service_name=ser1, city=ser)
                count1 = pro.count()
                terror = True
            except City.DoesNotExist:
                error = "City not found."
            except Service_Category.DoesNotExist:
                error = "Service category not found."

    d = {
        'c': c,
        'c1': c1,
        'count1': count1,
        'car1': car1,
        'car': car,
        'order': pro,
        'new': dic['new'],
        'count': dic['count'],
        'error': error,
        'terror': terror
    }
    return render(request, 'search_cities.html', d)

def search_services(request):
    dic = notification()
    error=False
    pro=""
    car = Service_Category.objects.all()
    c=""
    if request.method=="POST":
        c=request.POST['cat']
        ser = Service_Category.objects.get(category=c)
        pro = Service_Man.objects.filter(service_name=ser)
        error=True
    d = {'service':c,'car':car,'order':pro,'new': dic['new'], 'count': dic['count'],'error':error}
    return render(request,'search_services.html',d)

def new_message(request):
    dic = notification()
    try:
        sta = Status.objects.get(status='unread')
    except Status.DoesNotExist:
        # Handle the error or create the status if necessary
        sta = Status.objects.create(status='unread')
        sta.save()
    pro1 = Contact.objects.filter(status=sta)
    d = {'ser': pro1, 'new': dic['new'], 'count': dic['count']}
    return render(request, 'new_message.html', d)

def read_message(request):
    dic = notification()
    try:
        sta = Status.objects.get(status='read')
    except Status.DoesNotExist:
        # Handle the error or create the status if necessary
        sta = Status.objects.create(status='read')
        sta.save()
    pro1 = Contact.objects.filter(status=sta)
    d = {'ser': pro1, 'new': dic['new'], 'count': dic['count']}
    return render(request, 'read_message.html', d)

def Search_Report(request):
    dic = notification()
    status = Status.objects.get(status="pending")
    reg1 = Order.objects.filter(status=status)
    total = 0
    for i in reg1:
        total += 1
    data = Order.objects.all( )
    error = ""
    terror = ""
    reg=""
    if request.method == "POST":
        terror="found"
        i = request.POST['date1']
        n = request.POST['date2']
        i1 = datetime.datetime.fromisoformat(i).month
        i2 = datetime.datetime.fromisoformat(i).year
        i3 = datetime.datetime.fromisoformat(i).day
        n1 = datetime.datetime.fromisoformat(n).month
        n2 = datetime.datetime.fromisoformat(n).year
        n3 = datetime.datetime.fromisoformat(n).day
        for j in data:
            d1 =j.book_date.month
            d2 =j.book_date.year
            d3 = j.book_date.day
            day3 = (d2 * 365) + (d1 * 30) + d3
            day1 = (i2 * 365) + (i1 * 30) + i3
            day2 = (n2 * 365) + (n1 * 30) + n3
            if day3 > day1 and day3 < day2:
                j.report_status = 'active'
                j.save()
            else:
                j.report_status = 'inactive'
                j.save()
        reg = Order.objects.filter(report_status="active")
        if not reg:
            error="notfound"
    d = {'new': dic['new'], 'count': dic['count'],'order':reg,'error':error,'terror':terror,'reg1': reg1, 'total': total}
    return render(request,'search_report.html',d)

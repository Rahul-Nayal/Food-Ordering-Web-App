from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from QuickBite.models import ContactUs, SignUp, Category, Dish, Order, OrderItem, ShippingAddress
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
import json
import datetime


def indexpage(request):
    cate = Category.objects.all()
    dishes = Dish.objects.all()[:4]
    return render(request, 'index.html', {'category': cate, 'dishes': dishes})


def signuppage(request):
    if request.method == "POST":
        user_name = request.POST['name']
        user_email = request.POST['email']
        user_password = request.POST['password']
        con = request.POST['contact_num']

        usr = User.objects.create_user(user_email, user_email, user_password)
        usr.first_name = user_name
        usr.save()
        profile = SignUp(user=usr, contact_number=con)
        profile.save()
        msg = "Welcome To SERVEASY"
        return render(request, 'signup.html', {"status": msg})
    return render(request, 'signup.html')


def user_login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        pwd = request.POST['password']

        user = authenticate(username=email, password=pwd)
        if user:
            login(request, user)
            if user.is_superuser or user.is_staff:
                return HttpResponseRedirect('/admin')
            if user.is_active:
                return HttpResponseRedirect('/dashboard')
        else:
            return render(request, 'login.html', {"status": "Invalid username or password"})

    return render(request, 'login.html')


def aboutpage(request):
    return render(request, 'about.html')


def menu_by_category(request):
    category_id = request.GET.get('q')
    category = get_object_or_404(Category, id=category_id)
    dishes = Dish.objects.filter(category=category)
    for dish in dishes:
        if dish.details:
            dish.processed_details = dish.details.split('.') 
    context = {
        'category': category,
        'dishes': dishes
    }
    return render(request, 'menu.html', context)


def menupage(request):
    if request.user.is_authenticated:
        customer = request.user.signup
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_item': 0, 'shipping': False}

    dishes = Dish.objects.all()

    for dish in dishes:
        if dish.details:
            dish.processed_details = dish.details.split('.') 

    context = {'dishes': dishes, 'items': items, 'order': order}
    return render(request, 'menu.html', context)


def cartpage(request):
    if request.user.is_authenticated:
        customer = request.user.signup
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_item': 0, 'shipping': False}

    context = {'items': items, 'order': order}
    return render(request, 'cart.html', context)


def checkoutpage(request):
    if request.user.is_authenticated:
        customer = request.user.signup
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_item': 0, 'shipping': False}

    context = {'items': items, 'order': order}
    return render(request, 'checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)
    dishId = data['dishId']
    action = data['action']
    print('dishId:', dishId)
    print('action:', action)

    customer = request.user.signup
    dish = Dish.objects.get(id=dishId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, dish=dish)

    if action == 'add':
        orderItem.quantity += 1
    elif action == 'remove':
        orderItem.quantity -= 1
    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('item was added', safe=False)

from django.views.decorators.csrf import csrf_exempt  # Optional: Use this if CSRF protection causes issues.

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.signup  # Assuming the `signup` model is linked to the user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        if total == order.get_cart_total:
            order.complete = True
        order.save()

        if order.shipping:  # If shipping is required
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                state=data['shipping']['state'],
                zipcode=data['shipping']['zipcode'],
            )
    else:
        return JsonResponse({'error': 'User is not logged in'}, status=401)

    return JsonResponse({'message': 'Payment submitted successfully'}, safe=False)


def contactpage(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        con = request.POST['contact']
        sub = request.POST['subject']
        msg = request.POST['message']

        data = ContactUs(name=name, email=email, contact_number=con, subject=sub, message=msg)
        data.save()
        res = "Dear {} Thanks for your feedback".format(name)
        return render(request, 'contact.html', {"status": res})

    return render(request, 'contact.html')


def check_user(request):
    if request.method == "GET":
        email = request.GET.get('usern')
        if email is None:
            return JsonResponse({'status': 0, 'message': 'Email parameter is missing'})

        user_exists = User.objects.filter(username=email).exists()

        if not user_exists:
            return JsonResponse({'status': 0, 'message': 'Not Exist'})
        else:
            return JsonResponse({'status': 1, 'message': 'A user with this email already exists!'})
    else:
        return JsonResponse({'status': 0, 'message': 'Invalid request method'})


@login_required
def cust_dashboard(request):
    context = {}
    login_user = get_object_or_404(User, id=request.user.id)

    profile = SignUp.objects.get(user__username=request.user.username)
    context['profile'] = profile

    if 'update_profile' in request.POST:
        name = request.POST.get('name')
        contact = request.POST.get('number')
        pic = request.FILES.get('profile_pic')

        profile.user.first_name = name
        profile.user.save()
        profile.contact_number = contact
        if pic:
            profile.profile_pic = pic
        profile.save()
        context['status'] = 'Profile updated successfully!'

    if 'changePass' in request.POST:
        curr_password = request.POST.get('curr_password')
        new_password = request.POST.get('new_password')

        if login_user.check_password(curr_password):
            login_user.set_password(new_password)
            login_user.save()
            login(request, login_user)
            context['status'] = "Password updated successfully!"
        else:
            context['status'] = "Current password is incorrect!"

    orders = Order.objects.filter(customer=profile, complete=True).order_by('-date_ordered')

    for order in orders:
        order.update_delivery_status()

    context['orders'] = orders

    return render(request, 'dashboard.html', context)


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

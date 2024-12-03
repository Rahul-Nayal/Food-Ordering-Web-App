import json
from .models import*

def cookieCart(request):
	try:
		cart = json.loads(request.COOKIES['cart'])
	except:
		cart = {}
	items=[]
	order = {'get_cart_total': 0 ,'get_cart_item': 0 , 'shipping' : False}

	for i in cart:

		try:
			dish = Dish.objects.get(id = i)
			total = (dish.price * cart[i]['quantity'])

			order['get_cart_total'] += total
			order['get_cart_item'] += cart[i]['quantity']

			item = {
				'dish' : {
					'id' : dish.id,
					'name' : dish.dish_name,
					'price' : dish.price,
					'image' : dish.image,
				},
				'quantity' : cart[i]['quantity'],
				'get_total' : total,
			}

			items.append(item)

			order['shipping']  = True
		except:
			pass
	return {'order' : order, 'items' : items}


def cartData(request):
	if request.user.is_authenticated:
		customer = request.user.signup
		order,created = Order.objects.get_or_create(customer=customer,complete=False)
		items = order.orderitem_set.all()
		cartItem = order.get_cart_item		

	else:
		cookieData = cookieCart(request)
		items= cookieData['items']
		order = cookieData['order']
	return {'items':items,'order': order,}

def guestOrder(request, data):
    print('user is not logged in ...')

    username = data['form']['username']
    email = data['form']['email']
    contact = data['form']['contact']

    cookieData = cookieCart(request)
    items = cookieData['items']
    user, created = User.objects.get_or_create(
        username=username,
        defaults={'email': email}
    )
    customer, created = SignUp.objects.get_or_create(
        user=user,
        contact_number=contact
    )
    customer.username = username
    customer.save()

    order = Order.objects.create(
        customer=customer,
        complete=False,
    )

    for item in items:
        dish = Dish.objects.get(id=item['dish']['id'])
        if not OrderItem.objects.filter(dish=dish, order=order).exists():
            OrderItem.objects.create(
                dish=dish,
                order=order,
                quantity=item['quantity'],
            )
    
    return customer, order
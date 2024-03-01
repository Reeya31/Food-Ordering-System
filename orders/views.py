from django.shortcuts import render,redirect
from .forms import OrderForm
from carts.models import CartItem
from .models import Order
import datetime

# Create your views here.
def payments(request):
    return render(request,'orders/payments.html')



def place_order(request ,total=0,quantity=0):
    current_user = request.user
    
    #if the cart count <= 0 redirect to store
    
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    print(cart_count)
    if cart_count <= 0:
        return redirect('payments')
    
    grand_total =0
    tax = 0
    
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    tax = (13*total)/100
    grand_total = total + tax    
        
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        
        if form.is_valid():
            # to store all the billing address in table
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.Phone_number = form.cleaned_data['Phone_number']
            data.email = form.cleaned_data['email']
            data.address_1 = form.cleaned_data['address_1']
            data.address_2 = form.cleaned_data['address_2']
            data.province = form.cleaned_data['province']
            data.city = form.cleaned_data['city']
            data.area = form.cleaned_data['area']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            
            print(request.POST["email"])
            
            #Generate order number
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr,mt,dt)
            current_date= d.strftime("%Y%m%d")
            order_number = current_date + str(data.id)
            data.order_number = order_number
            print(data.order_number)
            data.save()
            
            order = Order.objects.get(user=current_user,is_ordered=False,order_number=order_number)
            print(order)
            context={
             'order' : order,
             'cart_items': cart_items,
             'total':total,
             'tax':tax,
             'grand_total': grand_total,
                
            }

            return render(request,'orders/payments.html',context)
        else:
            return redirect('checkout')
            
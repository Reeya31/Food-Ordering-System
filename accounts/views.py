from django.shortcuts import render,redirect
from .forms import RegistrationForm
from .models import Account
from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required
from carts.models import Cart,CartItem
from carts.views import _cart_id
# Create your views here.
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name'] 
            last_name = form.cleaned_data['last_name'] 
            email = form.cleaned_data['email'] 
            Phone_number = form.cleaned_data['Phone_number'] 
            password = form.cleaned_data['password'] 
            username = email.split("@")[0]
            
            user = Account.objects.create_user(first_name=first_name,last_name=last_name,email=email,password=password,username=username)
            
            user.Phone_number = Phone_number
           
            user.save()
            messages.success(request, 'You have succesfully Registered 😎')
            return redirect('register')
    else:
        form = RegistrationForm()        
        
    
    context={
        'form':form,
    }
    return render(request,'accounts/register.html',context)

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        user = auth.authenticate(email = email,password=password)
       
        if user is not None:
            try:
                cart = Cart.objects.get(cart_id = _cart_id(request))
                is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                if is_cart_item_exists:
                    cart_item = CartItem.objects.filter(cart = cart)
                    
                    for item in cart_item:
                      item.user = user
                      item.save()  
            except:
                pass
                
            auth.login(request,user)
            # messages.success(request,'You are Logged In ')
            return redirect('home')
        else:
            messages.error(request,'Invalid login credentials ')
            return redirect('login')
    return render(request,'accounts/login.html')


@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request,'You are logged out 🤔')
    return redirect('login')
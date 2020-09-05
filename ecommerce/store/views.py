from django.shortcuts import render, redirect
from .models import Product, Cart, Fpo_Registeration
from django.contrib.auth.decorators import login_required
from django.shortcuts import (get_object_or_404, 
                              render,  
                              HttpResponseRedirect) 
from .forms import Fpo_Registeration_form 
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView 

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from users.forms import SignUpForm
from django.conf import settings 
from django.core.mail import send_mail 
# Create your views here.
# cart fuctions
def repeat(request):
 if request.user.is_authenticated:
  carts=Cart.objects.filter(cartuser=request.user)
  total_price=0
  total_items=0
  for x in carts:
   total_price=total_price+x.price
   total_items=total_items+1
  return total_items
 else:
   return 0
 #redirect when user is not logged in
# ----------------------------------------------- marketplace site-------------------------------------
def store(request):
 carts=Cart.objects.all()
 if request.method=='POST':
   val=request.POST.get('search')
   products=Product.objects.filter(product_name__icontains=val)
   context={'products':products, 'total_items_in_cart':repeat(request), 'carts':carts}
   return render(request, 'store/store.html', context)

 
 products=Product.objects.all()
 context={'products':products, 'total_items_in_cart':repeat(request), 'carts':carts}
 return render(request, 'store/store.html', context)
#------------------------------------end------------------------------------------------------------------
#------------------------------------cart page------------------------------------------------------------------
def cart(request):
 carts=Cart.objects.filter(cartuser=request.user)
 total_price=0
 total_items=0
 for x in carts:
  total_price=total_price+x.price
  total_items=total_items+1
 context={'carts':carts,  'items':total_items, 'total_items_in_cart':total_items, 'total_price':total_price}
 return render(request, 'store/cart.html', context)
# -------------------------------------end---------------------------------------------------------------------
# -------------------------------------detail view---------------------------------------------------------------------
def detail(request, slag):
  print(slag)
  user=Fpo_Registeration.objects.get(pk=slag)
  prod=Product.objects.filter(product_by=slag)
  context={'products': prod , 'user':user}
  return render(request, "store/detail.html", context) 
# -----------------------------------end---------------------------------------------------------------------
# -------------adding to cart list store id of all products already in cart-------------------------


def addtocart(request, slag):
 
 
  
  repeat(request)
  
  item=Product.objects.get(pk=slag)
  # --------------to check if item already presentd in cart-------------------------------
  name=item.product_name
  carts=Cart.objects.filter(cartuser=request.user)
  # for cart in carts:
  #  if cart.name==name:
  #   products=Product.objects.all()
  #   context={'products':products, 'total_items_in_cart':repeat(request), }
  #   return render(request, 'store/store.html', context)
    
  # --------------else adding to cart------------------------------
  add=Cart(name=item.product_name, price=item.product_price, img=item.product_img1, cartuser=request.user,)
  add.save()
  products=Product.objects.all()
  context={'products':products, 'total_items_in_cart':repeat(request), }
  return render(request, 'store/store.html', context)
 
def delete_item(request, id):
       
    # fetch the object related to passed id 
    obj = get_object_or_404(Cart, id = id) 
    context ={'obj':obj, 'total_items_in_cart':repeat(request)}
  
    if request.method =="POST": 
        # delete object 
        obj.delete() 
        # after deleting redirect to  
        # home page 
        return HttpResponseRedirect("/market/cart") 
  
    return render(request, "store/delete_item.html", context) 

# --------------------------------------------end--------------------------------------------
# -------------------fpo registration form-------------------------------------------------
 
def fpo_register(request): 
    context ={} 
    context['form']= Fpo_Registeration_form () 
    
    if request.method=='POST':
      email=request.POST.get('email')
      name=request.POST.get('name')
      area=request.POST.get('area')
      pincode=request.POST.get('pincode')
      member=request.POST.get('members')
      u=request.POST.get('username')
      img=request.FILES.get('image')
        
      f=Fpo_Registeration(fpo_username=u, fpo_name = name, fpo_area = area, area_pincode = int(pincode), total_members =int(member) , fpo_email = email, fpo_img = img )

      f.save() 
            # ------------------sending mail-----------------------------------------------
      subject = 'welcome to jaljeevika'
      subject1 = 'New FPO Registration'
      message = f'''Hi {request.user.username}, thank you for registering.
                     Your username: {request.user.username},
                     password: {request.user.password},
                     You will be contacted soon. Once your informations is verified.'''
      message1 = f'''Hi {request.user.username}, has just registered as an FPO.
                     username: {request.user.username},
                     
                     '''
      email_from = settings.EMAIL_HOST_USER 
      recipient_list = [request.user.email,  ] 
      recipient_list1 = [ 'ashutoshkmrsingh380@gmail.com', ] 
      send_mail( subject, message, email_from, recipient_list ) 
      send_mail( subject1, message1, email_from, recipient_list1 ) 
      return render(request, "index.html")
       

    return render(request, "store/fpo_registration.html", context) 
# ---------------------------------end--------------------------------------------------
# ---------------------------------product createview--------------------------------------------------
class createview(LoginRequiredMixin, CreateView):
 model=Product
 fields = ['product_name', 'product_price', 'product_category', 'product_description', 'product_img1','product_img2', 'product_img3', 'product_img4', 'product_img5']

 def form_valid(self, form):
  form.instance.product_by = self.request.user
  form.instance.rating = 0
  return super().form_valid(form)
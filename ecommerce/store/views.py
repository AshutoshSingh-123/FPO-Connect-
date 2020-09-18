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

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin 
# from braces.views import LoginRequiredMixin, StaffuserRequiredMixin
# from braces import views
from users.forms import SignUpForm
from django.conf import settings 
from django.core.mail import send_mail 
from .decorator import allowed_users 
from django.core.paginator import Paginator
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
 else:
  products=Product.objects.all()
 paginator = Paginator(products, 6)
 page_number = request.GET.get('page')
 page_obj = paginator.get_page(page_number)
 total_result = products.count()

 context={'products':page_obj, 'total_items_in_cart':repeat(request), 'carts':carts, 'total_result':total_result}
 return render(request, 'store/store.html', context)
#------------------------------------end------------------------------------------------------------------
#------------------------------------cart page------------------------------------------------------------------
def cart(request):
 carts=Cart.objects.filter(cartuser=request.user)
 total_price=0
 total_items=0
 if request.method == 'POST':
  
     Cart.objects.all().delete()
   
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
  name=item.product_name
  carts=Cart.objects.filter(cartuser=request.user)
    
  # --------------else adding to cart------------------------------
  add=Cart(name=item.product_name, price=item.product_price, img=item.product_img1, cartuser=request.user,)
  add.save()
  products=Product.objects.all()
  paginator = Paginator(products, 6)
  page_number = request.GET.get('page')
  page_obj = paginator.get_page(page_number)
  context={'products':page_obj, 'total_items_in_cart':repeat(request), }
  return render(request, 'store/store.html', context)

def addtocart_onview_page(request, slag): 
  repeat(request)
  
  item=Product.objects.get(pk=slag)
  name=item.product_name
  carts=Cart.objects.filter(cartuser=request.user)
    
  # --------------else adding to cart------------------------------
  add=Cart(name=item.product_name, price=item.product_price, img=item.product_img1, cartuser=request.user,)
  add.save()
  products=Product.objects.get(pk=slag)
  similars=Product.objects.filter(product_category=products.product_category)
  similars2=Product.objects.filter(product_by=products.product_by)
  context={'product':products, 'total_items_in_cart':repeat(request), 'similars':similars, 'similars2':similars}
  return render(request, 'store/viewpage.html', context)
 
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

class product_fpo_del(DeleteView):
  model=Product
  success_url='/market/'
class fpo_update(UpdateView):
  model=Fpo_Registeration
  fields = [ 
        "fpo_name", 
        "fpo_description",
        
        
        "fpo_img",
        "fpo_area",
        "area_pincode",
        "fpo_email",
        "fpo_mobile1",
        "fpo_mobile2",
    ] 
  success_url='/market/allfpo/'
class product_fpo_update(UpdateView):
  model=Product
  fields = [ 
        "product_name", 
        "product_description",
        "product_unit",
        "product_price",
        "product_category",
        "product_img1",
        "product_img2",
        "product_img3",
        "product_img4",
        "product_img5",
    ] 
  
  
  
  success_url='/market/'
# --------------------------------------------end--------------------------------------------
# -------------------fpo registration form-------------------------------------------------
 
def fpo_register(request): 
    context ={} 
    context['form']= Fpo_Registeration_form () 
    
    if request.method=='POST':
      email=request.POST.get('email')
      name=request.POST.get('name')
      number1=request.POST.get('number1')
      number2=request.POST.get('number2')
      description=request.POST.get('description')
      area=request.POST.get('area')
      pincode=request.POST.get('pincode')
      member=request.POST.get('members')
      u=request.POST.get('username')
      img=request.FILES.get('image')
      category = request.POST.get('category')
      f=Fpo_Registeration(fpo_username=u, fpo_name = name, fpo_area = area, area_pincode = int(pincode), total_members =int(member) , fpo_email = email, fpo_img = img, fpo_mobile1=number1, fpo_mobile2=number2, fpo_description=description, fpo_category=category )

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
  fields = ['product_name','product_unit', 'product_price', 'product_category', 'product_description', 'product_img1','product_img2', 'product_img3', 'product_img4', 'product_img5']

  def form_valid(self, form):
   if self.request.user.is_staff: 
    form.instance.product_by = self.request.user
    form.instance.rating = 0
    return super().form_valid(form)
   else:
     return redirect(request, 'store')


@login_required(login_url='login')
def viewpage(request, slug):
  
  products=Product.objects.get(id=slug)
  user=User.objects.get(username=products.product_by)
  # print(products.product_by)
  fpo=Fpo_Registeration.objects.get(fpo_username=user)
  
  similars=Product.objects.filter(product_category=products.product_category)
  similars2=Product.objects.filter(product_by=products.product_by)
  context={'product':products, 'total_items_in_cart':repeat(request), 'similars':similars, 'similars2':similars2, 'fpo':fpo}
  if request.method == 'POST':
    email=request.POST.get('email')
    name=request.POST.get('name')
    sub=request.POST.get('subject')
    message=request.POST.get('message')
    number=request.POST.get('number')
    subject = sub
      
    message = f'''Hi 
                     {user.username}, 
                     username: {name},
                     email: {email},
                     phone number: {number},
                     wants to contact with you.
                     Message:
                     {message}'''
    email_from = settings.EMAIL_HOST_USER 
    recipient_list = [user.email,  ] 
     
    send_mail( subject, message, email_from, recipient_list ) 

  return render(request, 'store/viewpage.html', context)
 
#  ------------------------------------------ fpo listview-------------------------------------
@login_required(login_url='login') 
def fpo_listview(request):
  if request.method=='POST':
   val=request.POST.get('search')
   
   fpo1=Fpo_Registeration.objects.filter(fpo_name__icontains=val)  
   
   fpo2=Fpo_Registeration.objects.filter(fpo_area__icontains=val)
   fpo = fpo1 | fpo2
  else:
 
   fpo=Fpo_Registeration.objects.all()
  total_result = fpo.count()
  context={'fpos':fpo, 'total_result':total_result,'total_items_in_cart':repeat(request)}
  return render(request, 'store/allfpos.html', context)


@login_required(login_url='login')  
def fpo_view(request, slug):
  fpo=Fpo_Registeration.objects.get(pk=slug)
  by=fpo.fpo_username
  user =User.objects.get(username=by)
  by1=user.id
  products = Product.objects.filter(product_by=by1)
  print(user.email)
  context={'fpo':fpo, 'products':products, 'total_items_in_cart':repeat(request)}
  if request.method == 'POST':
    email=request.POST.get('email')
    name=request.POST.get('name')
    sub=request.POST.get('subject')
    message=request.POST.get('message')
    number=request.POST.get('number')
    subject = sub
      
    message = f'''Hi 
                     {user.username}, 
                     username: {name},
                     email: {email},
                     phone number: {number},
                     wants to contact with you.
                     Message:
                     {message}'''
    email_from = settings.EMAIL_HOST_USER 
    recipient_list = [user.email,  ] 
     
    send_mail( subject, message, email_from, recipient_list ) 
  return render(request, 'store/fpo_detail_view.html', context)
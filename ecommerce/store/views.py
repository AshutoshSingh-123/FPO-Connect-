from django.shortcuts import render, redirect
from .models import Product, Cart, Fpo_Registeration, Service, Ngo_Registeration, ServiceForCustomer
from users.models import Message
from django.contrib.auth.decorators import login_required
from django.shortcuts import (get_object_or_404, 
                              render,  
                              HttpResponseRedirect) 
from .forms import Fpo_Registeration_form, Ngo_Registeration_form 
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
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
from .decorators import unauthenticated_user, allowed_users, user_only
from django.utils.decorators import method_decorator
import random

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
  by_fpo=item.product_by
  by1=Fpo_Registeration.objects.get(fpo_username=by_fpo)
  by=by1.id
  name=item.product_name
  carts=Cart.objects.filter(cartuser=request.user)
    
  # --------------else adding to cart------------------------------
  add=Cart(name=item.product_name, price=item.product_price, img=item.product_img1, cartuser=request.user, fpo_id=by, cartuser_email=request.user.email, by_fpo=by1)
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
  by_fpo=item.product_by
  by1=Fpo_Registeration.objects.get(fpo_username=by_fpo)
  by=by1.id
  # --------------else adding to cart------------------------------
  add=Cart(name=item.product_name, price=item.product_price, img=item.product_img1, cartuser=request.user, fpo_id=by, cartuser_email=request.user.email, by_fpo=by1)
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
@user_only
def fpo_register(request): 
    context ={} 
    context['form']= Fpo_Registeration_form () 
    
    if request.method=='POST':
      n1 = random.randint(0,9)
      n2 = random.randint(0,9)
      n3 = random.randint(0,9)
      n4 = random.randint(0,9)
      n5 = random.randint(0,9)
      n6 = random.randint(0,9)
     
      email=request.POST.get('email')
      name=request.POST.get('name')
      number1=request.POST.get('number1')
      number2=request.POST.get('number2')
      description=request.POST.get('description')
      area=request.POST.get('area')
      pincode=request.POST.get('pincode')
      member=request.POST.get('members')
      state=request.POST.get('state')
      distric=request.POST.get('distric')
      registered_with=request.POST.get('registered_with')
      u=request.POST.get('username')
      img=request.FILES.get('image')
      pancard=request.FILES.get('pancard')
      certificate=request.FILES.get('certificate')
      category = request.POST.get('category')
      registeration_number=str(n1)+str(n2)+str(n3)+str(n4)+str(n5)+str(n6)+str(request.user.id)
      f=Fpo_Registeration(fpo_username=u, fpo_name = name, fpo_area = area, area_pincode = int(pincode), total_members =int(member) , fpo_email = email, fpo_img = img, fpo_mobile1=number1, fpo_mobile2=number2, fpo_description=description, fpo_category=category, fpo_state=state, fpo_distric=distric, fpo_registered_with=registered_with, fpo_registeration_number=registeration_number, fpo_certificate=certificate, fpo_pancard=pancard )

      f.save() 
      group=Group.objects.get(name='FPO')
      request.user.groups.add(group)
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
@user_only
def ngo_register(request): 
    context ={} 
    context['form']= Ngo_Registeration_form () 
    
    if request.method=='POST':
      n1 = random.randint(0,9)
      n2 = random.randint(0,9)
      n3 = random.randint(0,9)
      n4 = random.randint(0,9)
      n5 = random.randint(0,9)
      n6 = random.randint(0,9)
      email=request.POST.get('email')
      name=request.POST.get('name')
      number1=request.POST.get('number1')
      number2=request.POST.get('number2')
      description=request.POST.get('description')
      area=request.POST.get('area')
      pincode=request.POST.get('pincode')
      member=request.POST.get('members')

      state=request.POST.get('state')
      distric=request.POST.get('distric')
      registered_with=request.POST.get('registered_with')
      pancard=request.FILES.get('pancard')
      certificate=request.FILES.get('certificate')

      u=request.POST.get('username')
      img=request.FILES.get('image')
      category = request.POST.get('category')
      registeration_number=str(n1)+str(n2)+str(n3)+str(n4)+str(n5)+str(n6)+str(request.user.id)

      f=Ngo_Registeration(ngo_username=u, ngo_name = name, ngo_area = area, area_pincode = int(pincode),  ngo_email = email, ngo_img = img, ngo_mobile1=number1, ngo_mobile2=number2, ngo_description=description, ngo_state=state, ngo_distric=distric, ngo_registered_with=registered_with, ngo_registeration_number=registeration_number, ngo_certificate=certificate, ngo_pancard=pancard)
      
      f.save() 
      group=Group.objects.get(name='NGO')
      request.user.groups.add(group)
      return render(request, "index.html")
    return render(request, "store/ngo_registration.html", context)


@method_decorator(allowed_users(allowed_roles=['FPO']), name='dispatch')
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
  by=fpo.fpo_username
  similars=Product.objects.filter(product_category=products.product_category)
  similars2=Product.objects.filter(product_by=products.product_by)
  context={'product':products, 'total_items_in_cart':repeat(request), 'similars':similars, 'similars2':similars2, 'fpo':fpo}
  if request.method == 'POST':
    email=request.POST.get('email')
    name=request.POST.get('name')
    sub=request.POST.get('subject')
    message1=request.POST.get('message')
    number=request.POST.get('number')
    
      
    msg=Message(from1=request.user.username, to=fpo, email=email, subject=sub, message=message1, phone=number)
    msg.save()

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
    message1=request.POST.get('message')
    number=request.POST.get('number')
    subject = sub
    msg=Message(from1=request.user.username, to=fpo, email=email, subject=sub, message=message1, phone=number)
    msg.save()
    
  return render(request, 'store/fpo_detail_view.html', context)

@login_required(login_url='login')  
def ngo_view(request, slug):


  fpo=Ngo_Registeration.objects.get(pk=slug)
  by=fpo.ngo_username
  user =User.objects.get(username=by)
  by1=user.id
  services = Service.objects.filter(service_by=by1)
  print(user.email)
  context={'fpo':fpo, 'services':services, 'total_items_in_cart':repeat(request)}
  
    
  return render(request, 'store/ngo_detail_view.html', context)

@login_required(login_url='login')
def services(request):
  services=Service.objects.all()
  context={'services':services}
  return render(request, 'store/services.html', context)

@login_required(login_url='login')
def customer_services(request):
  services=ServiceForCustomer.objects.all()
  context={'services':services}
  return render(request, 'store/service_customer.html', context)

@method_decorator(allowed_users(allowed_roles=['NGO']), name='dispatch')
class ServiceCreateView(LoginRequiredMixin, CreateView):
 model=Service
 fields = ['service_description', 'service_title', 'service_unit', 'service_price']
 group = None
 
 def form_valid(self, form):
  user=self.request.user.username
  fpo=Ngo_Registeration.objects.get(ngo_username=user)
  form.instance.service_by = fpo
  form.instance.service_by1 = self.request.user
  return super().form_valid(form)

@method_decorator(allowed_users(allowed_roles=['NGO']), name='dispatch')
class ServiceUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
 model=Service
 fields = ['service_description', 'service_title', 'service_unit', 'service_price']
 
 def form_valid(self, form):
  user=self.request.user.username
  fpo=Ngo_Registeration.objects.get(ngo_username=user)
  form.instance.service_by = fpo
  form.instance.service_by1 = self.request.user
  return super().form_valid(form)
 def test_func(self):
  service = self.get_object()
  if self.request.user==service.service_by1:
   return True
  return False

@method_decorator(allowed_users(allowed_roles=['NGO']), name='dispatch')
class ServiceDeleteView(DeleteView, LoginRequiredMixin, UserPassesTestMixin,):
 model=Service
 success_url = '/ngo_dashboard/'
 def test_func(self):
  user=self.request.user.username
  fpo=Fpo_Registeration.objects.get(fpo_username=user)
  form.instance.service_by = fpo
  form.instance.service_by1 = self.request.user
  service = self.get_object()
  if self.request.user==service.service_by1:
   return True
  return False

@method_decorator(allowed_users(allowed_roles=['FPO']), name='dispatch')
class CustomerServiceCreateView(LoginRequiredMixin, CreateView):
 model=ServiceForCustomer
 fields = ['service_description', 'service_title', 'service_unit', 'service_price']
 group = None
 
 def form_valid(self, form):
  user=self.request.user.username
  fpo=Fpo_Registeration.objects.get(fpo_username=user)
  form.instance.service_by = fpo
  form.instance.service_by1 = self.request.user
  return super().form_valid(form)

@method_decorator(allowed_users(allowed_roles=['FPO']), name='dispatch')
class CustomerServiceUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
 model=ServiceForCustomer
 fields = ['service_description', 'service_title', 'service_unit', 'service_price']
 
 def form_valid(self, form):
  user=self.request.user.username
  fpo=Fpo_Registeration.objects.get(fpo_username=user)
  form.instance.service_by = fpo
  form.instance.service_by1 = self.request.user
  return super().form_valid(form)
 def test_func(self):
  service = self.get_object()
  if self.request.user==service.service_by1:
   return True
  return False

@method_decorator(allowed_users(allowed_roles=['FPO']), name='dispatch')
class CustomerServiceDeleteView(DeleteView, LoginRequiredMixin, UserPassesTestMixin,):
 model=ServiceForCustomer
 success_url = '/fpo_dashboard/'
 def test_func(self):
  user=self.request.user.username
  fpo=Fpo_Registeration.objects.get(fpo_username=user)
  form.instance.service_by = fpo
  form.instance.service_by1 = self.request.user
  service = self.get_object()
  if self.request.user==service.service_by1:
   return True
  return False
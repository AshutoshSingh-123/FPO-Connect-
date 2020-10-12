from django.shortcuts import render

# Create your views here.
def home(request):
 group=False
 name=''
 if request.user.is_authenticated:
  if request.user.groups.exists():
   group=True
   name=request.user.groups.all()[0].name
 context={'group':group, 'name':name}
 return render(request, 'index.html', context)

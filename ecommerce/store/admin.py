from django.contrib import admin
from .models import Product, Cart, Fpo_Registeration, Service, Ngo_Registeration
# Register your models here.
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Fpo_Registeration)
admin.site.register(Ngo_Registeration)
admin.site.register(Service)
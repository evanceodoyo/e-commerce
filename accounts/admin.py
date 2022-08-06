from django.contrib import admin
from .models import Customer
from .forms import CustomerAdminForm
from django.contrib.auth.hashers import make_password

class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'date_joined']
    search_fields = ['name', 'email', 'phone']

    def save_model(self, request, Customer, CustomerAdminForm, change):
        Customer.password = make_password(Customer.password)
        return super().save_model(request, Customer, CustomerAdminForm, change)

admin.site.register(Customer, CustomerAdmin)
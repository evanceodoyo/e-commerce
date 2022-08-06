from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

class Customer(models.Model):
    name = models.CharField(max_length=80)
    email = models.EmailField(max_length=80, unique=True)
    phone = PhoneNumberField()
    password = models.CharField(max_length=50)
    date_joined = models.DateTimeField(auto_now_add=True)


    class Meta:
        db_table = 'customers'
        ordering = ['name']

    def __str__(self):
        return self.name

    def email_exists(self):
        return Customer.objects.filter(email=self.email)

    def get_customer_by_email(email):
        try:
            return Customer.objects.get(email=email)
        except:
            return False


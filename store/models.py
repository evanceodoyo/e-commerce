from django.db import models
from django.urls import reverse
from PIL import Image
from  accounts.models import Customer
from phonenumber_field.modelfields import PhoneNumberField

class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'categories'
        ordering = ['name']
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'category_slug': self.slug})


class Product(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    old_price = models.DecimalField(max_digits=9, decimal_places=2, blank=True, default=0.00)
    image = models.ImageField(upload_to='products/images')
    description = models.TextField()
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    is_bestseller = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    # help text to be: Content for description meta tag.
    meta_description = models.CharField(max_length=250)
    # help text to be: Comma-delimted set of SEO keywrods
    meta_keywords = models.CharField(max_length=250) 
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        db_table = 'products'
        ordering = ['-date_created']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(args, kwargs)
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

    def get_absolute_url(self):
        return reverse('catalog_product', kwargs={'product_slug': self.slug})

    def get_products_by_slug(cart_product_slug):
        return Product.objects.filter(slug__in=cart_product_slug)

class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    address = models.CharField(max_length=80)
    region = models.CharField(max_length=80)
    phone = PhoneNumberField()
    date_ordered = models.DateTimeField(auto_now_add=True)
    order_complete = models.BooleanField(default=False)

    class Meta:
        db_table = 'orders'
        ordering = ['-date_ordered']

    def __str__(self):
        return f'Order for {self.customer}'
    
    def get_order_by_customer(customer_id):
        return Order.objects.filter(customer=customer_id)
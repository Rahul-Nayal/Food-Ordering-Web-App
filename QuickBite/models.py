from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta
from django.utils import timezone
# Create your models here.

class SignUp(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contact_number = models.IntegerField()
    profile_pic = models.ImageField( upload_to='profile/%y/%m/%d',null=True,blank=True)
    address = models.TextField(max_length=250,null = True, blank=True)
    def __str__(self):
        return self.user.first_name

    class Meta:
        verbose_name_plural = "Customer"

class Category(models.Model):
    category_name = models.CharField(max_length=250)
    cover_img = models.FileField(upload_to = 'media/%y/%m/%d')
    description = models.TextField()
    added_on = models.DateTimeField(auto_now_add = True)
    updated_on = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.category_name
    
    class Meta:
        verbose_name_plural = "Categories"


class Dish(models.Model):
    dish_name = models.CharField(max_length=250,unique=True)
    image = models.ImageField(upload_to='dishes/%y/%m/%d')
    ingredients = models.TextField()
    details = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,null=True,blank=True)
    price = models.FloatField()
    discounted_price = models.FloatField(blank = True,null=True)
    is_available = models.BooleanField(default = True)
    added_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.dish_name
    
    class Meta:
        verbose_name_plural = "Dish Table"

class Order(models.Model):
    customer = models.ForeignKey(SignUp,on_delete=models.SET_NULL,null=True,blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100,blank=True)
    estimated_delivery_time = models.DateTimeField(null=True,blank=True)
    delivery_status = models.CharField(max_length=20,default='Pending')

    def save(self,*args, **kwargs):
        if not self.estimated_delivery_time:
            self.estimated_delivery_time = timezone.now()+timedelta(minutes=30)
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.id)
    
    @property
    def shipping(self):
        return True
    
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total
    
    def get_cart_item(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total
    
    def update_delivery_status(self):
        if self.estimated_delivery_time and timezone.now() >= self.estimated_delivery_time:
            self.delivery_status = 'Delivered'
            self.save()


class OrderItem(models.Model):
    dish = models.ForeignKey(Dish,on_delete=models.SET_NULL,null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField(default=0,blank=True,null=True)

    def __str__(self):
        return self.dish.dish_name
    
    @property
    def get_total(self):
        total = self.quantity*self.dish.price
        return total
    
    class Meta:
        unique_together = (('dish','order'),)


class ShippingAddress(models.Model):
    customer = models.ForeignKey(SignUp,on_delete=models.SET_NULL,null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE,null=True)
    address = models.CharField(max_length=250,null=False)
    city = models.CharField(max_length=50,null=False)
    state = models.CharField(max_length=50,null=False)
    zipcode = models.CharField(max_length=50,null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address
    

class ContactUs(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    contact_number = models.IntegerField(unique=True,blank=True)
    subject = models.CharField(max_length=100)
    message = models.TextField()
    added_on = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Contact Us"
    
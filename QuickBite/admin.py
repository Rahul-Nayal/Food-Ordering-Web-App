from django.contrib import admin
from QuickBite.models import SignUp,Category,Dish,Order,OrderItem,ShippingAddress,ContactUs

admin.site.site_header = 'QuickBite'
# Register your models here.

class ContactUsAdmin(admin.ModelAdmin):
    list_display=['id','name','email','contact_number','subject','message','added_on']
    search_fields = ['name','contact_number','subject','added_on']
    list_editable = ['email']
    list_filter = ['name','subject','added_on']

class CategoryAdmin(admin.ModelAdmin):
    list_display=['id','category_name','description','added_on']

class DishAdmin(admin.ModelAdmin):
    list_display = ['id','dish_name','added_on','is_available']

admin.site.register(ContactUs,ContactUsAdmin)
admin.site.register(SignUp)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Dish,DishAdmin)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)




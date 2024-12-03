from django.contrib import admin
from django.urls import path
from QuickBite import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.indexpage, name='index'),
    path('signup/',views.signuppage,name='signup'),
    path('about/',views.aboutpage,name ='about'),
    path('contact/',views.contactpage,name='contact'),
    path('menu/',views.menupage,name='menu'),
    path('cart/',views.cartpage, name='cart'),
    path('dishes/',views.menu_by_category,name="all_dishes"),
    path('user_login/',views.user_login,name='user_login'),
    path('check_user/',views.check_user,name='check_user'),
    path('dashboard/',views.cust_dashboard,name='dashboard'),
    path('checkout/',views.checkoutpage,name='checkout'),
    path('update_item/',views.updateItem,name='update_item'),
    path('user_logout/',views.user_logout,name='user_logout'),
    path('process_order/',views.processOrder,name='process_order'),
]+static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
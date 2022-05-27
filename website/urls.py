from django.urls import path, re_path

from website.views import ShopView, CategoryView, add_to_cart, CartDeleteView
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('contact/', views.contactus, name='contactus'),
    path('logout/', views.user_logout, name='logout'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('cart/', views.get_cart_items, name='cart'),
    path('services/', views.service, name='services'),
    path('events/', views.actualite, name='events'),
    path('category/<slug>/', CategoryView.as_view(), name='category'),
    path('product/<slug>/', views.menuDetail, name='product'),
    path('projects/', views.project, name='projects'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<int:pk>/', CartDeleteView.as_view(), name='remove-from-cart'),
    path('adjust/<str:id>/', views.adjust_cart, name="adjust_cart"),
    path('ordered/', views.order_item, name='ordered'),
    path('order_details/', views.order_details, name='order_details'),
    path('gallery/', views.gallery, name='gallery'),
    path('aboutus/', views.aboutus, name='aboutus'),
    path('catalogue/', ShopView.as_view(), name='shop'),
    re_path('download/(?P<file_path>.*)/$', views.file_response_download, name='file_download'),

]

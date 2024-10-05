from django.urls import path
from .views import GetProducts, GetProduct, AddProduct, RegisterUser, LoginUser

urlpatterns = [
    path('products', GetProducts.as_view(), name="get_products"),
    path('product/<int:id>', GetProduct.as_view(), name="get_product"),
    path('product', AddProduct.as_view(), name="add_product"),
    path('user/register', RegisterUser.as_view(), name="create_user"),
    path('user/login', LoginUser.as_view(), name="login_user"),
    # path('user/logout', LogoutUser.as_view(), name="logout_user")
]

from django.urls import path

from .views import (
    product_list,
    category_products,
    product_detail,
    add_to_cart,
    cart_view,
    increase_cart,
    decrease_cart,
    remove_from_cart,
    checkout,
    track_order,
    order_success,
)


urlpatterns = [

    path(
        "",
        product_list,
        name="product_list"
    ),
    path(
        "category/<int:category_id>/",
        category_products,
        name="category_products"
    ),
    
    path(
        "product/<int:product_id>/",
        product_detail,
        name="product_detail"
    ),

    path(
        "cart/add/<int:product_id>/",
        add_to_cart,
        name="add_to_cart"
    ),

    path(
        "cart/",
        cart_view,
        name="cart"
    ),

    path(
        "cart/increase/<int:product_id>/",
        increase_cart,
        name="increase_cart"
    ),

    path(
        "cart/decrease/<int:product_id>/",
        decrease_cart,
        name="decrease_cart"
    ),

    path(
        "cart/remove/<int:product_id>/",
        remove_from_cart,
        name="remove_from_cart"
    ),

    path(
        "checkout/",
        checkout,
        name="checkout"
    ),

    path(
        "order-success/<int:order_id>/",
        order_success,
        name="order_success"
    ),

    path(
        "track-order/",
        track_order,
        name="track_order"
    ),

    path(
        "track-order/<int:order_id>/",
        track_order,
        name="track_order_direct"
    ),

]
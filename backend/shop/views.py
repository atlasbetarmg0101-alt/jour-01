from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import Count

from .models import Product, Category, Order, OrderItem

def category_products(request, category_id):
    category = get_object_or_404(Category, id=category_id)

    products = Product.objects.filter(
        category=category
    )

    product_count = products.count()

    return render(request, "shop/category_products.html", {
        "category": category,
        "products": products,
        "product_count": product_count,
    })
def product_list(request):
    query = request.GET.get("q", "")
    category_id = request.GET.get("category", "")

    products = Product.objects.all()

    if query:
        products = products.filter(name__icontains=query)

    if category_id:
        products = products.filter(category_id=category_id)

    categories = Category.objects.annotate(
        product_count=Count("products")
    )

    return render(request, "shop/product_list.html", {
        "products": products,
        "query": query,
        "categories": categories,
        "selected_category": category_id,
    })


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    return render(request, "shop/product_detail.html", {
        "product": product,
    })


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    cart = request.session.get("cart", {})

    product_id = str(product_id)

    if product_id in cart:
        cart[product_id] += 1
    else:
        cart[product_id] = 1

    request.session["cart"] = cart
    request.session.modified = True

    return redirect("product_detail", product_id=product.id)


def cart_view(request):
    cart = request.session.get("cart", {})

    cart_items = []
    total = 0

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)

        item_total = product.price * quantity
        total += item_total

        cart_items.append({
            "product": product,
            "quantity": quantity,
            "item_total": item_total,
        })

    return render(request, "shop/cart.html", {
        "cart_items": cart_items,
        "total": total,
    })


def increase_cart(request, product_id):
    cart = request.session.get("cart", {})

    product_id = str(product_id)

    if product_id in cart:
        cart[product_id] += 1

    request.session["cart"] = cart
    request.session.modified = True

    return redirect("cart")


def decrease_cart(request, product_id):
    cart = request.session.get("cart", {})

    product_id = str(product_id)

    if product_id in cart:
        cart[product_id] -= 1

        if cart[product_id] <= 0:
            del cart[product_id]

    request.session["cart"] = cart
    request.session.modified = True

    return redirect("cart")


def remove_from_cart(request, product_id):
    cart = request.session.get("cart", {})

    product_id = str(product_id)

    if product_id in cart:
        del cart[product_id]

    request.session["cart"] = cart
    request.session.modified = True

    return redirect("cart")


def checkout(request):
    cart = request.session.get("cart", {})

    if not cart:
        return redirect("cart")

    cart_items = []
    total = 0

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)

        item_total = product.price * quantity
        total += item_total

        cart_items.append({
            "product": product,
            "quantity": quantity,
            "item_total": item_total,
        })

    if request.method == "POST":

        customer_name = request.POST.get(
            "customer_name",
            ""
        ).strip()

        phone = request.POST.get(
            "phone",
            ""
        ).strip()

        city = request.POST.get(
            "city",
            ""
        ).strip()

        address = request.POST.get(
            "address",
            ""
        ).strip()

        if not customer_name or not phone or not city or not address:

            return render(request, "shop/checkout.html", {
                "cart_items": cart_items,
                "total": total,
                "error": "يرجى ملء جميع المعلومات المطلوبة.",
            })

        order = Order.objects.create(
            customer_name=customer_name,
            phone=phone,
            city=city,
            address=address,
            total=total,
        )

        for item in cart_items:

            OrderItem.objects.create(
                order=order,
                product=item["product"],
                quantity=item["quantity"],
                price=item["product"].price,
            )

        request.session["cart"] = {}
        request.session.modified = True

        return redirect(
            "order_success",
            order_id=order.id
        )

    return render(request, "shop/checkout.html", {
        "cart_items": cart_items,
        "total": total,
    })

def track_order(request, order_id=None):

    order = None
    error = None

    # فتح طلب محدد مباشرة من رابط الإدارة
    if order_id:

        order = get_object_or_404(
            Order,
            id=order_id
        )

    # التتبع بالطريقة العادية عن طريق رقم الطلب والهاتف
    elif request.method == "POST":

        order_id = request.POST.get(
            "order_id",
            ""
        ).strip()

        phone = request.POST.get(
            "phone",
            ""
        ).strip()

        if not order_id or not phone:

            error = "المرجو إدخال رقم الطلب ورقم الهاتف."

        else:

            try:

                order = Order.objects.get(
                    id=order_id,
                    phone=phone
                )

            except Order.DoesNotExist:

                error = (
                    "لم يتم العثور على الطلب. "
                    "تحقق من المعلومات المدخلة."
                )

    return render(request, "shop/track_order.html", {
        "order": order,
        "error": error,
    })

def order_success(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id
    )

    return render(
        request,
        "shop/order_success.html",
        {
            "order": order,
        }
    )
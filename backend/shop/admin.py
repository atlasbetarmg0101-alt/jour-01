from django.contrib import admin
from django.db.models import Sum
from django.urls import reverse
from django.utils.html import format_html

from .models import Category, Product, Order, OrderItem


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "created_at",
    )

    search_fields = (
        "name",
    )

    ordering = (
        "name",
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = (
    "name",
    "category",
    "price",
    "available",
    )

    list_filter = (
    "category",
    "available",
    )  

    search_fields = (
        "name",
    )


class OrderItemInline(admin.TabularInline):

    model = OrderItem

    extra = 0

    fields = (
        "product",
        "quantity",
        "price",
    )

    readonly_fields = (
        "price",
    )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "customer_name",
        "phone",
        "city",
        "total",
        "product_count",
        "colored_status",
        "quick_links",
        "created_at",
    )

    list_filter = (
        "status",
        "city",
        "created_at",
    )

    search_fields = (
        "customer_name",
        "phone",
        "city",
    )

    ordering = (
        "-created_at",
    )

    fieldsets = (
        (
            "معلومات العميل",
            {
                "fields": (
                    "customer_name",
                    "phone",
                    "city",
                    "address",
                )
            },
        ),
        (
            "معلومات الطلب",
            {
                "fields": (
                    "total",
                    "status",
                    "created_at",
                )
            },
        ),
    )

    readonly_fields = (
        "created_at",
    )

    inlines = (
        OrderItemInline,
    )
    def get_queryset(self, request):

        queryset = super().get_queryset(request)

        return queryset.annotate(
           total_products=Sum("items__quantity")
    )
    @admin.display(
        description="عدد المنتجات",
        ordering="total_products",
    )
    def product_count(self, obj):

        return obj.total_products

    @admin.display(
        description="الحالة",
        ordering="status",
    )
    def colored_status(self, obj):

        colors = {
            "new": "#2563eb",
            "processing": "#f59e0b",
            "shipped": "#7c3aed",
            "delivered": "#16a34a",
            "cancelled": "#dc2626",
        }

        color = colors.get(
            obj.status,
            "#6b7280"
        )

        return format_html(
            '<strong style="color: {};">{}</strong>',
            color,
            obj.get_status_display(),
        )

    @admin.display(
        description="روابط",
    )
    def quick_links(self, obj):

        admin_url = reverse(
            "admin:shop_order_change",
            args=[obj.pk]
        )

        tracking_url = reverse(
            "track_order_direct",
            args=[obj.pk]
        )

        return format_html(
            '<a href="{}" '
            'style="margin-left: 8px; color: #2563eb; font-weight: bold;">'
            'فتح الطلب</a>'
            '<a href="{}" '
            'style="color: #16a34a; font-weight: bold;">'
            'تتبع</a>',
            admin_url,
            tracking_url,
        )


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):

    list_display = (
        "order",
        "product",
        "quantity",
        "price",
    )

    search_fields = (
        "order__customer_name",
        "product__name",
    )
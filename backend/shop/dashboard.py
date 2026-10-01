from django.db.models import Sum
from .models import Order


def get_dashboard_stats():
    total_orders = Order.objects.count()

    new_orders = Order.objects.filter(
        status="new"
    ).count()

    processing_orders = Order.objects.filter(
        status="processing"
    ).count()

    total_sales = Order.objects.aggregate(
        total=Sum("total")
    )["total"] or 0

    return {
        "total_orders": total_orders,
        "new_orders": new_orders,
        "processing_orders": processing_orders,
        "total_sales": total_sales,
    }
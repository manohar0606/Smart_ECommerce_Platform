from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, Sum
from django.db.models.functions import TruncDate
from django.shortcuts import render

from products.models import Product
from .models import Order, OrderItem


@staff_member_required
def analytics_dashboard(request):
    paid_orders = Order.objects.filter(
        payment_status="paid"
    )

    total_sales = (
        paid_orders.aggregate(total=Sum("total"))["total"]
        or 0
    )

    total_orders = Order.objects.count()

    paid_orders_count = paid_orders.count()

    top_products = (
        OrderItem.objects.filter(
            order__payment_status="paid"
        )
        .values("product__name")
        .annotate(
            quantity_sold=Sum("quantity")
        )
        .order_by("-quantity_sold")[:10]
    )

    revenue_data = (
        paid_orders
        .annotate(day=TruncDate("timestamp"))
        .values("day")
        .annotate(revenue=Sum("total"))
        .order_by("day")
    )

    revenue_labels = [
        item["day"].strftime("%Y-%m-%d")
        for item in revenue_data
    ]

    revenue_values = [
        float(item["revenue"])
        for item in revenue_data
    ]

    low_stock_products = Product.objects.filter(
        stock__lte=5,
        is_active=True,
    ).order_by("stock")

    context = {
        "total_sales": total_sales,
        "total_orders": total_orders,
        "paid_orders": paid_orders_count,
        "low_stock_count": low_stock_products.count(),
        "top_products": top_products,
        "low_stock_products": low_stock_products,
        "revenue_labels": revenue_labels,
        "revenue_values": revenue_values,
    }

    return render(
        request,
        "admin/analytics.html",
        context,
    )
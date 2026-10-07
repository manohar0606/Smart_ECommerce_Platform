import csv
from io import BytesIO

from django.contrib import admin
from django.http import HttpResponse
from django.utils import timezone

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from .models import Cart, Notification, Order, OrderItem, Payment


def export_orders_csv(modeladmin, request, queryset):
    response = HttpResponse(
        content_type="text/csv",
    )
    response["Content-Disposition"] = (
        'attachment; filename="orders_report.csv"'
    )

    writer = csv.writer(response)

    writer.writerow(
        [
            "Order ID",
            "Customer",
            "Email",
            "Total",
            "Payment Status",
            "Order Status",
            "Timestamp",
        ]
    )

    for order in queryset.select_related("user"):
        writer.writerow(
            [
                order.id,
                order.user.username,
                order.user.email,
                order.total,
                order.payment_status,
                order.order_status,
                order.timestamp,
            ]
        )

    return response


export_orders_csv.short_description = (
    "Export selected orders as CSV"
)


def export_orders_pdf(modeladmin, request, queryset):
    buffer = BytesIO()

    pdf = canvas.Canvas(
        buffer,
        pagesize=A4,
    )

    width, height = A4
    y = height - 40

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(
        40,
        y,
        "Smart E-Commerce - Orders Report",
    )

    y -= 25

    pdf.setFont("Helvetica", 9)
    pdf.drawString(
        40,
        y,
        f"Generated: {timezone.now()}",
    )

    y -= 30

    pdf.setFont("Helvetica-Bold", 9)

    headers = [
        "ID",
        "Customer",
        "Total",
        "Payment",
        "Status",
    ]

    x_positions = [40, 80, 250, 330, 415]

    for index, header in enumerate(headers):
        pdf.drawString(
            x_positions[index],
            y,
            header,
        )

    y -= 18
    pdf.setFont("Helvetica", 8)

    for order in queryset.select_related("user"):
        values = [
            str(order.id),
            order.user.username[:25],
            str(order.total),
            order.payment_status,
            order.order_status,
        ]

        for index, value in enumerate(values):
            pdf.drawString(
                x_positions[index],
                y,
                value,
            )

        y -= 16

        if y < 50:
            pdf.showPage()
            y = height - 50

            pdf.setFont(
                "Helvetica-Bold",
                9,
            )

            for index, header in enumerate(headers):
                pdf.drawString(
                    x_positions[index],
                    y,
                    header,
                )

            y -= 18
            pdf.setFont("Helvetica", 8)

    pdf.save()

    buffer.seek(0)

    response = HttpResponse(
        buffer.getvalue(),
        content_type="application/pdf",
    )

    response["Content-Disposition"] = (
        'attachment; filename="orders_report.pdf"'
    )

    return response


export_orders_pdf.short_description = (
    "Export selected orders as PDF"
)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "product",
        "quantity",
    )

    search_fields = (
        "user__username",
        "product__name",
    )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "total",
        "payment_status",
        "order_status",
        "timestamp",
    )

    list_filter = (
        "payment_status",
        "order_status",
        "timestamp",
    )

    search_fields = (
        "user__username",
        "user__email",
    )

    actions = [
        export_orders_csv,
        export_orders_pdf,
    ]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "order",
        "product",
        "quantity",
        "price",
    )

    search_fields = (
        "order__id",
        "product__name",
    )


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "order",
        "amount",
        "payment_method",
        "transaction_id",
        "status",
        "created_at",
    )

    list_filter = (
        "payment_method",
        "status",
    )

    search_fields = (
        "transaction_id",
        "order__id",
    )


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "type",
        "message",
        "is_read",
        "timestamp",
    )

    list_filter = (
        "type",
        "is_read",
        "timestamp",
    )

    search_fields = (
        "user__username",
        "user__email",
        "message",
    )
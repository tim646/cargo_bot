from django.contrib import admin

from .models import Inventory, Category, Order, OrderItem


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ["name", "barcode", "price", "quantity", "category"]
    list_filter = ["category"]
    search_fields = ["name", "barcode"]

    class Meta:
        model = Inventory


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name"]

    class Meta:
        model = Category


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "cashier", "created_at"]
    list_filter = ["cashier"]
    search_fields = ["cashier", "id"]
    fields = ("cashier", "complete", "created_at", "get_cart_total", "get_cart_items")
    readonly_fields = ("created_at", "get_cart_total", "get_cart_items")

    class Meta:
        model = Order

    def has_add_permission(self, request):
        if request.user.role == "cashier":
            return False
        return True

    def has_change_permission(self, request, obj=None):
        if request.user.role == "cashier":
            return False
        return True


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ["product", "order", "quantity"]
    list_filter = ["order"]
    search_fields = ["order"]

    class Meta:
        model = OrderItem

    def has_add_permission(self, request):
        if request.user.role == "cashier":
            return False
        return True

    def has_change_permission(self, request, obj=None):
        return False

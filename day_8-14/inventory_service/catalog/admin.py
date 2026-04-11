from django.contrib import admin

from .models import Category, Product, Stock


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


class StockInline(admin.StackedInline):
    model = Stock
    can_delete = False


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "category", "price", "get_stock")
    list_filter = ("category",)
    search_fields = ("name", "description")
    inlines = (StockInline,)

    def get_stock(self, obj):
        return obj.stock.quantity if hasattr(obj, "stock") else 0

    get_stock.short_description = "Stock"


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ("product", "quantity")
    search_fields = ("product__name",)

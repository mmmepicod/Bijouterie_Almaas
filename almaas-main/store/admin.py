from django.contrib import admin
from .models import (
    Address,
    Category,
    Product,
    Cart,
    Order,
    Credit_Card,
    Sub_Category,
    Product_Shipping,
)


# Registre de modèles admin ( accessibles depuis l'interface de gestion sur le site),
# Créer en indiquant les champs accessibles depuis le crud de l'interface admin du site


class AddressAdmin(admin.ModelAdmin):
    list_display = ("user", "locality", "city", "state")
    list_filter = ("city", "state")
    list_per_page = 10
    search_fields = ("locality", "city", "state")


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "slug",
        "category_image",
        "description",
        "is_active",
        "is_featured",
        "updated_at",
    )
    list_editable = ("slug", "description", "is_active", "is_featured")
    list_filter = ("is_active", "is_featured")
    list_per_page = 10
    search_fields = ("title", "description")
    prepopulated_fields = {"slug": ("title",)}


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "slug",
        "category",
        "product_image",
        "short_description",
        "is_active",
        "is_featured",
        "updated_at",
    )
    list_editable = (
        "slug",
        "category",
        "short_description",
        "is_active",
        "is_featured",
    )
    list_filter = ("category", "is_active", "is_featured")
    list_per_page = 10
    search_fields = ("title", "category", "short_description")
    prepopulated_fields = {"slug": ("title",)}


class CartAdmin(admin.ModelAdmin):
    list_display = ("user", "product", "quantity", "created_at")
    list_editable = ("quantity",)
    list_filter = ("created_at",)
    list_per_page = 20
    search_fields = ("user", "product")


class OrderAdmin(admin.ModelAdmin):
    list_display = ("user", "product", "quantity", "status", "ordered_date")
    list_editable = ("quantity", "status")
    list_filter = ("status", "ordered_date")
    list_per_page = 20
    search_fields = ("user", "product")


class CreditCardAdmin(admin.ModelAdmin):
    list_display = ("user", "numero", "expiration_date")
    list_editable = ("numero", "expiration_date")
    list_filter = ("user", "numero")
    list_per_page = 20
    search_fields = ("user", "numero")


class SubCategoryAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "slug",
        "sub_category_image",
        "description",
        "is_active",
        "is_featured",
        "updated_at",
    )
    list_editable = ("slug", "description", "is_active", "is_featured")
    list_filter = ("is_active", "is_featured")
    list_per_page = 10
    search_fields = ("title", "description")
    prepopulated_fields = {"slug": ("title",)}


class ProductShippingAdmin(admin.ModelAdmin):
    list_display = ("order", "date_envoi", "lien_transporteur", "type_envoi")

    # quand on a rajouté plus haut la classe à rendre  gérable en crud sur l'interface d'administration,
    # enregistrer cette classe en indiquant la classe correspondante dans models,
    # la règle de bonne pratique est qu'ci la classe aura le nom nomClasseModel+Admin


admin.site.register(Address, AddressAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Sub_Category, SubCategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Credit_Card, CreditCardAdmin)
admin.site.register(Product_Shipping, ProductShippingAdmin)

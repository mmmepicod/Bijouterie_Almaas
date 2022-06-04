from django.db import models
from django.contrib.auth.models import User


# Facilité ORM , création et stockage des modèles tableaux ( classes et champs ) en code ( facilité de migration )
class Address(models.Model):
    user = models.ForeignKey(User, verbose_name="User", on_delete=models.CASCADE)
    locality = models.CharField(
        max_length=150,
        verbose_name="Région on met adresse? :models.py/adress pour modif)",
    )
    city = models.CharField(max_length=150, verbose_name="Ville")
    state = models.CharField(max_length=150, verbose_name="Pays")

    def __str__(self):
        return self.locality


class Category(models.Model):
    title = models.CharField(max_length=50, verbose_name="Titre")
    slug = models.SlugField(max_length=55, verbose_name="raccourci")
    description = models.TextField(blank=True, verbose_name="Description")
    category_image = models.ImageField(
        upload_to="category", blank=True, null=True, verbose_name="Image"
    )
    is_active = models.BooleanField(verbose_name="Actif ?")
    is_featured = models.BooleanField(verbose_name="Vedette ?")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated Date")

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ("-created_at",)

    def __str__(self):
        return self.title

    @property
    def image_url(self):
        if self.category_image and hasattr(self.category_image, "url"):
            return self.category_image.url


class Sub_Category(models.Model):
    title = models.CharField(max_length=50, verbose_name="Sub Category Title")
    slug = models.SlugField(max_length=55, verbose_name="Sub Category Slug")
    description = models.TextField(blank=True, verbose_name="Sub Category Description")
    sub_category_image = models.ImageField(
        upload_to="sub category",
        blank=True,
        null=True,
        verbose_name="Sub Category Image",
    )
    is_active = models.BooleanField(verbose_name="Is Active?")
    is_featured = models.BooleanField(verbose_name="Is Featured?")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated Date")

    class Meta:
        verbose_name_plural = "Sub_Categories"
        ordering = ("-created_at",)

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=150, verbose_name="Nom")
    slug = models.SlugField(max_length=160, verbose_name="Raccourci")
    sku = models.CharField(
        max_length=255, unique=True, verbose_name="Identifiant unique (SKU)"
    )
    short_description = models.TextField(verbose_name="Description")
    detail_description = models.TextField(
        blank=True, null=True, verbose_name="Description detaillée"
    )
    product_image = models.ImageField(
        upload_to="product", blank=True, null=True, verbose_name="Image"
    )
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Prix")
    category = models.ForeignKey(
        Category, verbose_name="Catégorie", on_delete=models.CASCADE
    )
    sub_category = models.ForeignKey(
        Sub_Category,
        verbose_name="Sous-catégorie",
        null=True,
        on_delete=models.CASCADE,
    )
    is_active = models.BooleanField(verbose_name="Actif ?")
    is_featured = models.BooleanField(verbose_name="Vedette ?")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated Date")

    # champs rajoutés
    en_promo = models.BooleanField(blank=False, verbose_name="En promo")
    taux = models.DecimalField(blank=0, max_digits=4, decimal_places=2)

    @property
    def image_url(self):
        if self.product_image and hasattr(self.product_image, "url"):
            return self.product_image.url

    # méthode de calcul de prix
    def prix_effectif(self):
        return round((self.price * ((100 - self.taux) / 100)), 2)

    def montant_promo(self):
        return round(self.price * (self.taux / 100), 2)

    class Meta:
        verbose_name_plural = "Products"
        ordering = ("-created_at",)

    def __str__(self):
        return self.title


class Cart(models.Model):
    user = models.ForeignKey(User, verbose_name="User", on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, verbose_name="Product", on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(default=1, verbose_name="Quantity")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated Date")

    def __str__(self):
        return str(self.user)

    # Creating Model Property to calculate Quantity x Price
    @property
    def total_price(self):
        return self.quantity * self.product.prix_effectif()

    def total_promo_produit(self):
        return self.quantity * self.product.montant_promo()


STATUS_CHOICES = (
    ("Pending", "Pending"),
    ("Accepted", "Accepted"),
    ("Packed", "Packed"),
    ("On The Way", "On The Way"),
    ("Delivered", "Delivered"),
    ("Cancelled", "Cancelled"),
)


class Order(models.Model):
    user = models.ForeignKey(User, verbose_name="User", on_delete=models.CASCADE)
    address = models.ForeignKey(
        Address, verbose_name="Shipping Address", on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product, verbose_name="Product", on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(verbose_name="Quantity")
    ordered_date = models.DateTimeField(auto_now_add=True, verbose_name="Ordered Date")
    status = models.CharField(choices=STATUS_CHOICES, max_length=50, default="Pending")


class Credit_Card(models.Model):
    user = models.ForeignKey(User, verbose_name="User", on_delete=models.CASCADE)
    numero = models.PositiveIntegerField(verbose_name="numero de la carte")
    expiration_date = models.DateTimeField(verbose_name="Expiration date")


SENDING_CHOICES = (
    ("Normal", "Normal"),
    ("Eco", "Eco"),
    ("Fast", "Fast"),
    ("Very Fast", "Very Fast"),
)


class Product_Shipping(models.Model):
    order = models.ForeignKey(Order, verbose_name="Order", on_delete=models.CASCADE)
    date_envoi = models.DateTimeField(auto_now_add=True, verbose_name="Date envoi")
    lien_transporteur = models.CharField(max_length=300, verbose_name="Suivi transport")
    type_envoi = models.CharField(
        choices=SENDING_CHOICES, max_length=50, default="Normal"
    )

from django.db.models import Q

from store.models import Address, Cart, Category, Order, Product
from django.shortcuts import redirect, render, get_object_or_404
from .forms import RegistrationForm, AddressForm, CategoryForm, ProductForm
from django.contrib import messages
from django.views import View
import decimal
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.conf import settings


# Création des vues
from .helpers import htmx_redirect


def home(request):
    categories = Category.objects.filter(is_active=True, is_featured=True)[:3]
    products = Product.objects.filter(is_active=True, is_featured=True)[:8]
    context = {
        "categories": categories,
        "products": products,
    }
    return render(request, "store/index.html", context)


def detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    related_products = Product.objects.exclude(id=product.id).filter(
        is_active=True, category=product.category
    )
    context = {
        "product": product,
        "related_products": related_products,
    }
    return render(request, "store/detail.html", context)


def all_categories(request):
    categories = Category.objects.filter(is_active=True)
    return render(request, "store/categories.html", {"categories": categories})


def category_products(request, slug):
    categorie = get_object_or_404(Category, slug=slug)
    produits = Product.objects.filter(is_active=True, category=categorie)
    categories = Category.objects.filter(is_active=True)
    context = {
        "category": categorie,
        "products": produits,
        "categories": categories,
    }
    return render(request, "store/category_products.html", context)


def registration_view(request):
    form = RegistrationForm()
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request, "Félicitations! Inscription réussie!")
            form.save()
    return render(request, "account/register.html", {"form": form})


@login_required
def profile(request):
    addresses = Address.objects.filter(user=request.user)
    orders = Order.objects.filter(user=request.user)
    return render(
        request, "account/profile.html", {"addresses": addresses, "orders": orders}
    )


@method_decorator(login_required, name="dispatch")
class AddressView(View):
    def get(self, request):
        form = AddressForm()
        return render(request, "account/add_address.html", {"form": form})

    def post(self, request):
        form = AddressForm(request.POST)
        if form.is_valid():
            utilisateur = request.user
            localite = form.cleaned_data["locality"]
            city = form.cleaned_data["city"]
            state = form.cleaned_data["state"]
            reg = Address(user=utilisateur, locality=localite, city=city, state=state)
            reg.save()
            messages.success(request, "Nouvelle adresse ajoutée.")
        return redirect("store:profile")


@login_required
def remove_address(request, id):
    a = get_object_or_404(Address, user=request.user, id=id)
    a.delete()
    messages.success(request, "Adresse supprimée.")
    return redirect("store:profile")


@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get("prod_id")
    product = get_object_or_404(Product, id=product_id)

    # On vérifie si le produit est dans le panier
    dans_le_panier = Cart.objects.filter(product=product_id, user=user)
    if dans_le_panier:
        cp = get_object_or_404(Cart, product=product_id, user=user)
        cp.quantity += 1
        cp.save()
    else:
        Cart(user=user, product=product).save()

    return redirect("store:cart")


@login_required
def cart(request):
    user = request.user
    cart_products = Cart.objects.filter(user=user)

    # afficher le total d'un panier frais de port compris

    amount = decimal.Decimal(0)
    shipping_amount = decimal.Decimal(10)

    # avoir le montant total en fonction du nombre de produits
    cp = [p for p in Cart.objects.all() if p.user == user]
    if cp:
        for p in cp:
            temp_amount = p.quantity * p.product.price
            amount += temp_amount

    addresses = Address.objects.filter(user=user)

    context = {
        "cart_products": cart_products,
        "amount": amount,
        "shipping_amount": shipping_amount,
        "total_amount": amount + shipping_amount,
        "addresses": addresses,
        "client_id": settings.CLIENT_ID,
    }
    return render(request, "store/cart.html", context)


@login_required
def remove_cart(request, cart_id):
    if request.method == "GET":
        c = get_object_or_404(Cart, id=cart_id)
        c.delete()
        messages.success(request, "Artice supprimé du panier !")
    return redirect("store:cart")


@login_required
def plus_cart(request, cart_id):
    if request.method == "GET":
        cp = get_object_or_404(Cart, id=cart_id)
        cp.quantity += 1
        cp.save()
    return redirect("store:cart")


@login_required
def minus_cart(request, cart_id):
    if request.method == "GET":
        cp = get_object_or_404(Cart, id=cart_id)

        # supprimer un produit du panier si decrementation et un seul
        if cp.quantity == 1:
            cp.delete()
        # decrementer son nombre sinon
        else:
            cp.quantity -= 1
            cp.save()
    return redirect("store:cart")


@login_required
def checkout(request):
    user = request.user
    address_id = request.GET.get("address")

    address = get_object_or_404(Address, id=address_id)
    cart = Cart.objects.filter(user=user)
    # proceed
    for c in cart:
        Order(user=user, address=address, product=c.product, quantity=c.quantity).save()
        c.delete()
    return redirect("store:orders")


@login_required
def orders(request):
    all_orders = Order.objects.filter(user=request.user).order_by("-ordered_date")
    return render(request, "store/orders.html", {"orders": all_orders})


def dashboard(
    request,
):
    return render(request, "admin/home.html")


def dashboard_categories(request):
    context = {"categories": Category.objects.all(), "form": CategoryForm()}

    return render(request, "admin/categories/list.html", context=context)


def dashboard_categorie_creation(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Catégorie bien enrgistrée")
        else:
            messages.error(request, f"{form.errors}")
    return redirect("store:dashboard-categories")


def dashboard_categorie_suppression(request, pk):
    categorie = get_object_or_404(Category, id=pk)
    categorie.delete()
    messages.success(request, "Catégorie supprimée !")
    return redirect("store:dashboard-categories")


def dashboard_categorie_modification(request, pk):
    categorie = get_object_or_404(Category, id=pk)
    form = CategoryForm(instance=categorie)
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, " Catégorie modifiée !")
            return redirect("store:dashboard-categories")
        else:
            messages.error(request, f"{form.errors}")
    return render(
        request,
        "admin/categories/modifcation.html",
        context={"form": form, "categorie": categorie},
    )


def dashboard_produits(request):
    return render(
        request,
        "admin/produits/list.html",
        context={"produits": Product.objects.all(), "form": ProductForm()},
    )


def dashboard_produit_suppression(request, pk):
    produit = get_object_or_404(Product, id=pk)
    produit.delete()
    messages.success(request, "Produit supprimé !")
    return redirect("store:dashboard-produits")


def dashboard_produit_modification(request, pk):
    produit = get_object_or_404(Product, id=pk)
    form = ProductForm(instance=produit)
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, " Produit modifiée !")
            return redirect("store:dashboard-produits")
        else:
            messages.error(request, f"{form.errors}")
    return render(
        request,
        "admin/produits/modification.html",
        context={"form": form, "produit": produit},
    )


def dashboard_produit_creation(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Produit bien enrgistré !")
        else:
            messages.error(request, f"{form.errors}")
    return redirect("store:dashboard-produits")


def dashboard_commandes(request):
    return render(request, "admin/commandes/list.html", {"orders": Order.objects.all()})


def search_view(request):

    if request.method == "POST":

        if request.POST.get("keyword") != "":

            # On vérifie si le mot clé de la recherche est une chaine de caractère vide

            # Recherche du mot clé dans le nom des produits ou dans la description du produit

            produits = Product.objects.filter(
                Q(title__icontains=request.POST.get("keyword"))
                | Q(short_description__icontains=request.POST.get("keyword"))
                | Q(category__title__icontains=request.POST.get("keyword")),
                is_active=True,
            )

            categories = Category.objects.filter(is_active=True)
            context = {
                "products": produits,
                "categories": categories,
            }
            return render(request, "partials/results.html", context)
    return htmx_redirect("store:home")

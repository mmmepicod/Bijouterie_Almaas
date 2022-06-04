from store.forms import (
    LoginForm,
    PasswordChangeForm,
    PasswordResetForm,
    SetPasswordForm,
)
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

# Routage

app_name = "store"

urlpatterns = [
    # Route page d'accueil
    path("", views.home, name="home"),
    # Routes pour les paiements et le panier
    path("add-to-cart/", views.add_to_cart, name="add-to-cart"),
    path("remove-cart/<int:cart_id>/", views.remove_cart, name="remove-cart"),
    path("plus-cart/<int:cart_id>/", views.plus_cart, name="plus-cart"),
    path("minus-cart/<int:cart_id>/", views.minus_cart, name="minus-cart"),
    path("cart/", views.cart, name="cart"),
    path("checkout/", views.checkout, name="checkout"),
    path("orders/", views.orders, name="orders"),
    # Routes pour les produits
    path("product/<slug:slug>/", views.detail, name="product-detail"),
    path("categories/", views.all_categories, name="all-categories"),
    path("<slug:slug>/", views.category_products, name="category-products"),
    # Routes d'authentification
    path("accounts/register/", views.registration_view, name="register"),
    path(
        "accounts/login/",
        auth_views.LoginView.as_view(
            template_name="account/login.html", authentication_form=LoginForm
        ),
        name="login",
    ),
    path("accounts/profile/", views.profile, name="profile"),
    path("accounts/add-address/", views.AddressView.as_view(), name="add-address"),
    path(
        "accounts/remove-address/<int:id>/", views.remove_address, name="remove-address"
    ),
    path(
        "accounts/logout/",
        auth_views.LogoutView.as_view(next_page="store:login"),
        name="logout",
    ),
    path(
        "accounts/password-change/",
        auth_views.PasswordChangeView.as_view(
            template_name="account/password_change.html",
            form_class=PasswordChangeForm,
            success_url="/accounts/password-change-done/",
        ),
        name="password-change",
    ),
    path(
        "accounts/password-change-done/",
        auth_views.PasswordChangeDoneView.as_view(
            template_name="account/password_change_done.html"
        ),
        name="password-change-done",
    ),
    path(
        "accounts/password-reset/",
        auth_views.PasswordResetView.as_view(
            template_name="account/password_reset.html",
            form_class=PasswordResetForm,
            success_url="/accounts/password-reset/done/",
        ),
        name="password-reset",
    ),
    path(
        "accounts/password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="account/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "accounts/password-reset-confirm/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="account/password_reset_confirm.html",
            form_class=SetPasswordForm,
            success_url="/accounts/password-reset-complete/",
        ),
        name="password_reset_confirm",
    ),
    path(
        "accounts/password-reset-complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="account/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
    # path("product/test/", views.test, name="test"),
    # ADMIN DASHBOARD
    path("dashboard", views.dashboard, name="dashboard"),
    path(
        "dashboard/categories", views.dashboard_categories, name="dashboard-categories"
    ),
    path(
        "dashboard/categories/creation",
        views.dashboard_categorie_creation,
        name="dashboard-categorie-creation",
    ),
    path(
        "dashboard/categorie/<pk>/suppression/",
        views.dashboard_categorie_suppression,
        name="dashboard-categorie-suppression",
    ),
    path(
        "dashboard/categorie/modification/<pk>/",
        views.dashboard_categorie_modification,
        name="dashboard-categorie-modification",
    ),
    path("dashboard/produits", views.dashboard_produits, name="dashboard-produits"),
    path(
        "dashboard/produits/suppression/<pk>/",
        views.dashboard_produit_suppression,
        name="dashboard-produit-suppression",
    ),
    path(
        "dashboard/produits/modification/<pk>/",
        views.dashboard_produit_modification,
        name="dashboard-produit-modification",
    ),
    path(
        "dashboard/produits/creation/",
        views.dashboard_produit_creation,
        name="dashboard-produit-creation",
    ),
    path("dashboard/commandes", views.dashboard_commandes, name="dashboard-commandes"),
    path("search", views.search_view, name="search"),
]

"""Formularios de la aplicación inventory."""
from django import forms

from .models import Product


class ProductForm(forms.ModelForm):
    """Formulario de creación/edición de productos con validación."""

    class Meta:
        model = Product
        fields = ["name", "sku", "description", "price", "stock_quantity"]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-input", "placeholder": "Nombre del producto"}
            ),
            "sku": forms.TextInput(
                attrs={"class": "form-input", "placeholder": "Código único (SKU)"}
            ),
            "description": forms.Textarea(
                attrs={"class": "form-input", "rows": 3}
            ),
            "price": forms.NumberInput(
                attrs={"class": "form-input", "step": "0.01", "min": "0"}
            ),
            "stock_quantity": forms.NumberInput(
                attrs={"class": "form-input", "min": "0"}
            ),
        }

    def clean_price(self):
        price = self.cleaned_data["price"]
        if price < 0:
            raise forms.ValidationError("El precio no puede ser negativo.")
        return price

    def clean_stock_quantity(self):
        quantity = self.cleaned_data["stock_quantity"]
        if quantity < 0:
            raise forms.ValidationError("La cantidad no puede ser negativa.")
        return quantity

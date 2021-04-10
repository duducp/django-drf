from django.contrib import admin
from django.forms import forms
from django.forms.models import ModelForm

from project.apps.favorites.models import Favorite
from project.apps.helpers.backends.products.exceptions import (
    ProductException,
    ProductNotFoundException
)
from project.apps.helpers.extensions.challenge.products.backend import (
    ProductBackend
)


class FavoriteForm(ModelForm):
    class Meta:
        model = Favorite
        fields = '__all__'

    def clean_product_id(self):
        data = self.cleaned_data['product_id']

        try:
            ProductBackend().get_product(product_id=str(data))
            return data
        except ProductNotFoundException:
            raise forms.ValidationError(
                'Product does not exist'
            )
        except ProductException:
            raise forms.ValidationError(
                'Errors occurred when validating product'
            )


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    form = FavoriteForm

    list_display = [
        'id',
        'product_id',
        'created_at',
        'updated_at',
    ]

    search_fields = [
        'id',
        'product_id',
        'client__id',
        'client__name'
    ]

    list_per_page = 30
    list_max_show_all = 30

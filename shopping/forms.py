from decimal import Decimal

from django import forms

from . import models


class ShoppingListForm(forms.ModelForm):
    class Meta:
        model = models.ShoppingList
        fields = ['name', 'is_active']
        widgets = {'name': forms.TextInput(attrs={'class': 'form-control'}), 'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'})}

    def clean_name(self):
        return self.cleaned_data['name'].strip()


class ShoppingItemForm(forms.ModelForm):
    class Meta:
        model = models.ShoppingItem
        fields = ['name', 'is_active']
        widgets = {'name': forms.TextInput(attrs={'class': 'form-control'}), 'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'})}

    def clean_name(self):
        name = self.cleaned_data['name'].strip()
        duplicates = models.ShoppingItem.objects.filter(shopping_list=self.instance.shopping_list, name__iexact=name).exclude(pk=self.instance.pk)
        if duplicates.exists():
            raise forms.ValidationError('Este item já está cadastrado nesta lista. Você pode editar ou reativar o cadastro existente.')
        return name


class ChooseListForm(forms.Form):
    shopping_list = forms.ModelChoiceField(queryset=models.ShoppingList.objects.none(), label='Lista de compras', empty_label='Selecione uma lista', widget=forms.Select(attrs={'class': 'form-select'}))

    def __init__(self, *args, owner, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['shopping_list'].queryset = models.ShoppingList.objects.filter(owner=owner, is_active=True)


class ItemSelectionForm(forms.Form):
    items = forms.ModelMultipleChoiceField(queryset=models.ShoppingItem.objects.none(), label='Itens que você vai comprar', widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}), error_messages={'required': 'Selecione pelo menos um item.'})

    def __init__(self, *args, shopping_list, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['items'].queryset = shopping_list.items.filter(is_active=True)


class QuantityForm(forms.Form):
    def __init__(self, *args, items, **kwargs):
        super().__init__(*args, **kwargs)
        for item in items:
            self.fields[f'quantity_{item.pk}'] = forms.DecimalField(
                label=item.name, required=False, min_value=Decimal('0'), max_digits=9, decimal_places=3,
                localize=True, initial=item.quantity,
                widget=forms.TextInput(attrs={'class': 'form-control', 'inputmode': 'decimal', 'placeholder': 'Quantidade', 'autocomplete': 'off'}),
            )


class FinishForm(forms.Form):
    total = forms.DecimalField(
        label='Valor total da compra (R$)', min_value=Decimal('0'), max_digits=12, decimal_places=2, localize=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'inputmode': 'decimal', 'placeholder': 'Ex.: 150,90', 'autocomplete': 'off'}),
    )

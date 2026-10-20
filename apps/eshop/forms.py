from django import forms

from eshop.models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'category', 'tags', 'text', 'price', 'image']
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': "Максимальная длина 200 символов"
            }),
            'text': forms.Textarea(attrs={
                'rows': 3,
                'cols': 20
            }),
            'price': forms.NumberInput(attrs={
                'placeholder': "0.00",
                'step': "0.01"
            }),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}) 
        }
        labels = {
        'title': 'Название товара:',
        'text': 'Описание товара:',
        'category': 'Категория:',
        'tags': 'Теги:',
        'price': 'Цена',
        'image': 'Картинка товара'
        }
        help_texts = {
        'category': "- можно выбрать только одну категорию",
        'tags': '- можно выбрать несколько тегов',
        }


    def clean_title(self):
        title = self.cleaned_data['title'].strip()
        if len(title) < 10:
            raise forms.ValidationError("Название не должно быть короче 10 символов.")
        return title

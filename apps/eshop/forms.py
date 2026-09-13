from django import forms

from eshop.models import Product

class PostForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'text', 'price']
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
            })  
        }
        labels = {
        'title': 'Название товара:',
        'text': 'Описание товара:',
        'price': 'Цена'
        }


    def clean_title(self):
        title = self.cleaned_data['title'].strip()
        if len(title) < 10:
            raise forms.ValidationError("Название не должно быть короче 10 символов.")
        return title

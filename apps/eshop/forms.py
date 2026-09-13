from django import forms

class PostForm(forms.Form):
    title = forms.CharField(
        max_length=200, 
        label="Название товара:", 
        widget=forms.TextInput(attrs={
            'placeholder': "Максимальная длина 200 символов"
        })  # Можно передавать другие атрибуты, например, "class": 'title-input'
    )  # Можно указать: required=False

    text = forms.CharField(
        label="Описание товара:", 
        widget=forms.Textarea(attrs={
            'rows': 3, 
            'cols': 20
        })
    )

    price = forms.DecimalField(
        label="Цена:",
        max_digits=10,       # Максимальное количество цифр всего (например, до 99999999.99)
        decimal_places=2,    # Количество знаков после запятой (копейки)
        min_value=0.00,      # Защита от ввода отрицательной цены
        widget=forms.NumberInput(attrs={
            'placeholder': '0.00',
            'step': '0.01'   # Шаг изменения цены в браузере
        })
    )


    def clean_title(self):
        title = self.cleaned_data['title'].strip()
        if len(title) < 10:
            raise forms.ValidationError("Название не должно быть короче 10 символов.")
        return title

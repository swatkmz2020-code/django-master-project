from django import forms

from eshop.models import Product

class PostForm(forms.ModelForm):
    tags_input = forms.CharField(
    required=False,
    widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите теги через запятую'
    }),
    label="Теги",
    help_text="- можно указать несколько тегов",
    )
    class Meta:
        model = Product
        fields = ['title', 'category', 'text', 'tags_input', 'price', 'image']
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
            'image': forms.FileInput(attrs={'class': 'form-control'}), 
        }
        labels = {
        'title': 'Название товара:',
        'text': 'Описание товара:',
        'category': 'Категория:',
        'price': 'Цена',
        'image': 'Картинка товара',
        }
        help_texts = {
        'category': "- можно выбрать только одну категорию"
        }


    def clean_title(self):
        title = self.cleaned_data['title'].strip()
        if len(title) < 10:
            raise forms.ValidationError("Название не должно быть короче 10 символов.")
        return title
    
    def clean_tags_input(self):
        # Если tags_input равен None, берем пустую строку ""
        tags_data = self.cleaned_data.get('tags_input') or ""
        
        tag_names = [
            tag_name.strip().lower()
            for tag_name in tags_data.split(',')
            if tag_name.strip()
        ]
        return tag_names


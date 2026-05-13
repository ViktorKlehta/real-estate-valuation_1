from django.forms import ModelForm, TextInput, NumberInput, Select, HiddenInput
from .models import RealEstate


class RealEstateForm(ModelForm):
    class Meta:
        model = RealEstate
        fields = '__all__'
        widgets = {
            # Категориальные поля
            'type': Select(attrs={
                'class': 'form-control form-control-custom select-custom',
                'placeholder': 'Выберите тип недвижимости'
            }),
            'room_count': Select(attrs={
                'class': 'form-control form-control-custom select-custom',
                'placeholder': 'Выберите количество комнат'
            }),
            'house_type': Select(attrs={
                'class': 'form-control form-control-custom select-custom',
                'placeholder': 'Выберите тип дома'
            }),
            'sale_type': Select(attrs={
                'class': 'form-control form-control-custom select-custom',
                'placeholder': 'Выберите тип продажи'
            }),
            'street': Select(attrs={
                'class': 'form-control form-control-custom select-custom',
                'placeholder': 'Выберите улицу'
            }),
            'district': Select(attrs={
                'class': 'form-control form-control-custom select-custom',
                'placeholder': 'Выберите район'
            }),

            # Числовые поля
            'total_area': NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите общую площадь (м²)',
                'step': '0.01',
                'min': '1'
            }),
            'floor': NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите этаж',
                'min': '1'
            }),
            'total_floors': NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите этажность дома',
                'min': '1'
            }),
            'latitude': HiddenInput(),
            'longitude': HiddenInput(),
            'distance_to_center': NumberInput(attrs={
                'readonly': 'readonly',
                'class': 'form-control'
            })
        }
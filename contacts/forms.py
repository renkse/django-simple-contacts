# -*- coding: utf8 -*-
__author__ = 'renkse'
from django import forms
from models import FeedbackMessage
from captcha.fields import CaptchaField
from autotech.utils import rus_verification, phone_verification


class FeedbackForm(forms.ModelForm):
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Ваш e-mail*'}),
                             error_messages={'invalid': 'Введите корректный e-mail.'})

    class Meta:
        model = FeedbackMessage
        exclude = (
            'sended_at',
        )
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ваше имя*'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Ваш номер телефона'}),
            # 'branch': forms.Select(attrs={'placeholder': 'Филиал'}),
            'message': forms.Textarea(attrs={'placeholder': 'Ваше сообщение*'})
        }

    def clean(self):
        cleaned_data = super(FeedbackForm, self).clean()
        if not self._errors:
            name = cleaned_data.get('name')
            phone = cleaned_data.get('phone')
            rus_verification(self, name, 'name')
            if phone != '' and phone is not None:
                phone_verification(self, phone, 'phone')
        return cleaned_data


# from django import forms
# from django.forms.models import BaseInlineFormSet
#
#
# class AtLeastOneRequiredInlineFormSet(BaseInlineFormSet):
#
#     def clean(self):
#         """Check that at least one service has been entered."""
#         super(AtLeastOneRequiredInlineFormSet, self).clean()
#         if any(self.errors):
#             return
#         if not any(cleaned_data and not cleaned_data.get('DELETE', False) for cleaned_data in self.cleaned_data):
#             raise forms.ValidationError('Добавьте хотя бы одну фотографию')
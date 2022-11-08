from django import forms

class OrderForm(forms.Form):
    order_csv = forms.FileField(label='order_csv', required=True)
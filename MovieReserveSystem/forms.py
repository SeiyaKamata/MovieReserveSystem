from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(
        label='User Name', 
        max_length=128, 
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'input-user-id',
            }
        )
    )
    password = forms.CharField(
        label='password', 
        max_length=128, 
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'input-password',
                'type':'password',
            }
        )
    )

class SignUpForm(forms.Form):
    username = forms.CharField(
        label='username', 
        max_length=128, 
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'input-username',
            }
        )
    )
    password = forms.CharField(
        label='password', 
        max_length=128, 
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'id': 'input-password',
                'type':'password',
            }
        )
    )


class ReserveForm(forms.Form):
    schedule = forms.CharField(
        label='schedule', 
        max_length=128, 
        widget=forms.TextInput(
            attrs={
                'type': 'hidden',
                'id': 'input-schedule',
            }
        )
    )
    seat = forms.CharField(
        label='seat', 
        widget=forms.TextInput(
            attrs={
                'type': 'hidden',
                'id': 'input-seat',
            }
        )
    )
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import UserCred, Staffs, Roles, Residents
from django.core.validators import RegexValidator

phone_regex = RegexValidator(
    regex=r'^\+?1?\d{9,15}$',
    message="Phone number must be entered in the format: '+234.....'. Up to 15 digits allowed."
)

class StaffRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    firstname = forms.CharField(max_length=150, required=False)
    lastname = forms.CharField(max_length=150, required=False)
    phone_number = forms.CharField(max_length=17, validators=[phone_regex], required=False)

    class Meta:
        model = UserCred
        fields = ('username', 'email', 'firstname', 'lastname', 'phone_number', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
            # Create the Staff instance without setting the role
            # Role will be assigned later by an admin
            Staffs.objects.create(user=user)
        return user
class StaffLoginForm(AuthenticationForm):
    username = forms.EmailField(label='Email', max_length=254)  # Changed to EmailField

class ResidentRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    firstname = forms.CharField(max_length=150, required=False)
    lastname = forms.CharField(max_length=150, required=False)
    phone_number = forms.CharField(max_length=17, validators=[phone_regex], required=False)
    guardian_phone_number = forms.CharField(max_length=17, validators=[phone_regex], required=False)

    class Meta:
        model = UserCred
        fields = ('username', 'email', 'firstname', 'lastname', 'phone_number')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
            # Create the Residents instance
            Residents.objects.create(
                user=user,
                guardian_phone_number=self.cleaned_data['guardian_phone_number']
            )
        return user
    
class ResidentLoginForm(AuthenticationForm):
    username = forms.EmailField(label='Email', max_length=254)  # Changed to EmailField
    room_number = forms.CharField(label='Room Number', max_length=10)


class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label='Email')
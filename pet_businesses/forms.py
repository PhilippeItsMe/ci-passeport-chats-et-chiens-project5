from django import forms
from .models import PetBusiness, Comment, CustomUser
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError

#----------------------- Form to manage pet businesses -----------------------#

class PetBusinessForm(forms.ModelForm):
    """
    Form for creating and updating PetBusiness instances.
    """
    class Meta:
        model = PetBusiness
        fields = [
            'firm',
            'slug',
            'street',
            'number',
            'npa',
            'locality',
            'phone',
            'email',
            'website',
            'featured_image',
            'linkedin',
            'facebook',
            'instagram',
            'tiktok',
            'business_pet_type',
            'business_service_type',
            'description',
        ]
        widgets = {
            'firm': forms.TextInput(attrs={'class': 'form-control',
                                           'id': 'firm-input'}),
            'slug': forms.TextInput(attrs={'class': 'form-control',
                                           'id': 'slug-input'}),
            'street': forms.TextInput(attrs={'class': 'form-control'}),
            'number': forms.TextInput(attrs={'class': 'form-control'}),
            'npa': forms.TextInput(attrs={'class': 'form-control'}),
            'locality': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'website': forms.URLInput(attrs={'class': 'form-control'}),
            'featured_image': forms.ClearableFileInput(attrs={'class':
                                                              'form-control'}),
            'linkedin': forms.URLInput(attrs={'class': 'form-control'}),
            'facebook': forms.URLInput(attrs={'class': 'form-control'}),
            'instagram': forms.URLInput(attrs={'class': 'form-control'}),
            'tiktok': forms.URLInput(attrs={'class': 'form-control'}),
            'business_pet_type': forms.CheckboxSelectMultiple(),
            'business_service_type': forms.CheckboxSelectMultiple(),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }
        labels = {
            'firm': 'Votre entreprise ',
            'slug': 'Url de votre page (remplie automatiquement) ',
            'street': 'Rue ',
            'number': 'N° ',
            'npa': 'Code postale ',
            'locality': 'Localité ',
            'phone': 'Téléphone ',
            'email': 'Email ',
            'website': 'Website (https://...) ',
            'featured_image': "Illustration ",
            'linkedin': 'Page LinkedIn (https://...) ',
            'facebook': 'Page Facebook (https://...) ',
            'instagram': 'Page Instagram (https://...) ',
            'tiktok': 'Page TikTok (https://...) ',
            'business_pet_type': 'Animaux servis ',
            'business_service_type': 'Types de services offerts ',
            'description': 'Description ',
        }


#-------------------------- Form to manage comments --------------------------#

class CommentForm(forms.ModelForm):
    """
    Form to enter comments.
    """
    class Meta:
        model = Comment
        fields = ('content',)
        widgets = {
            'content': forms.Textarea(attrs={'id': 'id_body'}),
        }
        labels = {
            'content': 'Contenu'
        }


#----------------------- Form to manage subscriptions -----------------------#

class UserRegistrationForm(UserCreationForm):
    """
    User registration form extending Django's built-in UserCreationForm.
    """
    first_name = forms.CharField(max_length=30, required=True, label="Prénom")
    last_name = forms.CharField(max_length=30, required=True, label="Nom")
    email = forms.EmailField(required=True, label="Email")
    mobile = forms.CharField(max_length=15, required=True, label="Téléphone")

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'mobile', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.mobile = self.cleaned_data['mobile']
        if commit:
            user.save()
        return user


class CustomSignupForm(forms.Form):
    """
    Custom signup form to register users by group.
    """
    group_choices = [
        ('Pet Owners', 'Pet Owners'),
        ('Business Owners', 'Business Owners'),
    ]
    group = forms.ChoiceField(choices=group_choices, label="Signez en tant que : ")

    def signup(self, request, user):
        group_name = self.cleaned_data['group']
        group = Group.objects.filter(name=group_name).first()
        
        if not group:
            raise ValidationError(f"Le groupe '{group_name}' n'existe pas.")

        user.groups.add(group)
        user.save()
        return user

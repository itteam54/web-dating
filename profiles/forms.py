from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
from .models import Profile, ProfileImage
from chat.models import Messages
from dating_app import settings

class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(label="Логин", widget=forms.TextInput(attrs={'maxlength':'12'}))
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Подтверждение пароля", widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True
        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def cleaned_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if User.objects.filter(email=email).exclude(username=username):
            raise forms.ValidationError(u'Данный e-mail существует. Попробуйте другой.')
        return email

    def cleaned_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if not password1 or password2:
            raise ValidationError("Поле должно быть заполнено!")
        if password1 != password2:
            raise ValidationError("Пароли не совпадают. Попробуйте снова.")
        return password2

class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class ProfileForm(forms.ModelForm):
    CHILDREN_CHOICES = (
        (True, "Yes"),
        (False, "No")
        )

    location = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'id':'autocomplete'}), required=True)
    bio = forms.CharField(widget=forms.Textarea(attrs={'class': 'bio-field', 'maxlength': '200'}), required=True)
    birth_date = forms.DateTimeField(input_formats=settings.DATE_INPUT_FORMATS)
    children = forms.ChoiceField(choices = CHILDREN_CHOICES, initial='', widget=forms.Select(), required=True)
    height = forms.CharField(max_length = 3, initial='150', widget=forms.TextInput(attrs={'id':'autocomplete'}), required=True)

    class Meta:
        model = Profile
        fields = ( 'bio', 'gender', 'hair_colour', 'hair_length', 'body_type', 'ethnicity', 'relationship_status', 'looking_for', 'education', 'height', 'children', 'location', 'birth_date')
        widgets = {
            'date' : forms.DateInput(attrs={'type':'date'})
        }

class ProfileImageForm(forms.ModelForm):
    image = forms.ImageField(label='', required=False, error_messages = {'invalid':"Image files only"}, widget=forms.FileInput(attrs = {'class': "profile-photo-input"}))

    class Meta:
        model = ProfileImage
        fields = ('image', )

class EditProfileForm(UserChangeForm):
    password = None
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user',None)
        super(EditProfileForm, self).__init__(*args, **kwargs)
        for fieldname in ['confirm_password', 'username']:
            self.fields[fieldname].help_text = None

    def clean_confirm_password(self):
        password = self.cleaned_data['confirm_password']
        if not self.user.check_password(password):
            raise forms.ValidationError("Введен неверный пароль")
        return password

    class Meta:
        model = User
        fields = ('email', 'username')

class MessagesForm(forms.ModelForm):
    class Meta:
        model = Messages
        fields = ('message_content', )

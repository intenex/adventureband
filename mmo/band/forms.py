from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.template import Context, loader
from django import forms
from django.utils.translation import ugettext_lazy as _
from band.models import *

# UPDATE - Successfully implemented case-insensitive usernames simply using 'username.lower()'. Haven't found any bugs yet, think it's working well.
# Note - implement case-insensitive username logins in the future. Remember to prevent case-sensitive registration when you do this as well by using 'to_python' perhaps
# http://blog.shopfiber.com/?p=220
# http://djangosnippets.org/snippets/1368/
# http://stackoverflow.com/questions/2350681/django-lowercasecharfield

class UserRegistrationForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given username and password.
    """
    username = forms.RegexField(label=_("Username"), max_length=30, regex=r'^[\w.@+-]+$',
        help_text = _("30 characters or less. Letters, digits and @-_+. only."),
        error_messages = {'invalid': _("This value may contain only letters, numbers and @-_+. characters.")})
    email = forms.EmailField(label=_("Email"),
        error_messages = {'invalid': _("This is not a valid email address.")})
    password1 = forms.CharField(label=_("Password"), widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password confirmation"), widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("username",)

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            User.objects.get(username=username.lower()) # since all usernames are lowercase, check if the lowercase version of the entered username is taken
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(_("A user with that username already exists."))

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1", "")
        password2 = self.cleaned_data["password2"]
        if password1 != password2:
            raise forms.ValidationError(_("The two password fields didn't match."))
        return password2

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        username = self.cleaned_data["username"]
        user.username = username.lower() # nicely done - this works to ensure that all usernames are stored in lowercase
        user.email = self.cleaned_data["email"]
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UserLogin(forms.Form):
    username = forms.RegexField(label=_("Username"), max_length=30, regex=r'^[\w.@+-]+$',
        error_messages = {'invalid': _("This value may contain only letters, numbers and @-_+. characters.")})
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput)

class CreateCharacter(forms.ModelForm):

    # defining 'name' here overrides the name field from the model referenced in 'class Meta' below
    name = forms.RegexField(label=_("Name"), max_length=20, regex=r'^[\w.@+-]+$',
        error_messages = {'invalid': _("This value may contain only letters, numbers, and @-_+. characters.")})

    class Meta:
        model = Character
        fields = ('name', 'sex', 'race', 'char_class')

    def clean_name(self):
        name = self.cleaned_data["name"] # Note - this doesn't need the 'name' defined above in the class - it can run this check just using the 'class Meta' 'fields' 'name' taken from 'models.py'
        try:
            Character.objects.get(name_lower=name.lower())
        except Character.DoesNotExist:
            return name
        raise forms.ValidationError(_("A character with that name already exists."))

class SetAttributes(forms.ModelForm):

    strength = forms.IntegerField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    intelligence = forms.IntegerField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    wisdom = forms.IntegerField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    dexterity = forms.IntegerField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    constitution = forms.IntegerField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    charisma = forms.IntegerField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    max_hp = forms.IntegerField(label=_("HP"), widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    class Meta: # very unnecessary I'm pretty sure :D
        model = Character
        fields = ('strength', 'intelligence', 'wisdom', 'dexterity', 'constitution', 'charisma')

    # this makes sure no one tampered with the javascript and manually added crazy stats
    def clean_max_hp(self): # set this to the last attribute to be cleaned or else an error will be thrown since not all of the self.cleaned_data[]'s will exist yet
        strength = self.cleaned_data["strength"]
        intelligence = self.cleaned_data["intelligence"]
        wisdom = self.cleaned_data["wisdom"]
        dexterity = self.cleaned_data["dexterity"]
        constitution = self.cleaned_data["constitution"]
        charisma = self.cleaned_data["charisma"]
        max_hp = self.cleaned_data["max_hp"]
        if strength + intelligence + wisdom + dexterity + constitution + charisma <= 69:
            pass
        else:
            raise forms.ValidationError(_("Well that didn't work."))
        if strength <= 20 and intelligence <= 20 and wisdom <= 20 and dexterity <= 20 and constitution <= 20 and charisma <= 20:
            pass
        else:
            raise forms.ValidationError(_("Well that didn't work."))
        if max_hp == constitution / 2:
            return max_hp
        else:
            raise forms.ValidationError(_("Well that didn't work."))
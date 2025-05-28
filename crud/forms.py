from django import forms
from .models import Users, Genders

class UserRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Users
        fields = ['full_name', 'gender', 'birth_date', 'address', 'contact_number', 'email', 'username']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if Users.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists.")
        return username

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 != password2:
            self.add_error('password1', "Passwords do not match.")
            self.add_error('password2', "Passwords do not match.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        # Manually hash the password
        import hashlib
        user.password = hashlib.sha256(self.cleaned_data["password1"].encode()).hexdigest()
        if commit:
            user.save()
        return user

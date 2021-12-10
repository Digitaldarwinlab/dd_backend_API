from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from Auth.models import User

class CustomUserCreationsForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = User
        fields = ('email',)

    def save(self,commit=True):
        user = super(CustomUserCreationsForm,self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user        

class CustomuserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email',)        
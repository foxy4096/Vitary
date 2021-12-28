from django import forms

from .models import DevProfile

class DevProfileCreationForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=30, required=True, help_text='Required.')
    last_name = forms.CharField(
        max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, required=True,
                             help_text='Required. Inform a valid email address.')
    location = forms.CharField(
        max_length=30, required=False, help_text='Optional.')

    class Meta:
        model = DevProfile
        fields = ['first_name', 'last_name', 'email', 'location']

    def save(self, commit=True):
        devprofile = super().save(commit=False)
        devprofile.first_name = self.cleaned_data['first_name']
        devprofile.last_name = self.cleaned_data['last_name']
        devprofile.email = self.cleaned_data['email']
        devprofile.location = self.cleaned_data['location']

        if commit:
            devprofile.save()

        return devprofile


class DevProfileForm(forms.ModelForm):
    class Meta:
        model = DevProfile
        fields = ['first_name', 'last_name', 'email', 'location', 'bio',
                  'github_handle', 'twitter_handle', 'linkedin_handle', 'website']
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'input', 'style': '''width: 100%;
                                                                        height: 150px;
                                                                        padding: 12px 20px;
                                                                        box-sizing: border-box;
                                                                        border: px solid rgb(0, 0, 0);
                                                                        background-color: #ffffff;
                                                                        color: #b9b9b9;
                                                                        background-color : #4a4a4a; 
                                                                        resize: both'''}),
            'website': forms.URLInput(attrs={'class': 'input', 'style': '''width: 100%;
                                                                            background-color: #ffffff;
                                                                            color: #b9b9b9;
                                                                            background-color : #4a4a4a;'''}),
        }

    def save(self, commit=True):
        devprofile = super().save(commit=False)
        devprofile.first_name = self.cleaned_data['first_name']
        devprofile.last_name = self.cleaned_data['last_name']
        devprofile.email = self.cleaned_data['email']
        devprofile.location = self.cleaned_data['location']
        devprofile.bio = self.cleaned_data['bio']
        devprofile.github_handle = self.cleaned_data['github_handle']
        devprofile.twitter_handle = self.cleaned_data['twitter_handle']
        devprofile.linkedin_handle = self.cleaned_data['linkedin_handle']
        devprofile.website = self.cleaned_data['website']

        if commit:
            devprofile.save()

        return devprofile

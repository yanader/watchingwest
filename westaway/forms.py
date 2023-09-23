from django import forms
from .models import Image, Entry, Competition, Opponent

class EntryUploadForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete':'new-password'}))
    location = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'off'}))

    class Meta:
        model = Entry
        fields = ['date', 'opponent',  'home', 'location', 'title', 'text_entry', 'competition']
    
    title = forms.CharField(max_length=64)
    photo = forms.ImageField()

    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    text_entry = forms.CharField(widget=forms.Textarea)

    home = forms.BooleanField(initial=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Populate 'competition' dropdown in alphabetical order
        self.fields['competition'].queryset = Competition.objects.order_by('competition')
        
        # Populate 'opponent' dropdown in alphabetical order
        self.fields['opponent'].queryset = Opponent.objects.order_by('name')

    def save(self, commit=True):
        image = Image(title=self.cleaned_data['title'], photo=self.cleaned_data['photo'])
        image.save()

        entry = Entry(
            opponent=self.cleaned_data['opponent'],
            date=self.cleaned_data['date'],
            location=self.cleaned_data['location'],
            text_entry=self.cleaned_data['text_entry'],
            competition=self.cleaned_data['competition'],
            image=image,
            home=self.cleaned_data['home']
        )

        if commit:
            entry.save()
        
        return entry
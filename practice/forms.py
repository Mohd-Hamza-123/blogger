from django import forms


class DemoForm(forms.Form):
    title = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder' : "Enter title",'class':'title_class_hai'})
        )
    content = forms.CharField(widget=forms.Textarea(attrs={'placeholder':'enter content'}))
    is_published = forms.BooleanField(required=False)
    password = forms.CharField(widget=forms.PasswordInput())
    email = forms.EmailField()
    dob = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    arrived_at = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time'})
    )
    event_datetime = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'})
    )

    gender = forms.ChoiceField(
        widget=forms.RadioSelect(), 
        choices=[('M', 'Male'), ('F', 'Female')]
        )
    skills = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(), 
        choices=[('html', 'HTML(Hyper text markup language)'), ('CSS', 'CSS'), ('JavaScript', 'JavaScript'), ('Python', 'Python'), ('Django', 'Django')]
        )
    
    interest = forms.MultipleChoiceField(choices=[("cricket","Cricket"),("soccer","football"),("basketball","Basketball")])
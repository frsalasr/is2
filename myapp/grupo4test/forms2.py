from django import forms

class PersonalDataForm(forms.Form):
   first_name = forms.CharField(required=True, max_length=255)
   last_name = forms.CharField(required=True, max_length=255)
   email = forms.EmailField(required=True)
   phone = forms.CharField(required=True, max_length=200)
   address = forms.CharField(max_length=1000, widget=forms.Textarea())
   more_info = forms.CharField(max_length=1000, widget=forms.Textarea())
   color = forms.TypedChoiceField(
       label="Choose color",
       choices=((0, "Red"), (1, "Blue"), (2, "Green")),
       coerce=lambda x: bool(int(x)),
       widget=forms.RadioSelect,
       initial='0',
       required=True)

   def __init__(self, *args, **kwargs):
       super(PersonalDataForm, self).__init__(*args, **kwargs)
       self.helper = FormHelper()
       self.helper.form_class = 'form-horizontal'
       self.helper.layout = Layout(
           Fieldset('Name',
                    Field('first_name', placeholder='Your first name',
                          css_class="some-class"),
                    Div('last_name', title="Your last name"),),
           Fieldset('Contact data', 'email', 'phone', style="color: brown;"),
           InlineRadios('color'),
           TabHolder(Tab('Address', 'address'),
                     Tab('More Info', 'more_info')))
from django import forms

class FullForm(forms.Form):

	# ociones para elegir en ChoiseField cuanto_gana
	options=(
		('si', 'si'),
		('no', 'no'),
		('tal vez', 'tal vez'),
		)
	#cuanto_gana = forms.ChoiceField(choices=options, initial='no')
	

	run = forms.IntegerField()
	nombre_empresa = forms.CharField(max_length=20)
	nombre = forms.CharField(max_length=20)
	apellido = forms.CharField(max_length=20)
	email = forms.EmailField()
	url = forms.URLField(required = False)

	hid_field = forms.IntegerField(required = False)
	var1 = forms.IntegerField()
	var2 = forms.IntegerField()
	var3 = forms.IntegerField()
from django import forms
from .models import Cliente, Coche, Servicio, CocheServicio

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'

class CocheForm(forms.ModelForm):
    class Meta:
        model = Coche
        fields = '__all__'

class ServicioForm(forms.ModelForm):
    class Meta:
        model = Servicio
        fields = '__all__'

class CocheServicioForm(forms.ModelForm):
    class Meta:
        model = CocheServicio
        fields = '__all__'

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'telefono', 'email']
class CocheForm(forms.ModelForm):
    class Meta:
        model = Coche
        fields = ['cliente', 'marca', 'modelo', 'matricula']
class ServicioForm(forms.ModelForm):
    class Meta:
        model = Servicio
        fields = ['nombre', 'descripcion']

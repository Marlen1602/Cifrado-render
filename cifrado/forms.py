# cifrado/forms.py
from django import forms


# Formulario para la sección Acerca de
class AboutEncryptionForm(forms.Form):
    name = forms.CharField(label='Nombre', max_length=100)
    description = forms.CharField(label='Descripción', widget=forms.Textarea)

# Formulario para Cifrado y Descifrado con AES (requiere una misma clave)
class AESForm(forms.Form):
    key = forms.CharField(label='Clave (16 caracteres)', max_length=16)
    data_nombre = forms.CharField(label='Nombre', required=False)
    data_telefono = forms.CharField(label='Teléfono', required=False)
    data_email = forms.CharField(label='Email', required=False)
    data_direccion = forms.CharField(label='Dirección', required=False)
    data_contraseña = forms.CharField(label='Contraseña', required=False)
    
# Formulario para Schnorr Signature con llaves pública y privada
class SchnorrSignatureForm(forms.Form):
    prime_number = forms.IntegerField(label='Número Primo (p)', initial=23)
    generator = forms.IntegerField(label='Generador (g)', initial=5)
    private_key = forms.IntegerField(label='Llave Privada')
    public_key = forms.IntegerField(label='Llave Pública')
    message = forms.CharField(label='Mensaje')

# Formulario para MD5
class MD5Form(forms.Form):
    text = forms.CharField(label='contraseña')

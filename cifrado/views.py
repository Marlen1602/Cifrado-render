from urllib import request
from django.shortcuts import render
from django.http import HttpResponse
from .forms import AESForm, AboutEncryptionForm, SchnorrSignatureForm, MD5Form
from Crypto.Cipher import AES
import hashlib
import secrets
import binascii

def cifrado_cye_view(request):
    return render(request, 'cifrado/cifrado_cye.html')


# Clave predefinida en el backend para cifrar y descifrar
BACKEND_KEY = "Marlen3@hdezad29"



def cifrado_ays_view(request):
    aes_form = AESForm()
    schnorr_form = SchnorrSignatureForm()
    result = {}
    decrypted = {}
    schnorr_result = {}  # Para almacenar resultados de Schnorr

    # Limpiar la sesión si la solicitud es GET (cuando se carga la página)
    if request.method == 'GET':
        request.session.clear()  # Limpia todos los datos de la sesión

    if request.method == 'POST':
        aes_form = AESForm(request.POST)
        schnorr_form = SchnorrSignatureForm(request.POST)

        # Verificar si la operación es para AES (cifrar o descifrar)
        if aes_form.is_valid():
            user_key = aes_form.cleaned_data['key']

            # Verificar si la clave ingresada coincide con la clave del backend
            if user_key == BACKEND_KEY:
                operation = request.POST.get('operation')

                if operation == 'cifrar':
                    # Obtener los datos del formulario
                    nombre = aes_form.cleaned_data['data_nombre'].encode('utf-8')
                    telefono = aes_form.cleaned_data['data_telefono'].encode('utf-8')
                    email = aes_form.cleaned_data['data_email'].encode('utf-8')
                    direccion = aes_form.cleaned_data['data_direccion'].encode('utf-8')
                    contraseña = aes_form.cleaned_data['data_contraseña'].encode('utf-8')

                    # Inicializar el cifrador AES con la clave definida en el backend
                    cipher = AES.new(user_key.encode('utf-8'), AES.MODE_ECB)
                    pad = lambda s: s + b" " * (16 - len(s) % 16)  # Padding para ajustar el tamaño

                    # Cifrar los datos
                    result['Nombre_Encriptado'] = binascii.hexlify(cipher.encrypt(pad(nombre))).decode('utf-8')
                    result['Telefono_Encriptado'] = binascii.hexlify(cipher.encrypt(pad(telefono))).decode('utf-8')
                    result['Email_Encriptado'] = binascii.hexlify(cipher.encrypt(pad(email))).decode('utf-8')
                    result['Direccion_Encriptada'] = binascii.hexlify(cipher.encrypt(pad(direccion))).decode('utf-8')
                    result['Contraseña_Encriptada'] = hashlib.md5(contraseña).hexdigest()  # Hash de la contraseña

                    # Guardar los datos encriptados en la sesión
                    request.session['encrypted_data'] = result

                elif operation == 'descifrar':
                    # Recuperar los datos encriptados de la sesión
                    encrypted_data = request.session.get('encrypted_data')

                    if encrypted_data:
                        decrypt_cipher = AES.new(user_key.encode('utf-8'), AES.MODE_ECB)

                        # Descifrar los datos
                        decrypted['Nombre'] = decrypt_cipher.decrypt(binascii.unhexlify(encrypted_data['Nombre_Encriptado'])).decode('utf-8').strip()
                        decrypted['Telefono'] = decrypt_cipher.decrypt(binascii.unhexlify(encrypted_data['Telefono_Encriptado'])).decode('utf-8').strip()
                        decrypted['Email'] = decrypt_cipher.decrypt(binascii.unhexlify(encrypted_data['Email_Encriptado'])).decode('utf-8').strip()
                        decrypted['Direccion'] = decrypt_cipher.decrypt(binascii.unhexlify(encrypted_data['Direccion_Encriptada'])).decode('utf-8').strip()
                        decrypted['Contraseña'] = "No es posible descifrar un hash."
                    else:
                        decrypted['error'] = "No hay datos cifrados disponibles para descifrar."
            else:
                decrypted['error'] = "La clave proporcionada es incorrecta. No se puede realizar la operación."

        # Verificar si la operación es para Schnorr
        if schnorr_form.is_valid() and request.POST.get('operation') == "generar_firma":
            message = schnorr_form.cleaned_data['message']
            p = schnorr_form.cleaned_data['prime_number']
            g = schnorr_form.cleaned_data['generator']
            private_key = schnorr_form.cleaned_data['private_key']
            public_key = schnorr_form.cleaned_data['public_key']

            try:
                # Generar firma digital utilizando Schnorr
                k = secrets.randbelow(p - 1)
                r = pow(g, k, p)
                e = int(hashlib.sha256((message + str(r)).encode('utf-8')).hexdigest(), 16)
                s = (k - private_key * e) % (p - 1)
                v = (pow(g, s, p) * pow(public_key, e, p)) % p
                verification = (v == r)

                schnorr_result['Schnorr_Signature'] = f"Firma: (r={r}, s={s})"
                schnorr_result['Verification'] = "La firma es válida" if verification else "La firma es inválida"
            except Exception as e:
                schnorr_result['Schnorr_Signature'] = "Error al generar la firma."
                schnorr_result['Verification'] = str(e)

    # Pasar los datos cifrados, descifrados y de Schnorr a la plantilla
    return render(request, 'cifrado/cifrado_ays.html', {
        'result': request.session.get('encrypted_data', {}),  # Datos encriptados
        'decrypted': decrypted,  # Datos descifrados
        'aes_form': aes_form,  # Formulario AES
        'schnorr_form': schnorr_form,  # Formulario Schnorr
        'schnorr_result': schnorr_result  # Resultados de Schnorr
    })
    
def acerca_de_view(request):
        if request.method == 'POST':
            form = AboutEncryptionForm(request.POST)
            if form.is_valid():
                name = form.cleaned_data['name']
                description = form.cleaned_data['description']
                return HttpResponse(f"Nombre: {name} <br> Descripción: {description}")
        else:
            form = AboutEncryptionForm()

        return render(request, 'cifrado/acerca_de.html', {'form': form})

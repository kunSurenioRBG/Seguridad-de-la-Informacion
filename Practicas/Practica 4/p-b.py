from Crypto.Hash import SHA256, HMAC
import base64
import json
import sys
from socket_class import SOCKET_SIMPLE_TCP
import funciones_aes
from Crypto.Random import get_random_bytes

# Paso 0: Inicializacion
########################

# Lee clave KBT
KBT = open("KBT.bin", "rb").read()

# Paso 1) B->T: KBT(Bob, Nb) en AES-GCM
#######################################

# Crear el socket de conexion con T (5551)
print("Creando conexion con T...")
socket = SOCKET_SIMPLE_TCP('127.0.0.1', 5551)
socket.conectar()

# Crea los campos del mensaje
t_n_origen = get_random_bytes(16)

# Codifica el contenido (los campos binarios en una cadena) y contruyo el mensaje JSON
msg_TE = []
msg_TE.append("Bob")
msg_TE.append(t_n_origen.hex())
json_ET = json.dumps(msg_TE) # json.dumps --> convierte los datos a un objeto ('s' al final = devuelve el objeto como String)
print("B -> T (descifrado): " + json_ET)

# Cifra los datos con AES GCM
aes_engine = funciones_aes.iniciarAES_GCM(KBT)
cifrado, cifrado_mac, cifrado_nonce = funciones_aes.cifrarAES_GCM(aes_engine,json_ET.encode("utf-8"))

# Envia los datos
socket.enviar(cifrado)
socket.enviar(cifrado_mac)
socket.enviar(cifrado_nonce)

# Paso 2) T->B: KBT(K1, K2, Nb) en AES-GCM
##########################################
# Recibe el mensaje de T
cifrado = socket.recibir()
cifrado_mac = socket.recibir()
cifrado_nonce = socket.recibir()

# Cerramos el socket entre B y T, no lo utilizaremos mas
socket.cerrar() 

# Descifra los datos con AES GCM
datos_descifrado_TB = funciones_aes.descifrarAES_GCM(KBT, cifrado_nonce, cifrado, cifrado_mac)

# Decodificar contenido : K1, K2, Nb
json_BT = datos_descifrado_TB.decode("utf-8", "ignore")
print("T -> B (descifrado): " + json_BT)
msg_BT = json.loads(json_BT)

# Extraigo el contenido 
K1_hex, K2_hex, n_tB_hex = msg_BT
K1 = bytes.fromhex(K1_hex)
K2 = bytes.fromhex(K2_hex)
n_tB = bytes.fromhex(n_tB_hex)

# Comprobamos en Nonce
if(n_tB != t_n_origen) :
    print("Nonce no coincide")
else :
    print("Nonce coincide")


# Paso 5) A->B: KAB(Nombre) en AES-CTR con HMAC
###############################################
# Crear el socket de escucha de Alice (5553)
print("Esperando a Alice...")
socket_Alice = SOCKET_SIMPLE_TCP('127.0.0.1', 5553)
socket_Alice.escuchar()

# Recibe los datos de Alice (nombre)
cifrado_nonce = socket_Alice.recibir()
cifrado = socket_Alice.recibir()
cifrado_mac = socket_Alice.recibir()

# Desciframos los datos con AES CTR
aes_descifrado = funciones_aes.iniciarAES_CTR_descifrado(K1, cifrado_nonce)
nombre_descifrado = funciones_aes.descifrarAES_CTR(aes_descifrado, cifrado).decode("utf-8", "ignore")
print("Mensaje recibido A -> B: " + nombre_descifrado)

# Comprobacion del MAC
h = HMAC.new(K2, nombre_descifrado.encode("utf-8"), digestmod=SHA256)
try:
    h.hexverify(cifrado_mac)
    print("MAC comprobada: MENSAJE AUTENTICO")
except:
    print("MAC comprobada: MENSAJE FALSIFICADO")

# Paso 6) B->A: KAB(Apellido) en AES-CTR con HMAC
#################################################

#Cifrado de los apellidos
apellidos = "Boqueron con Calamares"
aes_cifrado_CTR, nonce_cifrado_CTR = funciones_aes.iniciarAES_CTR_cifrado(K1)
apellidos_cifrado = funciones_aes.cifrarAES_CTR(aes_cifrado_CTR, apellidos.encode("utf-8"))

# Creamos el HMAC con K2
hmacBA= HMAC.new(K2, apellidos.encode("utf-8"), digestmod = SHA256)

# Enviamos los datos

socket_Alice.enviar(nonce_cifrado_CTR)
socket_Alice.enviar(apellidos_cifrado)
socket_Alice.enviar(hmacBA.hexdigest().encode('utf-8'))

# Paso 7) A->B: KAB(END) en AES-CTR con HMAC
############################################

# Recibe los datos de Alice
cifrado_nonce = socket_Alice.recibir()
cifrado = socket_Alice.recibir()
cifrado_mac = socket_Alice.recibir()

# Descifra los datos con AES CTR
mensaje_descifrado = funciones_aes.descifrarAES_CTR(aes_descifrado, cifrado).decode('utf-8', 'ignore')
print("Mensaje recibido A -> B: " +  mensaje_descifrado)

# Comprobacion de la MAC
h = HMAC.new(K2, mensaje_descifrado.encode("utf-8"), digestmod = SHA256)
try:
    h.hexverify(cifrado_mac)
    print("MAC comprobada: MENSAJE AUTENTICO")
except:
    print("MAC comprobada: MENSAJE FALSIFICADO")

# Si el mensaje es "END", cerramos la conexion
if(mensaje_descifrado == "END"):
    print("Cierre de la conexion con Alice")
    socket_Alice.cerrar()
else:
    print("Conexion con Alice todavia vigente...")

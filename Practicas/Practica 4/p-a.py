
from Crypto.Hash import SHA256, HMAC
import base64
import json
import sys
from socket_class import SOCKET_SIMPLE_TCP
import funciones_aes
from Crypto.Random import get_random_bytes

# Paso 0: Inicializacion
########################
# Lee la clave KAT
KAT = open("KAT.bin", "rb").read()

# Paso 3) A->T: KAT(Alice, Na) en AES-GCM
#########################################
# Crear el socket de conexion con T (5552)
print("Creando conexion con T...")
socket = SOCKET_SIMPLE_TCP('127.0.0.1', 5552)
socket.conectar()

# Crea los campos del mensaje
t_n_origen = get_random_bytes(16)

# Codifica el contenido (los campos binarios en una cadena) y construyo el mensaje JSON
msg_AT = []
msg_AT.append("Alice")
msg_AT.append(t_n_origen.hex())
json_AT = json.dumps(msg_AT)
print("A -> T (descifrado): " + json_AT)

# Cifra los datos con AES GCM
aes_engine = funciones_aes.iniciarAES_GCM(KAT)
cifrado, cifrado_mac, cifrado_nonce = funciones_aes.cifrarAES_GCM(aes_engine,json_AT.encode("utf-8"))

# Enviar los datos
socket.enviar(cifrado)
socket.enviar(cifrado_mac)
socket.enviar(cifrado_nonce)

# Paso 4) T->A: KAT(K1, K2, Na) en AES-GCM
##########################################
# Recibe el mensaje de T
cifrado = socket.recibir()
cifrado_mac = socket.recibir()
cifrado_nonce = socket.recibir()

# Cierro el socket de conexion con T 
socket.cerrar()

# Descifro los datos con AES GCM
datos_descifrado_TA = funciones_aes.descifrarAES_GCM(KAT, cifrado_nonce, cifrado, cifrado_mac)

#  Decodifica el contenido: Alice, Nb
json_TA = datos_descifrado_TA.decode("utf-8", "ignore")
print("T->A (descifrado): " + json_TA)
msg_TA = json.loads(json_TA)

# Extraigo el contenido
K1_hex, K2_hex, n_tA_hex = msg_TA
K1 = bytes.fromhex(K1_hex)
K2 = bytes.fromhex(K2_hex)
n_tA = bytes.fromhex(n_tA_hex)

# Comprobamos nonce
if(n_tA != t_n_origen) :
    print("Nonce no coincide")
else :
    print("Nonce coincide")

# Paso 5) A->B: KAB(Nombre) en AES-CTR con HMAC
###############################################
# Crear el socket de conexion con B (5553)
print("Creando conexion con B...")
socket = SOCKET_SIMPLE_TCP('127.0.0.1', 5553)
socket.conectar()

# Ciframos el nombre con CTR
nombre = "kunSurenio"
aes_cifrado_CTR, nonce_cifrado_CTR = funciones_aes.iniciarAES_CTR_cifrado(K1)
nombre_cifrado = funciones_aes.cifrarAES_CTR(aes_cifrado_CTR, nombre.encode("utf-8"))

# Creamos el HMAC con K2
hmacAB = HMAC.new(K2, nombre.encode("utf-8"), digestmod = SHA256)

# Enviamos los datos
socket.enviar(nonce_cifrado_CTR)
socket.enviar(nombre_cifrado)
socket.enviar(hmacAB.hexdigest().encode('utf-8'))

# Paso 6) B->A: KAB(Apellido) en AES-CTR con HMAC
#################################################

# Recibe los datos de Bob (apellidos)
cifrado_nonce = socket.recibir()
cifrado = socket.recibir()
cifrado_mac = socket.recibir()

# Descriframos el mensaje con AES CTR
aes_descifrado = funciones_aes.iniciarAES_CTR_descifrado(K1, cifrado_nonce)
apellidos_descifrados = funciones_aes.descifrarAES_CTR(aes_descifrado, cifrado).decode('utf-8')
print("Mensaje recibido B -> A: " + apellidos_descifrados)

# Comprobacion de la MAC
h = HMAC.new(K2, apellidos_descifrados.encode("utf-8"), digestmod=SHA256)
try:
    h.hexverify(cifrado_mac)
    print("MAC comprobada: MENSAJE AUTENTICO")
except:
    print("MAC comprobada: MENSAJE FALSIFICADO")

# Paso 7) A->B: KAB(END) en AES-CTR con HMAC
############################################

# Ciframos con AES CTR
mensaje = "END"
mensaje_cifrado = funciones_aes.cifrarAES_CTR(aes_cifrado_CTR, mensaje.encode("utf-8"))

# Creamos el HMAC con K2
hmacAB = HMAC.new(K2, mensaje.encode("utf-8"), digestmod = SHA256)

# Enviamos los datos
socket.enviar(nonce_cifrado_CTR)
socket.enviar(nombre_cifrado)
socket.enviar(hmacAB.hexdigest().encode('utf-8'))
print("Conexion finalizada entre A -> B")

# Cierre de la conexion
socket.cerrar()


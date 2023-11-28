from Crypto.Hash import SHA256, HMAC
import base64
import json
import sys
from socket_class import SOCKET_SIMPLE_TCP
import funciones_aes

# Paso 0: Crea las claves que T comparte con B y A
##################################################

# Crear Clave KAT, guardar a fichero
KAT = funciones_aes.crear_AESKey()
FAT = open("KAT.bin", "wb")
FAT.write(KAT)
FAT.close()

# Crear Clave KBT, guardar a fichero
KBT = funciones_aes.crear_AESKey()
FBT = open("KBT.bin", "wb")
FBT.write(KBT)
FBT.close()

# Paso 1) B->T: KBT(Bob, Nb) en AES-GCM
#######################################

# Crear el socket de escucha de Bob (5551)
print("Esperando a Bob...")
socket_Bob = SOCKET_SIMPLE_TCP('127.0.0.1', 5551)
socket_Bob.escuchar()

# Crea la respuesta para B y A: K1 y K2
K1 = funciones_aes.crear_AESKey()
K2 = funciones_aes.crear_AESKey()

# Recibe el mensaje
cifrado = socket_Bob.recibir()
cifrado_mac = socket_Bob.recibir()
cifrado_nonce = socket_Bob.recibir()

# Descifro los datos con AES GCM
datos_descifrado_ET = funciones_aes.descifrarAES_GCM(KBT, cifrado_nonce, cifrado, cifrado_mac)

# Decodifica el contenido: Bob, Nb
json_ET = datos_descifrado_ET.decode("utf-8","ignore")
print("B->T (descifrado): " + json_ET)
msg_ET = json.loads(json_ET)

# Extraigo el contenido
t_bob, t_nb = msg_ET
t_nb = bytearray.fromhex(t_nb)

# Paso 2) T->B: KBT(K1, K2, Nb) en AES-GCM
##########################################

# Codifica el contenido (los campos binarios en una cadena) y construllo el mensaje JSON
msg_TB = []
msg_TB.append(K1.hex())   # clave 1
msg_TB.append(K2.hex())   # clave 2
msg_TB.append(t_nb.hex()) # nonce B
json_TB = json.dumps(msg_TB)
print("T -> B (descifrado): " + json_TB)

# Cifra los datos con AES GCM
aes_engine = funciones_aes.iniciarAES_GCM(KBT)
cifrado, cifrado_mac, cifrado_nonce = funciones_aes.cifrarAES_GCM(aes_engine, json_TB.encode("utf-8"))

# Envia los datos
socket_Bob.enviar(cifrado)
socket_Bob.enviar(cifrado_mac)
socket_Bob.enviar(cifrado_nonce)

# Cerramos el socket entre B y T, no lo utilizaremos mas
socket_Bob.cerrar() 

# Paso 3) A->T: KAT(Alice, Na) en AES-GCM
#########################################
# Crear el socket de escucha de Alice (5552)
print("Esperando a Alice...")
socket_Alice = SOCKET_SIMPLE_TCP('127.0.0.1', 5552)
socket_Alice.escuchar()

# Recibo el mensaje
cifrado = socket_Alice.recibir()
cifrado_mac = socket_Alice.recibir()
cifrado_nonce = socket_Alice.recibir()

# Descifro los datos
datos_descifrado_ET = funciones_aes.descifrarAES_GCM(KAT, cifrado_nonce, cifrado, cifrado_mac)

#  Decodifica el contenido: Alice, Nb
json_ET = datos_descifrado_ET.decode("utf-8", "ignore")
print("A->T (descifrado): " + json_ET)
msg_ET = json.loads(json_ET)

# Estraigo el contenido
t_Alice, t_nA = msg_ET
t_nA = bytearray.fromhex(t_nA)

# Paso 4) T->A: KAT(K1, K2, Na) en AES-GCM
##########################################
# Codifica el contenido (los campos binarios en una cadena) y construllo el mensaje JSON
msg_TA = []
msg_TA.append(K1.hex())   # clave 1
msg_TA.append(K2.hex())   # clave 2
msg_TA.append(t_nA.hex()) # nonce B
json_TA = json.dumps(msg_TA)
print("T -> A (descifrado): " + json_TA)

# Cifra los datos con AES GCM
aes_engine = funciones_aes.iniciarAES_GCM(KAT)
cifrado, cifrado_mac, cifrado_nonce = funciones_aes.cifrarAES_GCM(aes_engine, json_TA.encode("utf-8"))

# Envia los datos
socket_Alice.enviar(cifrado)
socket_Alice.enviar(cifrado_mac)
socket_Alice.enviar(cifrado_nonce)

# Cerramos el socket entre B y T, no lo utilizaremos mas
socket_Bob.cerrar()

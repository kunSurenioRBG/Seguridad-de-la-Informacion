from Crypto.Random import get_random_bytes
import funciones_rsa, funciones_aes
import socket_class

# cargamos las clave privada de Alice y publica de Bob
claveAlice = funciones_rsa.cargar_RSAKey_Privada("clavePrivadaAlice.txt", "holaALice")
claveBob = funciones_rsa.cargar_RSAKey_Publica("clavePublicaBob.txt")

# cifrar array de 16 bytes
K1 = funciones_aes.crear_AESKey()
K1_cifrado = funciones_rsa.cifrarRSA_OAEP(K1, claveBob)

# firmar
K1_firma = funciones_rsa.firmarRSA_PSS(K1, claveAlice)

# enviar el cifrado y firma usando un socket
socketClient = socket_class.SOCKET_SIMPLE_TCP('127.0.0.1', 5551)
socketClient.conectar()
socketClient.enviar(K1_cifrado)
socketClient.enviar(K1_firma)
# socketClient.cerrar() --> no cerramos por el mismo motivo que con Bob



# =======================
# Parte 2
# =======================
# Alice recibe el texto cifrado con la clave simetrica y la firma digital
nonce = socketClient.recibir()
cadenaCifrada = socketClient.recibir()
cadenaFirmada = socketClient.recibir()

# Descifra la cadena de caracteres K1
aes_descifrado = funciones_aes.iniciarAES_CTR_descifrado(K1, nonce)
cadena = funciones_aes.descifrarAES_CTR(aes_descifrado, cadenaCifrada)
validez = funciones_rsa.comprobarRSA_PSS(cadena, cadenaFirmada, claveBob)
print(cadena)
print(validez)



# =======================
# Parte 3
# =======================
cadena2 = "Hola Bob"
(aes_cifrado2, nonce2) = funciones_aes.iniciarAES_CTR_cifrado(K1)
cadenaCifrada2 = funciones_aes.cifrarAES_CTR(aes_cifrado2, cadena2.encode("utf-8"))
cadenaFirmada2 = funciones_rsa.firmarRSA_PSS(cadena2.encode("utf-8"), claveAlice)
socketClient.enviar(nonce2)
socketClient.enviar(cadenaCifrada2)
socketClient.enviar(cadenaFirmada2)
socketClient.cerrar()

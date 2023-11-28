from Crypto.Random import get_random_bytes
import funciones_rsa
import funciones_aes
import socket_class

# cargamos las clave privada de Alice y publica de Bob
claveAlice = funciones_rsa.cargar_RSAKey_Publica("clavePublicaAlice.txt")
claveBob = funciones_rsa.cargar_RSAKey_Privada("clavePrivadaBob.txt", "holaBob")

# recibir texto cifrado y firma digital a traves del socket
socketServer = socket_class.SOCKET_SIMPLE_TCP('127.0.0.1', 5551)
socketServer.escuchar()
txtCifrado = socketServer.recibir()
firma = socketServer.recibir()
# socketServer.cerrar() -> no cerramos el socket porque lo vamos a seguir usando a lo largo del ejercicio 2. Sino, se debe cerrar

# Descrifrar el array K1
K1 = funciones_rsa.descifrarRSA_OAEP(txtCifrado, claveBob)
comprobarValidez = funciones_rsa.comprobarRSA_PSS(K1, firma, claveAlice)

print(K1)
print(comprobarValidez)


# =======================
# Parte 2
# =======================
cadena = "Hola Alice"
# El objeto AES se inicializa una vez (inicio el motos CTR)
# NOTA: se puede poner asi tmb:
(aes_cifrado, nonce) = funciones_aes.iniciarAES_CTR_cifrado(K1)
#aes_cifrado = funciones_aes.iniciarAES_CTR_cifrado(K1)
#nonce = funciones_aes.iniciarAES_CTR_cifrado(K1)
# Y luego vamos llamando a aes_cifrado
cadenaCifrada = funciones_aes.cifrarAES_CTR(aes_cifrado, cadena.encode("utf-8"))
# Firmamos la cadena
cadenaFirmada = funciones_rsa.firmarRSA_PSS(cadena.encode("utf-8"), claveBob)

socketServer.enviar(nonce)
socketServer.enviar(cadenaCifrada)
socketServer.enviar(cadenaFirmada)


# =======================
# Parte 3
# =======================
nonce2 = socketServer.recibir()
cadenaCifrada2 = socketServer.recibir()
cadenaFirmada2 = socketServer.recibir()
aes_descifrado2 = funciones_aes.iniciarAES_CTR_descifrado(K1, nonce2)
cadena2 = funciones_aes.descifrarAES_CTR(aes_descifrado2, cadenaCifrada2)
validez2 = funciones_rsa.comprobarRSA_PSS(cadena2, cadenaFirmada2, claveAlice)
print(cadena2)
print(validez2)
socketServer.cerrar()

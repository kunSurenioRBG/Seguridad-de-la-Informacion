from Crypto.Random import get_random_bytes
from Crypto.Cipher import DES, AES
from Crypto.Util.Padding import pad,unpad
from Crypto.Util import Counter

# Datos necesarios
key = get_random_bytes(16) # Clave aleatoria de 64 bits
IV = get_random_bytes(16)  # IV aleatorio de 64 bits
BLOCK_SIZE_DES = 16 # Bloque de 64 bits
data = "Hola amigos de la seguridad".encode("utf-8") # Datos a cifrar
data2 = "Hola amigas de la seguridad".encode("utf-8") # Datos a cifrar
print(data)
print(data2)

# CIFRADO ##########################################################################

# Creamos un mecanismo de cifrado AES en modo CBC con un vector de inicialización IV
cipher = AES.new(key, AES.MODE_CBC, IV)

# Ciframos, haciendo que la variable “data” sea múltiplo del tamaño de bloque
ciphertext = cipher.encrypt(pad(data,BLOCK_SIZE_DES))
ciphertext2 = cipher.encrypt(pad(data2,BLOCK_SIZE_DES))

# Mostramos el cifrado por pantalla en modo binario
print(ciphertext)
print(ciphertext2)

# DESCIFRADO #######################################################################

# Creamos un mecanismo de (des)cifrado DES en modo CBC con una inicializacion IV
# Ambos, cifrado y descifrado, se crean de la misma forma
decipher_aes = AES.new(key, AES.MODE_CBC, IV)

# Desciframos, eliminamos el padding, y recuperamos la cadena
new_data = unpad(decipher_aes.decrypt(ciphertext), BLOCK_SIZE_DES).decode("utf-8", "ignore")
new_data2 = unpad(decipher_aes.decrypt(ciphertext2), BLOCK_SIZE_DES).decode("utf-8", "ignore")

# Imprimimos los datos descifrados
print(new_data)
print(new_data2)
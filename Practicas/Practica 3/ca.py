import funciones_rsa

# creo la clave
keyAlice = funciones_rsa.crear_RSAKey()
keyBob = funciones_rsa.crear_RSAKey()

# guardar claves Alice
funciones_rsa.guardar_RSAKey_Publica("clavePublicaAlice.txt",keyAlice)
funciones_rsa.guardar_RSAKey_Privada("clavePrivadaAlice.txt",keyAlice,"holaALice")

# guardad claves Bob
funciones_rsa.guardar_RSAKey_Publica("clavePublicaBob.txt",keyBob)
funciones_rsa.guardar_RSAKey_Privada("clavePrivadaBob.txt",keyBob,"holaBob")
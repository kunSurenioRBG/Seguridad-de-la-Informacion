TAM_CLAVE = 26
#XYZ VENI! VIDI_ VINCI AURIA

def obtenerModo():
    while True:
        print('Selecciona si vas a encriptar o desencriptar')
        modo = input().lower()
        if modo in 'encriptar e desencriptar d'.split():
            return modo
        else:
            print('Ingresa "encriptar" o "e" o "desencriptar" o "d"')


def obtenerMensaje():
    print('Ingresa el mensaje:')
    return input()

def obtenerClave():
    clave = 0
    while True:
        print('Ingresa el numero de clave (1-%s)' % TAM_CLAVE)
        clave = int(input())
        if (clave >= 1 and clave <= TAM_CLAVE):
            return clave
        

def  ObtenerMensajeTraducido(modo, mensaje, clave):
    if modo == 'd':
        clave = -clave #decrementa por el valor de clave
    traduccion = '' #cadena de caracteres a devolver
    
    for simbolo in mensaje:
        if simbolo.isalpha():
            num = ord(simbolo)
            
            if (num >= 65 and num <= 90):
                num = (((num - 65) + clave) %26) + 65
            else:
                num = (((num - 97) + clave) %26) + 97
            traduccion += chr(num)
        else:
            traduccion += simbolo
    return traduccion

modo = obtenerModo()
mensaje = obtenerMensaje()
clave = obtenerClave()

print('El texto traducido es:')
print(ObtenerMensajeTraducido(modo,mensaje,clave))
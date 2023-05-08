import xmlrpc.server

def cifrado(texto,desplazamiento):
    texto = texto.upper()
    alfabeto = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
    cifrado = ""
    for letra in texto:
        if letra in alfabeto:
            posicion = alfabeto.find(letra)
            nueva_posicion = (posicion + desplazamiento) % 27
            cifrado += alfabeto[nueva_posicion]
        else:
            cifrado += letra
    return cifrado

def descifrado(texto,desplazamiento):
    texto = texto.upper()
    alfabeto = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
    descifrado = ""
    for letra in texto:
        if letra in alfabeto:
            posicion = alfabeto.find(letra)
            nueva_posicion = (posicion - desplazamiento) % 27
            descifrado += alfabeto[nueva_posicion]
        else:
            descifrado += letra
    return descifrado

def linea():
    return "Servidor en linea 192.168.1.75 en puerto 3312"

server = xmlrpc.server.SimpleXMLRPCServer(("192.168.1.183", 3313))
print("Esperando consultas de cifrado...")

server.register_function(cifrado, "cifrado")
server.register_function(descifrado, "descifrado")
server.register_function(linea, "linea")


server.serve_forever()

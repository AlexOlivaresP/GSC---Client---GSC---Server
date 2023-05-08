import concurrent.futures
import time
import xmlrpc.client
import logging

# Configurar el registro
#El formato de la bitácora es: fecha y hora, nivel de registro, mensaje, nombre del hilo, nombre de la función y número de línea 
#El nivel de registro es INFO para que se muestren todos los mensajes de la bitácora

logging.basicConfig(filename='bitacora.log', level=logging.DEBUG,filemode='w', 
                    format='%(asctime)s | %(levelname)s:%(message)s | %(threadName)s | %(funcName)s | %(lineno)d|')

# Crear logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Crear manejador para la consola
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# Formatear mensaje de log
formatter = logging.Formatter('%(levelname)s || %(message)s')
ch.setFormatter(formatter)

# Agregar manejador al logger
logger.addHandler(ch)

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

def decifrado(cifrado,corrimientos):
    # código que se ejecutará en el hilo
    cifrado = cifrado.upper()
    alfabeto = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
    decifrado = ""
    for letra in cifrado:
        if letra in alfabeto:
            posicion = alfabeto.find(letra)
            nueva_posicion = (posicion - corrimientos) % 27
            decifrado += alfabeto[nueva_posicion]
        else:
            decifrado += letra
    return decifrado

#esta funcion pregunta el estado actual de los servidores
def serverStat():
    # Crear proxy
    logging.debug(f"TESTEANDO LOS SERVIDORES ...")
    #print("CONECTANDO CON VM...")
    #http://
    proxy = xmlrpc.client.ServerProxy("http://192.168.56.1:3312/RPC2")
    logging.debug("Conectado para testear")
    libres = proxy.libres()
    print(f"Servidores libres: {libres}")

def solicitud(texto,desplazamiento):
    # Crear proxy
    logging.debug(f"Solicitando servidor al gsc desde el cliente ...")
    proxy = xmlrpc.client.ServerProxy("http://192.168.56.1:3312/RPC2")
    logging.debug("Conectado")
    resultado = proxy.solicitud(texto,desplazamiento)
    return resultado
    #print(f"Servidores libres: {libres}")

def gsc(texto,desplazamiento):
    # Crear proxy
    logging.debug("Conectando con GSC...")
    #print("CONECTANDO CON VM...")
    #http://192.168.1.75:3312/RPC2
    proxy = xmlrpc.client.ServerProxy("http://192.168.56.1:3312/RPC2")
    #print("CONECTADO CON VM...\n")
    # Llamar función del servidor
    resultado = proxy.solicitud(texto,desplazamiento)
    # Imprimir resultado
    return resultado


#hola = serverStat()

#Se lee el texto a cifrar
logging.debug("Iniciando programa")
logging.debug("Leyendo archivo")
try:
    #Se abre el archivo con codificación utf-8
    with open("P4/texto copy.txt", "r") as archivo:
        Frase = archivo.read()
except (FileNotFoundError, IOError) as e:
    logging.error(f"Error al abrir el archivo: {e}")

Desplazamiento = int(input("Ingrese el desplazamiento: "))
print("\n\n")

#Se divide el texto en 2
logging.debug("Dividiendo texto en 5")
mitad = len(Frase)//2
mitad1 = Frase[:mitad]
mitad2 = Frase[mitad:]


#Se ejecutan los hilos
#Crear un executor de hilos
logging.debug("Iniciando executor de hilos")
ejecutaHilo = concurrent.futures.ThreadPoolExecutor()

#Inicia cronómetro de hilo virtual
inicio = time.time()

# Ejecutar la función en un hilo y obtener una instancia de Future

logging.debug("Ejecutando hilo virtual")
mi_hilo = ejecutaHilo.submit(solicitud, mitad1, Desplazamiento)

logging.debug("Ejecutando hilo local")
mi_hilo2 = ejecutaHilo.submit(cifrado, mitad2, Desplazamiento)

# Obtener el resultado de la función

logging.debug("Obteniendo resultado de hilo virtual")
resultado = mi_hilo.result()

logging.debug("Obteniendo resultado de hilo local")
resultado2= mi_hilo2.result()

fin = time.time()
tiempo_total = fin - inicio
print("Tiempo de ejecución concurrente: ", tiempo_total, "segundos")
logging.debug("Fin de executor de hilos")

#Se guarda el texto cifrado
try:
    with open("P4/cifrado.txt", "w") as archivo:
        archivo.write(resultado+resultado2)
    logging.debug("Archivo Cifrados.txt guardado con exito")
except (FileNotFoundError, IOError) as e:
    logging.error(f"Error al abrir el archivo: {e}")



#Inicia cronómetro de descifrado, solo con hilo local
tiempoSolo = time.time()
descif = decifrado(resultado+resultado2, Desplazamiento)
finTiempoSolo = time.time()
tiempoTotalSolo = finTiempoSolo - tiempoSolo
print("Tiempo de ejecución local: ", tiempoTotalSolo, "segundos")


try:
    with open("P4/descifrado.txt", "w") as archivo:
        archivo.write(descif)
    logging.debug("Archivo descifrado.txt guardado con exito")
except (FileNotFoundError, IOError) as e:
    logging.error(f"Error al abrir el archivo: {e}")

#Se cierra el executor de hilos
ejecutaHilo.shutdown()

logging.debug("Fin del programa")




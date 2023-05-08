import logging
import xmlrpc.server
import xmlrpc.client
import time
import concurrent.futures


logging.basicConfig(filename='bitacoraGSC.log', level=logging.DEBUG,filemode='w', 
                    format='%(asctime)s | %(levelname)s:%(message)s | %(threadName)s | %(funcName)s | %(lineno)d|')

listaServidores = [[1,"http://192.168.1.75:3312/RPC2"],[1,"http://192.168.1.161:3312/RPC2"]]
listaActivos = []


def Servidores():
    while(1):
        for i in range(len(listaServidores)):
            try:
                serverStat(i)
                listaServidores[i][0] = 1
            except:
                print("Servidor caido")
                logging.debug(f"Servidor {listaServidores[i][1]} caido")
                print(listaServidores[i][1])
                listaServidores[i][0] = 0
            if i == 1:
                time.sleep(5)
            #print(listaServidores[i][0])

    

def serverLocal():
    try:
        logging.debug("Iniciando servidor")
        server = xmlrpc.server.SimpleXMLRPCServer(("192.168.56.1", 3312))
        logging.debug("Servidor iniciado")
    except:
        logging.debug("No se pudo iniciar el servidor")
        print("No se pudo iniciar el servidor")

    server.register_function(handle_connection, "_dispatch")
    server.register_function(ServerFree, "libres")
    server.register_function(solicitud, "solicitud")
    server.serve_forever()
    

def serverStat(a):
    # Crear proxy
    #logging.debug(f"Conectando con {listaServidores[a][1]}...")
    #print("CONECTANDO CON VM...")
    #http://192.168.1.75:3312/RPC2
    proxy = xmlrpc.client.ServerProxy(listaServidores[a][1])
    #print("CONECTADO CON VM...\n")
    # Llamar función del servidor
    resultado = proxy.linea()
    # Imprimir resultado
    #print(resultado)
    #return resultado


#la funcion linea manda a quien la invoca un hola mundo
def ServerFree():
    listaActivos = []
    for i in range(len(listaServidores)):
        if listaServidores[i][0] == 1:
            listaActivos.append(listaServidores[i][1])
    return listaActivos

def handle_connection(client_ip):
    # Registra la conexión en la bitácora
    logging.info(f"Cliente {client_ip} se ha conectado")

def solicitud(texto,desplazamiento):
    i=0
    while i<len(listaServidores):
        if (listaServidores[i][0]==1):
            listaServidores[i][0]==0
            proxy = xmlrpc.client.ServerProxy(listaServidores[i][1])
            resultado = proxy.cifrado(texto,desplazamiento)
            #print(resultado)
            listaServidores[i][0]==1
            i=len(listaServidores)
            return resultado
        
        else:
            n=n+1




print("SERVIDOR GSC CORRIENDO...")


servers = [[1,"http://192.168.1.75:3312/RPC2"],[1,"http://192.168.1.161:3312/RPC2"]]



logging.debug("Iniciando executor de hilos")
ejecutaHilo = concurrent.futures.ThreadPoolExecutor()

logging.debug("Ejecutando hilo 2")
mi_hilo = ejecutaHilo.submit(Servidores)

logging.debug("Ejecutando hilo 1")
mi_hilo2 = ejecutaHilo.submit(serverLocal)


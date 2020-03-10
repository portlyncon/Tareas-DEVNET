       #Crear un programa que permita conectarse con el controlador APIC-EM de Cisco
    #El usuario tendrá que escoger la opción que quiera (no tendrá que especificar la url a mano)
    #Añadir, como mínimo, 4 funcionalidades

# Import modules.
import requests
import json

# Desabilitar warnings.
requests.packages.urllib3.disable_warnings()

# Variables
direccion = "https://sandboxapicem.cisco.com/api/v1"
etiqueta ="pol"


def obtener_token(url):

    llamada_api ="/ticket"
    datos = { "username": "devnetuser", "password": "Cisco123!" }
    headers = {"content-type" : "application/json"}
    url += llamada_api
    try:
        response = requests.post(url, data=json.dumps(datos), headers=headers, verify=False).json()
    except:
         print("No hay conexion a internet")
         

    return response["response"]["serviceTicket"]


def obtener_hosts_ip(token, url): 
    
    llamada_api = "/host"
    headers = {"X-AUTH-TOKEN": token}

    # Combinacion URL, variables API
    url += llamada_api
    try:
        response = requests.get(url, headers=headers, verify=False).json()
    except:
        print("No se ha podido establecer la llamada API")
    # lista de response
    hosts = response["response"]
    return hosts
       
def obtener_serial(token, url): 
    
    llamada_api = "/network-device" 
    headers = {"X-AUTH-TOKEN": token}

    # Combinacion URL, variables API
    url += llamada_api
    try:
        response = requests.get(url, headers=headers, verify=False).json()
    except:
        print("No se ha podido establecer la llama API")

    # lisa de response 
    hosts = response["response"]
    return hosts

def obtener_ip_mantenimiento(token, url): 
    
    llamada_api = "/location" 
    headers = {"X-AUTH-TOKEN": token}

    # Combinacion URL, variables API
    url += llamada_api
	
    try:
        response = requests.get(url, headers=headers, verify=False).json()
    except:
        print("No se ha podido establecer la llamada API")
    # lisa de response 
    hosts = response["response"]
    return hosts

def obtener_configuracion(token, url): 
    
    llamada_api = "/network-device/config" 
    headers = {"X-AUTH-TOKEN": token}

    # Combinacion URL, variables API
    url += llamada_api
	
    try:
        response = requests.get(url, headers=headers, verify=False).json()
    except:
        print("No se ha podido establecer la llamada API")
    # lisa de response 
    hosts = response["response"]
    return hosts

def escojer_tarea(etiqueta):

    operacion = input('''
introduce la operacion que quieres realizar:
1 lista IP hosts
2 lista macs dispositivos
3 localizacion 
4 serialNumber dispositivo
''')
    
       
    
    if operacion == '1':
        hosts = obtener_hosts_ip(autorizacion, direccion)
        etiqueta ="hostIp"
        print("Listado IP hosts")
        imprimir_lista(hosts,etiqueta)
        
    elif operacion =='2':
        hosts = obtener_configuracion(autorizacion, direccion) 
        etiqueta ="hostMac"
        print("configuracion de dispositivo")
        imprimir_configuraciones(hosts,etiqueta)
    
    elif operacion =='3':
        hosts = obtener_ip_mantenimiento(autorizacion, direccion)
        etiqueta ="id"
        print("localizacion equipos")
        imprimir_ip_mantenimiento(hosts,etiqueta)  
   
    elif operacion =='4':
        hosts = obtener_serial(autorizacion, direccion) 
        etiqueta ="hostname"
        print("Listado de serial number dispositivos")
        imprimir_lista_serial_dispositivos(hosts,etiqueta)
        
counter = 0 

def imprimir_lista(hosts,etiqueta):
    for host in hosts: 
            print("nombre host:",host["id"],"ip:",host[etiqueta],"macaddress:",host["hostMac"]) 
   
    otra_tarea()

def imprimir_lista_serial_dispositivos(hosts,etiqueta):
    for host in hosts: 
            print("nombre dispositivo:",host["hostname"],"macaddress:",host["macAddress"]) 
   
    otra_tarea()

def imprimir_ip_mantenimiento(hosts,etiqueta):
    for host in hosts: 
            print("nombre dispositivo:",host["locationName"],host["id"],"localizacion:",host["geographicalAddress"]) 
   
    otra_tarea()

def imprimir_configuraciones(hosts,etiqueta):
    for host in hosts: 
            print("id del dispositivo:",host["id"],"configuracion",host["runningConfig"]) 
   
    otra_tarea()


def otra_tarea():
    otra_accion = input('''
quieres realizar otra operacion?
introduce Y para YES o N para NO.
''')

    if otra_accion.upper() == 'Y':
        escojer_tarea(etiqueta)
    elif otra_accion.upper() == 'N':
        print('Adios')
    else:
        otra_tarea()

# obetener autorizacion en APIC-EM
try:
    autorizacion = obtener_token(direccion)
except:
    print("erro de connexion en al red")
#Escojer que tarea quiere realizar el usuario
try:
    escojer_tarea(etiqueta)
except:
    print("error en la ejecucion de tarea")

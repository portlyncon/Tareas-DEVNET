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

    response = requests.post(url, data=json.dumps(datos), headers=headers, verify=False).json()

    return response["response"]["serviceTicket"]


def obtener_hosts_ip(token, url): 
    
    llamada_api = "/host"
    headers = {"X-AUTH-TOKEN": token}

    # Combinacion URL, variables API
    url += llamada_api

    response = requests.get(url, headers=headers, verify=False).json()
    
    # lista de response
    hosts = response["response"]
    return hosts
       
def obtener_serial(token, url): 
    
    llamada_api = "/network-device" 
    headers = {"X-AUTH-TOKEN": token}

    # Combinacion URL, variables API
    url += llamada_api
	
    response = requests.get(url, headers=headers, verify=False).json()
    
    # lisa de response 
    hosts = response["response"]
    return hosts

def escojer_tarea(etiqueta):

    operacion = input('''
introduce la operacion que quieres realizar:
1 lista IP hosts
2 lista macs
3 conectado a
4 serialNumber dispositivo
''')
    
    if operacion != '4':
        hosts = obtener_hosts_ip(autorizacion, direccion)
    else:
        hosts = obtener_serial(autorizacion, direccion)    
    
    if operacion == '1':
        
        etiqueta ="hostIp"
        print("Listado IP hosts")
        imprimir_lista(hosts,etiqueta)
        
    elif operacion =='2':

        etiqueta ="hostMac"
        print("Listado mac hosts")
        imprimir_lista(hosts,etiqueta)
    
    elif operacion =='3':
   
        etiqueta ="connectedNetworkDeviceIpAddress"
        print("Listado equipos conectados")
        imprimir_lista(hosts,etiqueta)  
   
    elif operacion =='4':

        etiqueta ="hostname"
        print("Listado de serial number dispositivos")
        imprimir_lista_serial(hosts,etiqueta)
        
counter = 0 

def imprimir_lista(hosts,etiqueta):
    for host in hosts: 
            print("nombre equipo:",host["id"],"ip:",host[etiqueta],"macaddress:",host["hostMac"]) 
   
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    #for host in hosts: 
     #   print("{ip:20} {mac:20} {type:10}".format(ip=host["hostIp"], 
      #                                           mac=host["hostMac"], 
       #                                          type=host["hostType"]))
            #print("Nombre equipo",hosts[counter][etiqueta],"device mac addres")
    otra_tarea()

def imprimir_lista_serial(hosts,etiqueta):
    for host in hosts: 
            print("nombre equipo:",host["hostname"],"macaddress:",host["macAddress"]) 
   
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
autorizacion = obtener_token(direccion)

#Escojer que tarea quiere realizar el usuario
escojer_tarea(etiqueta)

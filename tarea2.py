    #Crear un programa que permita conectarse con el controlador APIC-EM de Cisco
    #El usuario tendrá que escoger la opción que quiera (no tendrá que especificar la url a mano)
    #Añadir, como mínimo, 4 funcionalidades

# Import modules.
import requests
import json

# Desabilitar warnings.
requests.packages.urllib3.disable_warnings()

# Variables
apic_em_ip = "https://sandboxapicem.cisco.com/api/v1"
etiqueta ="pol"


def obtener_token(url):

    # Define API Call to get authentication token.
    api_call ="/ticket"

    # Payload contains authentication information.
    payload = { "username": "devnetuser", "password": "Cisco123!" }

    # Header information.
    headers = {"content-type" : "application/json"}

    # Add the API call to the URL argument.
    url += api_call

    response = requests.post(url, data=json.dumps(payload), headers=headers, verify=False).json()

    # Return authentication token from respond body.
    return response["response"]["serviceTicket"]


def obtener_hosts_ip(token, url): 
    # Define API Call
    api_call = "/host"

    # Header 
    headers = {"X-AUTH-TOKEN": token}

    # Combine URL, API call and parameters variables
    url += api_call
	
    response = requests.get(url, headers=headers, verify=False).json()
    
    # list from response 
    hosts = response["response"]
    return hosts
       
def obtener_serial(token, url): 
    # Define API Call
    api_call = "/network-device"

    # Header 
    headers = {"X-AUTH-TOKEN": token}

    # Combine URL, API call and parameters variables
    url += api_call
	
    response = requests.get(url, headers=headers, verify=False).json()
    
    # list from response 
    hosts = response["response"]
    return hosts

def escojer_tarea(etiqueta):
   
    hosts = obtener_hosts_ip(auth_token, apic_em_ip)

    operacion = input('''
introduce la operacion que quieres realizar:
1 lista IP hosts
2 lista macs
3 conectado a
4 serialNumber dispositivo
''')
    if operacion == '1':
        
        etiqueta ="hostIp"
        print("Listado IP hosts")
        imprimir_lista(hosts,etiqueta)
        
    elif operacion =='2':

        etiqueta ="hostMac"
        print("Listado mac hosts")
        imprimir_lista(hosts,etiqueta)
    
    elif  operacion =='3':
   
        etiqueta ="connectedNetworkDeviceIpAddress"
        print("Listado equipos conectados")
        imprimir_lista(hosts,etiqueta)  
   
    elif operacion =='4':

        hosts = obtener_serial(auth_token, apic_em_ip)
        etiqueta ="hostname"
        print("Listado de serial number dispositivos")
        imprimir_lista(hosts,etiqueta)
        


def imprimir_lista(hosts,etiqueta):
    for host in hosts: 
            print(host[etiqueta]) 
    
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    #for host in hosts: 
     #   print("{ip:20} {mac:20} {type:10}".format(ip=host["hostIp"], 
      #                                           mac=host["hostMac"], 
       #                                          type=host["hostType"]))
    otra_opercion()


def otra_opercion():
    otro_calculo = input('''
quieres realizar otra operacion?
introduce Y para YES o N para NO.
''')

    if otro_calculo.upper() == 'Y':
        escojer_tarea(etiqueta)
    elif otro_calculo.upper() == 'N':
        print('Adios')
    else:
        otra_opercion()

# Assign obtained authentication token to a variable. Provide APIC-EM's URL address.
auth_token = obtener_token(apic_em_ip)

#Escojer que tarea quiere realizar el usuario

escojer_tarea(etiqueta)

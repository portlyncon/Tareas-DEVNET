#Crear un programa que permita conectarse con el controlador APIC-EM de Cisco
   # El usuario tendrá que escoger la opción que quiera (no tendrá que especificar la url a mano)
    #Añadir, como mínimo, 4 funcionalidades

# Import modules.
import requests
import json

# Disable warnings.
requests.packages.urllib3.disable_warnings()

# Variables
apic_em_ip = "https://sandboxapicem.cisco.com/api/v1"
tarea ="pol"


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
    
    #  list from response 
    hosts = response["response"]
    return hosts
       


def escojer_tarea(tarea):
   
    hosts = obtener_hosts_ip(auth_token, apic_em_ip)

    operacion = input('''
introduce la operacion que quieres realizar:
1 lista IP hosts
2 sumar
3 multiplicar
4 dividir
''')
    if operacion == '1':
        
        tarea ="hostIp"
        print("Listado IP hosts")
     #passar el metode imrpimir hosts a general !!!!!!!!!!!!!!!!!
        for host in hosts: 
            print(host[tarea])
        otra_opercion()
    elif operacion =='2':

        tarea ="hostMac"
        print("Listado mac hosts")
        #  list of hosts
        for host in hosts: 
            print(host[tarea])
        otra_opercion()
    elif  operacion =='3':
   
        tarea ="connectedNetworkDeviceIpAddress"
        print("Listado mac hosts")
        #  list of hosts
        for host in hosts: 
            print(host[tarea])
        otra_opercion()  


def otra_opercion():
    otro_calculo = input('''
quieres realizar otra operacion?
introduce Y para YES o N para NO.
''')

    if otro_calculo.upper() == 'Y':
        escojer_tarea(tarea)
    elif otro_calculo.upper() == 'N':
        print('Adios')
    else:
        otra_opercion()

# Assign obtained authentication token to a variable. Provide APIC-EM's URL address.
auth_token = obtener_token(apic_em_ip)

#Escojer que tarea quiere realizar el usuario

escojer_tarea(tarea)
    

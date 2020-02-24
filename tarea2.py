
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

def obtener_token(url):

    # Define API Call to get authentication token.
    api_call ="/ticket"

    # Payload contains authentication information.
    payload = { "username": "devnetuser", "password": "Cisco123!" }

    # Header information.
    headers = {"content-type" : "application/json"}

    # Add the API call to the URL argument.
    url +=api_call

    response = requests.post(url, data=json.dumps(payload), headers=headers, verify=False).json()

    # Return authentication token from respond body.
    return response["response"]["serviceTicket"]



def obtener_hosts(token, url): 
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
       

# Assign obtained authentication token to a variable. Provide APIC-EM's URL address.
auth_token = obtener_token(apic_em_ip)


#  list of hosts
hosts = obtener_hosts(auth_token, apic_em_ip)


print("Client List from APIC-EM")


for host in hosts: 
    print(host["hostIp"])



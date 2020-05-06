from ncclient import manager
import json
import requests
import xml.dom.minidom
import ast
from tabulate import tabulate
from netmiko import ConnectHandler
from device_info import ios_xe1 as device


#requests.packages.urllib3.disable_warnings()




#api_url = "https://10.10.20.48/restconf/data/ietf-interfaces:interfaces/"

headers = { "Accept": "application/yang-data+json",
            "Content-type":"application/yang-data+json"
            }  
basicauth = ("cisco", "cisco_1234!")


m = manager.connect(
         host="10.10.20.48",
         port=830,
         username="cisco",
         password="cisco_1234!",
         hostkey_verify=False
         )

netconf_data = ""   

def escojer_tarea():

    operacion = input('''
introduce la operacion que quieres realizar:
1 lista interficies
2 lista macs dispositivos
3 localizacion 
4 serialNumber dispositivo
''')
    


    if operacion =='1':

        
        api_url = "https://10.10.20.48/restconf/data/ietf-interfaces:interfaces/"
        resp = requests.get(api_url, auth=basicauth, headers=headers, verify=False)

        data = resp.text    

        
        pol = json.loads(data)
        
        

        cabeceras = ['     nombre     ','       ip         ','      mascara     ']
        
        datos = [[]]
        
       
        cuenta = 0
        
        for value in pol['ietf-interfaces:interfaces']['interface']:
               
                datos[cuenta].append(pol['ietf-interfaces:interfaces']['interface'][cuenta]['name'])
                #print(pol['ietf-interfaces:interfaces']['interface'][cuenta]['name']) 
                if ((pol['ietf-interfaces:interfaces']['interface'][cuenta]['enabled'])):
                    datos[cuenta].append(pol['ietf-interfaces:interfaces']['interface'][cuenta]['ietf-ip:ipv4']['address'][0]['ip'])
                    #print(pol['ietf-interfaces:interfaces']['interface'][cuenta]['ietf-ip:ipv4']['address'][0]['ip'])
                    datos[cuenta].append(pol['ietf-interfaces:interfaces']['interface'][cuenta]['ietf-ip:ipv4']['address'][0]['netmask'])
                    #print(pol['ietf-interfaces:interfaces']['interface'][cuenta]['ietf-ip:ipv4']['address'][0]['netmask'])
                datos.append([])
                print(cuenta)
                cuenta = cuenta +1   
                #print(pol['ietf-interfaces:interfaces']['interface'][cuenta]['name'],pol['ietf-interfaces:interfaces']['interface'][cuenta]['ietf-ip:ipv4']['address'][0]['ip'],pol['ietf-interfaces:interfaces']['interface'][cuenta]['ietf-ip:ipv4']['address'][0]['netmask'])
        print(datos)        
        print(tabulate(datos, headers=cabeceras, floatfmt=".3f"))
        
       
        otra_tarea()
        

    if operacion == '2':

            interficie = input('''
que interficie quieres crear?
''')
            ip = input ('''
que ip quieres poner?
''')

            loopback = {"int_name": interficie,
            "description": "Demo interface by CLI and netmiko",
            "ip": ip,
            "netmask": "255.255.255.0"}

# Create a CLI configuration
            interface_config = [
            "interface {}".format(loopback["int_name"]),
            "description {}".format(loopback["description"]),
            "ip address {} {}".format(loopback["ip"], loopback["netmask"]),
            "no shut"
        ]

# Open CLI connection to device
            with ConnectHandler(ip = device["address"],
                    port = device["ssh_port"],
                    username = device["username"],
                    password = device["password"],
                    device_type = device["device_type"]) as ch:

    # Send configuration to device
                output = ch.send_config_set(interface_config)

                # Print the raw command output to the screen
                print("The following configuration was sent: ")
                print(output)

            otra_tarea()


    if operacion == '3':
            interficie = input('''
que interficie quieres borrar?
''')

##             operacion = input('''
##que interficie queire borrar?
##''')
            
            loopback = {"int_name": interficie}

    # Create a CLI configuration
            interface_config = [
                "no interface {}".format(loopback["int_name"])
    ]

    # Open CLI connection to device
            with ConnectHandler(ip = device["address"],
                        port = device["ssh_port"],
                        username = device["username"],
                        password = device["password"],
                        device_type = device["device_type"]) as ch:

        # Send configuration to device
                output = ch.send_config_set(interface_config)

        # Print the raw command output to the screen
                print("The following configuration was sent: ")
                print(output)
        

            otra_tarea()

    if operacion == '4':

         print("enviando comando sh route")
         ssh_client = ConnectHandler(
         device_type='cisco_ios',
         host="sbx-iosxr-mgmt.cisco.com",
         port=8181,
         username="admin",
         password="C1sco12345"
         )
        
        output= ssh_client.send_command("show ip route")
        
        print("tabla de enrutamiento:\n{}\n".format(output)) 
        
        otra_tarea()



        
            
def otra_tarea():
 otra_accion = input('''
quieres realizar otra operacion?
introduce Y para YES o N para NO.
''')

 if otra_accion.upper() == 'Y':
       escojer_tarea()
 elif otra_accion.upper() == 'N':
        print('Adios')
 else:
        otra_tarea()



    
escojer_tarea()

   

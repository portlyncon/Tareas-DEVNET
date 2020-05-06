


##Esta practica se ha realizado  con la emulación de DE IOSX con reserva en el sandbox de cisco
##
##Con acceso mediente VPN de Cisco i con la ip del servicio 10.10.20.48
##
##Actualmente cisco ha canviado esta infraestructura,pero se ha decidido seguir con esta version debido a la carga de trabajo
##
##que supone ahora mismo realizar los canvios correspondientes
##
##Se han testeado la s4 opciones de forma exitosa
##
##Isaac Estatuet Salmeron 05/05/2020





from ncclient import manager
import json
import re
import sys
import requests
import xml.dom.minidom
import ast
from tabulate import tabulate
from netmiko import ConnectHandler
from device_info import ios_xe1 as device



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
1 lista interficies(CON ANTGUA VIRTUALIZACION DE IOSX 10.10.20.48)
2 crear interficie(CON ANTGUA VIRTUALIZACION DE IOSX 10.10.20.48)
3 borrar inerficie(CON ANTGUA VIRTUALIZACION DE IOSX 10.10.20.48)
4 tabla de enrutamiento(CON ANTGUA VIRTUALIZACION DE IOSX 10.10.20.48)
''')
    


    if operacion =='1':

        
        api_url = "https://sbx-iosxr-mgmt.cisco.com/restconf/data/ietf-interfaces:interfaces/"
        resp = requests.get(api_url, auth=basicauth, headers=headers, verify=False)

        data = resp.text    

        
        pol = json.loads(data)
        
        

        cabeceras = ['     nombre     ','       ip         ','      mascara     ']
        
        datos = [[]]
        
       
        cuenta = 0
        
        for value in pol['ietf-interfaces:interfaces']['interface']:
               
                datos[cuenta].append(pol['ietf-interfaces:interfaces']['interface'][cuenta]['name'])
                
                if ((pol['ietf-interfaces:interfaces']['interface'][cuenta]['enabled'])):
                    datos[cuenta].append(pol['ietf-interfaces:interfaces']['interface'][cuenta]['ietf-ip:ipv4']['address'][0]['ip'])
                   
                    datos[cuenta].append(pol['ietf-interfaces:interfaces']['interface'][cuenta]['ietf-ip:ipv4']['address'][0]['netmask'])
                    
                datos.append([])
                print(cuenta)
                cuenta = cuenta +1   
                
        print(datos)        
        print(tabulate(datos, headers=cabeceras, floatfmt=".3f"))
        
       
        otra_tarea()
   


        otra_tarea()

    if operacion == '2':

            interficie = input('''
que interficie quieres crear?
''')
            ip = input ('''
que ip quieres poner?
''')

            nombre = {"int_name": interficie,
            "description": "Demo interface by CLI and netmiko",
            "ip": ip,
            "netmask": "255.255.255.0"}


            interface_config = [
            "interface {}".format(nombre["int_name"]),
            "description {}".format(nombre["description"]),
            "ip address {} {}".format(nombre["ip"], nombre["netmask"]),
            "no shut"
        ]


            with ConnectHandler(ip = device["address"],
                    port = device["ssh_port"],
                    username = device["username"],
                    password = device["password"],
                    device_type = device["device_type"]) as ch:

    
                output = ch.send_config_set(interface_config)

                
                print("The following configuration was sent: ")
                print(output)

            otra_tarea()


    if operacion == '3':
            interficie = input('''
que interficie quieres borrar?
''')


            
            nombre = {"int_name": interficie}

   
            interface_config = [
                "no interface {}".format(nombre["int_name"])
    ]

   
            with ConnectHandler(ip = device["address"],
                        port = device["ssh_port"],
                        username = device["username"],
                        password = device["password"],
                        device_type = device["device_type"]) as ch:

       
                output = ch.send_config_set(interface_config)

        
                print("The following configuration was sent: ")
                print(output)
        

            otra_tarea()

    if operacion == '4':

       
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

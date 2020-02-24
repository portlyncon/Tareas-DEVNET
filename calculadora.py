import math 
def calculadora():
    operacion = input('''
introduce la operacion que quieres realizar:
- restar
+ sumar
* multiplicar
/ dividir
** potencia
> raiz 
''')
    #s'ha d'afeguir un control exception si no es un int el valor introduit
    numero_1 = int(input('introduce un numero: '))
        
    
    if operacion != '>' and operacion == '-' or operacion =='+' or operacion == '*' or operacion == '/' or operacion == '**':
        print("introduce un operador valido")
        
        numero_2 = int(input('introduce un numero: '))
    else:
        print("introduce un operador valido")

    if operacion == '-':
        
        print('{} - {} = '.format(numero_1, numero_2))
        print(numero_1 - numero_2)

    elif operacion == '+':
        
        print('{} + {} = '.format(numero_1, numero_2))
        print(numero_1 + numero_2)

    elif operacion == '*':
        
        print('{} * {} = '.format(numero_1, numero_2))
        print(numero_1 * numero_2)

    elif operacion == '/':
        
        print('{} / {} = '.format(numero_1, numero_2))
        try :
                print(numero_1 / numero_2)
        except ZeroDivisionError:
                print('no se puede dividir por zero')
    elif operacion == '**':
        
        print('{} * {} = '.format(numero_1, numero_2))
        print(numero_2 ** numero_2)
  
    elif operacion =='>' and  numero_1 > 0:
        
        print(math.sqrt(numero_1))
    else:
        print('no has introducido un operador valido.')

    # Add again() function to calculate() function
    otra_opercion()

def otra_opercion():
    otro_calculo = input('''
quieres realizar otra operacion?
introduce Y para YES o N para NO.
''')

    if otro_calculo.upper() == 'Y':
        calculadora()
    elif otro_calculo.upper() == 'N':
        print('Adios')
    else:
        otra_opercion()

calculadora()

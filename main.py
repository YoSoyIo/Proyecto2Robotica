import math
import random
import matplotlib.pyplot as plt
import numpy as np
import serial

Arduino = serial.Serial("COM7",9600)

# Son los vectores que guargaran las coordenadas
# Ori es el vector de los origenes(Donde esta el robot en ese momento) para graficar
# Izq son las posiciones encontradas en la parte izquierda del robot con el sensor de luz y el servo
# Der son las posiciones encontradas en la parte derecha del robot con el sensor de luz y el servo
# La forma sera (x,y) o si es necesario (distancia, angulo)

ori = []
izq = []
der = []

# Para poder ubicar al robot de forma automatica es necesario guardar los nodos con los cuales podra regresar
# o ir a donde considere necesario

grafo = {
  0: [0,0,1]
}

conexiones = []

# Para poder ubicar a donde voltear, se necesitara un sensor de angulo
sentido = 1
posAct = [0,0]

def PosAleatorias(n):
  x = []
  y = []
  aux = 0
  aux2 = 0
  aux3 = 0

  for i in range(0, 5000, n):
    x.append(0)
    y.append(i)
    aux = i

  for i in range(0, 8000, n):
    x.append(i)
    y.append(aux)
    aux2 = i

  for i in range(aux, -1, -n):
    x.append(aux2)
    y.append(i)
    aux3 = i

  for i in range(aux2, -1, -n):
    x.append(i)
    y.append(aux3)

  return x,y

def LimAlea():
  a = []
  b = []
  for i in range(0,181):
    print(i)
    if(i < 65 or i > 115):
      if(i == 0 or i == 180):
        r = 500
        a.append(round(r * math.cos(i),2))
        b.append(round(r * math.sin(i),2))
      else:
        r = round(500 * math.atan(i),2)
        a.append(round(r * math.cos(i), 2))
        b.append(round(r * math.sin(i), 2))
      print(round(r * math.cos(i), 2),',',round(r * math.sin(i), 2))
  return a,b


def Leer():
  Arduino.write(b'8')
  cadena = Arduino.read(3)
  return str(cadena.decode())

def Navega(sentido, nodos, i, pos, conexiones, tam):
  valor = Leer()
  if(valor == "0"):
    Arduino.write(b'3')
    if sentido == 8:
      sentido = 1
    else:
      sentido +=1
  else:
    Arduino.write(b'1')
    if(sentido == 1):
      pos[1] += tam
    elif (sentido == 2):
      pos[0] += tam*math.cos(45)
      pos[1] += tam*math.sin(45)
    elif (sentido == 3):
      pos[0] += tam
    elif (sentido == 4):
      pos[0] += tam * math.cos(45)
      pos[1] -= tam * math.sin(45)
    elif (sentido == 5):
      pos[1] -= tam
    elif (sentido == 6):
      pos[0] -= tam * math.cos(45)
      pos[1] -= tam * math.sin(45)
    elif (sentido == 7):
      pos[0] -= tam
    elif (sentido == 8):
      pos[0] -= tam * math.cos(45)
      pos[1] += tam * math.sin(45)

    grafo[i+1] = [pos[0],pos[1],sentido]
    conexiones.append([i,i+1])

def ejecuta(sentido,nodo, nodo2):
  a = movimientos[len(movimientos) - 1]
  if (a == "000"):
    regresa()
  elif (a == "001"):
    Arduino.write('1'.encode('ascii'))
  elif (a == "010"):
    Arduino.write('4'.encode('ascii'))
    Arduino.write('1'.encode('ascii'))
    if (sentido == 1):
      sentido = 4
    else:
      sentido -= 1
  elif (a == "100"):
    Arduino.write('3'.encode('ascii'))
    Arduino.write('1'.encode('ascii'))
    if (sentido == 4):
      sentido = 1
    else:
      sentido += 1

print(grafo)
grafo[1] = [0,1,2]
print(grafo[1][0])
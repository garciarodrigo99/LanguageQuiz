import time
import datetime
import csv
import logging
import random
import os

# Defining MACROS
LOG_FILE_NAME = 'history.log'
DATABASE_FILENAME = 'dataBase.csv'
ID_SESSION = int(time.time())
HIT_SYMBOL = '\033[92m' + u'\u2713' + '\033[0m'
FAIL_SYMBOL = '\033[91m' + u'\u2717' + '\033[0m'

# Defining Functions

def clear_screen():
  os.system('clear' if os.name == 'posix' else 'cls')

# Update last session information in CSV
def overWriteFile(lista: list[list[str]]) -> None:
  # Abrir el archivo CSV en modo escritura
  with open(DATABASE_FILENAME, 'w', newline='') as archivo:

    # Crear un objeto escritor de CSV
    escritor_csv = csv.writer(archivo)

    # Escribir todos los datos actualizados en el archivo
    escritor_csv.writerows(lista)

# Delete non-visible words
def filterByVisibility(lista: list[list[str]]) -> dict:
  filter = {}
  # Filtro visibilidad
  for elemento in range(len(lista)):
    if lista[elemento][0]:
      filter[lista[elemento][1]] = elemento
  return filter

# Set to false the words asked in the penultimate session
def eraseLastSessionData(lista: list[list[str]]) -> None:
  nColumns = len(lista[0])
  for word in lista:
    # isAskedLastSession
    word[nColumns-2] = 0
    word[nColumns-1] = 0

# Save in a list of lists object i+the content of CSV
def readAndCopy() -> list[list[str]]:
  # Abrir el archivo CSV original en modo lectura
  with open(DATABASE_FILENAME,'r') as archivo_origen:
    # Crear un objeto lector de CSV
    lector_csv = csv.reader(archivo_origen)
    next(lector_csv)
    # Leer el contenido del archivo original y almacenarlo en una lista
    dataBase = list(lector_csv)
    return dataBase

# Erase all information of each word in CSV
def resetInformation(lista: list[list[str]]) -> None:
  nColumns = len(lista[0])
  for word in lista:
    word[0] = 1
    nWords = 2
    for i in range(nWords+1,nColumns):
      word[i] = 0
  overWriteFile(lista)
  logging.info(f'[{ID_SESSION}] Database reseted')

# Save in a dict the words that are going to be asked
def setSelection(dataBase: list[list[str]], filter: dict) -> dict:
  for clave, valor in filter.copy().items():
    selection = {}
    # Add recent failures
    if (int(dataBase[valor][7]) == True) and (int(dataBase[valor][8]) == False):
      selection[clave] = valor
      del filter[clave]
    else:
      if int(dataBase[valor][3]) == minTimesAsked: continue
      del filter[clave]

  while len(selection) < numberofWords:
    index = random.choice(list(filter.values()))
    word = dataBase[index][1]
    if word not in selection:
      selection[word] = index

  return selection

# Configurar el módulo de logging
logging.basicConfig(filename=LOG_FILE_NAME,level=logging.INFO)
logging.info(f'{datetime.datetime.now()} {ID_SESSION}')

dataBase = readAndCopy()
resetInformation(dataBase)
exit()

# numberofWords = int(input("Número de palabra que desea trabajar: "))
numberofWords = 10

filter = filterByVisibility(dataBase)

minTimesAsked = min(int(dataBase[i][4]) for i in filter.values())

selection = setSelection(dataBase,filter)

answer = []
hits = []

for clave,valor in selection.items():
  iterationAnswer = input(f"{clave}: ")
  answer.append(iterationAnswer)
  if dataBase[int(valor)][2] == iterationAnswer:
    hits.append(True)
  else:
    hits.append(False)

counter = hits.count(True)

print(f"¡Aciertos: {counter}/{len(hits)}!")
logging.info(f'[{ID_SESSION}] Hits: {counter}/{len(hits)}')

eraseLastSessionData(dataBase)

# Actualizar valores sesion actual
for i, (clave, valor) in enumerate(selection.items()):
  # timesAsked
  dataBase[int(valor)][3] = int(dataBase[int(valor)][3]) + 1
  
  if hits[i] == True:
    # timesCorrect
    dataBase[int(valor)][4] = int(dataBase[int(valor)][4]) + 1
    # consecTimesCorrect
    dataBase[int(valor)][5] = int(dataBase[int(valor)][5]) + 1
    # isCorrectLastSession
    dataBase[int(valor)][8] = 1
    print(f"{HIT_SYMBOL} {dataBase[int(valor)][1]} -> {dataBase[int(valor)][2]}")
  else:
    # consecTimesCorrect
    dataBase[int(valor)][5] = 0
    # isCorrectLastSession
    dataBase[int(valor)][8] = 0

    print(f"{FAIL_SYMBOL}({answer[i]}){FAIL_SYMBOL} {dataBase[int(valor)][1]} -> {dataBase[int(valor)][2]}")

  # lastSessionAsked
  dataBase[int(valor)][6] = ID_SESSION
  # isAskedLastSession
  dataBase[int(valor)][7] = 1

overWriteFile(dataBase)
import sys
import time

import ConnectionDB
from LogObj import EscreverTela, EscreverTelaMesmaLinha
from datetime import datetime


print(sys.version)

#pip install pipreqs
#pipreqs --force ./

for i in range(10):
    with open('fileTxt.txt','a+') as myFile:
        myFile.write('{}\t{}\n'.format(str(datetime.now().strftime('%H:%M:%S')), i+1))


EscreverTela('teste1')
EscreverTelaMesmaLinha('teste2')
EscreverTelaMesmaLinha('teste3')
EscreverTela('teste4')
EscreverTela('teste5')
EscreverTelaMesmaLinha('teste6')
EscreverTelaMesmaLinha('teste7')
EscreverTela('teste8')


for i in range(101):
    s = str(i) + '%'                        # string for output
    EscreverTelaMesmaLinha(s)                        # just print and flush
    time.sleep(0.2)                         # sleep for 200ms


s1 = datetime.now()

print('Inicio em: {}'.format(s1.strftime('%A, %d/%B/%Y %H:%M:%S')))

time.sleep(10)  # or do something more productive

s2 = datetime.now()
tdelta = s2 - s1
tempoGasto = ''

plural = '(s)' if tdelta.days > 1 else ''
if tdelta.days > 0:
    tempoGasto += '{} dia{} '.format(tdelta.days, plural)

hour = tdelta.seconds//3600
plural = '(s)' if hour > 1 else ''
if hour > 0:    
    tempoGasto += '{} hora{} '.format(hour, plural)

minutes = (tdelta.seconds//60)%60
tempoGasto += '{} min e {} seg'.format(minutes, tdelta.seconds)
print('Tempo Gasto: {}'.format(tempoGasto))
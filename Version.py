import sys
import time

import ConnectionDB
from LogObj import EscreverTela, EscreverTelaMesmaLinha
from datetime import datetime
import TelegramBotMsg
import time


for x in range (0,5):  
    b = "Loading" + "." * x
    print (b, sep=' ', end='', flush=True)
    time.sleep(1)

for i in range(0, 3):
    # EscreverTela('\r'*99, False, False)
    EscreverTelaMesmaLinha('{} de {}\t'.format(i+1, 3))

EscreverTela('', False, True)


TelegramBotMsg.send_message('tab\t~~funciona?~~ e\\agora   ?\n')

TelegramBotMsg.send_message('[16/04 – iPhone X Gold, Vazamentos, Bate-Papo com Livros e muito mais](http://feeds.cocatech.com.br/~r/cocatechpodcast/~3/pHOGQEwKHSo/16-de-abril-de-2018)')

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
import sys

import ConnectionDB
from Classes import DateTimeDiff, GetDate, LogObj


class MsgObj(object):
    pass


logObj = LogObj()
logObj.msgs = []

qtChars = 0

def Inicio():
    logObj.dataInicio = GetDate()
    Escrever('Inicio...', 0)


def EscreverLog(texto):
    msg = MsgObj()
    msg.dataHora = GetDate()
    msg.Texto = texto
    logObj.msgs.append(msg)

def EscreverTela(texto, data = True, linhanova = True):
    s = '\r'
    if data:
        s += '{}\t'.format(GetDate())
    s += texto

    global qtChars    # Needed to modify global copy of globvar
    qtChars = len(s)
    e = '\n' if linhanova else '\r'
    print(s, end=e)


def ApagarLinhaTela(n):
    print(' ' * n, end='\r')


def EscreverTelaMesmaLinha(texto):    
    # ApagarLinhaTela(99)
    EscreverTela(texto, True, False)


def Escrever(texto, nivel=0):
    EscreverLog(texto)
    EscreverTela(('\t'*nivel) + texto)


def Resultado(value):
    logObj.sucesso = value
    Escrever('Resultado. Sucesso: {}'.format(str(value)), 0)


def Sucesso():
    Resultado(True)


def Erro(erro):
    Escrever('Exceção: {}'.format(erro), 0)
    Resultado(False)


def Alterado(value):
    logObj.alterado = value


def FinalizarLog():
    logObj.dataFim = GetDate()
    Escrever('FINALIZADO', 0)
    # Escrever(DateTimeDiff(logObj.dataInicio, logObj.dataFim))
    json = logObj.toJSON()
    ConnectionDB.InsertLog(json)

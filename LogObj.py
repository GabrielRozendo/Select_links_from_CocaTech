import ConnectionDB
from Classes import GetDate, LogObj


class MsgObj(object):
    pass


logObj = LogObj()
logObj.msgs = []


def Inicio():
    logObj.dataInicio = GetDate()
    Escrever('Inicio...', 0)


def EscreverLog(texto):
    msg = MsgObj()
    msg.dataHora = GetDate()
    msg.Texto = texto
    logObj.msgs.append(msg)


def EscreverTela(texto):
    print('{}\t{}'.format(GetDate(), texto))


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
    json = logObj.toJSON()
    ConnectionDB.InsertLog(json)

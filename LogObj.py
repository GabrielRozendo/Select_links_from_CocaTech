import json

import ConnectionDB


class LogObj(object):
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


class MsgObj(object):
    pass


logObj = LogObj()
logObj.msgs = []


def Inicio():
    logObj.dataInicio = ConnectionDB.GetDate()
    Escrever('Inicio...')


def EscreverLog(texto):
    msg = MsgObj()
    msg.dataHora = ConnectionDB.GetDate()
    msg.Texto = texto
    logObj.msgs.append(msg)


def EscreverTela(texto):
    print('{}\t{}'.format(ConnectionDB.GetDate(), texto))


def Escrever(texto):
    EscreverLog(texto)
    EscreverTela(texto)


def Resultado(value):
    logObj.sucesso = value
    Escrever('Resultado: {}'.format(str(value)))


def Sucesso():
    Resultado(True)


def Erro(erro):
    Escrever('Exceção: {}'.format(erro))
    Resultado(False)


def Alterado(value):
    logObj.alterado = value


def FinalizarLog():
    logObj.dataFim = GetDate()
    value = logObj.toJSON()
    value = json.loads(value)
    ConnectionDB.InsertLog(value)

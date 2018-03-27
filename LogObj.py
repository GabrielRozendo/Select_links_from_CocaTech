import ConnectionDB
import json

class LogObj(object): 
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

class MsgObj(object):
    pass


logObj = LogObj()
logObj.msgs = []


def Inicio():
    logObj.dataInicio = ConnectionDB.GetDate()
    Registrar('Inicio...', True)


def Registrar(texto, tela=False):
    dataHora = ConnectionDB.GetDate()
    msg = MsgObj()
    msg.dataHora = dataHora
    msg.Texto = texto
    logObj.msgs.append(msg)

    if tela:
        print('{}\t{}'.format(dataHora, texto))


def FinalizarLog():
    logObj.dataFim = ConnectionDB.GetDate()
    value = logObj.toJSON()
    value = json.loads(value)
    ConnectionDB.InsertLog(value)



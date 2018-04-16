from datetime import datetime 
import json
import warnings
from enum import Enum


def GetDate():
    return str(datetime.now())

def GetTime():
    return str(datetime.now().strftime('%H:%M:%S'))


def InList(lstBuscar, conteudo):
    return any(x in conteudo for x in lstBuscar)


def InListAnyInS(lstBuscar, conteudo):
    if isinstance(conteudo, (list)):
        conteudoUpper = [x.upper() for x in conteudo]
    else:
        conteudoUpper = conteudo.upper()

    lstBuscarUpper = [x.upper() for x in lstBuscar]
    return any(x in conteudoUpper for x in lstBuscarUpper)


def InListAllInS(lstBuscar, conteudo):
    if isinstance(conteudo, (list)):
        conteudoUpper = [x.upper() for x in conteudo]
    else:
        conteudoUpper = conteudo.upper()

    lstBuscarUpper = [x.upper() for x in lstBuscar]
    return all(x in conteudoUpper for x in lstBuscarUpper)


class LogObj:
    def toJSON(self):
        dumps = json.dumps(self, default=lambda o: o.__dict__, sort_keys=False, indent=4)
        return json.loads(dumps)


class PostFeed(object):
    def __init__(self, titulo, tags, link, data, origem):
        self.titulo = titulo
        self.tags = tags
        self.link = str(link)
        self.data = data
        self.origem = origem
        self.criadoEm = GetDate()

    def toJSON(self):
        dumps = json.dumps(self, default=lambda o: o.__dict__, sort_keys=False, indent=4)
        return json.loads(dumps)


class TipoLink(Enum):
    Desconhecido = 'Desconhecido'
    AppStore = 'Apple Store (iOS)'
    Mac = 'Mac Store'
    PlayStore = 'Google Play Store (Android)'
    News = 'Notícias'
    Video = 'Vídeo'
    Crowdfunding = 'Crowdfunding'


class LinkObj(object):
    def __init__(self, fonte, texto, postUrl, link, tipoLink):
        self.fonte = fonte
        self.texto = texto
        self.postUrl = postUrl
        self.link = str(link)
        self.tipo = tipoLink.value
        self.criadoEm = GetDate()

    
    def toJSON(self):
        dumps = json.dumps(self, default=lambda o: o.__dict__, sort_keys=False, indent=4)
        return json.loads(dumps)


def DateTimeDiff(s1, s2):
    tdelta = s2 - s1
    tempoGasto = ''

    plural = '(s)' if tdelta.days > 1 else ''
    if tdelta.days > 0:
        tempoGasto += '{} dia{} '.format(tdelta.days, plural)

    hora = tdelta.seconds//3600
    plural = '(s)' if hora > 1 else ''
    if hora > 0:    
        tempoGasto += '{} hora{} '.format(hora, plural)

    minutos = (tdelta.seconds//60)%60
    plural = '(s)' if minutos > 1 else ''
    if minutos > 0:    
        tempoGasto += '{} minuto{} '.format(minutos, plural)

    tempoGasto += '{} seg'.format(tdelta.seconds)

    return tempoGasto
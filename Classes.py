import datetime
from enum import Enum


def GetDate():
    return str(datetime.datetime.now())


class PostFeed(object):
    def __init__(self, title, tags, link, data, origem):
        self.title = title
        self.tags = tags
        self.link = link
        self.data = data
        self.origem = origem


class TipoLink(Enum):
    Desconhecido = 'Desconhecido'
    AppStore = 'Apple Store (iOS)'
    Mac = 'Mac Store'
    PlayStore = 'Google Play Store (Android)'
    News = 'Notícias'
    Video = 'Vídeo'
    Crowdfunding = 'Crowdfunding'


class LinkObj(object):
    def __init__(self, fonte, titulo, postUrl, link, tipoLink):
        self.fonte = fonte
        self.titulo = titulo
        self.postUrl = postUrl
        self.link = str(link)
        self.tipo = tipoLink.value


class Sources(Enum):
    CocaTech = 'Coca Tech'
    LoopMatinal = 'Loop Matinal'
    AreaTransferencia = 'Área de Transferência'

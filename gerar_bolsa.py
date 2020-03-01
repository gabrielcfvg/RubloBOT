from pickle import dumps
from gen_graph import gen_graph

class Bolsas():

    def __init__(self, media, nome):
        self.media = media
        self.valor = media
        self.nome = nome
        self.hist = [0 for A in range(900)]
    
    def passar(self):
        
        self.valor = gen_graph(1, self.media, self.valor)[0]
        self.hist.insert(0, self.valor)
        self.hist.pop()

nome = input('nome:')
obj = Bolsas(int(input('media:')), nome)
open(f'./bolsas/{nome}', 'wb').write(dumps(obj))

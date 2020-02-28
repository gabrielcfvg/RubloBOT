import discord, datetime, time, pickle, traceback, threading, time
from discord.ext import commands
from os.path import exists
from sys import exc_info
from os import listdir
from gen_graph import gen_graph


#VARIAVEIS
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

token = open("token.txt", 'r', encoding='utf-8-sig').read()
cliente = commands.Bot(command_prefix='ru!')
log = "log.txt"
database = "./camaradas/"
database_bolsas = './bolsas/'


#FUNÇÕES
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

def loop_bolsas():

    while True:

        for A in listdir(database_bolsas):

            bolsa = pickle.loads(open(database_bolsas + A, 'rb').read())
            bolsa.passar()          
            open(database_bolsas + A, 'wb').write(pickle.dumps(bolsa))
            del bolsa
        
        time.sleep(5)


class Bolsas():

    def __init__(self, media, nome):
        self.media = media
        self.valor = media
        self.nome = nome
    
    def passar(self):
        
        self.valor = gen_graph(1, self.media, self.valor)[0]


class Camarada:

    next_work = 0
    ações = {}

    def __init__(self):
        self.rublos = 0
            
    def trabalhar(self, num):

        self.rublos += num*funções.eficiencia_de_trabalho(num)
        self.next_work = (int(time.time()))+num*60
    
    def next_work_data(self):

        return datetime.datetime.fromtimestamp(self.next_work).strftime('%Y-%m-%d %H:%M:%S')


class Resposta:

    @staticmethod
    async def ping(enviar):
        
        await enviar(f"{round(cliente.latency * 1000)}ms")

    @staticmethod
    async def registrar(enviar, autor):
        
        if not exists(database+str(autor.id)):
            new_obj = Camarada()
            open(database+str(autor.id), 'wb').write(pickle.dumps(new_obj))
            del new_obj
            
            await enviar("Registrado com sucesso")
        
        else:
            
            await enviar("registro já existente!")
        
    @staticmethod
    async def conta(enviar, autor):

        if funções.verificar(autor):
        
            obj = pickle.loads(open(database+str(autor.id), 'rb').read())
            valor = obj.rublos
            open(database+str(autor.id), 'wb').write(pickle.dumps(obj))
            del obj
            
            await enviar(f"Você possui {valor} rublos")
        
        else:
            
            await enviar("Você ainda não está registrado")

    #temp
    @staticmethod
    def aumentar(autor, num):

        if funções.verificar(autor):

            obj = pickle.loads(open(database+str(autor.id), 'rb').read())
            obj.rublos += num
            open(database+str(autor.id), 'wb').write(pickle.dumps(obj))
            del obj
            return "Aumentado com sucesso!"
        else:
            return "Você ainda não está registrado"
    
    #temp
    @staticmethod
    def diminuir(autor, num):

        if funções.verificar(autor):

            obj = pickle.loads(open(database+str(autor.id), 'rb').read())
            obj.rublos -= num
            open(database+str(autor.id), 'wb').write(pickle.dumps(obj))
            del obj
            return "Diminuído com sucesso!"
        else:
            return "Você ainda não está registrado"

    @staticmethod
    async def ajuda(enviar, mensagem):
        from helpfiles_base import helpfile

        split = mensagem.split(' ')
        msg = split[1] if len(split) == 2 else "default"
        
        
        if msg in helpfile:
            
            return open(helpfile[msg], 'r', encoding='utf-8').read()
        
        else:
            return "Ajuda não existente para este comando"
            
        del helpfile

    @staticmethod
    async def trabalhar(enviar, autor, mensagem):
        
        num = int(mensagem.split(' ')[1])

        #---------------------------

        if funções.verificar(autor):
            
            obj = pickle.loads(open(database+str(autor.id), 'rb').read())
            if obj.next_work < time.time():
                
                if num <= 0:
                    return "Não é possivel trabalhar por um valor negativo ou nulo"
                elif num > 1440:
                    return "Não é possivel trabalhar por um periodo maior que 24 horas"
                
                obj.trabalhar(num)


            else:
                return f"Você só poderá trabalhar novamente em {obj.next_work_data()}"

            temp = obj.next_work_data()
            open(database+str(autor.id), 'wb').write(pickle.dumps(obj))
            del obj

            return f"Trabalho concluido com sucesso, eficiencia de {funções.eficiencia_de_trabalho(num)} rublos por minuto, foram adicionados {num*funções.eficiencia_de_trabalho(num)} rublos a sua conta, só poderá trabalhar novamente em {num} minutos, ou seja, {temp}"
    
    @staticmethod
    async def rank(enviar):
        
        saida = discord.Embed(title="Ranking", description="Ranking dos camaradas mais ricos do servidor", color=0x00ff00)
        saida.add_field(name=':', value=funções.forbes())
        
        await enviar(embed=saida)

    @staticmethod
    async def bolsa_valores(enviar):
        
        await enviar(funções.bolsa_valores())

    @staticmethod
    async def compra_venda_ações(enviar, mensagem, autor):

        if funções.verificar(autor):
            
            li = mensagem.split(' ')
            
            ação = li[2]
            if li[1] == "comprar":
                op = 1
            elif li[1] == "vender":
                op = 2

            num = int(li[3])

            await enviar(funções.comprar_vender_ações(autor, ação, num, op))

        else:
            await enviar("Você não está registrado")

    #temp
    @staticmethod
    async def teste(enviar):

        await enviar("funcionou")


class funções:

    @staticmethod
    def erro(error):
        open(log, 'a', encoding='utf-8').write(f"\n-------------------------------\n{datetime.datetime.now()}\n{error}\n-----------------------------------------\n\n")


    @staticmethod
    def verificar(autor):
        return True if exists(database+str(autor.id)) else False


    @staticmethod
    def eficiencia_de_trabalho(num):

        if num <= 5:
            return 40 
        elif num > 5 and num <= 20:
            return 50   
        elif num > 20 and num <= 60:
            return 40    
        elif num > 60 and num <= 300:
            return 30   
        elif num > 300 and num <= 600:
            return 20   
        elif num > 600 and num <= 1440:
            return 13


    @staticmethod  
    def forbes():

        server = cliente.get_guild(272166101025161227)
        data = []
        for A in listdir(database):

            obj = pickle.loads(open(database + A, 'rb').read())
            
            data.append([str(server.get_member(int(A))), obj.rublos])

            open(database + A, 'wb').write(pickle.dumps(obj))
            del obj
        
        data.sort(key=lambda num: num[1], reverse=True)


        saida = ''
        saida += '```diff\n'

        for A in range(21 if len(data)> 20 else len(data)):
            temp1 = f"\n{'-' if A%2 else '+'}{('0'+str(A+1)) if A+1 < 10 else A+1} - {data[A][0]}"
            temp2 = f"{'-'*(30-len(temp1))}{data[A][1]}"
            saida += temp1+temp2
        
        saida += '\n';saida += '\n```'

        return saida
    

    @staticmethod
    def bolsa_valores():

        saida = ''
        for A in listdir(database_bolsas):

                bolsa = pickle.loads(open(database_bolsas + A, 'rb').read())
                saida += str(bolsa.nome)+' = '+str(bolsa.valor)+'\n'
                open(database_bolsas + A, 'wb').write(pickle.dumps(bolsa))
                del bolsa
        return saida
    

    @staticmethod
    def comprar_vender_ações(autor, ação, num, op):
        import helpfiles_base
        
        obj = pickle.loads(open(database + str(autor.id), 'rb').read())
        bolsa = pickle.loads(open(helpfiles_base.ações[ação], 'rb').read())
        saida = ''
        if op == 1:
            
            if obj.rublos >= bolsa.valor*num:           
                
                obj.rublos -= bolsa.valor*num
                
                if ação in obj.ações:
                    obj.ações[ação] += num
                else:
                    obj.ações[ação] = num
                
                
                bolsa.valor += num*8

                saida = "Ações compradas com sucesso"
            
            else:
                saida = "Rublos insuficientes para compra"
        
        elif op == 2:

            if ação in obj.ações:
                if obj.ações[ação] >= num:
                    
                    obj.rublos += bolsa.valor*num
                    obj.ações[ação] -= num
                    bolsa.valor -+ num*8

                    saida = "Ações vendidas com sucesso"
                
            else:
                saida = "Ações insuficientes para realizar a venda"
        
        open(helpfiles_base.ações[ação], 'wb').write(pickle.dumps(bolsa))
        open(database + str(autor.id), 'wb').write(pickle.dumps(obj))
        del obj
        del bolsa
        del helpfiles_base

        return saida


#PROGRAMA PRINCIPAL
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
threading.Thread(target=loop_bolsas, daemon = True).start()

@cliente.event
async def on_ready():

    print('\n######\n  ON\n######')
    print(datetime.datetime.now())
    print("\n"*2)

@cliente.event
async def on_message(message):
    
    if message.content.startswith('ru'):
         
        if message.author.bot == False:

            try:
                #=====================================
                mensagem = message.content[3:]
                enviar = message.channel.send
                autor = message.author
                #=====================================

                if mensagem.startswith('ping'):
                    
                    await Resposta.ping(enviar)

                elif mensagem.startswith("registrar"):

                    await Resposta.registrar(enviar, autor)
                
                #temp
                elif mensagem.startswith("aumentar"):

                    valor = int(mensagem.split(' ')[1])
                    await enviar(Resposta.aumentar(autor, valor))
                
                #temp
                elif mensagem.startswith("diminuir"):

                    valor = int(mensagem.split(' ')[1])
                    await enviar(Resposta.diminuir(autor, valor))
                
                elif mensagem.startswith("conta"):

                    await Resposta.conta(enviar, autor)

                elif mensagem.startswith("trabalhar"):
                    
                    await Resposta.trabalhar(enviar, autor, mensagem)

                #temp
                elif mensagem.startswith("mod"):

                    obj = pickle.loads(open(database+str(autor.id), 'rb').read())
                    obj.next_work = 0
                    open(database+str(autor.id), 'wb').write(pickle.dumps(obj))
                    del obj
                
                elif mensagem.startswith("rank"):
                    
                    await Resposta.rank(enviar)

                elif mensagem.startswith("bolsas"):
                    
                    await Resposta.bolsa_valores(enviar)

                elif mensagem.startswith("ações"):

                    await Resposta.compra_venda_ações(enviar, mensagem, autor)

                #temp
                elif mensagem.startswith("teste"):

                    await Resposta.teste(enviar)

                elif mensagem.startswith("ajuda"):

                    await Resposta.ajuda(enviar, mensagem)

                else:
                    await enviar("Comando não existente!")

            except Exception as error:
                funções.erro(error)
                traceback.print_tb(error.__traceback__)
                await enviar("Ocorreu um erro camarada\n Utilize o comando 'ru ajuda' para ler a documentação dos comandos")
            

#FIM
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

cliente.run(token)
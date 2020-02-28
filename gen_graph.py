
def gen_graph(size, media, start=False, high=1.7, mid=1.2):

    from random import randint

    saida = []
    n1 = start if start != False else media

    X = 0
    Y = 0

    for A in range(size):
        a = randint(100, 200)
        
        if n1 >= media/mid and n1 <= media*mid:
            X = int(a*-1)
            Y = int(a)
            
        
        elif n1 < media:

            if n1 < media/mid:              
                X = int((a*-1)/2)
                Y = int(a)
                

            elif n1 < media/high:
                X = int((a*-1)/5)
                Y = int(a)
                

        elif n1 > media:
            
            if n1 > media*mid:              
                X = int((a*-1))
                Y = int(a/2)
                

            elif n1 > media*high:
                X = int((a*-1))
                Y = int(a/5)
                
        n1 += randint(X, Y)
        saida.append(n1)

    return saida



class dic():

    N = 134404155.0 # suma de todas  las frecuencias absolutas
    PALABRAS = dict()

    with open('C:/Users/Ant2D/Desktop/WaoMovies/Wao/apps/peliculas/frecuencia.txt', 'r') as datafile:
        for line in datafile:
            valores = line.strip('\n').split()
            PALABRAS[valores[1]] = int(valores[2])

    def P(self, palabra, N=sum(PALABRAS.values())): 
        "Probabilidad de `palabra`."
        return PALABRAS[palabra] / N

    def correccion(self, palabra): 
        "Corrección más probable de una palabra."
        return max(candidatos(palabra), key=P)

    def candidatos(self, palabra): 
        "Genera posibles correcciones para una palabra."
        return (conocidas([palabra]) or conocidas(edicion1(palabra)) or conocidas(edicion2(palabra)) or [palabra])

    def conocidas(self, palabras): 
        "El subconjunto de `palabras` que aparecen en el diccionario de PALABRAS."
        return set(w for w in palabras if w in PALABRAS)

    def edicion1(self, palabra):
        "Todas las ediciones que están a una edición de `palabra`."
        letras    = 'abcdefghijklmnopqrstuvwxyzáéíóúüñ'
        divisiones     = [(palabra[:i], palabra[i:])    for i in range(len(palabra) + 1)]
        omisiones    = [L + R[1:]               for L, R in divisiones if R]
        transposiciones = [L + R[1] + R[0] + R[2:] for L, R in divisiones if len(R)>1]
        remplazos   = [L + c + R[1:]           for L, R in divisiones if R for c in letras]
        inserciones    = [L + c + R               for L, R in divisiones for c in letras]
        return set(omisiones + transposiciones + remplazos + inserciones)

    def edicion2(self, palabra): 
        "Todas las ediciones que están a dos ediciones de `palabra`."
        return (e2 for e1 in edicion1(palabra) for e2 in edicion1(e1))


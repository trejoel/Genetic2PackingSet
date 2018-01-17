#    Este archivo es parte de DEAP.

#

#    DEAP es un sofware libre: puedes redistribuirlo  y/o modificarlo

#    esta bajo los terminos de la GNU Lesser General Public License es

#    publicado por la fundacion de software libre, posterior de la version 3 de

#    la licencia, o ( a tu opinion ninguna version posterior.

#

#    DEAP is distributed in the hope that it will be useful,

#    but WITHOUT ANY WARRANTY; without even the implied warranty of

#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the

#    GNU Lesser General Public License for more details.

#

#    You should have received a copy of the GNU Lesser General Public

#    License along with DEAP. If not, see <http://www.gnu.org/licenses/>.





#    Ejemplo que busca maximizar la cantidad de enteros en una solucion

#    en donde cada valor puede ser 0 o 1



import random



import numpy as np



from deap import base

from deap import creator

from deap import tools



_MA=[[1,1,1,0,0,0,0],[1,1,1,1,0,0,0],[1,1,1,0,1,0,0],[0,1,0,1,1,1,0],[0,0,1,1,1,1,0],[0,0,0,1,1,1,1],[0,0,0,0,0,1,1]]

e=np.matmul(_MA,_MA)

for i in range(7):

    e[i][i]=0

tsolucion=7

#Se crea la funcion que asigna el fitnnes  de tipo maximisacion

creator.create("FitnessMax", base.Fitness, weights=(1.0,))

#Se define el tipo de dato que es el gen del algoritmo

creator.create("Individual", list, fitness=creator.FitnessMax)

#Se crea una instancia de la clase Toolbox con los metodos para algoritmos geneticos

toolbox = base.Toolbox()



# Generador de atributos

#                      define  a 'attr_bool' como un atributo ('gene')

#                      que corresponde a enteros aleatorios de forma equitativa

#                      en el rango de  [0,1] (i.e. 0 o 1 con igual

#                      probabilidad)

toolbox.register("attr_bool", random.randint, 0, 1)



# Inicializacion de estructuras

#                         define  'individual' como un individuo

#                         consistiendo de  100 'attr_bool' elementos  ('genes')

toolbox.register("individual", tools.initRepeat, creator.Individual, 

    toolbox.attr_bool, tsolucion)



# define la poblacion como una lista de individuos

toolbox.register("population", tools.initRepeat, list, toolbox.individual)



# la funcion objetivo  ('fitness')  que se busca maximizar

def eval2packing(x):

    """s=0

    su=[]

    if sum(x)==0:

        for k in range(len(x)):

            su.append(-100)

    else:

        for i in range(len(x)):

            if x[i]==1:

                for j in range(len (x)):

                    if e[i][j]==0:

                        s+=1

                    if e[i][j]!=0:

                        s-=1

                su.append(s)"""

    f=0

    for i in range(len(x)):

        f+=x[i]

        penaliza=0

        for j in range(i,len(x)):

            penaliza+=e[i][j]*x[j]

        penaliza*=len(x)*x[i]

        f-=penaliza

            

    return float(f),



#----------

# Registro de Operadores

#----------

# Registra el objetivo / funcion para determinar fitness 

toolbox.register("evaluate", eval2packing)



# registro del operador de crusamiento

toolbox.register("mate", tools.cxTwoPoint)



# registra un operador de mutacion con una probabilidad  de 

# cambiar cada atributo/gen del  0.05

toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)



# registro del operador que selecciona a los individuos para crear la siguiente

# generacion: cada individuo de la actual generacion 

# es remplazado por el 'fittest' (mejor) de tres individuos

# trazando aleatoreamente  desde la actual generacion .

toolbox.register("select", tools.selTournament, tournsize=3)



#----------

#Se declara el metodo principal que contendra el algoritmo genetico

def main():

    print("La matriz cuadrada es :")

    print(e)

    random.seed(64)



    # crea una poblacion inicial de 300 individuos (Donde

    # cada individuo es una lista de enteros)

    pop = toolbox.population(n=200)



    # CXPB  es la probabilidad con la que cada dos individuos

    #       son cruzados 

    #

    # MUTPB es la probabilidad para mutar un  individuo

    CXPB, MUTPB = 0.5, 0.2

    

    print("Comienza la Evolucion")

    

    # Evalua la problacion entera

    fitnesses = list(map(toolbox.evaluate, pop))

    for ind, fit in zip(pop, fitnesses):

        ind.fitness.values = fit

    

    print("  Evaluado %i individuos" % len(pop))



    # Extrallendo todos los  fitnesses de 

    fits = [ind.fitness.values[0] for ind in pop]



    # Nimero de generaciones

    g = 0

    

    # Comienza la evolucion

    while  g < 100:

        # Una nueva generacion 

        g = g + 1

        print("-- Generacion  %i --" % g)

        

        # Selecciona la siguiente generacion de individuos

        offspring = toolbox.select(pop, len(pop))

        #Clona la descendencia 

        offspring = list(map(toolbox.clone, offspring))

    

        # Aplica el cruzamiento y mutacion en la descendencia 

        for child1, child2 in zip(offspring[::2], offspring[1::2]):



            # Cruza dos individuos con probabilidad CXPB

            if random.random() < CXPB:

                toolbox.mate(child1, child2)



                # fitness valores de los hijos

                # para ser recalculados despues

                del child1.fitness.values

                del child2.fitness.values



        for mutant in offspring:



            # muta un individuo con probabilidad MUTPB

            if random.random() < MUTPB:

                toolbox.mutate(mutant)

                del mutant.fitness.values

    

        # Evalua los individuos con un fitness invalido

        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]

        fitnesses = map(toolbox.evaluate, invalid_ind)

        for ind, fit in zip(invalid_ind, fitnesses):

            ind.fitness.values = fit

        

        print("  Evaluados %i individuos" % len(invalid_ind))

        

        # la poblacion es enteramente remplasada por la descendencia

        pop[:] = offspring

        

        # Reune todos los fitnesses en una lista e imprime las estadisticas

        fits = [ind.fitness.values[0] for ind in pop]

        

        length = len(pop)

        mean = sum(fits) / length

        sum2 = sum(x*x for x in fits)

        std = abs(sum2 / length - mean**2)**0.5

        

        print("  Min fitness %s" % min(fits))

        print("  Max fitness %s" % max(fits))

        print("  Media %s" % mean)

        print("  Std %s" % std)

    

    print("-- Fin de (Termino) la evolucion --")

    

    best_ind = tools.selBest(pop, 1)[0]

    print("El mejor individuo es  %s, %s" % (best_ind, best_ind.fitness.values))



if __name__ == "__main__":

    main()





















        

        



    


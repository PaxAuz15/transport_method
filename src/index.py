from pulp import *

#SETS
arrocera = ['Isidro Ayora','Santa Lucía', 'Pedro Carbo']
plantas = ['Daule','Naranjal','Durán']

#Diccionario de la cantidad maxima que puede ser trasladada por cada planta
mship= {'Daule' : 200000,
        'Naranjal' : 600000,
        'Durán' : 225000}
#Diccionario de la cantidad maxima que puede proveer cada arrocera
produccion = {  'Isidro Ayora': 275000,
                'Santa Lucía' : 400000,
                'Pedro Carbo' : 300000}

#Diccionar de la cantidad en km de la distancia entre arroceras y plantas
distancia = {   'Isidro Ayora': {'Daule':21,'Naranjal':50,'Durán':40},
                'Santa Lucía' : {'Daule':35,'Naranjal':30,'Durán':22},
                'Pedro Carbo' : {'Daule':55,'Naranjal':20,'Durán':25}}

#Set Problem Variable
prob = LpProblem("Transportation", LpMinimize)

routes = [(i,j) for i in arrocera for j in plantas]

#Variables de decision
amount_vars = LpVariable.dicts("ShipAmount",(arrocera,plantas),0)

#Funcion Objetivo
prob += lpSum(amount_vars[i][j]*distancia[i][j] for (i,j) in routes)

#CONSTRAINTS:
for j in plantas:
    prob += lpSum(amount_vars[i][j] for i in arrocera) <= mship[j]

for i in arrocera:
    prob += lpSum(amount_vars[i][j] for j in plantas) == produccion[i]

prob.solve()
print("Status:",LpStatus[prob.status])

for v in prob.variables():
    if v.varValue > 0:
        print(v.name,"=",v.varValue)

print("Distancia total =", value(prob.objective))

#Knapsack Problem Code
import random
import pprint

#Enter weights and values of the items in order
weights = [1,   3,  6,  9,  14]
values =  [300,700,900,1000,1400]
#Enter weight constraint of the knapsack
weight_constraint = 10
mutation_rate = 10 #in percentage, not fraction

def gen_popn(pop_size):
    randomBinList = lambda n : [random.randint(0,1) for _ in range(n)]
    popn = [ randomBinList(5) for i in range(pop_size) ]
    #pprint.pprint(popn)
    return popn
    
def calc_fitness(popn):
    global values
    f_table = dict((tuple(individual),sum(a*b for a,b in zip(individual,values))) for individual in popn)
    #pprint.pprint(f_table)
    return f_table
    #Dictionaries can't have multiple keys. Dictionary formed will have
    #fewer entries than pop_size
    
def calc_weight(popn):
    global weights
    w_table = dict((tuple(individual),sum(a*b for a,b in zip(individual,weights))) for individual in popn)
    #pprint.pprint(w_table)
    return w_table
    
def apply_constraint(w_table,f_table):
    global weight_constraint
    
    for individual,weight in w_table.items():
        #pprint.pprint(individual)
        #pprint.pprint(weight)
        if weight > weight_constraint:
            f_table[individual] = -1
    return f_table
    
def take_sample():
    global population
    sample_popn = random.sample(population, 20)
    sample_popn = [tuple(e)   for e   in sample_popn]
    return sample_popn
    
def select_parents():
    global constrained_fitness_table
    global sample_population
    sample_popn_fitness = {}
    for individual in sample_population:
        sample_popn_fitness[individual] = constrained_fitness_table[individual]
    pprint.pprint(sample_popn_fitness)
    parent1 = max(sample_popn_fitness, key=sample_popn_fitness.get)
    del sample_popn_fitness[parent1]
    parent2 = max(sample_popn_fitness, key=sample_popn_fitness.get)
    del sample_popn_fitness[parent2]
    return [parent1 , parent2]

def spawn(parents):
    idx = random.randint(1,4)
    print(idx)
    child1 = parents[0][:idx] + parents[1][idx:]
    child2 = parents[1][:idx] + parents[0][idx:]
    return [child1,child2]
    
def mutate(children):
    child1 = list(children[0])
    child2 = list(children[1])
    
    if random.randint(1,10000) <= (mutation_rate * 100):
        rand_idx = random.randint(0,4)        
        child1[rand_idx] = int(not(child1[rand_idx]))
        
    if random.randint(1,10000) <= (mutation_rate * 100):
        rand_idx = random.randint(0,4)        
        child2[rand_idx] = int(not(child2[rand_idx]))
        
    print(child1,child2)


def find_weakest():
    global constrained_fitness_table
    global sample_population
    sample_popn_fitness = {}
    
    for individual in sample_population:
        sample_popn_fitness[individual] = constrained_fitness_table[individual]
        
    print("Sample Population Fitness")
    pprint.pprint(sample_popn_fitness)
    
    weakest1 = min(sample_popn_fitness, key=sample_popn_fitness.get)
    del sample_popn_fitness[weakest1]
    weakest2 = min(sample_popn_fitness, key=sample_popn_fitness.get)
    del sample_popn_fitness[weakest2]
    return [weakest1 , weakest2]
    
def merge_sample(children, weak_ones):
    
    global sample_population
    global population
    
    child1 = list(children[0])
    child2 = list(children[1])
    
    weak1 = list(weak_ones[0])
    weak2 = list(weak_ones[1])
    
    print("Merging",child1,child2,weak1,weak2)
    print("Merging",len(sample_population),len(population))
    
    population.remove(weak1)
    population.remove(weak2)
    
    population.append(child1)
    population.append(child2)

    
    
    
    
population = gen_popn(2000)

for i in range(3000):
    fitness_table = calc_fitness(population)
    weight_table = calc_weight(population)
    constrained_fitness_table = apply_constraint(weight_table,fitness_table)
    sample_population = take_sample()
    #pprint.pprint(len(sample_population))
    parents = select_parents()
    print("Parents",parents)
    #pprint.pprint(len(sample_population))
    children = spawn(parents)
    print("Children",children)
    mutate(children)
    weak_ones = find_weakest()
    print("weakest ones",weak_ones)
    print(len(sample_population))
    merge_sample(children, weak_ones)

print("Sample Population")
for indiv in sorted(sample_population):
    print(indiv)

#See "Sample Population Fitness" to get the top answers
#"Sample Population" shows the concentrations of various genes in the genepool
#This program works but has bugs. One that comes up often is when parents
#can't be selected because the constrained fitness table has less than
#2 entries. But this actually gives us the solution.  

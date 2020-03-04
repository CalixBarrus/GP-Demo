### Goal:
# Generate random strings -> Using "phenotypic representation" (represent each agent as just a string
#   as opposed to an int or binary string that is converted into a string) 
# Measure how close they are to the target
# Modify and select it based on its fitness
# Repeat 2. and 3. until convergence
###

# TODO Separate into genotypic represention to generalize
# TODO change representation into bits not ints/strings
# TODO Change mutate to use bitflips based on some probability 
# TODO Implemement separate problem (practice that generalization)

import sys
import random

###
# Global Constants
###

POSSIBLE_CHARACTERS = [' ', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', \
    'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', \
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', \
            't', 'u', 'v', 'w', 'x', 'y', 'z']
POPULATION_SIZE = 5
REPRODUCTION_CUTOFF = .5 # Threshold above which all individuals in the population will reproduce with eachother
MUTATION_SEVERITY = 1 # A real positive number. On a 1, the normal distribution within 3 standard deviations 
    # covers the whole of POSSIBLE_CHARACTERS. Higher than one, will truncate the edges of the distribution 
    # (should encounter performance issues for very large numbers, anything n >= 100 should roughly be completely random)
NUMBER_OF_OFFSPRING = 3

###
# Function definitions
###

def printUsage():
    print("Please include a target string") # max string length of, say, 64 characters, 
    #   limit to alphabetic symbols and spaces

def getRandStr(stringLength):
    # Function is dependent on global constant POSSIBLE_CHARACTERS
    result = ""
    for i in range(stringLength):
        randInt = random.randrange(len(POSSIBLE_CHARACTERS))

        result += POSSIBLE_CHARACTERS[randInt]
    return result

def generateRandomPopulation(stringLength, populationSize):
    result = []
    for i in range(populationSize):
        result.append(getRandStr(stringLength))
    return result

def calculateFitness(inputString, targetString):
    # How to calculate fitness?
    # Each letter's "distance from the target letter"
    # Should be more continuous than the discrete "is it correct? y/n".
    # Due to this implementation, the order of the characters in POSSIBLE_CHARACTERS will influence how the
    # evolving string will look.

    # Fitness is a 
    # A string is more fit the closer each letter is to the target letter, so inverse of distance from the actual letter to the target letter.
    maximumDistance = len(POSSIBLE_CHARACTERS) - 1
    fitness = 0
    for index in range(len(inputString)):
        distance = abs(POSSIBLE_CHARACTERS.index(inputString[index]) - POSSIBLE_CHARACTERS.index(targetString[index]))
        fitness += maximumDistance - distance
    return fitness

def calculateFitnessofArray(stringArray, targetString):
    fitnessList = []
    for string in stringArray:
        fitnessList.append(calculateFitness(string, targetString))
    return fitnessList

def mutate(inputString):
    outputString = ''
    for character in inputString:
        outputString += mutateLetter(character)
    return outputString

def mutateLetter(character): # Changes
    #Dependent on MUTATION_SEVERITY and POSSIBLE_CHARACTERS
    randomFloat = -1.
    while -.5 > randomFloat or randomFloat > .5: # Truncates results outside the range (-.5, .5)
        randomFloat = random.normalvariate(0., MUTATION_SEVERITY * (.5/3))
    newCharacterDistance = int((len(POSSIBLE_CHARACTERS) * randomFloat))
    newCharacterIndex = POSSIBLE_CHARACTERS.index(character) + newCharacterDistance
    if newCharacterIndex >= len(POSSIBLE_CHARACTERS): # If the newCharacterIndex is negative, that's OK
        newCharacterIndex -= len(POSSIBLE_CHARACTERS) # TODO: Verify that the random float can theoretically transfer mutate to any letter
    return POSSIBLE_CHARACTERS[newCharacterIndex]


def crossover(parent1, parent2):
    assert len(parent1) == len(parent2)
    splitIndex = random.randrange(len(parent1) + 1)
    return parent1[:splitIndex] + parent2[splitIndex:len(parent2)]


# Test mutateLetter
# character = 'k'
# for i in range(10):
#     character = mutateLetter(character)
#     print(character)

def sortListByFitness(inputList):
    # Dependent on targetString
    fitnessArray = calculateFitnessofArray(population, targetString)
    mergedList = list(map(lambda string, fitness: (string, fitness), population, fitnessArray))
    mergedList.sort(reverse=True, key=(lambda val: val[1]))
    newList = []
    for tuple in mergedList:
        newList.append(tuple[0])
    return newList


def mutate_reproduction(population):
    for individual in range(POPULATION_SIZE):
        population += [mutate(population[individual]) for iteration in range(NUMBER_OF_OFFSPRING)]

def crossover_reproduction(population):
    assert population[0] != None and population[1] != None
    population = sortListByFitness(population) #Pick top two, and reproduce with those two
    return [mutate(crossover(population[0], population[1])) for iteration in range(POPULATION_SIZE)]  

def combination_reproduction(population):
    # Crossover Reproduction
    for i in range(int(POPULATION_SIZE * REPRODUCTION_CUTOFF)):
        for j in range(1, int(POPULATION_SIZE * REPRODUCTION_CUTOFF)):
            population.append(crossover(population[i], population[j]))

    # Mutation Reproduction (of original population)
    for index in range(POPULATION_SIZE):
        population.append(mutate(population[index]))

    

    

def select_by_fitness(population):
    population = sortListByFitness(population)
    return population[:POPULATION_SIZE]

###
# Start of Program
###

if len(sys.argv) != 2:
    printUsage()
    sys.exit(2)

# print("This is the name of the script: ", sys.argv[0])
# print("Number of arguments: ", len(sys.argv))
# print("The arguments are: " , str(sys.argv))
targetString = sys.argv[1]

population = []    

# print(population)
# fitnessList = calculateFitnessofArray(population, targetString)
# print(fitnessList)

# Traditional Evolutionary Strategy (ES) approach - see Handbook of Natural Computing p. 627

# print(population)
# for iteration in range(10):
#     for index in range(len(population)):
#         population[index] = mutate(population[index])
#     print(population)

# print(population)
# for string in population:
#     population[population.index(string)] = mutate(string)
# print(population)
# print(calculateFitnessofArray(population, targetString))

# Mutation Approach

print("Mutation")
population = generateRandomPopulation(len(targetString), POPULATION_SIZE)

print(population)
print(calculateFitnessofArray(population, targetString))
for iteration in range(50000):
    mutate_reproduction(population)
    # print(population)
    population = select_by_fitness(population)
    # print(population)
print(population)
print(calculateFitnessofArray(population, targetString))

# Crossover approach

print("Crossover")
population = generateRandomPopulation(len(targetString), POPULATION_SIZE)

print(population)
print(calculateFitnessofArray(population, targetString))
for iteration in range(50000):
    population = crossover_reproduction(population)
print(population)
print(calculateFitnessofArray(population, targetString))


# Use both crossover and mutation
print("Combination")
population = generateRandomPopulation(len(targetString), POPULATION_SIZE)

print(population)
print(calculateFitnessofArray(population, targetString))
for iteration in range(50000):
    combination_reproduction(population)
    population = select_by_fitness(population)
print(population)
print(calculateFitnessofArray(population, targetString))
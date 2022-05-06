# date finished: 2022/04/09
# initialize
class Cities:
    def __init__(self,max_distance,length_of_tour):
        self.POPULATION = dict()
        self.LOT = length_of_tour
        self.M_DISTANCE = max_distance
        self.LETTERS = ''
        self.generateNewCities()

    def generateNewCities(self):
        LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWYZ"
        self.__LETTERS = ''
        self.POPULATION = dict()
        # START COORD
        USED = list()
        PT = self.generatePoint(self.M_DISTANCE,USED)
        self.START_COORD = PT
        USED.append(PT)
        # OTHER COORDS
        for x in range(self.LOT):
            POINT = self.generatePoint(self.M_DISTANCE, USED)
            USED.append(POINT)
            self.POPULATION[LETTERS[x]] = POINT
        self.LETTERS = LETTERS[:self.LOT]
    def generatePoint(self,distance,l):
        from random import randrange
        while True:
            DATA = (randrange(0, distance + 1), randrange(0, distance + 1))
            if DATA not in l:
                return DATA
    def getData(self):
        return self.POPULATION
    def getLetters(self):
        return self.LETTERS
    def getX(self):
        return self.START_COORD
    def setMaxDistance(self,NUM):
        self.M_DISTANCE = NUM
    def set_LOT(self,NUM):
        self.LOT = NUM
def readCities(file):
    LINES = file.readlines()
    CITIES = dict()
    POS = 0
    for i,line in enumerate(LINES):
        if i == 0:
            LETTERS = line
        elif i == 2:
            NUMS = line.split()
            START_COORD = (int(NUMS[0]),int(NUMS[1]))
        else:
            NUMS = line.split()
            CITIES[LETTERS[POS]] = (int(NUMS[0]),int(NUMS[1]))
            POS += 1
    return CITIES,LETTERS,START_COORD
def storeCities(GRAPH,LETTERS,START_COORD,cities):
    cities.write(LETTERS+"\n")
    cities.write(f"{START_COORD[0]} {START_COORD[1]}\n")
    for key in GRAPH:
        VALUE = GRAPH[key]
        cities.write(f"{VALUE[0]} {VALUE[1]}\n")
def calcDistance(P1,P2):
    from math import sqrt
    DISTANCE = sqrt((P2[0]-P1[0])**2 + (P2[1]-P1[1])**2)
    return DISTANCE

def calcTotalDistance(TOUR,GRAPH,X):
    FITNESS = 0
    CURRENT = X
    for x in TOUR:
        # calc distance between current and next in line
        COORD = GRAPH[x]
        FITNESS += calcDistance(COORD,CURRENT)
        CURRENT = COORD
    return FITNESS
def generatePop(SIZE,LETTER):
    from random import shuffle
    POP = set()

    while len(POP) < SIZE:
        LETTERS = list(LETTER)
        shuffle(LETTERS)
        POP.add(''.join(LETTERS))

    return list(POP)
def evaluate(GRAPH,POP,START_COORD,BEST_DISTANCE,BEST_ORD):
    RESULT = list()
    CUR_BEST = BEST_DISTANCE
    CUR_ORD = BEST_ORD
    for x in POP:
        # Fitness calculation
        FITNESS = (1/(calcTotalDistance(x,GRAPH,START_COORD)+1))*100 # multiply by 100 to visually see change
        RESULT.append(FITNESS)
        # store best tours
        if calcTotalDistance(x,GRAPH,START_COORD) < CUR_BEST:
            CUR_BEST = calcTotalDistance(x,GRAPH,START_COORD)
            CUR_ORD = x

    return RESULT,CUR_BEST,CUR_ORD
# selection func
def roulette(POP,FITNESS,POOL_SIZE):
    from numpy import random
    RESULTS = list()
    # normalize fitness
    NORMALIZED = list()
    SUM = sum(FITNESS)
    for x in FITNESS:
        NORMALIZED.append(x/SUM)
    for x in range(POOL_SIZE):
        RESULTS.append(random.choice(POP,p=NORMALIZED))
    return RESULTS
def sus(POP,FITNESS,POOL_SIZE):
    from numpy import random
    RESULTS = list()
    NUM_OF_POINTERS = POOL_SIZE
    SUM = sum(FITNESS)
    DISTANCE_POINTER = sum(FITNESS)/NUM_OF_POINTERS
    OFFSET = random.uniform(0,DISTANCE_POINTER)
    # Create pointers
    POINTERS = [OFFSET+i*DISTANCE_POINTER for i in range(NUM_OF_POINTERS)]
    # Select parents
    for POINTER in POINTERS:
        CUR_FIT = 0
        for i,x in enumerate(FITNESS):
            CUR_FIT += x
            if POINTER <= CUR_FIT:
                RESULTS.append(POP[i])
                break
    return RESULTS
def tournament(POP,FITNESS,POOL_SIZE,TOURNAMENT_SIZE):
    from random import choice
    RESULTS = list()
    # combining the list to make it easier to compute
    COMBINED = [(POP[i],FITNESS[i]) for i in range(len(FITNESS))]
    for x in range(POOL_SIZE):
        # running tournament
        TOURNAMENT = set()
        while len(TOURNAMENT) < TOURNAMENT_SIZE:
            TOURNAMENT.add(choice(COMBINED))
        # sorting tournament
        TOURNAMENT = sorted(TOURNAMENT,key=lambda x: x[1],reverse=True)
        RESULTS.append(TOURNAMENT[0][0])
    return RESULTS
def truncation(POP,FITNESS,POOL_SIZE,PERCENTAGE):
    RESULTS = list()
    # combining the list to make it easier to compute
    COMBINED = sorted([(POP[i], FITNESS[i]) for i in range(len(FITNESS))],key=lambda x:x[1],reverse=True)
    END = int(len(FITNESS)*PERCENTAGE)
    RESULTS = [COMBINED[i][0] for i in range(END)]
    # duping values until it is equal to or greater than pool size
    while len(RESULTS) < POOL_SIZE:
       RESULTS = RESULTS + RESULTS
    # truncate the end results to match our pool size
    RESULTS = RESULTS[:POOL_SIZE]
    return RESULTS
# Cross over strats
def PMX(P1,P2):
    from random import randrange
    RESULT = [0 for x in range(len(P1))]
    # random length to copy from
    LENGTH = randrange(1,len(P1))
    OFFSET = randrange(0,len(P1)-LENGTH)
    # copy string over
    for i in range(OFFSET,OFFSET+LENGTH):
        RESULT[i] = P1[i]
    # element wise mapping
    for i,x in enumerate(RESULT):
        if x == 0:
            # setup mapping
            POS = i
            while True:
                if P2[POS] not in RESULT:
                    RESULT[i] = P2[POS]
                    break
                POS = P1.index(P2[POS])
    return ''.join(RESULT)
def OX(P1,P2):
    from random import randrange
    RESULT = [0 for x in range(len(P1))]
    # random length to copy from
    LENGTH = randrange(1, len(P1))
    OFFSET = randrange(0, len(P1) - LENGTH)
    # copy string over
    for i in range(OFFSET, OFFSET + LENGTH):
        RESULT[i] = P1[i]
    POS = OFFSET+LENGTH
    POS_2 = POS
    while True:
        if RESULT[POS] != 0:
            break
        while True:
            if P2[POS_2] not in RESULT:
                RESULT[POS] = P2[POS_2]
                break
            POS_2 += 1
            if POS_2 == len(P2):
                POS_2 = 0
        POS += 1
        if POS == len(P1):
            POS = 0
    return ''.join(RESULT)
def CX(P1,P2):
    RESULT = [0 for x in range(len(P1))]
    POS = 0
    # cycle
    while True:
        RESULT[POS] = P1[POS]
        if P2[POS] in RESULT:
            break
        POS = P1.index(P2[POS])


    # fill out the rest
    for i,x in enumerate(RESULT):
        if x == 0:
            RESULT[i] = P2[i]
    return ''.join(RESULT)
# mutation
def mutate(CHILD):
    from random import randrange
    RESULT = list(CHILD)
    # Choose two index to swap
    c1 = randrange(0,len(RESULT))
    c2 = randrange(0,len(RESULT))
    while c1 == c2:
        c1 = randrange(0,len(RESULT))
    temp = RESULT[c1]
    RESULT[c1] = RESULT[c2]
    RESULT[c2] = temp
    return ''.join(RESULT)

## init
Cities = Cities(400,20)
GRAPH = Cities.getData()
START_COORD = Cities.getX()
LETTERS = Cities.getLetters()
SAMPLE_SIZE = 5000
POOL_SIZE = 2500
POPULATION = generatePop(SAMPLE_SIZE,LETTERS)

##### settings
SELECTION_MODE = 3 # 0: roulette 1: stochastic 2: tournament 3: truncation
CROSS_MODE = 1 # 0: PMX 1: OX 2: CX
printing = True # print best of generation?
NUM_OF_ITERS = 100
# tournament
TOURNAMENT_SIZE = 2
# truncation
PERCENTAGE = 0.25
MUTATION_RATE = 0.1


# file creation
outputs = open("outputs.txt","a")
try:
    cities = open("cities.txt","r")
    if input("Use cities from last time? y/N ").lower() == "n":
        cities = open("cities.txt", "w")
        storeCities(GRAPH, LETTERS, START_COORD, cities)
    else:
        GRAPH, LETTERS, START_COORD = readCities(cities)
except Exception as e:
    cities = open("cities.txt","x")
    storeCities(GRAPH,LETTERS,START_COORD,cities)
cities.close()

sm = ["roulette","SUS","tournament","truncation"]
cm = ["PMX","OX","CX"]

BEST_DISTANCE = 999999999
BEST_ORD = None

## MAIN CODE
from random import choice, random
CURRENT_ITER = 0
while True:
    # Evaluation
    CURRENT_ITER += 1
    if CURRENT_ITER >= NUM_OF_ITERS:
        print("Best Order:",BEST_ORD,"Best distance:",BEST_DISTANCE)
        outputs.write(f"Selection: {sm[SELECTION_MODE]}, Crossover: {cm[CROSS_MODE]}, Iterations Lasted: {CURRENT_ITER}, Best Order: {BEST_ORD}, Best Distance: {BEST_DISTANCE}, MUTATION_RATE: {MUTATION_RATE}, Tournament Size: {TOURNAMENT_SIZE}, Truncation %: {PERCENTAGE}\n")
        outputs.close()
        break
    if printing:
        print("Lowest distance:",BEST_DISTANCE,"Iteration:",CURRENT_ITER)
    FITNESS_SCORES,BEST_DISTANCE,BEST_ORD = evaluate(GRAPH,POPULATION,START_COORD,BEST_DISTANCE,BEST_ORD)
    # Selection
    if SELECTION_MODE == 0:
        POOL = roulette(POPULATION,FITNESS_SCORES,POOL_SIZE)
    elif SELECTION_MODE == 1:
        POOL = sus(POPULATION,FITNESS_SCORES,POOL_SIZE)
    elif SELECTION_MODE == 2:
        POOL = tournament(POPULATION,FITNESS_SCORES,POOL_SIZE,TOURNAMENT_SIZE)
    elif SELECTION_MODE == 3:
        POOL = truncation(POPULATION,FITNESS_SCORES,POOL_SIZE,PERCENTAGE)
    # Crossovers
    NEW_POPULATION = list()
    while len(NEW_POPULATION) < SAMPLE_SIZE:
        # pick two parents
        P1, P2 = choice(POOL), choice(POOL)
        i = 0
        while P1 == P2:
            i += 1
            if i > 1000:
                print("Convergence is reached")
                NUM_OF_ITERS = 0
                break
            P1 = choice(POOL)
        if NUM_OF_ITERS == 0:
            break
        # crossing over
        if CROSS_MODE == 0:
            CHILD = PMX(P1,P2)
        elif CROSS_MODE == 1:
            CHILD = OX(P1,P2)
        elif CROSS_MODE == 2:
            CHILD = CX(P1,P2)
        # mutation
        if random() <= MUTATION_RATE:
            CHILD = mutate(CHILD)
        NEW_POPULATION.append(CHILD)
    POPULATION = NEW_POPULATION



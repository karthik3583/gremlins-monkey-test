import random
from deap import base
from deap import creator
from deap import tools
import array
import random
import json
import numpy as np
from math import sqrt
from deap import algorithms
from deap import base
from deap import benchmarks
from deap.benchmarks.tools import diversity, convergence, hypervolume
from deap import creator
from deap import tools
from random import shuffle
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from  selenium.webdriver.common.action_chains import ActionChains
import argparse
from read_gremlins_logs import parse_line, Ind
from datetime import datetime
#from read_gremlins_logs import atomic_sequences


parser = argparse.ArgumentParser()

parser.add_argument(
    "--url",
    help="echo the url you use here")
parser.add_argument(
    "--ngen",
    default=100,
    help="echo the number of generations you use here")
parser.add_argument(
    "--npop",
    default=100,
    help="echo the number of populations you use here")

args = parser.parse_args()


creator.create("FitnessMulti", base.Fitness, weights=(1.0, 1.0))
creator.create("TestCase", list, fitness=creator.FitnessMulti, testcase=None, best=None)

to_cur = 0


def read_large_file(file_object):
    global to_cur
    """
    Uses a generator to read a large file lazily
    """
    while True:
        skip = 0
        while skip <= to_cur:
            data = file_object.readline()
            skip += 1
        to_cur = skip
        if not data:
            break
        yield data


def initTestCase(size):
    ret = []
    path = "genes.csv"
    try:
        with open(path) as file_handler:
            i = 0
            for line in read_large_file(file_handler):
                # process line
                ret.append(line)
                i += 1
                if i >= size:
                    break
    except (IOError, OSError):
        print("Error opening / processing file")
    return ret


toolbox = base.Toolbox()
toolbox.register("testcase", initTestCase, creator.TestCase, size=10)


# creator.create("FitnessMin", base.Fitness, weights=(-1.0, -1.0))
# creator.create("Individual", array.array, typecode='d', fitness=creator.FitnessMin)

toolbox = base.Toolbox()

# Problem definition
# Functions zdt1, zdt2, zdt3, zdt6 have bounds [0, 1]
BOUND_LOW, BOUND_UP = 0.0, 1.0

# Functions zdt4 has bounds x1 = [0, 1], xn = [-5, 5], with n = 2, ..., 10
# BOUND_LOW, BOUND_UP = [0.0] + [-5.0]*9, [1.0] + [5.0]*9

# Functions zdt1, zdt2, zdt3 have 30 dimensions, zdt4 and zdt6 have 10
NDIM = 30


def uniform(low, up, size=None):
    try:
        return [random.uniform(a, b) for a, b in zip(low, up)]
    except TypeError:
        return [random.uniform(a, b) for a, b in zip([low] * size, [up] * size)]


toolbox.register("attr_generator", initTestCase, 10)
toolbox.register("individual", tools.initIterate, creator.TestCase, toolbox.attr_generator)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)


def evaluate(individual, report=False):
    errors = []
    driver = webdriver.Chrome("./chromedriver")
    driver.get(args.url)

    for tc in individual:
        o = parse_line(tc)

        if o is None: 
            continue

        if o.event == "type" or o.event == "input":
            elems = driver.find_elements_by_tag_name(o.dom)
            for elem in elems:
                try:
                    if elem and elem.is_displayed():
                        elem.send_keys(o.input)
                        elem.send_keys(Keys.RETURN)
                except:
                    actions = ActionChains(driver)
                    actions.send_keys(Keys.RETURN)
                    actions.perform()
        else:
            actions = ActionChains(driver)
            actions.move_by_offset(o.locx, o.locy)
            actions.click()
            actions.perform()

    for entry in driver.get_log('browser'):
        errors.append(entry)

    driver.close()
    obj1 = len(individual)
    obj2 = len(errors)

    if report is not False:
        report.write("Number of Errors: {} \n".format(len(errors)))
        report.write("Test Cases Length: {} \n".format(len(errors)))
        report.write("Errors Found:\n")
        report.write(str(errors))
        report.write("\n")
        report.write("Test Cases:\n")
        report.write(str(list(individual)))

    # print("Obj#1: {},\tObj#2: {}".format(obj1, obj2))

    return obj1, obj2


def mate(a, b):
    choice = np.random.randint(0, 4)
    if choice == 0:
        ret = a.extend(b)
    elif choice == 1:
        ret = b.extend(a)
    elif choice == 2:
        ret = [None] * (len(a) + len(b))
        ret[::2] = a
        ret[1::2] = b
    elif choice == 3:
        ret = [None] * (len(a) + len(b))
        ret[::2] = b
        ret[1::2] = a
    return ret


def synthesize():
    if np.random.randint(0, 1e3) % 2 == 0:
        tc = Ind(_e="click")
    else:
        tc = Ind(_e="type")
    tc.fuzzy()
    return tc


def mutate(individual):
    shuffle(individual)

    new_genes = np.random.randint(0, 3)
    for i in range(new_genes):
        individual.insert(np.random.randint(0, len(individual)), synthesize())

    for tc in individual:
        tc.fuzzy()

    return individual


toolbox.register("evaluate", evaluate)
toolbox.register("mate", mate)
toolbox.register("mutate", mutate)
toolbox.register("select", tools.selNSGA2)


def main(seed=None):
    random.seed(seed)

    NGEN = int(args.ngen)
    MU = int(args.npop)
    CXPB = 0.9

    stats = tools.Statistics(lambda ind: ind.fitness.values)
    # stats.register("avg", np.mean, axis=0)
    # stats.register("std", np.std, axis=0)
    stats.register("min", np.min, axis=0)
    stats.register("max", np.max, axis=0)

    logbook = tools.Logbook()
    logbook.header = "gen", "evals", "min", "max"

    pop = toolbox.population(n=MU)

    # Evaluate the individuals with an invalid fitness
    invalid_ind = [ind for ind in pop if not ind.fitness.valid]
    fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
    for ind, fit in zip(invalid_ind, fitnesses):
        ind.fitness.values = fit

    # This is just to assign the crowding distance to the individuals
    # no actual selection is done
    pop = toolbox.select(pop, len(pop))

    record = stats.compile(pop)
    logbook.record(gen=0, evals=len(invalid_ind), **record)
    print(logbook.stream)

    # Begin the generational process
    for gen in range(1, NGEN):
        # Vary the population
        offspring = tools.selTournamentDCD(pop, len(pop))
        offspring = [toolbox.clone(ind) for ind in offspring]

        for ind1, ind2 in zip(offspring[::2], offspring[1::2]):
            if random.random() <= CXPB:
                toolbox.mate(ind1, ind2)

            toolbox.mutate(ind1)
            toolbox.mutate(ind2)
            del ind1.fitness.values, ind2.fitness.values

        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        # Select the next generation population
        pop = toolbox.select(pop + offspring, MU)
        record = stats.compile(pop)
        logbook.record(gen=gen, evals=len(invalid_ind), **record)
        print(logbook.stream)

    print("Final population hypervolume is %f" % hypervolume(pop, [11.0, 11.0]))

    return pop, logbook


if __name__ == "__main__":
    # with open("pareto_front/zdt1_front.json") as optimal_front_data:
    #     optimal_front = json.load(optimal_front_data)
    # Use 500 of the 1000 points in the json file
    # optimal_front = sorted(optimal_front[i] for i in range(0, len(optimal_front), 2))

    pop, stats = main()

    with open("report_{:%B_%d_%Y}.txt".format(datetime.now()), "w") as f:
        for ind in pop:
            f.write(str(ind))
            f.write("\n")
            evaluate(ind, f)

    # pop.sort(key=lambda x: x.fitness.values)

    # print(stats)
    # print("Convergence: ", convergence(pop, optimal_front))
    # print("Diversity: ", diversity(pop, optimal_front[0], optimal_front[-1]))

    # import matplotlib.pyplot as plt
    # import np

    # front = np.array([ind.fitness.values for ind in pop])
    # optimal_front = np.array(optimal_front)
    # plt.scatter(optimal_front[:,0], optimal_front[:,1], c="r")
    # plt.scatter(front[:,0], front[:,1], c="b")
    # plt.axis("tight")
    # plt.show()

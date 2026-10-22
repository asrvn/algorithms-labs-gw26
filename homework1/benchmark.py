import matplotlib.pyplot as plt
import random
import time

from ost_avl import *
from splay_tree import *

# Reference:
# https://docs.python.org/3/library/random.html
# https://matplotlib.org/stable/api/pyplot_summary.html

def generate_sequential_workload(n):

    workload = (
        [i for i in range(1, n + 1)],
        [i for i in range(1, n + 1)]
    )

    return workload

def generate_uniform_workload(n, rng):

    '''
    random.sample(population, k, *, counts=None)
        Return a k length list of unique elements chosen from the population sequence.
        Used for random sampling without replacement.

    random.choices(population, weights=None, *, cum_weights=None, k=1)
        Return a k sized list of elements chosen from the population with replacement.
    '''

    keys = rng.sample(population = range(1, n + 1), k = n)
    searches = rng.choices(population = keys, k = n)

    return keys, searches

def generate_locality_workload(n, rng):

    '''
    random.shuffle(x)
        Shuffle the sequence x in place.
    '''

    keys = rng.sample(population = range(1, n + 1), k = n)

    divider = n // 5
    hot_set, cold_set = keys[:divider], keys[divider:]

    searches = rng.choices(population = hot_set, k = divider * 8)
    searches.extend(rng.choices(population = cold_set, k = divider * 2))

    rng.shuffle(searches)
    return keys, searches

def run_workload(tree_class, insert_keys, search_keys):

    current_tree = tree_class()
    start_time = time.perf_counter()

    for key in insert_keys:

        current_tree.insert(key)

    insert_runtime = 1000 * (time.perf_counter() - start_time)
    start_time = time.perf_counter()

    if isinstance(current_tree, AVLOrderStatisticTree):

        for key in search_keys:

            current_tree.find(key)

    else:

        for key in search_keys:

            current_tree.search(key)

    search_runtime = 1000 * (time.perf_counter() - start_time)

    return {"insert" : insert_runtime, "search" : search_runtime, "cumulative" : insert_runtime + search_runtime}

if __name__ == "__main__":

    tree_sizes = [500, 1000, 2000, 4000]
    workloads = {"Sequential" : generate_sequential_workload,
                 "Uniform Random" : generate_uniform_workload,
                 "80/20 Locality" : generate_locality_workload}
    workload_names = list(workloads)
    trees = {"AVL" : AVLOrderStatisticTree,
             "Splay" : SplayTree}

    fig, axes = plt.subplots(1, 3, figsize = (20, 10))
    print("Workload            N     Tree      Insert (ms)    Search (ms)    Cumulative (ms)")

    for i in range(len(workload_names)):

        name = workload_names[i]
        generator = workloads[name]
        data = {"AVL" : [], "Splay" : []}

        for n in tree_sizes:

            rng = random.Random(n)

            if name == "Sequential":

                insert_keys, search_keys = generator(n)

            else:

                insert_keys, search_keys = generator(n, rng)

            for tree_name in trees:

                run = run_workload(trees[tree_name], insert_keys, search_keys)
                data[tree_name].append(run["cumulative"])

                print(f"{name:<20}{n:<6}{tree_name:<10}"
                      f"{run['insert']:<15.3f}{run['search']:<15.3f}{run['cumulative']:<15.3f}")

        for tree_name in trees:

            axes[i].plot(tree_sizes, data[tree_name], label=tree_name)

        axes[i].set_title(name)
        axes[i].set_xlabel("Tree Size (N)")
        axes[i].set_ylabel("Cumulative Time Taken (ms)")
        axes[i].legend()

    plt.savefig("workload_benchmark.png")
    plt.close()
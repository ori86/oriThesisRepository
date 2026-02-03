# imports
import random
import os
import new_types
import copy
from time import time

# imports from eckity
from eckity.algorithms.simple_evolution import SimpleEvolution
from eckity.breeders.simple_breeder import SimpleBreeder
from eckity.genetic_operators.selections.tournament_selection import TournamentSelection
from eckity.statistics.best_average_worst_statistics import BestAverageWorstStatistics
from eckity.subpopulation import Subpopulation
from eckity.algorithms.simple_evolution import SimpleEvolution
from eckity.breeders.simple_breeder import SimpleBreeder
from eckity.creators.gp_creators.grow import GrowCreator
from eckity.genetic_operators.crossovers.subtree_crossover import SubtreeCrossover
from eckity.genetic_operators.mutations.subtree_mutation import SubtreeMutation
from eckity.genetic_operators.selections.tournament_selection import TournamentSelection
from eckity.subpopulation import Subpopulation
from eckity.creators.gp_creators.grow import GrowCreator
from eckity.genetic_encodings.gp.tree.utils import get_func_types

# imports from my files
from new_primitives2 import FUNCTION_SET2
from irena_evaluator import AssemblyEvaluator
from assembly_parameters import terminal_set as terminal_set

# my parameters
WINDOWS = True
survivors_path = "corewars8086-master\\bundle\\survivors"
cgx_path = "corewars8086-master\\bundle\\cgx.bat"
cgx_lite_path = "corewars8086-master\\bundle\\cgx-lite.bat"
cgx_legacy_path = "corewars8086-master\\bundle\\cgx-legacy.bat"
root_path = "C:\\Users\\oriei\\Thesis\\oriWorkNewVenv"
nasm_path = "C:\\Users\\oriei\\Thesis\\nasm-folder\\nasm.exe"




def setup(competition_size=3):
    try:
        files = os.listdir(survivors_path)
        # Filter out non-file entries if needed
        survivor_names = [f for f in files if os.path.isfile(os.path.join(survivors_path, f))]
        print("Survivor names:")
        for name in survivor_names:
            print(name)
    except Exception as e:
        print(f"Error reading survivors directory: {e}")
    all_survivors = os.listdir(survivors_path)
    group_survivors = list(set([survivor[:-1] for survivor in all_survivors]))  # avoid the warrior enumeration
    k = min(len(group_survivors), competition_size)
    train_set = random.sample(group_survivors, k=k)
    print(os.listdir(os.path.join(root_path, "corewars8086-master\\bundle", "survivors")))




def create_algo():

    algo = SimpleEvolution(
            Subpopulation(creators=GrowCreator(init_depth=(2,20),
                                           terminal_set=terminal_set,
                                           function_set=FUNCTION_SET2,
                                           root_type = new_types.t_section,
                                           bloat_weight=0.00001),
                          population_size=100,
                          evaluator=AssemblyEvaluator(root_path=root_path, nasm_path=nasm_path),
                          # minimization problem (fitness is sum of values), so lower fitness is better
                          higher_is_better=True,
                          elitism_rate=0.00,
                          operators_sequence=[
                            SubtreeCrossover(probability=0.5, arity=2), # crossover inner trees of 2 individuals, can be more
                            SubtreeMutation(probability=0.5, arity=1), # mutate a subtree of one inner tree of 1 individual
                          ],
                          selection_methods=[
                              # (selection method, selection probability) tuple
                              (TournamentSelection(tournament_size=4, higher_is_better=True), 1)
                          ]),
            breeder=SimpleBreeder(),
            max_workers=1,
            max_generation=100,
            statistics=BestAverageWorstStatistics()
        )
    return algo
def main():

    start_time = time()

    algo = create_algo()
    algo.evolve()
    
    

    # total evolution time
    print('total time:', time() - start_time)

    # Evaluate the winner using the same evaluator used during evolution
    print("The winner's test run:")
    evaluator: AssemblyEvaluator = algo.population.sub_populations[0].evaluator
    best = copy.deepcopy(algo.best_of_run_)

    total_fitness = evaluator.evaluate_individual(best)
    print("Total fitness:", total_fitness)

    # If you want the extra stats (from extra_stats):
    if hasattr(best, "extra_stats"):
        s = best.extra_stats
        print(
            "Tree1 fitness: {}\nTree2 fitness: {}\nScore: {}, Lifetime: {}, Bytes written: {}, Writing rate: {}".format(
                s["fitness1"],
                s["fitness2"],
                s["norm_group"][0],
                s["norm_group"][1],
                s["norm_group"][2],
                s["norm_group"][3],
            )
        )

    # Make sure the winners directory exists
    winners_dir = os.path.join(root_path, "winners")
    os.makedirs(winners_dir, exist_ok=True)


    
    # Build the winner filename exactly like the old code
    s = getattr(best, "extra_stats", None)

    if s is not None:
        fname = (
            "t_" + str(time()) +
            "_fg_" + str(s.get("fitness_group", total_fitness)) +
            "_s_" + str(s["norm_group"][0]) +
            "_a_" + str(s["norm_group"][1]) +
            "_wb_" + str(s["norm_group"][2]) +
            "_wr_" + str(s["norm_group"][3]) +
            ".asm"
        )
    else:
        fname = "t_" + str(time()) + "_fg_" + str(total_fitness) + ".asm"

    out_path = os.path.join(winners_dir, fname)

    # Let algo.execute write the best individual to a file, like in the old version
# Save the winner ASM by reusing the evaluator writer
    with open(out_path, "w+", encoding="utf-8") as f:
        evaluator._write_survivor_to_file(best, out_path)
    
    print("Winner saved to:", out_path)


    print("Winner saved to:", out_path)



if __name__ == '__main__':
    main()



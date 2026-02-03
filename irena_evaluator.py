import csv
import os
import subprocess
import inspect
import shutil
import threading
import time
import numpy as np
import copy
import glob
from numbers import Number
from concurrent.futures.thread import ThreadPoolExecutor
from assembly_individual import AssemblyIndividual
from eckity.evaluators.simple_individual_evaluator import SimpleIndividualEvaluator
from eckity.genetic_encodings.gp.tree.tree_node import FunctionNode, TerminalNode

# 0 - score, 1 - lifetime, 2 - written bytes
SCORE = 0
LIFETIME = 1
BYTES = 2
RATE = 3

# casting_utils.py
from typing import Literal, Optional
from eckity.genetic_encodings.gp.tree.tree_individual import Tree
import new_types



Slot = Literal["tree1", "tree2", "both"]


def cast_tree_to_assembly(tree_ind: Tree,
                          *,
                          slot: Slot = "tree1",
                          fitness_for_whole: Optional[object] = None) -> AssemblyIndividual:
    """
    Wrap a plain GP Tree individual into an AssemblyIndividual.

    - Copies function_set, terminal_set, erc_range, root_type
    - Deep-copies the tree nodes
    - Preserves fitness objects (deepcopy) unless fitness_for_whole provided for the outer fitness
    - Places the tree into tree1, tree2, or both
    """
    ai = AssemblyIndividual(
        function_set=tree_ind.function_set,
        terminal_set=tree_ind.terminal_set,
        erc_range=tree_ind.erc_range,
        root_type=tree_ind.root_type,
        fitness=fitness_for_whole or copy.deepcopy(tree_ind.fitness),
        fitness1=copy.deepcopy(tree_ind.fitness),
        fitness2=copy.deepcopy(tree_ind.fitness),
        update_parents=False,
    )

    if slot in ("tree1", "both"):
        ai.tree1.tree = copy.deepcopy(tree_ind.tree)
    if slot in ("tree2", "both"):
        ai.tree2.tree = copy.deepcopy(tree_ind.tree)

    # Maintain evaluated state if relevant
    try:
        if hasattr(tree_ind.fitness, "is_fitness_set") and tree_ind.fitness.is_fitness_set():
            ai.tree1.fitness.set_fitness(tree_ind.fitness.get_pure_fitness())
            ai.tree2.fitness.set_fitness(tree_ind.fitness.get_pure_fitness())
            ai.fitness.set_not_evaluated()  # let the combined fitness be recomputed
    except Exception:
        # If the fitness API differs, just ignore and evaluate later
        pass

    return ai


class AssemblyEvaluator(SimpleIndividualEvaluator):
    # Allow some evaluators run in parallel. Need to modify the paths for the execution.
    # Need to duplicate the original directory for this to work properly
    def __init__(self, root_path, nasm_path):
        super().__init__()
        self.nasm_path = nasm_path
        self.root_path = root_path

        # Jar you already have at the project root
        self.engine_jar = os.path.join(
            root_path,
            "corewars8086-5.0.1.jar"
        )

        # Bundle directory where cgx.bat lives
        self.bundle_dir = os.path.join(
            root_path,
            "corewars8086-master",
            "bundle"
        )
        self.cgx_path = os.path.join(self.bundle_dir, "cgx.bat")


        self.executor = ThreadPoolExecutor(max_workers=4)



    # def _write_survivor_to_file(self, tree, file_path):
    #     def execute_with_file(pos, output, **kwargs):
    #         node = tree.tree[pos[0]]

    #         if isinstance(node, FunctionNode):
    #             # evaluate children first
    #             args = []
    #             for _ in range(node.n_args):
    #                 pos[0] += 1
    #                 args.append(execute_with_file(pos, output, **kwargs))

    #             func = node.function
    #             sig = inspect.signature(func)

    #             # count regular positional params (no *args, **kwargs)
    #             params = [
    #                 p for p in sig.parameters.values()
    #                 if p.kind in (p.POSITIONAL_ONLY, p.POSITIONAL_OR_KEYWORD)
    #             ]
    #             n_params = len(params)

    #             # Call the primitive in the right style
    #             if n_params == len(args):
    #                 res = func(*args)
    #             elif n_params == len(args) + 1:
    #                 res = func(output, *args)
    #             else:
    #                 res = func(*args)

    #             # If a primitive returns assembly text, emit it

    #             # Only emit full instruction lines (t_section), never operands
    #             if isinstance(res, new_types.t_section):
    #                 print(str(res), file=output)

    #             return res

    #         else:  # TerminalNode
    #             # return kwargs.get(getattr(node, "value", None), getattr(node, "value", None))
    #             v = getattr(node, "value", None)

    #             # if this terminal is a section terminal (like "nop"), wrap it as t_section
    #             if v in tree.terminal_set and tree.terminal_set[v] is new_types.t_section:
    #                 return new_types.t_section(v)

    #             return kwargs.get(v, v)

    #     with open(file_path, "w+", encoding="utf-8") as file:
    #         # Safer, predictable skeleton
    #         print("bits 16", file=file)
    #         print("org 0", file=file)
    #         print("start:", file=file)
    #         print("push cs", file=file)
    #         print("pop ds", file=file)
    #         print("push cs", file=file)
    #         print("pop es", file=file)
    #         print("cld", file=file)
    #         print("xor di, di", file=file)

    #         before = file.tell()
    #         execute_with_file([0], file)
    #         after = file.tell()

    #         # If the GP produced nothing, at least do something valid
    #         if after == before:
    #             print("nop", file=file)

    #         # Prevent falling into padding bytes
    #         print("jmp start", file=file)

    #         # Pad in BYTES (NASM), not text length
    #         # Keep 510 to match your original intention
    #         print("times 510-($-$$) db 0x90", file=file)

                

    def _write_survivor_to_file(self, tree, file_path):
        def execute_with_file(pos, output, **kwargs):
            node = tree.tree[pos[0]]

            if isinstance(node, FunctionNode):
                # evaluate children first
                args = []
                for _ in range(node.n_args):
                    pos[0] += 1
                    args.append(execute_with_file(pos, output, **kwargs))

                func = node.function
                sig = inspect.signature(func)

                params = [
                    p for p in sig.parameters.values()
                    if p.kind in (p.POSITIONAL_ONLY, p.POSITIONAL_OR_KEYWORD)
                ]
                n_params = len(params)

                # Call primitive
                if n_params == len(args):
                    res = func(*args)
                elif n_params == len(args) + 1:
                    res = func(output, *args)
                else:
                    res = func(*args)

                # Only emit full instructions / blocks
                if isinstance(res, new_types.t_section):
                    print(str(res), file=output)

                return res

            # TerminalNode
            v = getattr(node, "value", None)

            # If terminal is a section terminal (like "nop"), wrap it
            if v in tree.terminal_set and tree.terminal_set[v] is new_types.t_section:
                return new_types.t_section(v)

            return kwargs.get(v, v)

        with open(file_path, "w+", encoding="utf-8") as file:
            # Minimal required header for NASM/corewars
            print("bits 16", file=file)
            print("org 0", file=file)
            print("start:", file=file)

            before = file.tell()
            execute_with_file([0], file)
            after = file.tell()

            # If GP produced nothing, keep it valid
            if after == before:
                print("nop", file=file)

            # No forced loop. Execution will fall into padding (NOPs).
            print("times 510-($-$$) db 0x90", file=file)






    def _compile_survivor(self, asm_path, individual_name, survivors_path, nasm_path):
        out_bin = os.path.join(survivors_path, individual_name)

        proc = subprocess.Popen(
            [nasm_path, "-f", "bin", asm_path, "-o", out_bin],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        stdout, stderr = proc.communicate()

        if proc.returncode != 0 or (not os.path.exists(out_bin)) or os.path.getsize(out_bin) == 0:
            print(f"NASM failed for {individual_name} (rc={proc.returncode})")
            try:
                print(stderr.decode(errors="ignore"))
            except Exception:
                print(stderr)
            return -1

        return 0



    def _read_scores(self, scores_path, individual_name1):
        group_data = []
        indiv_data = []

        with open(scores_path, 'r') as scores:
            info = csv.reader(scores)
            flag_ind = False
            for line in info:
                if not line:
                    continue

                if "Groups:" in line:
                    continue

                if not flag_ind and "Warriors:" not in line:
                    if line[0] == individual_name1[:-1]:
                        group_data.append(line[1:])
                    continue

                if "Warriors:" in line:
                    flag_ind = True
                    continue

                if flag_ind:
                    if line[0][:-1] == individual_name1[:-1]:
                        indiv_data.append(line[1:])


        # If nothing was found, return zeros
        if not group_data or not indiv_data:
            return {
                "group_data": [[0, 0, 0, 0]],
                "indiv_data": [[0, 0, 0, 0]],
                "group_index": 0,
                "indiv1_index": 0,
                "indiv2_index": 0,
            }

        # Determine indices safely based on actual length
        n = len(indiv_data)
        if n == 1:
            indiv1_index = 0
            indiv2_index = 0
        else:
            indiv1_index = 0
            indiv2_index = 1

        return {
            "group_data": group_data,
            "indiv_data": indiv_data,
            "group_index": 0,
            "indiv1_index": indiv1_index,
            "indiv2_index": indiv2_index,
        }



    def evaluate_individual(self, individual: AssemblyIndividual):
        """
        Compute the fitness value of a given individual.
        """
        worker_root = self.root_path
        survivors_path = os.path.join(
            self.root_path,
            "corewars8086-master",
            "bundle",
            "survivors",
        )
        os.makedirs(survivors_path, exist_ok=True)
        train_survivors = os.path.join(self.root_path, "survivors")


        # Clean only old GA warriors, keep the training ones
        for f in os.listdir(survivors_path):
            if "try" in f:
                try:
                    os.remove(os.path.join(survivors_path, f))
                except Exception:
                    pass

                
        # Clean previous survivors
        for f in os.listdir(survivors_path):
            if "try" in f:
                try:
                    os.remove(os.path.join(survivors_path, f))
                except Exception:
                    continue

        # Copy training warriors from the bundle



        train_survivors = os.path.join(self.root_path, "survivors")  # C:\Users\oriei\Thesis\oriWorkNewVenv\survivors

        if not os.path.isdir(train_survivors):
            raise FileNotFoundError(f"Training survivors folder not found: {train_survivors}")

        for opponent in os.listdir(train_survivors):
            src = os.path.join(train_survivors, opponent)
            dst = os.path.join(survivors_path, opponent)

            if not os.path.isfile(src):
                continue

            if os.path.abspath(src) == os.path.abspath(dst):
                continue

            shutil.copy2(src, dst)



        nasm_path = self.nasm_path
        individual_name1 = f"{individual.id}try1"
        individual_name2 = f"{individual.id}try2"


        asm_debug_dir = os.path.join(self.root_path, "asm_debug")
        os.makedirs(asm_debug_dir, exist_ok=True)

        asm_path1 = os.path.join(asm_debug_dir, individual_name1 + ".asm")
        asm_path2 = os.path.join(asm_debug_dir, individual_name2 + ".asm")

        self._write_survivor_to_file(individual, asm_path1)
        self._write_survivor_to_file(individual, asm_path2)

        score1 = self._compile_survivor(asm_path1, individual_name1, survivors_path, nasm_path)
        score2 = self._compile_survivor(asm_path2, individual_name2, survivors_path, nasm_path)

        print("compiled check:",
            individual_name1, os.path.exists(os.path.join(survivors_path, individual_name1)),
            individual_name2, os.path.exists(os.path.join(survivors_path, individual_name2)))

        if score1 == -1 or score2 == -1:
            return 0.0


        requested_scores = os.path.join(worker_root, f"scores_{individual.id}.csv")
        default_scores = os.path.join(self.bundle_dir, "scores.csv")

        # delete stale files
        if os.path.exists(requested_scores):
            os.remove(requested_scores)
        if os.path.exists(default_scores):
            os.remove(default_scores)

        # Make sure bundle/bin/corewars8086-5.0.1.jar exists for cgx.bat
        bin_dir = os.path.join(self.bundle_dir, "bin")
        os.makedirs(bin_dir, exist_ok=True)

        jar_in_bin = os.path.join(bin_dir, os.path.basename(self.engine_jar))
        if not os.path.exists(jar_in_bin):
            shutil.copy(self.engine_jar, jar_in_bin)


        t0 = time.time()
        #print(f"EVAL {individual.id}: starting cgx at {t0:.1f}")
        #print("EVAL survivors count:", len(os.listdir(survivors_path)))

        # scores files: cgx might ignore the requested path, but we must define one
        requested_scores = os.path.join(worker_root, f"scores_{individual.id}.csv")
        default_scores = os.path.join(self.bundle_dir, "scores.csv")

        # clean stale files
        if os.path.exists(requested_scores):
            os.remove(requested_scores)
        if os.path.exists(default_scores):
            os.remove(default_scores)

        # pass requested path to cgx (even if it ignores it)
        scores_path = requested_scores

        # Run the engine via cgx.bat, from inside the bundle directory
        proc = subprocess.Popen(
            ["cmd.exe", "/c", self.cgx_path, survivors_path, scores_path],
            cwd=self.bundle_dir,              # IMPORTANT: run from bundle dir
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        try:
            stdout, stderr = proc.communicate(timeout=180)  # 3 minutes for debugging
        except subprocess.TimeoutExpired:
            print(f"EVAL {individual.id}: cgx TIMEOUT, killing process")
            proc.kill()
            stdout, stderr = proc.communicate()
            return 0.0
        
        if stderr:
            print(stderr.decode(errors="ignore"))

        t1 = time.time()
        # print(f"EVAL {individual.id}: cgx finished in {t1 - t0:.1f}s, rc={proc.returncode}")
        if stdout:
            print("cgx stdout:", stdout.decode(errors="ignore")[:500])
        if stderr:
            print("cgx stderr:", stderr.decode(errors="ignore")[:500])

        # cgx sometimes ignores requested path and writes bundle/scores.csv
        actual_scores = None
        if os.path.exists(requested_scores):
            actual_scores = requested_scores
        elif os.path.exists(default_scores):
            actual_scores = default_scores

        if actual_scores is None:
            print("EVAL: no scores file produced")
            print("Requested:", requested_scores)
            print("Default:", default_scores)
            return 0.0

        # Copy to per-individual file so it will not be overwritten by the next eval
        if actual_scores != requested_scores:
            shutil.copy2(actual_scores, requested_scores)

        scores_path = requested_scores

        base = f"{individual.id}try"
        deadline = time.time() + 60
        txt = ""

        while time.time() < deadline:
            if os.path.exists(scores_path):
                with open(scores_path, "r", encoding="utf-8", errors="ignore") as f:
                    txt = f.read()
                if base in txt:
                    break
            time.sleep(0.5)

        if base not in txt:
            print("EVAL: scores file exists but missing my warrior:", base)
            print("Scores path:", scores_path)
            return 0.0



        # Read and process scores
        results = self._read_scores(scores_path, individual_name1)
        #print("EVAL parsed group rows:", results["group_data"][:2], "indiv rows:", results["indiv_data"][:2])

        # norm_indiv1 = normalize_data(results["indiv_data"], results["indiv1_index"])
        # fitness1 = fitness_calculation(
        #     norm_indiv1[SCORE],
        #     norm_indiv1[LIFETIME],
        #     norm_indiv1[BYTES],
        #     norm_indiv1[RATE],
        # )

        # norm_indiv2 = normalize_data(results["indiv_data"], results["indiv2_index"])
        # fitness2 = fitness_calculation(
        #     norm_indiv2[SCORE],
        #     norm_indiv2[LIFETIME],
        #     norm_indiv2[BYTES],
        #     norm_indiv2[RATE],
        # )

        norm_group = normalize_data(results["group_data"], results["group_index"])
        fitness_group = fitness_calculation(
            norm_group[SCORE],
            norm_group[LIFETIME],
            norm_group[BYTES],
            norm_group[RATE],
        )
        #print(f"EVAL id={individual.id} group_row={norm_group} fitness_group={fitness_group}")

        
        # individual.extra_stats = {
        #     "fitness1": float(fitness1),
        #     "fitness2": float(fitness2),
        #     "fitness_group": float(fitness_group),
        #     "norm_group": [float(x) for x in norm_group],
        # }


        # Remove the compiled individual warriors from survivors
        for name in (individual_name1, individual_name2):
            compiled_path = os.path.join(survivors_path, name)
            if os.path.exists(compiled_path):
                os.remove(compiled_path)



        return float(fitness_group)

        #return [fitness1, fitness2, fitness_group, norm_group]





    def calculate_avg_fitness(self, individual):
        # This function is relevant for more than one opponent
        all_train_set = os.listdir(os.path.join(self.root_path, "corewars8086-master\\bundle", "survivors"))
        opponents = list(set([survivor[:-1] for survivor in all_train_set]))

        eval_results = self.executor.map(self.evaluate_individual, [individual] * len(opponents), opponents)
        fitness_array = []
        for opp, result in zip(opponents, eval_results):
            fitness_array.append(result)

        # calculate the average fitness between all the games against each opponent
        first_tree = sum(fit[0] for fit in fitness_array) / len(fitness_array)
        second_tree = sum(fit[1] for fit in fitness_array) / len(fitness_array)
        group = sum(fit[2] for fit in fitness_array) / len(fitness_array)
        score = sum(fit[3][SCORE] for fit in fitness_array) / len(fitness_array)
        life = sum(fit[3][LIFETIME] for fit in fitness_array) / len(fitness_array)
        bytes = sum(fit[3][BYTES] for fit in fitness_array) / len(fitness_array)
        rate = sum(fit[3][RATE] for fit in fitness_array) / len(fitness_array)

        return [first_tree, second_tree, group, [score, life, bytes, rate]]

    def __getstate__(self):
        state = self.__dict__.copy()
        del state['executor']

        return state

    # Necessary for valid unpickling, since SimpleQueue object cannot be pickled
    def __setstate__(self, state):
        self.__dict__.update(state)
        self.executor = ThreadPoolExecutor(max_workers=4)



def normalize_data(data, index):
    data = np.array(data).astype(float)

    if len(data) == 0:
        return [0, 0, 0, 0]

    if index >= len(data):
        index = len(data) - 1

    score = data[index][SCORE]
    lifetime = data[index][LIFETIME]
    bytes_written = data[index][BYTES]
    rate = data[index][RATE]
    return [score, lifetime, bytes_written, rate]


def fitness_calculation(score, alive_time, bytes_written, writing_rate):
   # if bytes_written >= 5:
    #    bytes_written = 10 # 4 is the maximum in regular commands
    max_value = 10
    return round(2 * score + 0.02 * alive_time + 0.03 * min(max_value, bytes_written) + 0.01 * min(max_value, writing_rate), 5)


def create_survivor_name(individual):
    """
    returning the survivior name without number at the end
    """
    if individual[-1] == '1' or individual[-1] == '2':
        return individual[:-1]
    
    return individual  # if no number at the end, return as is


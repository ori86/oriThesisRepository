# assembly_individual.py
import copy
import itertools
from eckity.genetic_encodings.gp.tree.tree_individual import Tree

class AssemblyIndividual(Tree):
    id_iter = itertools.count()

    def __init__(self,
                 *,
                 function_set,
                 terminal_set,
                 erc_range=None,
                 root_type=None,
                 fitness=None,
                 fitness1=None,
                 fitness2=None,
                 update_parents=False):
        # Match Tree.__init__(fitness, function_set, terminal_set, tree=None, erc_range=None, root_type=None, update_parents=False)
        super().__init__(fitness=fitness,
                         function_set=function_set,
                         terminal_set=terminal_set,
                         tree=None,
                         erc_range=erc_range,
                         root_type=root_type,
                         update_parents=update_parents)

        # Two internal trees with their own fitnesses
        self.tree1 = Tree(fitness=fitness1 or copy.deepcopy(fitness),
                          function_set=function_set,
                          terminal_set=terminal_set,
                          tree=None,
                          erc_range=erc_range,
                          root_type=root_type,
                          update_parents=update_parents)

        self.tree2 = Tree(fitness=fitness2 or copy.deepcopy(fitness),
                          function_set=function_set,
                          terminal_set=terminal_set,
                          tree=None,
                          erc_range=erc_range,
                          root_type=root_type,
                          update_parents=update_parents)

        self.id = next(self.id_iter)
        self.fitness_parts = []

    def size(self):
        return max(self.tree1.size(), self.tree2.size())

    def empty_tree(self):
        self.tree1.empty_tree()
        self.tree2.empty_tree()

    def depth(self):
        return max(self.tree1.depth(), self.tree2.depth())

    # If you really need output markers, keep them; otherwise remove the file-like 'output'
    def execute1(self, *args, **kwargs):
        return self.tree1.execute(*args, **kwargs)

    def execute2(self, *args, **kwargs):
        return self.tree2.execute(*args, **kwargs)

    def execute(self, *args, **kwargs):
        r1 = self.execute1(*args, **kwargs)
        r2 = self.execute2(*args, **kwargs)
        return r1, r2

    def random_subtree1(self, node_type=None):
        return self.tree1.random_subtree(node_type)

    def random_subtree2(self, node_type=None):
        return self.tree2.random_subtree(node_type)

    def replace_subtree1(self, old_subtree, new_subtree):
        self.tree1.replace_subtree(old_subtree, new_subtree)

    def replace_subtree2(self, old_subtree, new_subtree):
        self.tree2.replace_subtree(old_subtree, new_subtree)

    def show(self):
        print("tree 1:\n")
        self.tree1.show()
        print("\ntree 2:\n")
        self.tree2.show()

    def set_evaluation(self, prev_fitness1, prev_fitness2, prev_fitness, fitness_parts):
        self.tree1.fitness.set_fitness(prev_fitness1)
        self.tree2.fitness.set_fitness(prev_fitness2)
        self.fitness.set_fitness(prev_fitness)
        self.fitness_parts = fitness_parts

    def unset_evaluation(self):
        self.tree1.fitness.set_not_evaluated()
        self.tree2.fitness.set_not_evaluated()
        self.fitness.set_not_evaluated()

    def deep_copy(self):
        indiv_copy = copy.deepcopy(self)
        indiv_copy.set_evaluation(self.tree1.fitness.get_pure_fitness(),
                                  self.tree2.fitness.get_pure_fitness(),
                                  self.fitness.get_pure_fitness(),
                                  self.fitness_parts)
        return indiv_copy

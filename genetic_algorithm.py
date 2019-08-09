
# task: maximize value y = of x^5 + 2.94*x^4 - 31.2x^3 + 15x^2 -300x  - 115
# gene has two traits, a and b, both integers ranging from 1 to 100
# fit function is x^2 + x +  y + w + z.

import random
from matplotlib import pyplot as plt

class Genome(object):
    gene_pool = {}

    def __init__(self, traits = {}):
        if len(traits) == 0:
            traits = {
                '1': random.random()*1000,
                '2': random.random()*1000,
                '3': random.random()*1000,
                '4': random.random()*1000,
                '5': random.random()*1000
            }
        self.traits = traits # traits are a dictionary obj
        self.fitness = self.get_fitness()
        Genome.update_gene_pool(self)
        return None

    def mutate(self, trait):
        self.traits[trait] = random.random()*1000
        Genome.update_gene_pool(self)
        return None

    def get_traits(self):
        return self.traits

    def get_fitness(self):
        #sum = 0
        #for i in self.traits.keys():
         #   sum = sum + self.traits[i]
        fitness = (
                 self.traits['1']
            +   self.traits['2']
            +   self.traits['3']
            +   self.traits['4']
            +   self.traits['5']
        )
        return fitness

    def __add__(self, other):
        child_traits = {'1': None, '2': None, '3': None, '4': None, '5': None}
        which_parent = 1
        for i in child_traits.keys():
            which_parent = random.randint(1, 3)
            child_traits[i] = self.traits[i] if which_parent == 1 else other.traits[i]
        child = Genome(child_traits)
        if child.get_fitness() <= max(self.get_fitness(), other.get_fitness()):
            child.mutate(
                str( random.randint(1,5) )
            )
        return child

    def __str__(self):
       return f"traits: {self.get_traits()}, \n fitness: {self.get_fitness()}"

    @classmethod
    def update_gene_pool(cls, genome):
        cls.gene_pool[genome] = genome.get_fitness()
        return None

    @classmethod
    def get_gene_pool(cls, pos = -1):
        if pos >= 0:
            try:
                gene_pool_list = [i for i in cls.gene_pool.items()]
                return gene_pool_list[pos]
            except IndexError:
                print("Subscript out of bound. Returning the full gene_pool instead.")
                return cls.gene_pool
        else:
            return cls.gene_pool

    @classmethod
    def set_gene_pool(cls, new_gene_pool):
        cls.gene_pool = new_gene_pool
        return None

    @classmethod
    def top_n_genomes(cls, n = 2):
        ranked_by_fitness = Genome.sort_by_value(cls.gene_pool)
        return dict(tuple(ranked_by_fitness[0:n]))

    @staticmethod
    def sort_by_value(dict):
        output = sorted(dict.items(), key = lambda t: t[1], reverse = True)
        return output #ouputs a list!

class Natural_Selection():
    def __init__(
            self,
            max_epochs = 100,
            keep_top_n = 50,
            selection_ratio = 0.01,
    ):
        self.max_epochs = int(max_epochs)
        self.keep_top_n = int(keep_top_n)
        self.selection_ratio = selection_ratio
        self.population_size = int(keep_top_n/selection_ratio)
        return None

    def launch(self, show_polt = True):
        for i in range(int(self.population_size)):
            Genome()
        x = []
        y = []
        Genome.set_gene_pool(Genome.top_n_genomes(self.keep_top_n))
        epoch = 0
        for j in range(self.max_epochs):
            epoch = epoch + 1
            x.append(epoch)
            for i in range(self.population_size):
                parent1 = Genome.get_gene_pool(random.randint(0, self.keep_top_n - 1))[0]
                parent2 = Genome.get_gene_pool(random.randint(0, self.keep_top_n - 1))[0]
                child = parent1 + parent2
            Genome.set_gene_pool(Genome.top_n_genomes(self.keep_top_n))
            y.append(Genome.get_gene_pool(0)[1])
            best_genome = Genome.get_gene_pool(0)[0]
        if show_polt:
            plt.xkcd()
            plt.plot(x, y, color = 'turquoise', marker = '.')
            plt.xlabel("Epoch")
            plt.ylabel("Fitness")
            plt.show()
        print(best_genome)
        return best_genome

def main():
    scenario = Natural_Selection(selection_ratio = .01, max_epochs= 40, keep_top_n = 10)
    scenario.launch(show_polt= True)


if __name__ == "__main__":
    main()



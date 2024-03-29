from contrast_opt.multilayer import MultiLayer
import pygad
from contrast_opt.multilayer import *
from contrast_opt.materialutil import *
import numpy as np

class ContrastOpt:
    def __init__(self, multilayer: MultiLayer):
        self.multilayer = multilayer
        self.nk_tensor = multilayer.nk_tensor
        self.wls = multilayer.wls
        self.lambda_ref = multilayer.lambda_ref
        self.lambda_ref_index = np.argmin(np.abs(self.wls-self.lambda_ref))
        self.num_levels = len(multilayer.levels)
        self.num_layers = len(multilayer.layers)
        self.optimal_thickness = None
        self.optimise_quantity = multilayer.optimise_quantity

    def my_fitness_func(self, optimise_what="R"):
        if self.optimise_quantity is not None:
            optimise_what = self.optimise_quantity
        if optimise_what == "R":
            def fitness_func(ga_instance, solution, solution_idx):
                thickness_tensor = generate_thickness_tensor(self.nk_tensor, solution)
                level_spectra = calc_R(self.nk_tensor, thickness_tensor, self.wls)
                R_levels = []
                # Calculate the fitness based on the spectra
                fitness = 0
                # Optimise at a single wavelength
                i_wl = self.lambda_ref_index
                for i_lvl in range(self.num_levels):
                    R_levels.append(level_spectra[i_lvl,i_wl])
                R_levels.sort()
                R_levels = np.array(R_levels)
                delta_R = R_levels[1:-1] - R_levels[0:-2]
                mean_delta_R = np.mean(delta_R)
                max_delta_R = R_levels[-1]-R_levels[0]
                w_mean_delta_R = 10 # Contrast between levels should weigh heigher
                fitness = max_delta_R - w_mean_delta_R*np.sqrt(np.sum((mean_delta_R-delta_R)**2))
                # fitness = np.prod(delta_R)
                # for i_lvl in range(num_levels-1):
                #     fitness += R_levels[i_lvl+1]/R_levels[i_lvl]
                return fitness
            
        elif optimise_what == "argR":
                def fitness_func(ga_instance, solution, solution_idx):
                    thickness_tensor = generate_thickness_tensor(self.nk_tensor, solution)
                    level_spectra = calc_argR(self.nk_tensor, thickness_tensor, self.wls)
                    levels = []
                    fitness = 0 # Calculate the fitness based on the spectra
                    # Optimise at a single wavelength
                    i_wl = self.lambda_ref_index
                    for i_lvl in range(self.num_levels):
                        levels.append(level_spectra[i_lvl,i_wl])
                    levels.sort()
                    levels = np.array(levels)
                    argR_targets = np.linspace(0,2*np.pi,num=len(levels), endpoint=False) # For len(levels)=4: targetR=[0, pi/2, pi, 3pi/4]
                    delta_targets = 0
                    for i, level in enumerate(levels):
                        delta_target_1 = np.abs(argR_targets[i]-levels[i])
                        delta_target_2 = 2*np.pi - delta_target_1
                        delta_targets = delta_targets + min(delta_target_1, delta_target_2) # Shortest arc length
                    delta_levels = levels[1:-1] - levels[0:-2]
                    mean_delta_levels = np.mean(delta_levels)
                    fitness = -delta_targets - 0*np.sqrt(np.sum((mean_delta_levels-delta_levels)**2))
                    return fitness
                
        elif optimise_what == "argT":
                def fitness_func(ga_instance, solution, solution_idx):
                    thickness_tensor = generate_thickness_tensor(self.nk_tensor, solution)
                    level_spectra = calc_argT(self.nk_tensor, thickness_tensor, self.wls)
                    levels = []
                    fitness = 0 # Calculate the fitness based on the spectra
                    # Optimise at a single wavelength
                    i_wl = self.lambda_ref_index
                    for i_lvl in range(self.num_levels):
                        levels.append(level_spectra[i_lvl,i_wl])
                    levels.sort()
                    levels = np.array(levels)
                    argR_targets = np.linspace(0,2*np.pi,num=len(levels), endpoint=False) # For len(levels)=4: targetR=[0, pi/2, pi, 3pi/4]
                    delta_targets = 0
                    for i, level in enumerate(levels):
                        delta_target_1 = np.abs(argR_targets[i]-levels[i])
                        delta_target_2 = 2*np.pi - delta_target_1
                        delta_targets = delta_targets + min(delta_target_1, delta_target_2) # Shortest arc length
                    delta_levels = levels[1:-1] - levels[0:-2]
                    mean_delta_levels = np.mean(delta_levels)
                    fitness = -delta_targets - 0*np.sqrt(np.sum((mean_delta_levels-delta_levels)**2))
                    return fitness
                
        return fitness_func

    def init_ga(self):

        fitness_func = self.my_fitness_func()

        def callback_gen(ga_instance):
            if ga_instance.generations_completed % 10 == 0:
                print("Generation : ", ga_instance.generations_completed)
                print("Fitness of the best solution :", ga_instance.best_solution()[1])


        self.ga_instance = pygad.GA(num_generations=self.num_generations,
                            parent_selection_type="rank",
                            num_parents_mating=self.num_parents_mating, 
                            fitness_func=fitness_func,
                            sol_per_pop=self.sol_per_pop, 
                            num_genes=self.num_layers,
                            # init_range_low=self.init_range_low,
                            # init_range_high=self.init_range_high,
                            mutation_percent_genes=self.mutation_percent_genes,
                            gene_space=self.gene_space,
                            on_generation=callback_gen)

    def run_ga(self):
        self.ga_instance.run()
        solution, solution_fitness, solution_idx = self.ga_instance.best_solution()
        self.optimal_thickness = solution

    def plot_ga_results(self):
        fig = self.ga_instance.plot_fitness()

        solution, solution_fitness, solution_idx = self.ga_instance.best_solution()
        print("Parameters of the best solution : {solution}".format(solution=solution))
        print("Fitness value of the best solution = {solution_fitness}".format(solution_fitness=solution_fitness))
        print("Index of the best solution : {solution_idx}".format(solution_idx=solution_idx))
        return fig

    def init_optimisation(self, indata_file):
        self.load_data(indata_file)

    def load_data(self, indata_file):
        indata = load_settings(indata_file)
        self.sol_per_pop = indata["sol_per_pop"]
        # self.init_range_low = indata["init_range_low"]
        # self.init_range_high = indata["init_range_high"]
        self.mutation_percent_genes = indata["mutation_percent_genes"]
        self.num_generations = indata["num_generations"]
        self.num_parents_mating = indata["num_parents_mating"]
        self.gene_space = self.load_thickness_constraints(indata)


    def load_thickness_constraints(self, indata):
        """
        indata: indata dictionary
        """
        thickness_range = indata["layer_thickness_range"]

        gene_space = []

        ### t_range[2]==0: Genes take values from a continuous range
        ### t_range[2]!=0: Genes take values from a discrete range
        for t_range in thickness_range:
            if t_range[2] == 0:
                gene_space.append({'low': t_range[0], 'high': t_range[1]})
            else:
                gene_space.append({'low': t_range[0], 'high': t_range[1], 'step': t_range[2]})

        return gene_space
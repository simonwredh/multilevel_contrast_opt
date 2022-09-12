from contrast_opt.materialutil import *
from contrast_opt.optics import *
from contrast_opt.multilayer import *
from contrast_opt.optimisation import *
from contrast_opt import figutil

import numpy as np
import shutil


if __name__ == "__main__":
    print("Running example 2...")
    # Model input data
    indata_file = "indata_test.yaml"
    # Thickness of layer
    my_t = np.array([8,5,15])

    # Prepare the structure
    multilayer = MultiLayer()
    multilayer.init_multilayer(indata_file)
    multilayer.set_layer_thickness(my_t)
    stack_name = multilayer.description
    R = multilayer.calc_R()
    # fig_stack_init, ax = multilayer.plot_R()

    # Run optimisation
    contrastopt = ContrastOpt(multilayer)
    contrastopt.init_optimisation(indata_file)
    contrastopt.init_ga()
    contrastopt.run_ga()
    fig_ga = contrastopt.plot_ga_results()

    # Create reflectivity plot of optimised stack
    multilayer.set_layer_thickness(contrastopt.optimal_thickness)
    R = multilayer.calc_R()
    fig_stack_opt, ax = multilayer.plot_R()

    # Create a report file
    report = {
        "description": multilayer.description,
        "ambient": multilayer.ambient,
        "substrate": multilayer.substrate,
        "layers": multilayer.layers,
        "optimal_thickness": contrastopt.optimal_thickness.tolist(), 
    }
    report_file = "report.yaml"

    # Dump the report to a yaml file
    with open(report_file, 'w') as file:
        yaml.dump(report, file, default_flow_style=False, sort_keys=False)

    # Save stuff
    figutil.savefig(f"{stack_name}_ga.png",fig_handle=fig_ga)
    figutil.savefig(f"{stack_name}_opt.png",fig_handle=fig_stack_opt)

    shutil.copy(indata_file,figutil.DATEDIR)
    shutil.copy(report_file,figutil.DATEDIR)
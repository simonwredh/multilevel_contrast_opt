from contrast_opt.materialutil import *
from contrast_opt.optics import *
from contrast_opt.multilayer import *
from contrast_opt.optimisation import *
from contrast_opt import ioutil

import numpy as np
import shutil
from datetime import datetime


if __name__ == "__main__":
    print("Running contrast optimisation...")

    # Model input parameters
    indata_file = "indata.yaml"

    # Thickness of layer
    my_t = np.array([8,5,15]) # Not required for optimisation

    # Prepare the structure
    multilayer = MultiLayer()
    multilayer.init_multilayer(indata_file)
    multilayer.set_layer_thickness(my_t) # Not required for optimisation
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
    plt.show()

    # Create a report file
    report = {
        "date": datetime.now().strftime("%Y%m%d %H:%M:%S"),
        "description": multilayer.description,
        "ambient": multilayer.ambient,
        "substrate": multilayer.substrate,
        "layers": multilayer.layers,
        "optimal_thickness": contrastopt.optimal_thickness.tolist(), 
    }
    report_file_out = f"{stack_name}_report.yaml"
    indata_file_out = f"{stack_name}_indata.yaml"

    # Dump the report to a yaml file
    with open(report_file_out, 'w') as file:
        yaml.dump(report, file, default_flow_style=False, sort_keys=False)

    # Save stuff
    outdir, datedir = ioutil.mkoutdir() # Create an out directory named after today's date
    ioutil.savefig(f"{stack_name}_ga.png",fig_handle=fig_ga)
    ioutil.savefig(f"{stack_name}_opt.png",fig_handle=fig_stack_opt)
    
    indata_out = os.path.join(datedir, indata_file_out)
    report_out = os.path.join(datedir, report_file_out)
    shutil.copy(indata_file, indata_out)
    shutil.move(report_file_out, report_out)
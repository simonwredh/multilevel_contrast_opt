# contrast_opt
Contrast optimisation of multi-layer stacks

Objective:
- Maximise optical contrast between different programmable states of a multi-layer PCM stack.

Method:
- Transfer matrix method to solve the Fresnel equations
    - Currently using implementation from https://github.com/MLResearchAtOSRAM/tmm_fast
- Genetic algorithm for optimising the thickness of the independent layers in the multi-layer stack
    - Using PyGAD package https://pygad.readthedocs.io/en/latest/

Input data required:
- Amorphous and crystalline (n,k) for each PCM in the stack
- (n,k) for diffusion barrier

Input parameters:
- Input parameters for the material structure and optimisation are supplied in indata.yaml

Cost function for optimisation:
- The current cost function tries to do the following
    - Maximise the distance between minimum and maximum reflectivity levels at the reference wavelength
    - Equalize the distance between neighbouring reflectivity levels at the reference wavelength

Constraints
- The thickness range of each layer can be constrained in indata.yaml
- Not implemented: total stack thickness
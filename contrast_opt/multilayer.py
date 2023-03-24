from contrast_opt.materialutil import *
from contrast_opt.optics import *

class MultiLayer:
    def __init__(self, indata_file=None):
        if indata_file is not None:
            self.init_multilayer(indata_file)
        pass

    def calc_R(self):
        R = calc_R(self.nk_tensor, self.thickness_tensor, self.wls)
        self.reflectivity = R
        return R
    
    def calc_T(self):
        T = calc_T(self.nk_tensor, self.thickness_tensor, self.wls)
        self.transmission = T
        return T

    def plot_R(self):
        fig, ax = plt.subplots()
        for i,R in enumerate(self.reflectivity):
            plt.plot(self.wls, R, label=self.levels[i])
        plt.xlabel("Wavelength (nm)")
        plt.ylabel("Reflectance")
        plt.legend()
        return fig, ax
    
    def plot_T(self):
        fig, ax = plt.subplots()
        for i,T in enumerate(self.transmission):
            plt.plot(self.wls, T, label=self.levels[i])
        plt.xlabel("Wavelength (nm)")
        plt.ylabel("Transmission")
        plt.legend()
        return fig, ax

    def set_layer_thickness(self, t_layers=None):
        if t_layers is not None:
            self.layer_thickness = t_layers
            self.layer_thickness_all = np.concatenate([[np.inf], t_layers, [np.inf]])
        else:
            self.layer_thickness_all = np.concatenate([[np.inf], self.layer_thickness, [np.inf]])
        self.thickness_tensor = generate_thickness_tensor(self.nk_tensor, self.layer_thickness)


    def init_multilayer(self, indata_file):
        self.load_data(indata_file)
        self.nk_dict = create_nk_dict(self.materials_dict)
        self.material_states = create_material_states_dict(self.layers, self.materials_dict)
        self.levels = generate_levels(self.layers, self.material_states)
        self.levels_all = generate_levels(self.layers_all, self.material_states)
        self.nk_tensor = generate_nk_tensor(self.levels_all, self.layers_all, self.wls, self.nk_dict, self.materials_path)
        self.print_multilayer()

    def load_data(self, indata_file):
        indata = load_settings(indata_file)
        self.description = indata["description"]
        self.materials_dict = indata["materials"]
        self.materials_path = indata["materials_path"]
        self.substrate = indata["substrate"]
        self.ambient = indata["ambient"]
        self.layers = indata["layers"]
        self.layers_all = [self.ambient] + self.layers + [self.substrate] 
        self.lambda_min = indata["lambda_min"]
        self.lambda_max = indata["lambda_max"]
        self.lambda_ref = indata["lambda_ref"]
        self.layer_thickness = indata["layer_thickness"]
        self.wls = np.linspace(self.lambda_min,self.lambda_max, self.lambda_max-self.lambda_min)

    def print_multilayer(self):
        print(f"Stack layers: \n {self.layers}")
        print(f"Stack levels: \n {self.levels}")
    

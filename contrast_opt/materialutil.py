import yaml
import os.path
import itertools
import numpy as np
from scipy.interpolate import interp1d

def load_settings(settings_file = "indata.yaml"):
    with open(settings_file, "r") as file:
        settings_dict = yaml.load(file, Loader=yaml.Loader)
    return settings_dict

def create_nk_dict(materials_dict):
    nk_dict = {}
    for material in materials_dict:
        for i,state in enumerate(material["states"]):
            nk_dict[state] = material["nk_files"][i]
    return nk_dict

def create_material_states_dict(layers, materials_dict):
    material_states_dict = {}
    for layer in layers:
        for material in materials_dict:
            if material["name"] == layer:
                material_states_dict[layer] = material["states"]
    return material_states_dict

def generate_levels(layers, material_states):
    """
    Generates all different level combinations of pcm states
    
    material_states: dictonary of possible material states
    """
    combined_layers = []
    for layer in layers:
        if layer in material_states:
            combined_layers.append(material_states[layer])
        else:
            combined_layers.append([layer])
    levels = list(itertools.product(*combined_layers))
    levels = np.asarray(levels)
    return levels

def load_nk_from_text(material_data_path, skiprows=0):
    material_nk = np.loadtxt(material_data_path, skiprows=skiprows)
    return material_nk

def interp_nk(material_nk_data, wls):
    wl = material_nk_data[:,0] # Convert from nm to m
    n = material_nk_data[:,1]
    k = material_nk_data[:,2]
    material_n_fn = interp1d(wl, n, kind='quadratic')
    material_k_fn = interp1d(wl, k, kind='quadratic')
    material_nk = material_n_fn(wls) + material_k_fn(wls)*1j
    return material_nk

def generate_nk_tensor(levels, layers, wls, nk_dict, nk_data_path):
    num_levels = len(levels)
    num_layers = len(layers)
    num_wls = len(wls)

    nk_tensor = np.zeros([num_levels,num_layers,num_wls], dtype=complex)
    for i_lvl, level in enumerate(levels):
        for i_mat, material in enumerate(level):
            if material == "Air":
                nk_tensor[:,i_mat,:] = 1
            else:
                nk_file = nk_dict[material]
                nk_path = os.path.join(nk_data_path,nk_file)
                nk_raw = load_nk_from_text(nk_path)
                nk_interp = interp_nk(nk_raw, wls)
                nk_tensor[i_lvl, i_mat, :] = nk_interp
    return nk_tensor

def generate_thickness_tensor(nk_tensor, t_layers):
    """
    Generates a tensor containing layer thicknesses
    Shape = [num_levels, num_layers]
    """
    num_levels, num_layers, num_wls = nk_tensor.shape
    thickness_tensor = np.zeros([num_levels,num_layers])
    for i,t in enumerate(t_layers):
        thickness_tensor[:,i+1] = t
    thickness_tensor[:,0] = np.inf # Infinite thickness ambient
    thickness_tensor[:,-1] = np.inf # Infinite thickness substrate
    return thickness_tensor
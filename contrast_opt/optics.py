import numpy as np
import matplotlib.pyplot as plt
from contrast_opt.materialutil import *

def tmm_vec(pol,nk_tensor,thickness_tensor,theta,wls):
    """
    Wrapper around tmm_fast's vectorized tmm solver
    """
    from contrast_opt.tmm_fast.vectorized_tmm_dispersive_multistack import coh_vec_tmm_disp_mstack
    result = coh_vec_tmm_disp_mstack(pol,nk_tensor,thickness_tensor,theta,wls)
    return result

def tmm_calc(nk_tensor, thickness_tensor, wls):
    """
    nk_tensor: shape = [num_levels, num_layers, num_wls]
    thickness_tensor: thickness in meters, shape = [num_levels, num_layers]
    wls: wavelenghts in meters
    """
    nk_tensor[:,-1,:] = np.real(nk_tensor[:,-1,:]) # Force substrate to be lossless
    nk_tensor[:,0,:] = np.real(nk_tensor[:,0,:]) # Force ambient to be lossless
    theta = np.linspace(0, 0, 2) * (np.pi/180) # Theta must be a tensor with more than 1 element
    res = tmm_vec('s',nk_tensor,thickness_tensor,theta,wls)
    # R = res['R'][:,0,:]
    return res

def calc_R(nk_tensor, thickness_tensor, wls):
    """
    nk_tensor: shape = [num_levels, num_layers, num_wls]
    thickness_tensor: thickness in meters, shape = [num_levels, num_layers]
    wls: wavelenghts in meters
    """
    nk_tensor[:,-1,:] = np.real(nk_tensor[:,-1,:]) # Force substrate to be lossless
    nk_tensor[:,0,:] = np.real(nk_tensor[:,0,:]) # Force ambient to be lossless

    theta = np.linspace(0, 0, 2) * (np.pi/180) # Theta must be a tensor with more than 1 element
    res = tmm_vec('s',nk_tensor,thickness_tensor,theta,wls)
    R = res['R'][:,0,:]
    return R

def calc_argR(nk_tensor, thickness_tensor, wls):
    """
    nk_tensor: shape = [num_levels, num_layers, num_wls]
    thickness_tensor: thickness in meters, shape = [num_levels, num_layers]
    wls: wavelenghts in meters
    """
    nk_tensor[:,-1,:] = np.real(nk_tensor[:,-1,:]) # Force substrate to be lossless
    nk_tensor[:,0,:] = np.real(nk_tensor[:,0,:]) # Force ambient to be lossless

    theta = np.linspace(0, 0, 2) * (np.pi/180) # Theta must be a tensor with more than 1 element
    res = tmm_vec('s',nk_tensor,thickness_tensor,theta,wls)
    r = res['r'][:,0,:]
    argR = np.pi+np.angle(r)
    return argR

def calc_T(nk_tensor, thickness_tensor, wls):
    """
    nk_tensor: shape = [num_levels, num_layers, num_wls]
    thickness_tensor: thickness in meters, shape = [num_levels, num_layers]
    wls: wavelenghts in meters
    """
    nk_tensor[:,-1,:] = np.real(nk_tensor[:,-1,:]) # Force substrate to be lossless
    nk_tensor[:,0,:] = np.real(nk_tensor[:,0,:]) # Force ambient to be lossless

    theta = np.linspace(0, 0, 2) * (np.pi/180) # Theta must be a tensor with more than 1 element
    res = tmm_vec('s',nk_tensor,thickness_tensor,theta,wls)
    T = res['T'][:,0,:]
    return T

def calc_argT(nk_tensor, thickness_tensor, wls):
    """
    nk_tensor: shape = [num_levels, num_layers, num_wls]
    thickness_tensor: thickness in meters, shape = [num_levels, num_layers]
    wls: wavelenghts in meters
    """
    nk_tensor[:,-1,:] = np.real(nk_tensor[:,-1,:]) # Force substrate to be lossless
    nk_tensor[:,0,:] = np.real(nk_tensor[:,0,:]) # Force ambient to be lossless

    theta = np.linspace(0, 0, 2) * (np.pi/180) # Theta must be a tensor with more than 1 element
    res = tmm_vec('s',nk_tensor,thickness_tensor,theta,wls)
    t = res['t'][:,0,:]
    argT = np.pi+np.angle(t)
    return argT

def calc_r(nk_tensor, thickness_tensor, wls):
    """
    Returns complex reflection coefficient
    nk_tensor: shape = [num_levels, num_layers, num_wls]
    thickness_tensor: thickness in meters, shape = [num_levels, num_layers]
    wls: wavelenghts in meters
    """
    nk_tensor[:,-1,:] = np.real(nk_tensor[:,-1,:]) # Force substrate to be lossless
    nk_tensor[:,0,:] = np.real(nk_tensor[:,0,:]) # Force ambient to be lossless

    theta = np.linspace(0, 0, 2) * (np.pi/180) # Theta must be a tensor with more than 1 element
    res = tmm_vec('s',nk_tensor,thickness_tensor,theta,wls)
    r = res['r'][:,0,:]
    return r

def calc_t(nk_tensor, thickness_tensor, wls):
    """
    Returns complex transmission coefficient
    nk_tensor: shape = [num_levels, num_layers, num_wls]
    thickness_tensor: thickness in meters, shape = [num_levels, num_layers]
    wls: wavelenghts in meters
    """
    nk_tensor[:,-1,:] = np.real(nk_tensor[:,-1,:]) # Force substrate to be lossless
    nk_tensor[:,0,:] = np.real(nk_tensor[:,0,:]) # Force ambient to be lossless

    theta = np.linspace(0, 0, 2) * (np.pi/180) # Theta must be a tensor with more than 1 element
    res = tmm_vec('s',nk_tensor,thickness_tensor,theta,wls)
    t = res['t'][:,0,:]
    return t

# def plot_R(wls,R):
#     for i,y in enumerate(R):
#         plt.plot(wls,y, label=levels[i])
#     plt.legend()
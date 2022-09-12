#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
Copyright (c) 2022, Simon Wredh, SUTD
Created Date: Thursday, July 28th 2022, 9:57:32 am
Author: Simon Wredh
Description: Utility functions for initialising default plot settings and simplifying saving of figures
CHANGELOG:
Date      	By	Comments
----------	---	----------------------------------------------------------
"""

import matplotlib.pyplot as plt
from datetime import date
import os

SMALL_SIZE = 12
MEDIUM_SIZE = 14
BIGGER_SIZE = 16
plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title
plt.rc('lines', linewidth=1.5)


def mkoutdir():
    d = (str(date.today().year) + '-' +
        str(date.today().month).zfill(2) + '-' +
        str(date.today().day).zfill(2))

    out_dir = 'out'
    date_dir = os.path.join('out',d)
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)
    if not os.path.exists(date_dir):
        os.mkdir(date_dir)
    return out_dir, date_dir
    
def savefig(fig_name, plt=plt, fig_handle=None):
    """
    Save figure in ./out/YYYY-MM-DD.
    """
    out_dir, date_dir = mkoutdir()
    save_path = os.path.join(date_dir, fig_name)

    if fig_handle is None:
        plt.gcf().savefig(save_path,bbox_inches='tight',facecolor='white',dpi=300)
    else:
        fig_handle.savefig(save_path,bbox_inches='tight',facecolor='white',dpi=300)
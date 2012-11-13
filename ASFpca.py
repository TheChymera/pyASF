#!/usr/bin/env python
from __future__ import division
__author__ = 'Horea Christian'

from matplotlib.ticker import MultipleLocator, FuncFormatter, FormatStrFormatter
import mdp
import os
import matplotlib.pyplot as plt
import numpy as np
from loadsums import ca_loadsum
from pylab import close, xlabel, ylabel, show, legend, savefig
from mpl_toolkits.axes_grid1 import ImageGrid
from load_vdaq_conds import vdaq_conds
from get_data import unpack_block_file

stim_start = 15
stim_length = 5
en_masse = True # whether or not to show the result for a single block file or export the results of a list of block files

if en_masse == False:
    from get_data import data_name_get
    data_name = data_name_get()
    lenheader, nframesperstim, framewidth, frameheight, _, _, _, _ = unpack_block_file(data_name)
    nframesperstim = np.array(nframesperstim)

    timepts = np.array(nframesperstim)
    img_range_zero = np.arange(0, nframesperstim) # put reading head at the beginning of the baseline condition images (and set limit)
    img_range_one = np.arange(nframesperstim, nframesperstim * 2) # move reading point to the trial condition images (and set limit)
    
    data_type, bytes_per_pixel = vdaq_conds(data_name)
    
    fimg_ca_one = ca_loadsum(data_name, img_range_one, True, data_type, framewidth, frameheight, lenheader, bytes_per_pixel)
    fimg_ca_zero = ca_loadsum(data_name, img_range_zero, True, data_type, framewidth, frameheight, lenheader, bytes_per_pixel)
    fimg_ca = fimg_ca_one / fimg_ca_zero # normalize trial condition to baseline condition
    
    pca = mdp.nodes.PCANode()
    pca_result = pca(fimg_ca)
    pca_time = pca.get_projmatrix()
    
    ica = mdp.nodes.CuBICANode(white_comp=10)
    ica_result = ica(fimg_ca)
    ica_time = ica.get_projmatrix()
    
    
    fig1 = plt.figure(1,(22,10),facecolor='#eeeeee')
    fig1.suptitle('Components according to: PCA (first panel) and ICA (second panel)')
    
    x0=fig1.add_subplot(3,2,1)
    x0.plot(pca_time[:,0]-np.mean(pca_time[:stim_start,0]), 'c', alpha = 1, label="Component 1")
    x0.plot(pca_time[:,1]-np.mean(pca_time[:stim_start,1]), 'm', alpha = 0.9, label="Component 2")
    x0.plot(pca_time[:,2]-np.mean(pca_time[:stim_start,2]), 'y', alpha = 0.8, label="Component 3")
    x0.plot(pca_time[:,3]-np.mean(pca_time[:stim_start,3]), 'k', alpha = 0.7, label="Component 4")
    ylabel('Component Activity', fontsize='12')
    xlabel('Time [s]', fontsize='12')
    x0.xaxis.set_major_formatter(FuncFormatter(lambda x,i: "%.0f" % (x/10)))
    x0.xaxis.set_minor_locator(MultipleLocator(5))
    x0.yaxis.set_major_formatter(FormatStrFormatter('%0.1f'))
    legend(bbox_to_anchor=(1.04, 1.25), ncol=4)
    x0.set_xlim(0, timepts-1)
    
    C = pca_result[:,0]
    height = np.sqrt(len(C))
    a0 = np.reshape(C,(height,height))
    
    C = pca_result[:,1]
    a1 = np.reshape(C,(height,height))
    
    C = pca_result[:,2]
    a2 = np.reshape(C,(height,height))
    
    C = pca_result[:,3]
    a3 = np.reshape(C,(height,height))
    
    C = pca_result[:,4]
    a4 = np.reshape(C,(height,height))
    
    C = pca_result[:,5]
    a5 = np.reshape(C,(height,height))
    
    ZS = [a0, a1, a2]
    grid = ImageGrid(fig1, 323,
                      nrows_ncols = (1, 3),
                      direction="row",
                      axes_pad = 0.4,
                      cbar_location="top",
                      cbar_mode="each",
                      cbar_size="10%",
                      cbar_pad=0.05
                      )
    for ax, z in zip(grid, ZS):
        im = ax.imshow(z,origin="upper",interpolation="none")
        ax.cax.colorbar(im)
    
    ZS = [a3, a4, a5]
    grid = ImageGrid(fig1, 325,
                      nrows_ncols = (1, 3),
                      direction="row",
                      axes_pad = 0.4,
                      cbar_location="top",
                      cbar_mode="each",
                      cbar_size="10%",
                      cbar_pad=0.05
                      )
    for ax, z in zip(grid, ZS):
        im = ax.imshow(z,origin="upper",interpolation="none")
        ax.cax.colorbar(im)
    
    x0=fig1.add_subplot(3,2,2)
    x0.plot(ica_time[:,0]-np.mean(ica_time[:stim_start,0]), 'c', alpha = 1, label="Component 1")
    x0.plot(ica_time[:,1]-np.mean(ica_time[:stim_start,1]), 'm', alpha = 0.9, label="Component 2")
    x0.plot(ica_time[:,2]-np.mean(ica_time[:stim_start,2]), 'y', alpha = 0.8, label="Component 3")
    x0.plot(ica_time[:,3]-np.mean(ica_time[:stim_start,3]), 'k', alpha = 0.7, label="Component 4")
    ylabel('Component Activity', fontsize='12')
    xlabel('Time [s]', fontsize='12')
    x0.xaxis.set_major_formatter(FuncFormatter(lambda x,i: "%.0f" % (x/10)))
    x0.xaxis.set_minor_locator(MultipleLocator(5))
    x0.yaxis.set_major_formatter(FormatStrFormatter('%0.1f'))
    legend(bbox_to_anchor=(1.04, 1.25), ncol=4)
    x0.set_xlim(0, timepts-1)
    
    C = ica_result[:,0]
    height = np.sqrt(len(C))
    a0 = np.reshape(C,(height,height))
    
    C = ica_result[:,1]
    a1 = np.reshape(C,(height,height))
    
    C = ica_result[:,2]
    a2 = np.reshape(C,(height,height))
    
    C = ica_result[:,3]
    a3 = np.reshape(C,(height,height))
    
    C = ica_result[:,4]
    a4 = np.reshape(C,(height,height))
    
    C = ica_result[:,5]
    a5 = np.reshape(C,(height,height))
    
    ZS = [a0, a1, a2]
    grid = ImageGrid(fig1, 324,
                      nrows_ncols = (1, 3),
                      direction="row",
                      axes_pad = 0.4,
                      cbar_location="top",
                      cbar_mode="each",
                      cbar_size="10%",
                      cbar_pad=0.05
                      )
    for ax, z in zip(grid, ZS):
        im = ax.imshow(z,origin="upper",interpolation="none")
        ax.cax.colorbar(im)
    
    ZS = [a3, a4, a5]
    grid = ImageGrid(fig1, 326,
                      nrows_ncols = (1, 3),
                      direction="row",
                      axes_pad = 0.4,
                      cbar_location="top",
                      cbar_mode="each",
                      cbar_size="10%",
                      cbar_pad=0.05
                      )
    for ax, z in zip(grid, ZS):
        im = ax.imshow(z,origin="upper",interpolation="none")
        ax.cax.colorbar(im)
    show()
else:
    from get_data import data_names_get
    data_names = data_names_get()
    for i in data_names:
        lenheader, nframesperstim, framewidth, frameheight, _, _, _, _ = unpack_block_file(i)
        nframesperstim = np.array(nframesperstim)
        
        timepts = np.array(nframesperstim)
        img_range_zero = np.arange(0, nframesperstim) # put reading head at the beginning of the baseline condition images (and set limit)
        img_range_one = np.arange(nframesperstim, nframesperstim * 2) # move reading point to the trial condition images (and set limit)
        
        data_type, bytes_per_pixel = vdaq_conds(i)
        
        fimg_ca_one = ca_loadsum(i, img_range_one, True, data_type, framewidth, frameheight, lenheader, bytes_per_pixel)
        fimg_ca_zero = ca_loadsum(i, img_range_zero, True, data_type, framewidth, frameheight, lenheader, bytes_per_pixel)
        fimg_ca = fimg_ca_one / fimg_ca_zero # normalize trial condition to baseline condition
        
        pca = mdp.nodes.PCANode()
        pca_result = pca(fimg_ca)
        pca_time = pca.get_projmatrix()
        
        ica = mdp.nodes.CuBICANode(white_comp=10)
        ica_result = ica(fimg_ca)
        ica_time = ica.get_projmatrix()
        
        
        fig1 = plt.figure(1,(22,10),facecolor='#eeeeee')
        fig1.suptitle('Components according to: PCA (first panel) and ICA (second panel)')
        
        x0=fig1.add_subplot(3,2,1)
        x0.plot(pca_time[:,0]-np.mean(pca_time[:stim_start,0]), 'c', alpha = 1, label="Component 1")
        x0.plot(pca_time[:,1]-np.mean(pca_time[:stim_start,1]), 'm', alpha = 0.9, label="Component 2")
        x0.plot(pca_time[:,2]-np.mean(pca_time[:stim_start,2]), 'y', alpha = 0.8, label="Component 3")
        x0.plot(pca_time[:,3]-np.mean(pca_time[:stim_start,3]), 'k', alpha = 0.7, label="Component 4")
        ylabel('Component Activity', fontsize='12')
        xlabel('Time [s]', fontsize='12')
        x0.xaxis.set_major_formatter(FuncFormatter(lambda x,i: "%.0f" % (x/10)))
        x0.xaxis.set_minor_locator(MultipleLocator(5))
        x0.yaxis.set_major_formatter(FormatStrFormatter('%0.1f'))
        legend(bbox_to_anchor=(1.04, 1.25), ncol=4)
        x0.set_xlim(0, timepts-1)
        
        C = pca_result[:,0]
        height = np.sqrt(len(C))
        a0 = np.reshape(C,(height,height))
        
        C = pca_result[:,1]
        a1 = np.reshape(C,(height,height))
        
        C = pca_result[:,2]
        a2 = np.reshape(C,(height,height))
        
        C = pca_result[:,3]
        a3 = np.reshape(C,(height,height))
        
        C = pca_result[:,4]
        a4 = np.reshape(C,(height,height))
        
        C = pca_result[:,5]
        a5 = np.reshape(C,(height,height))
        
        ZS = [a0, a1, a2]
        grid = ImageGrid(fig1, 323,
                          nrows_ncols = (1, 3),
                          direction="row",
                          axes_pad = 0.4,
                          cbar_location="top",
                          cbar_mode="each",
                          cbar_size="10%",
                          cbar_pad=0.05
                          )
        for ax, z in zip(grid, ZS):
            im = ax.imshow(z,origin="upper",interpolation="none")
            ax.cax.colorbar(im)
        
        ZS = [a3, a4, a5]
        grid = ImageGrid(fig1, 325,
                          nrows_ncols = (1, 3),
                          direction="row",
                          axes_pad = 0.4,
                          cbar_location="top",
                          cbar_mode="each",
                          cbar_size="10%",
                          cbar_pad=0.05
                          )
        for ax, z in zip(grid, ZS):
            im = ax.imshow(z,origin="upper",interpolation="none")
            ax.cax.colorbar(im)
        
        x0=fig1.add_subplot(3,2,2)
        x0.plot(ica_time[:,0]-np.mean(ica_time[:stim_start,0]), 'c', alpha = 1, label="Component 1")
        x0.plot(ica_time[:,1]-np.mean(ica_time[:stim_start,1]), 'm', alpha = 0.9, label="Component 2")
        x0.plot(ica_time[:,2]-np.mean(ica_time[:stim_start,2]), 'y', alpha = 0.8, label="Component 3")
        x0.plot(ica_time[:,3]-np.mean(ica_time[:stim_start,3]), 'k', alpha = 0.7, label="Component 4")
        ylabel('Component Activity', fontsize='12')
        xlabel('Time [s]', fontsize='12')
        x0.xaxis.set_major_formatter(FuncFormatter(lambda x,i: "%.0f" % (x/10)))
        x0.xaxis.set_minor_locator(MultipleLocator(5))
        x0.yaxis.set_major_formatter(FormatStrFormatter('%0.1f'))
        legend(bbox_to_anchor=(1.04, 1.25), ncol=4)
        x0.set_xlim(0, timepts-1)
        
        C = ica_result[:,0]
        height = np.sqrt(len(C))
        a0 = np.reshape(C,(height,height))
        
        C = ica_result[:,1]
        a1 = np.reshape(C,(height,height))
        
        C = ica_result[:,2]
        a2 = np.reshape(C,(height,height))
        
        C = ica_result[:,3]
        a3 = np.reshape(C,(height,height))
        
        C = ica_result[:,4]
        a4 = np.reshape(C,(height,height))
        
        C = ica_result[:,5]
        a5 = np.reshape(C,(height,height))
        
        ZS = [a0, a1, a2]
        grid = ImageGrid(fig1, 324,
                          nrows_ncols = (1, 3),
                          direction="row",
                          axes_pad = 0.4,
                          cbar_location="top",
                          cbar_mode="each",
                          cbar_size="10%",
                          cbar_pad=0.05
                          )
        for ax, z in zip(grid, ZS):
            im = ax.imshow(z,origin="upper",interpolation="none")
            ax.cax.colorbar(im)
        
        ZS = [a3, a4, a5]
        grid = ImageGrid(fig1, 326,
                          nrows_ncols = (1, 3),
                          direction="row",
                          axes_pad = 0.4,
                          cbar_location="top",
                          cbar_mode="each",
                          cbar_size="10%",
                          cbar_pad=0.05
                          )
        for ax, z in zip(grid, ZS):
            im = ax.imshow(z,origin="upper",interpolation="none")
            ax.cax.colorbar(im)
        le_path, le_file = os.path.split(i)
        le_file, le_extension = os.path.splitext(le_file)        
        if os.path.isdir(le_path+'/ca-figs/'):
            pass
        else: os.mkdir(le_path+'/ca-figs/')    
        savefig(le_path+'/ca-figs/'+le_file+'-ca.png', bbox_inches=0)
        close()
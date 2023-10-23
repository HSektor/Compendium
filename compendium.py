# -*- coding: utf-8 -*-
"""
Created on Mon Sep 19 05:58:18 2022

@author: pc
"""

import numpy as np
from scipy import constants

'''|====|====|====|Constants|====|====|====|'''

c = constants.c

pi = constants.pi

'''|====|====|====|Fun Stuff|====|====|====|'''

def numpy_isqrt(number, x):
    #Quake 3 lmao
    threehalfs = 1.5
    x2 = number * 0.5
    y = np.float32(number)
    
    i = y.view(np.int32)
    i = np.int32(0x5f3759df) - np.int32(i >> 1)
    y = i.view(np.float32)
    
    for i in range(x):
        y = y * (threehalfs - (x2 * y * y))
    return float(y)

#compares elements from lists of lists, this assumes that at least the first element of list1 and 2 is a list
def comparison_multi(list1 , list2):
    if type(list1) == type(list2) == list:
        comp_mat = np.zeros(shape=(len(list1),len(list2)))
        for i in range(len(list1)):
            for j in range(len(list2)):
                dif = sum(np.array(list1[i]) == np.array(list2[j]))
                comp_mat[i,j] = (dif)/((len(list1[i])+len(list2[i]))/2)
        return comp_mat
    else:
        raise TypeError
        
def correlation_matrix(list1):
    if type(list1) == list:
        cormat = np.zeros(shape=(len(list1),len(list1)))
        for i in range(len(list1)):
            for j in range(len(list1)):
                dif = sum(np.array(list1[i]) == np.array(list1[j]))
                cormat[i,j] = ((dif)/len(list1[i]));             
    return cormat

def rect_tf(t, lim):
    """Basic rectangular pulse"""
    return 1 * (abs(t) < lim)

def rcf_tf(nsamples, Rsymbol, Fs, B, r):
    
    #Lower and upper frequencies where RCF transfer function is not constante
    freq_inf_limit= (B/2)*(1-r)
    freq_sup_limit= (B/2)*(1+r)

    #Lower and upper frequencies expressed in the n-domain
    n_inf_limit= int(np.ceil((((nsamples-1)/Fs)*(freq_inf_limit))))
    n_sup_limit= int(np.floor((((nsamples-1)/Fs)*(freq_sup_limit))))

    rc_filter_f = []

    if r==0:
        #Filter transfer function up to the limit where it is constant and unit
        for i in range(0,n_sup_limit):
           rc_filter_f.append(1)
        #Filter transfer function in the range where it is constant and null
        for i in range(n_sup_limit,int(nsamples/2)):
           rc_filter_f.append(0)
    else:
        #Filter transfer function up to the limit where it is constant and unit
        for i in range(0,n_inf_limit):
           rc_filter_f.append(1)
        #Filter transfer function in the range where it is not constant (i.e., it is a raised cosine)
        for i in range(n_inf_limit,n_sup_limit):
           f= (Fs*(i-1)/(nsamples-1)); 
           rc_filter_f.append(0.5*(1-np.sin((pi/(r*Rsymbol))*(f-0.5*Rsymbol))))
        #Filter transfer function in the range where it is constant and null
        for i in range(n_sup_limit,int(nsamples/2)):
           rc_filter_f.append(0)

    #The next loop completes the transfer function values in the double-sided spectrum.
    # Important note: Rigorously, conjugate function should be applied to the 
    # right-hand side of equations below. This was not done because the RC 
    # transfer function is real.
    for i in range(int(nsamples/2), int(nsamples-1)):
       rc_filter_f.append(rc_filter_f[nsamples-i-2])

    #output in frequency and time domains
    rc_filter_f = np.array(rc_filter_f).astype(complex)
    
    return rc_filter_f
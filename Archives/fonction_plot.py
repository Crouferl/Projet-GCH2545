#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 10:13:19 2023

@author: nicolasguillemette
"""

import matplotlib.pyplot as plt


def fonction_plot(x_data_list, y_data_list, list_labels, xlabel='', ylabel='', title='', grid=True, legend=True):
    """fonction permettant de tracer une ou plusieurs courbes
    
    Entrées:
        - vecteur_x : vecteur de données pour l'abscice'
        - vecteur_y : vecteur de données pour l'ordonné
        - list_label : liste de label pour les courbes
        - x_label : Titre abscise (string)
        - y_label : Titre ordonné (string)
        - title : Tire du graphique (string)
        
        
    Sorties
        - graphique de une ou plusieurs courbes
    """
    for i in range(len(x_data_list)):
        plt.plot(x_data_list[i], y_data_list[i], label=list_labels[i])

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    
    if grid:
        plt.grid()
    
    if legend:
        plt.legend()
    
    plt.show()
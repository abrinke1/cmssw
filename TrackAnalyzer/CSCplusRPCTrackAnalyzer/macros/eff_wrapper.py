# ============================
# Runs eff.py in parrallel. 
# Choose your configuration option here.
#
# by David Curry


import sys
import os
import re
import fileinput
import subprocess
import numpy as np
from matplotlib import interactive
from ROOT import *
import multiprocessing



#  ===== Settings ======

# Endcap splitting
endcap_list = []
endcap_list = ['plus', 'minus']


# Run splitting
run_list = []
run_list = ['251168', '251244', '251251', '251252']





# Loop over Endcap list.  Change eff.py as needed

for endcap in endcap_list:


    print '\n\n========== Starting New Endcap Analysis Loop ==========='
    print 'Endcap: ', endcap
    
    if endcap is 'plus':
        new_endcap = '        if reco.gmrEta[iReco] <= 0: continue\n'
        new_plot_name = "newfile = TFile('plots/trig_eff_plots_muonPhys_plusEta.root','recreate')\n"
        

    if endcap is 'minus':
        new_endcap = '        if reco.gmrEta[iReco] >= 0: continue\n'    
        new_plot_name = "newfile = TFile('plots/trig_eff_plots_muonPhys_minusEta.root','recreate')\n"


    for line in fileinput.input('eff.py', inplace=True):

        if 'newfile = TFile' in line:

            print line.replace(line, new_plot_name),

        else: print line,
    # end file modification

    for line in fileinput.input('eff.py', inplace=True):

        if 'if reco.gmrEta[iReco]' in line:

            print line.replace(line, new_endcap),

        else: print line,
    # end file modification

    os.system('python eff.py')    


# end endcap loop


# Loop over Runs
for run in run_list:

    print '\n\n========== Starting New Run Analysis Loop ==========='
    print 'Run: ', run

    new_run = '    if reco.Run != '+run+': continue\n'
    new_plot_name = 'newfile = TFile("plots/trig_eff_plots_muonPhys_allEta_'+run+'.root","recreate")\n'
    
        
    for line in fileinput.input('eff.py', inplace=True):

        if 'newfile = TFile' in line:

            print line.replace(line, new_plot_name),
            
        else: print line,
    # end file modification

    for line in fileinput.input('eff.py', inplace=True):

        if 'if reco.Run' in line:

            print line.replace(line, new_run),

        else: print line,
    # end file modification

    os.system('python eff.py')


# end run loop




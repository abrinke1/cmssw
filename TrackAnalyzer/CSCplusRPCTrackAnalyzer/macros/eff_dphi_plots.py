###########################################
# Plot Maker for quick plots
#
# by David Curry
#
# 7.22.1014
###########################################

import sys
import os
import re
from ROOT import *
from matplotlib import interactive
from ROOT import gROOT


# Root file of Histograms
#file = TFile('plots/mc_allEvents.root')
file = TFile('plots/EMFT_analysis_singleMu.root')


# Get the Hists
dphi12_trk15  = file.Get('dphi12_trk15')
dphi13_trk15  = file.Get('dphi13_trk15')
dphi14_trk15  = file.Get('dphi14_trk15')
dphi23_trk15  = file.Get('dphi23_trk15')
dphi24_trk15  = file.Get('dphi24_trk15')
dphi23_trk15  = file.Get('dphi34_trk15')

dphi_trk15 = file.Get('h2dphi_trk15')
deta_trk15 = file.Get('h2deta_trk15')

dphi_trk10 = file.Get('h2dphi_trk10')
deta_trk10 = file.Get('h2deta_trk10')

dphi_trk15_leg = file.Get('h2dphi_trk15_leg')
deta_trk15_leg = file.Get('h2deta_trk15_leg')

label_list = ['1-2', '1-3', '1-4', '2-3', '2-4', '3-4']


c1 = TCanvas('c1')
c1.SetLogz()
dphi_trk15.SetStats(0)

for i in range(0, len(label_list)):
    dphi_trk15.GetXaxis().SetBinLabel(i+1, label_list[i])
    
dphi_trk15.GetYaxis().SetTitle('EMTF |#Delta #phi|')
dphi_trk15.Draw('COLZ')


c2 = TCanvas('c2')
c2.SetLogz()
deta_trk15.SetStats(0)

for i in range(0, len(label_list)):
    deta_trk15.GetXaxis().SetBinLabel(i+1, label_list[i])

deta_trk15.GetYaxis().SetTitle('EMTF |#Delta #eta|')
deta_trk15.Draw('COLZ')

c3 = TCanvas('c3')
c3.SetLogz()
dphi_trk15_leg.SetStats(0)

for i in range(0, len(label_list)):
    dphi_trk15_leg.GetXaxis().SetBinLabel(i+1, label_list[i])

dphi_trk15_leg.GetYaxis().SetTitle('Legacy |#Delta #phi|')
dphi_trk15_leg.Draw('COLZ')

c5 = TCanvas('c5')
c5.SetLogz()
deta_trk15_leg.SetStats(0)

for i in range(0, len(label_list)):
    deta_trk15_leg.GetXaxis().SetBinLabel(i+1, label_list[i])

deta_trk15_leg.GetYaxis().SetTitle('Legacy |#Delta #eta|')
deta_trk15_leg.Draw('COLZ')


c4 = TCanvas('c4')
c4.SetLogz()
dphi_trk10.SetStats(0)

for i in range(0, len(label_list)):
    dphi_trk10.GetXaxis().SetBinLabel(i+1, label_list[i])

dphi_trk10.GetYaxis().SetTitle('EMTF Mode 10 |#Delta #phi|')
dphi_trk10.Draw('COLZ')

c6 = TCanvas('c6')
c6.SetLogz()
deta_trk10.SetStats(0)

for i in range(0, len(label_list)):
    deta_trk10.GetXaxis().SetBinLabel(i+1, label_list[i])

deta_trk10.GetYaxis().SetTitle('EMTF Mode 10 |#Delta #eta|')
deta_trk10.Draw('COLZ')


raw_input('Press return to continue...')

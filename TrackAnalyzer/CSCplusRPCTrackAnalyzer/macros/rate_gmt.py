########################################################
## eff.py   A script to find CSCTF efficiency by segment-Lct matching
##
## By David Curry
##
########################################################

print '------> Setting Environment'

import sys
from ROOT import *
import numpy as np
from array import *
from collections import Counter
from eff_modules import *


# Set the print level. Default = 0
if len(sys.argv) is 1: printLevel = 0
else: printLevel = sys.argv[1]

print '------> Importing Root File'

# Rate Sample
filename = 'root://eoscms.cern.ch//eos/cms/store/user/dcurry/EMTF/rate_v7/zeroBias_merge_v7.root'

file = TFile.Open(filename)

# Set the branch address of TTree in Tfile
tree = file.Get("ntuple/tree")

# Output Histograms
newfile = TFile("plots/rate.root","recreate")

# A more efficient way to count
muon_count  = Counter()

# Eta Cuts
eta_min = 1.7
eta_max = 2.4


# ================ Histograms ===================

hgbl_pt   = TH1F('hgbl_pt', '', 50 , 0, 50)
hcsctf_pt = TH1F('hcsctf_pt', '', 50 , 0, 50)
hgbl_eta  = TH1F('hgbl_eta', '', 50 , -2.5, 2.5)
hgbl_phi  = TH1F('hgbl_phi', '', 50 , -3.14, 3.14)


# =========== For matching Efficiencies ==========================================
hpt  = TH1F('hpt', '', len(scale_pt_temp)-1,  scale_pt)
heta = TH1F('heta', '', len(scale_eta_temp)-1, scale_eta)
hphi = TH1F('hphi', '', len(scale_phi_temp)-1, scale_phi)

heta_m = TH1F('heta_m', '', len(scale_eta_temp)-1, scale_eta)
heta_p = TH1F('heta_p', '', len(scale_eta_temp)-1, scale_eta)

# EMTF
hpt_trigger  = TH1F('hpt_trigger', '', len(scale_pt_temp)-1, scale_pt)
heta_trigger = TH1F('heta_trigger', '', len(scale_eta_temp)-1, scale_eta)
hphi_trigger = TH1F('hphi_trigger', '', len(scale_phi_temp)-1, scale_phi)
heta_trigger_m = TH1F('heta_trigger_m', '', len(scale_eta_temp)-1, scale_eta)
heta_trigger_p = TH1F('heta_trigger_p', '', len(scale_eta_temp)-1, scale_eta)

hpt_trigger_15_14_13_11  = TH1F('hpt_trigger_15_14_13_11', '', len(scale_pt_temp)-1, scale_pt)
hpt_trigger_15_14_13  = TH1F('hpt_trigger_15_14_13', '', len(scale_pt_temp)-1, scale_pt)
hpt_trigger_15_14  = TH1F('hpt_trigger_15_14', '', len(scale_pt_temp)-1, scale_pt)
hpt_trigger_15  = TH1F('hpt_trigger_15', '', len(scale_pt_temp)-1, scale_pt)

hpt_trigger_gmt = TH1F('hpt_trigger_gmt', '', len(scale_pt_temp)-1, scale_pt)

heta_trigger_15_14_13_11  = TH1F('heta_trigger_15_14_13_11', '', len(scale_eta_temp)-1, scale_eta)
heta_trigger_15_14_13  = TH1F('heta_trigger_15_14_13', '', len(scale_eta_temp)-1, scale_eta)
heta_trigger_15_14  = TH1F('heta_trigger_15_14', '', len(scale_eta_temp)-1, scale_eta)
heta_trigger_15  = TH1F('heta_trigger_15', '', len(scale_eta_temp)-1, scale_eta)

heta_trigger_gmt = TH1F('heta_trigger_gmt', '', len(scale_eta_temp)-1, scale_eta)

heta_trigger_15_14_13_11_m  = TH1F('heta_trigger_15_14_13_11_m', '', len(scale_eta_temp)-1, scale_eta)
heta_trigger_15_14_13_m  = TH1F('heta_trigger_15_14_13_m', '', len(scale_eta_temp)-1, scale_eta)
heta_trigger_15_14_m  = TH1F('heta_trigger_15_14_m', '', len(scale_eta_temp)-1, scale_eta)
heta_trigger_15_m  = TH1F('heta_trigger_15_m', '', len(scale_eta_temp)-1, scale_eta)

hphi_trigger_15_14_13_11  = TH1F('hphi_trigger_15_14_13_11', '', len(scale_phi_temp)-1, scale_phi)
hphi_trigger_15_14_13  = TH1F('hphi_trigger_15_14_13', '', len(scale_phi_temp)-1, scale_phi)
hphi_trigger_15_14  = TH1F('hphi_trigger_15_14', '', len(scale_phi_temp)-1, scale_phi)
hphi_trigger_15  = TH1F('hphi_trigger_15', '', len(scale_phi_temp)-1, scale_phi)

hphi_trigger_gmt = TH1F('hphi_trigger_gmt', '', len(scale_phi_temp)-1, scale_phi)

# CSCTF
hpt_trigger_leg  = TH1F('hpt_trigger_leg', '', len(scale_pt_temp)-1, scale_pt)
heta_trigger_leg = TH1F('heta_trigger_leg', '', len(scale_eta_temp)-1, scale_eta)
hphi_trigger_leg = TH1F('hphi_trigger_leg', '', len(scale_phi_temp)-1, scale_phi)
heta_trigger_m_leg = TH1F('heta_trigger_m_leg', '', len(scale_eta_temp)-1, scale_eta)
heta_trigger_p_leg = TH1F('heta_trigger_p_leg', '', len(scale_eta_temp)-1, scale_eta)

hpt_trigger_gmt_leg = TH1F('hpt_trigger_gmt_leg', '', len(scale_pt_temp)-1, scale_pt)

hpt_trigger_15_14_13_11_leg  = TH1F('hpt_trigger_15_14_13_11_leg', '', len(scale_pt_temp)-1, scale_pt)
hpt_trigger_15_14_13_leg  = TH1F('hpt_trigger_15_14_13_leg', '', len(scale_pt_temp)-1, scale_pt)
hpt_trigger_15_14_leg  = TH1F('hpt_trigger_15_14_leg', '', len(scale_pt_temp)-1, scale_pt)
hpt_trigger_15_leg  = TH1F('hpt_trigger_15_leg', '', len(scale_pt_temp)-1, scale_pt)

heta_trigger_gmt_leg  = TH1F('heta_trigger_gmt_leg', '', len(scale_eta_temp)-1, scale_eta)

heta_trigger_15_14_13_11_leg  = TH1F('heta_trigger_15_14_13_11_leg', '', len(scale_eta_temp)-1, scale_eta)
heta_trigger_15_14_13_leg  = TH1F('heta_trigger_15_14_13_leg', '', len(scale_eta_temp)-1, scale_eta)
heta_trigger_15_14_leg  = TH1F('heta_trigger_15_14_leg', '', len(scale_eta_temp)-1, scale_eta)
heta_trigger_15_leg  = TH1F('heta_trigger_15_leg', '', len(scale_eta_temp)-1, scale_eta)

heta_trigger_15_14_13_11_leg_m  = TH1F('heta_trigger_15_14_13_11_leg_m', '', len(scale_eta_temp)-1, scale_eta)
heta_trigger_15_14_13_leg_m  = TH1F('heta_trigger_15_14_13_leg_m', '', len(scale_eta_temp)-1, scale_eta)
heta_trigger_15_14_leg_m  = TH1F('heta_trigger_15_14_leg_m', '', len(scale_eta_temp)-1, scale_eta)
heta_trigger_15_leg_m  = TH1F('heta_trigger_15_leg_m', '', len(scale_eta_temp)-1, scale_eta)

hphi_trigger_gmt_leg  = TH1F('hphi_trigger_gmt_leg', '', len(scale_phi_temp)-1, scale_phi)

hphi_trigger_15_14_13_11_leg  = TH1F('hphi_trigger_15_14_13_11_leg', '', len(scale_phi_temp)-1, scale_phi)
hphi_trigger_15_14_13_leg  = TH1F('hphi_trigger_15_14_13_leg', '', len(scale_phi_temp)-1, scale_phi)
hphi_trigger_15_14_leg  = TH1F('hphi_trigger_15_14_leg', '', len(scale_phi_temp)-1, scale_phi)
hphi_trigger_15_leg  = TH1F('hphi_trigger_15_leg', '', len(scale_phi_temp)-1, scale_phi)



# Now for all modes
mode_list = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
n_modes = len(mode_list)

hpt_trigger_modes    = [0]*n_modes
heta_trigger_modes   = [0]*n_modes
hphi_trigger_modes   = [0]*n_modes
heta_trigger_m_modes = [0]*n_modes
heta_trigger_p_modes = [0]*n_modes

hpt_trigger_leg_modes     = [0]*n_modes
heta_trigger_leg_modes    = [0]*n_modes
hphi_trigger_leg_modes    = [0]*n_modes
heta_trigger_m_leg_modes  = [0]*n_modes
heta_trigger_p_leg_modes  = [0]*n_modes

for ihist, mode in enumerate(mode_list):
    
    hpt_trigger_modes[ihist]    = TH1F('hpt_trigger_modes_'+str(mode), '', len(scale_pt_temp)-1, scale_pt)
    hpt_trigger_leg_modes[ihist] = TH1F('hpt_trigger_leg_modes_'+str(mode), '', len(scale_pt_temp)-1, scale_pt)
    


# Debug Hists for high pt failures
htrk_2hitmode_fail  = TH1F('htrk_2hitmode_fail', '', 7 , 0, 7)
htrk_2hitmode_all   = TH1F('htrk_2hitmode_all', '', 7 , 0, 7)
htrk_phi_fail       = TH1F('htrk_phi_fail', '', 50 , -3.14, 3.14)
htrk_eta_fail       = TH1F('htrk_eta_fail', '', 50 , -2.5, 2.5)
htrk_dphi_2hit_fail = TH1F('htrk_dphi_2hit_fail', '', 50 , 0, 500) 

htrk_mode_fail = TH1F('htrk_mode_fail', '', 15 , 0, 15)
htrk_mode_all  = TH1F('htrk_mode_all', '', 15 , 0, 15)

htrk_Q_fail = TH1F('htrk_Q_fail', '', 4, 0, 4)
htrk_Q_all  = TH1F('htrk_Q_all', '', 4, 0, 4)

hLct_endcap_fail  = TH1F('hLct_endcap_fail', '', 2 , 0, 1)
hLct_sector_fail  = TH1F('hLct_sector_fail', '', 12 , 0, 12)
hLct_ring_fail    = TH1F('hLct_ring_fail', '', 4 , 0, 4)
hLct_chamber_fail = TH1F('hLct_chamber_fail', '', 42 , 0, 42)

# Delta Phi for Event LCTs
hdphi12 = TH1F('hdphi12', '', 50 , 0, 1.57)
hdphi13 = TH1F('hdphi13', '', 50 , 0, 1.57)
hdphi14 = TH1F('hdphi14', '', 50 , 0, 1.57)
hdphi23 = TH1F('hdphi23', '', 50 , 0, 1.57)
hdphi24 = TH1F('hdphi24', '', 50 , 0, 1.57)
hdphi34 = TH1F('hdphi34', '', 50 , 0, 1.57)

# Delta Phi for EMTF Tracks LCTs
hdphi12_trk = TH1F('hdphi12_trk', '', 50 , 0, 1.57)
hdphi13_trk = TH1F('hdphi13_trk', '', 50 , 0, 1.57)
hdphi14_trk = TH1F('hdphi14_trk', '', 50 , 0, 1.57)
hdphi23_trk = TH1F('hdphi23_trk', '', 50 , 0, 1.57)
hdphi24_trk = TH1F('hdphi24_trk', '', 50 , 0, 1.57)
hdphi34_trk = TH1F('hdphi34_trk', '', 50 , 0, 1.57)

hdphi12_trk15 = TH1F('hdphi12_trk15', '', 50 , 0, 1.57)
hdphi13_trk15 = TH1F('hdphi13_trk15', '', 50 , 0, 1.57)
hdphi14_trk15 = TH1F('hdphi14_trk15', '', 50 , 0, 1.57)
hdphi23_trk15 = TH1F('hdphi23_trk15', '', 50 , 0, 1.57)
hdphi24_trk15 = TH1F('hdphi24_trk15', '', 50 , 0, 1.57)
hdphi34_trk15 = TH1F('hdphi34_trk15', '', 50 , 0, 1.57)

h2dphi_trk15     = TH2F('h2dphi_trk15', '', 6, 1, 7, 20, 0 , 10)
h2dphi_trk15_leg = TH2F('h2dphi_trk15_leg', '', 6, 1, 7, 20, 0 , 10) 

h2deta_trk15 = TH2F('h2deta_trk15', '', 6, 1, 7, 20, 0 , 40)



# efficiency(turn on)
pt_thresh = [5., 7., 10., 12., 16.]
n_thresh = len(pt_thresh)

ptbin = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 16, 20, 100]
ptbin_array = array('d', ptbin)
n_ptbin = len(ptbin)

csctfPt = [0]*n_thresh
csctfPt_eta1 = [0]*n_thresh
csctfPt_eta2 = [0]*n_thresh
csctfPt_eta3 = [0]*n_thresh
csctfPt_eta4 = [0]*n_thresh

csctfPt_all = TH1F('csctfPt_all', '', n_ptbin-1, ptbin_array)
csctfPt_all_eta1 = TH1F('csctfPt_all_eta1', '', n_ptbin-1, ptbin_array)
csctfPt_all_eta2 = TH1F('csctfPt_all_eta2', '', n_ptbin-1, ptbin_array)
csctfPt_all_eta3 = TH1F('csctfPt_all_eta3', '', n_ptbin-1, ptbin_array)
csctfPt_all_eta4 = TH1F('csctfPt_all_eta4', '', n_ptbin-1, ptbin_array)


for ihist, thresh in enumerate(pt_thresh):
    csctfPt[ihist] = TH1F('csctfPt_'+str(thresh), '', n_ptbin-1, ptbin_array)
    csctfPt_eta1[ihist] = TH1F('csctfPt_eta1_'+str(thresh), '', n_ptbin-1, ptbin_array)
    csctfPt_eta2[ihist] = TH1F('csctfPt_eta2_'+str(thresh), '', n_ptbin-1, ptbin_array)
    csctfPt_eta3[ihist] = TH1F('csctfPt_eta3_'+str(thresh), '', n_ptbin-1, ptbin_array)
    csctfPt_eta4[ihist] = TH1F('csctfPt_eta4_'+str(thresh), '', n_ptbin-1, ptbin_array)



# ===== rate ======
rate = [0, 3, 5, 7, 10, 12, 16, 20, 30]
rate_array = array('d', rate)
n_rate = len(rate)
   
hrate     = TH1F('hrate', '', n_rate-1, rate_array)
hrate_leg = TH1F('hrate_leg', '', n_rate-1, rate_array)

hrate_gmt     = TH1F('hrate_gmt', '', n_rate-1, rate_array)
hrate_gmt_leg = TH1F('hrate_gmt_leg', '', n_rate-1, rate_array)

hrate_15_14_13_11 = TH1F('hrate_15_14_13_11', '', n_rate-1, rate_array)
hrate_15_14_13 = TH1F('hrate_15_14_13', '', n_rate-1, rate_array)
hrate_15_14 = TH1F('hrate_15_14', '', n_rate-1, rate_array)
hrate_15 = TH1F('hrate_15', '', n_rate-1, rate_array)

hrate_15_14_13_11_leg  = TH1F('hrate_15_14_13_11_leg', '', n_rate-1, rate_array)
hrate_15_14_13_leg  = TH1F('hrate_15_14_13_leg', '', n_rate-1, rate_array)
hrate_15_14_leg  = TH1F('hrate_15_14_leg', '', n_rate-1, rate_array)
hrate_15_leg  = TH1F('hrate_15_leg', '', n_rate-1, rate_array)

hrate_modes     = [0]*n_modes
hrate_modes_leg = [0]*n_modes

for ihist, mode in enumerate(mode_list):
    hrate_modes[ihist]     = TH1F('hrate_modes_'+str(mode), '', n_rate-1, rate_array)
    hrate_modes_leg[ihist] = TH1F('hrate_leg_modes_'+str(mode), '', n_rate-1, rate_array)



# BX plots
htrkBx     = TH1F('htrkBx', '', 9, -4.5, 4.5)
htrkBx_leg = TH1F('htrkBx_leg', '', 9, -4.5, 4.5)



hist_list = [csctfPt_all, csctfPt_all_eta1, csctfPt_all_eta2, csctfPt_all_eta3, csctfPt_all_eta4, \
                 hgbl_pt, hcsctf_pt, hgbl_eta, hgbl_phi, htrk_2hitmode_fail, htrk_2hitmode_all, \
                 htrk_phi_fail, hLct_chamber_fail, hLct_sector_fail, hLct_endcap_fail, hLct_ring_fail, \
                 htrk_dphi_2hit_fail, htrk_mode_all, htrk_mode_fail, htrk_Q_all, htrk_Q_fail, \
                 hpt, heta, hphi, hpt_trigger, heta_trigger, hphi_trigger, \
                 hdphi12, hdphi13, hdphi14, hdphi23, hdphi24, hdphi34,\
                 hdphi12_trk, hdphi13_trk, hdphi14_trk, hdphi23_trk, hdphi24_trk, hdphi34_trk,\
                 hdphi12_trk15, hdphi13_trk15, hdphi14_trk15, hdphi23_trk15, hdphi24_trk15, hdphi34_trk15,\
                 h2dphi_trk15, h2deta_trk15, h2dphi_trk15_leg,\
                 heta_trigger_m, heta_trigger_p, heta_trigger_m_leg, heta_trigger_p_leg,\
                 hpt_trigger_15_14_13_11, hpt_trigger_15_14_13_11_leg,\
                 hpt_trigger_15_14_13,  hpt_trigger_15_14_13_leg,  hpt_trigger_15_14,  hpt_trigger_15_14_leg,\
                 hpt_trigger_15,  hpt_trigger_15_leg,\
                 hpt_trigger_leg, hphi_trigger_leg, heta_trigger_leg,\
                 heta_trigger_15_14_13_11, heta_trigger_15_14_13_11_leg,\
                 heta_trigger_15_14_13,  heta_trigger_15_14_13_leg,  heta_trigger_15_14,  heta_trigger_15_14_leg,\
                 heta_trigger_15,  heta_trigger_15_leg,\
                 hphi_trigger_15_14_13_11, hphi_trigger_15_14_13_11_leg,\
                 hphi_trigger_15_14_13,  hphi_trigger_15_14_13_leg,  hphi_trigger_15_14,  hphi_trigger_15_14_leg,\
                 hphi_trigger_15,  hphi_trigger_15_leg,\
                 heta_trigger_15_14_13_11_m, heta_trigger_15_14_13_11_leg_m,\
                 heta_trigger_15_14_13_m,  heta_trigger_15_14_13_leg_m,  heta_trigger_15_14_m,  heta_trigger_15_14_leg_m,\
                 heta_trigger_15_m,  heta_trigger_15_leg_m,\
                 hpt_trigger_gmt_leg, heta_trigger_gmt_leg, hphi_trigger_gmt_leg,\
                 hpt_trigger_gmt, heta_trigger_gmt, hphi_trigger_gmt,\
                 hrate, hrate_leg, hrate_15_14_13_11, hrate_15_14_13_11_leg, hrate_15_14_13, hrate_15_14_13_leg,\
                 hrate_15_14, hrate_15_14_leg, hrate_15, hrate_15_leg, hrate_gmt, hrate_gmt_leg,\
                 htrkBx_leg, htrkBx
                 ]

# ==================================================================================================



# ==================================================================================================
# Loop over over events in TFile
for iEvt in range(tree.GetEntries()):

    # for testing
    if iEvt > 500000: break
    
    tree.GetEntry(iEvt)
    
    if iEvt % 10000 is 0: print 'Event #', iEvt
    
    if printLevel > 1:
        print '\n============== New Event # ', tree.event, ' =================\n'\
              '\n  Run             = ', tree.run,  \
              '\n  Muons in Event  = ', tree.numGblRecoMuons,   \
              '\n  Tracks in Event = ', tree.numTrks
        
        
    #if tree.numTrks != 1: continue
    #if tree.numGmtTrks != 1: continue
    #if tree.numGblRecoMuons > 1: continue
    
    # ======================================================================
    # RATE Plots
    
    for icscTrk in range(tree.numTrks):
        
        if abs(tree.trkEta[icscTrk]) < eta_min: continue

        # temp hack to find EMTF Bx
        trkBx = EMTF_Bx(iEvt, tree, icscTrk, printLevel)
        
        #trkBx = tree.trkBx[icscTrk]

        if trkBx != 0: continue
        
        trkPt = tree.trkPt[icscTrk]
        
        trkMode = tree.trkMode[icscTrk]
        
        for bin in reversed(rate):

            if trkPt > bin: 
                hrate.Fill(bin)
         
            if trkPt > bin and trkMode == 15:
                hrate_15_14_13_11.Fill(bin)
                hrate_15_14_13.Fill(bin)
                hrate_15_14.Fill(bin)
                hrate_15.Fill(bin)
                hrate_gmt.Fill(bin)
                
            if trkPt > bin and trkMode == 14:
                hrate_15_14_13_11.Fill(bin)
                hrate_15_14_13.Fill(bin)
                hrate_15_14.Fill(bin)
                hrate_gmt.Fill(bin)

            if trkPt > bin and trkMode == 13:
                hrate_15_14_13_11.Fill(bin)
                hrate_15_14_13.Fill(bin)
                hrate_gmt.Fill(bin)
                
            if trkPt > bin and trkMode == 11:
                hrate_15_14_13_11.Fill(bin)
                hrate_gmt.Fill(bin)
                    
            # legacy GMT Q3
            if trkPt > bin and trkMode == 7:
                hrate_gmt.Fill(bin)
                
            # rate for all modes
            #for ihist, mode in enumerate(mode_list):
            #    if tree.trkMode[icscTrk] == mode:
            #        if tree.trkPt[icscTrk] > bin: 
            #            hrate_modes[ihist].Fill(bin)


    for iLegcscTrk in range(tree.numLegGmtTrks):
        
        if tree.legGMT_trkBx[iLegcscTrk] != 0: continue
        
        if abs(tree.legGMT_trkEta[iLegcscTrk]) < eta_min: continue

        gmt_trkPt = tree.legGMT_trkPt[iLegcscTrk]
        
        for bin in reversed(rate):
            
            if gmt_trkPt > bin and tree.legGMT_trkQual[iLegcscTrk] > 5:
                hrate_gmt_leg.Fill(bin)
                        
# end event loop 



#  ======== Write Hists ==========

# For Mode Histograms
for ihist, mode in enumerate(mode_list):
    
    hpt_trigger_modes[ihist].Write()
    hpt_trigger_leg_modes[ihist].Write()


# For rate
for ihist, rates in enumerate(rate):

    hrate_modes[ihist].Write()
    hrate_modes_leg[ihist].Write()

# Little more work for turn on curves
for ihist, thresh in enumerate(pt_thresh):

    csctfPt[ihist].Write()
    csctfPt_eta1[ihist].Write()
    csctfPt_eta2[ihist].Write()
    csctfPt_eta3[ihist].Write()
    csctfPt_eta4[ihist].Write()
    

for hist in hist_list:
    if isinstance(hist, list):
        newfile.mkdir('%s' % hist[0].GetName()).cd()
        for i in hist: i.Write()
    else: hist.Write()

del newfile

# ================================


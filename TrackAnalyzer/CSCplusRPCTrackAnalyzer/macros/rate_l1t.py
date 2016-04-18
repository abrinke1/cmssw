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
filename = '/afs/cern.ch/work/d/dcurry/private/rpc_mtf8/CMSSW_8_0_0_pre6/src/L1Ntuple.root'
#filename = '/afs/cern.ch/work/a/abrinke1/public/EMTF/Emulator/trees/2016_02_28/EMTF_RATE_ZeroBias4_259626.root'

file = TFile.Open(filename)

# Set the branch address of TTree in Tfile
tree = file.Get("l1UpgradeEmuTree/L1UpgradeTree")

evtTree = file.Get("l1EventTree/L1EventTree")

print tree
print evtTree

# Output Histograms
newfile = TFile("plots/rate.root","recreate")

# A more efficient way to count
counter = Counter()

# Eta Cuts
eta_min = 1.2
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

hrate_fromGMT =  TH1F('hrate_fromGMT', '', n_rate-1, rate_array)


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
                 htrkBx_leg, htrkBx, hrate_fromGMT
                 ]

# ==================================================================================================



# ==================================================================================================
# Loop over over events in TFile
for iEvt in range(tree.GetEntries()):

    # for testing
    #if iEvt > 100: break
    
    tree.GetEntry(iEvt)
    
    evtTree.GetEntry(iEvt)

    if iEvt % 10000 is 0: print 'Event #', iEvt
    
    if printLevel > 1:
        print '\n============== New Event # ', evtTree.Event.event, ' =================\n'\
        '\n  Tracks in Event = ', tree.L1Upgrade.nMuons
    


    # filter runs for WBM rate checks
    #if tree.run != 259626: continue
    #if tree.lumi < 115 or tree.lumi == 168 or tree.lumi == 169 or tree.lumi > 245: continue

    counter['total_events'] += 1
   
    #if tree.numTrks != 1: continue
    #if tree.numLegTrks != 1: continue
    #if tree.numGblRecoMuons > 1: continue
    #if tree.trkMode[0] != tree.leg_trkMode[0]: continue

    # ======================================================================
    # RATE Plots
    
    # uGMT muons(EMTF Muons)
    
    for iTrk in range(0,tree.L1Upgrade.nMuons):

        trkPt = tree.L1Upgrade.muonEt[iTrk]
        trkBx = tree.L1Upgrade.muonBx[iTrk]

        if abs(tree.L1Upgrade.muonEta[iTrk]) < eta_min: continue
                
        if abs(tree.L1Upgrade.muonEta[iTrk]) > eta_max: continue

        if printLevel > 0:
            print '\nEMTF Track #', iTrk,\
                'Pt:', trkPt,\
                'Eta:',  tree.L1Upgrade.muonEta[iTrk],\
                'Phi:',  tree.L1Upgrade.muonPhi[iTrk],\
                'Qual:',  tree.L1Upgrade.muonQual[iTrk],\
                'Bx:',  tree.L1Upgrade.muonBx[iTrk]
             
        if trkBx != 0: continue
        
        if tree.L1Upgrade.muonQual[iTrk] < 12: continue
        
        counter['EMTF_goodTracks'] +=1


        for bin in reversed(rate):

            if trkPt >= bin: 
                hrate.Fill(bin)
         

    '''
    # Fill GMT rates
    for iTrk in range(0,tree.numLegGmtTrks):
        
        if tree.legGMT_trkBx[iTrk] != 0: continue
        
        if abs(tree.legGMT_trkEta[iTrk]) < eta_min: continue
        
        if tree.legGMT_trkQual[iTrk] < 3: continue

        for bin in reversed(rate):
            
            if tree.legGMT_trkPt[iTrk]  >= bin:
                hrate_fromGMT.Fill(bin)
    '''




    '''
    leg_singleMu16_trigger = False
            
    for iLegcscTrk in range(tree.numLegTrks):
        
        #if leg_singleMu16_trigger: continue

        if tree.leg_trkBx[iLegcscTrk] != 0: continue

        if abs(tree.leg_trkEta[iLegcscTrk]) < eta_min: continue

        leg_trkPt = tree.leg_trkPt[iLegcscTrk]

        leg_trkMode = tree.leg_trkMode[iLegcscTrk]

        for bin in reversed(rate):
            
            if leg_trkPt >= bin: 
                hrate_leg.Fill(bin)
                
            if leg_trkPt >= bin and leg_trkMode == 15:
                hrate_15_14_13_11_leg.Fill(bin)
                hrate_15_14_13_leg.Fill(bin)
                hrate_15_14_leg.Fill(bin)
                hrate_15_leg.Fill(bin)
                hrate_gmt_leg.Fill(bin)
                
                if bin == 16:
                    counter['L1GMT_SingleMu16_count'] += 1
                    leg_singleMu16_trigger = True
                    
            if leg_trkPt >= bin and leg_trkMode == 14:
                hrate_15_14_13_11_leg.Fill(bin)
                hrate_15_14_13_leg.Fill(bin)
                hrate_15_14_leg.Fill(bin)
                hrate_gmt_leg.Fill(bin)

                if bin == 16:
                    counter['L1GMT_SingleMu16_count'] += 1
                    leg_singleMu16_trigger = True

            if leg_trkPt >= bin and leg_trkMode == 13:
                hrate_15_14_13_11_leg.Fill(bin)
                hrate_15_14_13_leg.Fill(bin)
                hrate_gmt_leg.Fill(bin)

                if bin == 16:
                    counter['L1GMT_SingleMu16_count'] += 1
                    leg_singleMu16_trigger = True

            if leg_trkPt >= bin and leg_trkMode == 11:
                hrate_15_14_13_11_leg.Fill(bin)
                hrate_gmt_leg.Fill(bin)

                if bin == 16:
                    counter['L1GMT_SingleMu16_count'] += 1
                    leg_singleMu16_trigger = True

            # legacy GMT Q3
            if leg_trkPt >= bin and leg_trkMode == 7:
                hrate_gmt_leg.Fill(bin)

                if bin == 16:
                    counter['L1GMT_SingleMu16_count'] += 1
                    leg_singleMu16_trigger = True
                    
            # rate for all modes
            #for ihist, mode in enumerate(mode_list):
            #    if tree.leg_trkMode[iLegcscTrk] == mode:
            #        if tree.leg_trkPtGmt[iLegcscTrk] > bin:
            #            hrate_modes_leg[ihist].Fill(bin)
    '''        
    # ======= Rate Pt assignment Debug ========
    # when EMTF triggers SM16 but CSCTF does not

    #if tree.numTrks != 1: continue
    #if tree.numLegTrks != 1: continue

    #if tree.numGblRecoMuons != 1: continue
    '''
    if singleMu16_trigger == True and leg_singleMu16_trigger == False:
        
        print '\n======= EMTF Rate DEBUG ======='
        print 'Event: ', tree.event, ' Run: ', tree.run, '\n'
        
        for iReco in range(0, tree.numGblRecoMuons):
            if printLevel == 0: print 'Gbl Muon Reco Pt: ', tree.gmrPt[0], 'eta: ', tree.gmrEta[0], 'phi: ', tree.gmrPhi[iReco] 
            
        for iLegTrk in range(tree.numLegTrks):

            if printLevel == 0:
                print '\nCSCTF Track # ', iLegTrk, \
                    ' trkPt: ', tree.leg_trkPt[iLegTrk], \
                    ' trkEta: ', tree.leg_trkEta[iLegTrk], \
                    ' trkPhi: ', tree.leg_trkPhi[iLegTrk], \
                    ' trkMode:  ', tree.leg_trkMode[iLegTrk]

            for iLct in range(0, tree.numLegTrkLCTs[iLegTrk]):
                if printLevel == 0:
                    print 'CSCTF Lct #', iLct, \
                        ' Station:', tree.leg_trkLctStation[iLegTrk*4 + iLct], \
                        ' Endcap:', tree.leg_trkLctEndcap[iLegTrk*4 + iLct], \
                        ' Sector:', tree.leg_trkLctSector[iLegTrk*4 + iLct], \
                        ' Ring:', tree.leg_trkLctRing[iLegTrk*4 + iLct], \
                        ' Wire:', tree.leg_trkLctWire[iLegTrk*4 + iLct], \
                        ' Strip:', tree.leg_trkLctStrip[iLegTrk*4 + iLct], \
                        ' Eta:', tree.leg_trkLctGblEta[iLegTrk*4 + iLct], \
                        ' Phi:', tree.leg_trkLctGblPhi[iLegTrk*4 + iLct]

        for iTrk in range(tree.numTrks):
            
            if iTrk > 3: continue

            if printLevel == 0:
                print '\nEMTF Track # ', iTrk, \
                    ' trkPt:', tree.trkPt[iTrk], \
                    ' trkEta:', tree.trkEta[iTrk], \
                    ' trkPhi:', tree.trkPhi[iTrk], \
                    ' trkMode:', tree.trkMode[iTrk]


            ring1 = False
            for iLct in range(0, tree.numTrkLCTs[iTrk]):    
                
                if printLevel == 0:
                    print 'EMTF Lct #', iLct, \
                        ' Station:', tree.trkLctStation[iTrk*4 + iLct], \
                        ' Endcap:', tree.trkLctEndcap[iTrk*4 + iLct], \
                        ' Sector:', tree.trkLctSector[iTrk*4 + iLct], \
                        ' Ring:', tree.trkLctRing[iTrk*4 + iLct], \
                        ' Wire:', tree.trkLctWire[iTrk*4 + iLct], \
                        ' Strip:', tree.trkLctStrip[iTrk*4 + iLct], \
                        ' Eta:', tree.trkLctGblEta[iTrk*4 + iLct], \
                        ' Phi:', tree.trkLctGblPhi[iTrk*4 + iLct]
        
                if tree.trkLctRing[iTrk*4 + iLct] == 1 and not ring1: 
                    counter['num_EMTF_ring2_singleMu16'] += 1
                    ring1 = True

        if printLevel == 0: print '\nEvent LCTs'
        for iLct in range(tree.numLCTs):
            
            if printLevel == 0:
                print 'Event Lct #', iLct, \
                    ' Station:', tree.lctStation[iLct], \
                    ' Endcap:', tree.lctEndcap[iLct], \
                    ' Sector:', tree.lctSector[iLct], \
                    ' Ring:', tree.lctRing[iLct], \
                    ' Wire:', tree.lctWire[iLct], \
                    ' Strip:', tree.lctStrip[iLct], \
                    ' Eta:', tree.lctGlobalEta[iLct], \
                    ' Phi:', tree.lctGlobalPhi[iLct]
                
# end event loop 
    '''

 




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



# Calculate L1 GMT Rate
#11245.6 Hz * N_colliding_bunches * N_passing_events / N_total_zeroBias_events

print counter

n_passing_events = float(counter['L1GMT_SingleMu16_count'])

nEMTF_passing_events = float(counter['EMTF_singleMu16_count'])

n_total_zeroBias_events = float(counter['total_events'])

#l1_rate = 11245.6 * 589 * (n_passing_events/n_total_zeroBias_events)

#emtf_rate = 11245.6 * 589 * (nEMTF_passing_events/n_total_zeroBias_events)

#print '\n=========== Analaysis Results ============'

#print 'CSCTF SingleMu16 Rate: ', l1_rate
#print 'EMTF SingleMu16  Rate: ', emtf_rate
#print 'GT SingleMu Rate   : 2266 Hz'

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

# Efficiency
#filename = '/afs/cern.ch/work/a/abrinke1/public/EMTF/Emulator/trees/2016_02_28/TEST_EMTF_EFF_SingleMuon_ZMu_260627.root'
filename = 'root://eoscms//eos/cms/store/user/dcurry/EMTF/EMTF_effStudies_ZMu-PromptReco_v3.root'
file = TFile.Open(filename)

# Pt cut for plots
pt_cut = 16

# Set the branch address of TTree in Tfile
tree = file.Get("ntuple/tree")

# Output histograms
newfile = TFile("plots/eff.root","recreate")

# A more efficient way to count
muon_count  = Counter()
final_count = Counter() 
eta_count   = Counter() 
trk_count   = Counter()
gen_count   = Counter()

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
    #if iEvt > 20000: break
    
    tree.GetEntry(iEvt)
    
    if iEvt % 1000 is 0: print 'Event #', iEvt
    
    if printLevel > 1:
        print '\n============== New Event # ', tree.event, ' =================\n'\
              '\n  Run             = ', tree.run,  \
              '\n  Muons in Event  = ', tree.numGblRecoMuons,   \
              '\n  Tracks in Event = ', tree.numTrks
        

    #if tree.numTrks > 1: continue
    #if tree.numLegTrks > 1: continue
    if tree.numGblRecoMuons > 1: continue

    # Now check each muon individually and fill hists
    for iReco in range(0, tree.numGblRecoMuons):
        
        if printLevel > 1: print '\n===== Looping over Muon', iReco, '====='
        
        #if tree.gmrPt[iReco] < 3: continue
        
        if tree.gmrPt[iReco] < 3: continue

        if abs(tree.gmrEta[iReco]) > 2.4 or abs(tree.gmrEta[iReco]) < 1.24: continue
        
        # only high quality muons
        if tree.gmrValHits[iReco] < 10: continue
        if tree.gmrD0[iReco] > 0.2    : continue
        if tree.gmrChi2Norm[iReco] > 3: continue
        #if reco.gmrDXY[iReco] > 0.2 and reco.gmrDz[iReco] > 0.5: continue

        #if reco.gmrEta[iReco] >= 0: continue
        
        if printLevel > 1: print '-----> Muon is Global w/ pT > 3 and eta < 2.4 & > 1.2.  Continue on'
        
        muon_count['total_gbl_muons'] +=1
        
        # set gbl muon pt
        pt_muon  = tree.gmrPt[iReco]
        eta_muon = abs(tree.gmrEta[iReco])
        #eta_muon = tree.gmrEta[iReco]
        phi_muon = tree.gmrPhi[iReco]
        eta_muon_plot = tree.gmrEta[iReco]
        
        # =============================================================================================
        # Function that takes global and gives back is Matched to two Segs. Returns list[Bool, Lct id[] ]
        match_list = is_two_segs(iEvt, iReco, tree, printLevel) 

        if not match_list[0]: continue 
        
        id_list = match_list[1]
            
        if printLevel > 0: print '\n-----> Muon has two Segs matched.  Fill denominator'
         
        muon_count['denominator'] += 1

        # efficiencies
        hpt.Fill(pt_muon)
        heta.Fill(eta_muon)
        hphi.Fill(phi_muon)

        # =============================================================================================
        # Does a track have the same Lcts that segs matched to?  Returns list[Bool, track Id]
        track_list = is_track_match(iEvt, tree, id_list, printLevel)
        
        # Does a legacy track have the same Lcts that segs matched to?  Returns list[Bool, track Id]
        track_list_leg = is_track_match_leg(iEvt, tree, id_list, printLevel)


        # track_list[0] is True for a match
        # Look at only matched CSCTF and EMTF events
        if track_list[0]:
        
            icscTrk = track_list[1]            

            # BX has to be equal to zero to have triggered the global reco muon
            #if trkBx[icscTrk] != 0: continue

            if printLevel > 0: print '\n-----> EMTF Track #', track_list[1], ' has Lct matched to Segment.  Fill numerator'
                      
            muon_count['numerator'] += 1

            hgbl_pt.Fill(pt_muon)
            hgbl_eta.Fill(eta_muon_plot)
            hgbl_phi.Fill(phi_muon)

            trkPt = tree.trkPt[icscTrk] - 1
            
            # efficiencies
            if tree.trkPt[icscTrk] >= pt_cut: 
                hpt_trigger.Fill(pt_muon)
                heta_trigger.Fill(eta_muon)
                hphi_trigger.Fill(phi_muon)
            
            # EMTF Mode combinations
            if tree.trkMode[icscTrk] == 15 and trkPt >= pt_cut:
                 hpt_trigger_15_14_13_11.Fill(pt_muon)
                 hpt_trigger_15_14_13.Fill(pt_muon)
                 hpt_trigger_15_14.Fill(pt_muon)
                 hpt_trigger_15.Fill(pt_muon)
                 hpt_trigger_gmt.Fill(pt_muon)

                 heta_trigger_15_14_13_11.Fill(eta_muon)
                 heta_trigger_15_14_13.Fill(eta_muon)
                 heta_trigger_15_14.Fill(eta_muon)
                 heta_trigger_15.Fill(eta_muon)
                 heta_trigger_gmt.Fill(eta_muon)

                 hphi_trigger_15_14_13_11.Fill(phi_muon)
                 hphi_trigger_15_14_13.Fill(phi_muon)
                 hphi_trigger_15_14.Fill(phi_muon)
                 hphi_trigger_15.Fill(phi_muon)
                 hphi_trigger_gmt.Fill(phi_muon)
                 
            if tree.trkMode[icscTrk] == 14 and trkPt >= pt_cut:
                hpt_trigger_15_14_13_11.Fill(pt_muon)
                hpt_trigger_15_14_13.Fill(pt_muon)
                hpt_trigger_15_14.Fill(pt_muon)
                hpt_trigger_gmt.Fill(pt_muon)

                heta_trigger_15_14_13_11.Fill(eta_muon)
                heta_trigger_15_14_13.Fill(eta_muon)
                heta_trigger_15_14.Fill(eta_muon)
                heta_trigger_gmt.Fill(eta_muon)

                hphi_trigger_15_14_13_11.Fill(phi_muon)
                hphi_trigger_15_14_13.Fill(phi_muon)
                hphi_trigger_15_14.Fill(phi_muon)
                hphi_trigger_gmt.Fill(phi_muon)

            if tree.trkMode[icscTrk] == 13 and trkPt >= pt_cut:
                hpt_trigger_15_14_13_11.Fill(pt_muon)
                hpt_trigger_15_14_13.Fill(pt_muon)
                hpt_trigger_gmt.Fill(pt_muon)

                heta_trigger_15_14_13_11.Fill(eta_muon)
                heta_trigger_15_14_13.Fill(eta_muon)
                heta_trigger_gmt.Fill(eta_muon)

                hphi_trigger_15_14_13_11.Fill(phi_muon)
                hphi_trigger_15_14_13.Fill(phi_muon)
                hphi_trigger_gmt.Fill(phi_muon)

            if tree.trkMode[icscTrk] == 11 and trkPt >= pt_cut:
                hpt_trigger_15_14_13_11.Fill(pt_muon)
                heta_trigger_15_14_13_11.Fill(eta_muon)
                hphi_trigger_15_14_13_11.Fill(phi_muon)
                
                hpt_trigger_gmt.Fill(pt_muon)
                heta_trigger_gmt.Fill(eta_muon)
                hphi_trigger_gmt.Fill(phi_muon)

            # legacy GMT Q3
            if tree.trkMode[icscTrk] == 7 and trkPt >= pt_cut:
                hpt_trigger_gmt.Fill(pt_muon)
                heta_trigger_gmt.Fill(eta_muon)
                hphi_trigger_gmt.Fill(phi_muon)

            # Efficiencies for all modes
            for ihist, mode in enumerate(mode_list):
                if tree.trkMode[icscTrk] == mode:
                    hpt_trigger_modes[ihist].Fill(pt_muon)
        
        
        if track_list_leg[0]:

            iLegcscTrk = track_list_leg[1]            

            # BX has to be equal to zero to have triggered the global reco muon
            #if leg_trkBx[iLegcscTrk] != 0: continue
            
            if printLevel > 0: print '\n-----> CSCTF Track #', track_list[1], ' has Lct matched to Segment.  Fill numerator'

            # CSCTF track GMT quality
            leg_trkQ = whichQ(iLegcscTrk, tree)
            
            if tree.leg_trkPt[iLegcscTrk] >= pt_cut:
                hpt_trigger_leg.Fill(pt_muon)
                heta_trigger_leg.Fill(eta_muon)
                hphi_trigger_leg.Fill(phi_muon)


            # CSCTF Mode combinations
            if leg_trkQ == 3 and tree.leg_trkPt[iLegcscTrk] >= pt_cut:
                hpt_trigger_gmt_leg.Fill(pt_muon)
                heta_trigger_gmt_leg.Fill(eta_muon)
                hphi_trigger_gmt_leg.Fill(phi_muon)

            if tree.leg_trkMode[iLegcscTrk] == 15 and tree.leg_trkPt[iLegcscTrk] >= pt_cut:
                hpt_trigger_15_14_13_11_leg.Fill(pt_muon)
                hpt_trigger_15_14_13_leg.Fill(pt_muon)
                hpt_trigger_15_14_leg.Fill(pt_muon)
                hpt_trigger_15_leg.Fill(pt_muon)
                
                heta_trigger_15_14_13_11_leg.Fill(eta_muon)
                heta_trigger_15_14_13_leg.Fill(eta_muon)
                heta_trigger_15_14_leg.Fill(eta_muon)
                heta_trigger_15_leg.Fill(eta_muon)
                
                hphi_trigger_15_14_13_11_leg.Fill(phi_muon)
                hphi_trigger_15_14_13_leg.Fill(phi_muon)
                hphi_trigger_15_14_leg.Fill(phi_muon)
                hphi_trigger_15_leg.Fill(phi_muon)

            if tree.leg_trkMode[iLegcscTrk] == 14 and tree.leg_trkPt[iLegcscTrk] >= pt_cut:
                hpt_trigger_15_14_13_11_leg.Fill(pt_muon)
                hpt_trigger_15_14_13_leg.Fill(pt_muon)
                hpt_trigger_15_14_leg.Fill(pt_muon)
                
                heta_trigger_15_14_13_11_leg.Fill(eta_muon)
                heta_trigger_15_14_13_leg.Fill(eta_muon)
                heta_trigger_15_14_leg.Fill(eta_muon)

                hphi_trigger_15_14_13_11_leg.Fill(phi_muon)
                hphi_trigger_15_14_13_leg.Fill(phi_muon)
                hphi_trigger_15_14_leg.Fill(phi_muon)

            if tree.leg_trkMode[iLegcscTrk] == 13 and tree.leg_trkPt[iLegcscTrk] >= pt_cut:
                hpt_trigger_15_14_13_11_leg.Fill(pt_muon)
                hpt_trigger_15_14_13_leg.Fill(pt_muon)

                heta_trigger_15_14_13_11_leg.Fill(eta_muon)
                heta_trigger_15_14_13_leg.Fill(eta_muon)

                hphi_trigger_15_14_13_11_leg.Fill(phi_muon)
                hphi_trigger_15_14_13_leg.Fill(phi_muon)

            if tree.leg_trkMode[iLegcscTrk] == 11 and tree.leg_trkPt[iLegcscTrk] >= pt_cut:
                hpt_trigger_15_14_13_11_leg.Fill(pt_muon)
                heta_trigger_15_14_13_11_leg.Fill(eta_muon)
                hphi_trigger_15_14_13_11_leg.Fill(phi_muon)

            # Efficiencies for all modes
            for ihist, mode in enumerate(mode_list):
             
                if tree.leg_trkMode[iLegcscTrk] == mode:    
                    hpt_trigger_leg_modes[ihist].Fill(pt_muon)
                    




        # DEBUG Printouts
        # Muon has to have matched to both EMTF and CSCTF.
        # Muon has to have low pT while EMTF has high PT
        if track_list_leg[0] != 1 or track_list[0] != 1: continue
        if pt_muon > 15: continue
        if tree.leg_trkPt[iLegcscTrk] > 15: continue
        if tree.trkPt[icscTrk] < 20: continue

        # both are mode 15
        #if tree.trkMode[icscTrk] != 15 or tree.leg_trkMode[iLegcscTrk] != 15: continue

        if printLevel == 0:

            print '\n======= EMTF Rate DEBUG ======='
            print 'Event: ', tree.event, ' Run: ', tree.run, '\n'

            print 'Gbl Muon Reco Pt: ', pt_muon, 'eta: ', eta_muon, 'phi: ', phi_muon

            for iLegTrk in range(tree.numLegTrks):

                print '\nCSCTF Track # ', iLegTrk, \
                    ' trkPt: ', tree.leg_trkPt[iLegTrk], \
                    ' trkEta: ', tree.leg_trkEta[iLegTrk], \
                    ' trkPhi: ', tree.leg_trkPhi[iLegTrk], \
                    ' trkMode:  ', tree.leg_trkMode[iLegTrk]

                for iLct in range(0, tree.numLegTrkLCTs[iLegTrk]):
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

                print '\nEMTF Track # ', iTrk, \
                    ' trkPt:', tree.trkPt[iTrk], \
                    ' trkEta:', tree.trkEta[iTrk], \
                    ' trkPhi:', tree.trkPhi[iTrk], \
                    ' trkMode:', tree.trkMode[iTrk]

                for iLct in range(0, tree.numTrkLCTs[iTrk]):

                    print 'EMTF Lct #', iLct, \
                        ' Station:', tree.trkLctStation[iTrk*4 + iLct], \
                        ' Endcap:', tree.trkLctEndcap[iTrk*4 + iLct], \
                        ' Sector:', tree.trkLctSector[iTrk*4 + iLct], \
                        ' Ring:', tree.trkLctRing[iTrk*4 + iLct], \
                        ' Wire:', tree.trkLctWire[iTrk*4 + iLct], \
                        ' Strip:', tree.trkLctStrip[iTrk*4 + iLct], \
                        ' Eta:', tree.trkLctGblEta[iTrk*4 + iLct], \
                        ' Phi:', tree.trkLctGblPhi[iTrk*4 + iLct]

                # For Alex
                print '\nEMTF LCTs for Alex'
                for iLct in range(0, tree.numTrkLCTs[iTrk]):
                    print tree.trkLctBx[iTrk*4 + iLct], \
                        tree.trkLctEndcap[iTrk*4 + iLct], \
                        tree.trkLctSector[iTrk*4 + iLct], \
                        tree.trkLctSubSector[iTrk*4 + iLct], \
                        tree.trkLctValid[iTrk*4 + iLct], \
                        tree.trkLctQuality[iTrk*4 + iLct], \
                        tree.trkLctPattern[iTrk*4 + iLct], \
                        tree.trkLctWire[iTrk*4 + iLct], \
                        tree.trkLctCSCID[iTrk*4 + iLct], \
                        tree.trkLctBend[iTrk*4 + iLct], \
                        tree.trkLctStrip[iTrk*4 + iLct] \

                    

            print '\nEvent LCTs'
            for iLct in range(tree.numLCTs):
                print 'Event Lct #', iLct, \
                    ' Station:', tree.lctStation[iLct], \
                    ' Endcap:', tree.lctEndcap[iLct], \
                    ' Sector:', tree.lctSector[iLct], \
                    ' Ring:', tree.lctRing[iLct], \
                    ' Wire:', tree.lctWire[iLct], \
                    ' Strip:', tree.lctStrip[iLct], \
                    ' Eta:', tree.lctGlobalEta[iLct], \
                    ' Phi:', tree.lctGlobalPhi[iLct]



        # ======= Turn On Curves ========
            '''
            # get track quality
            trkQ = whichQ(icscTrk, tree)
            
            # track mode
            trkMode = track_mode(icscTrk, tree)

            htrk_mode_all.Fill(trkMode)
            htrk_Q_all.Fill(trkQ)

            # choose 2 or 3 hit tracks to plot
            #if tree.NumLCTsTrk[iTREETrk] < 3:
            if trkQ == 3:
            
                # Fill histograms for turn on curves
                treetfPt_all.Fill(pt_muon)

                # Eta regions
                if eta_muon > 0.9 and eta_muon <= 1.2: csctfPt_all_eta1.Fill(pt_muon)
                if eta_muon > 1.2 and eta_muon <= 2.1: csctfPt_all_eta2.Fill(pt_muon)
                if eta_muon > 2.1 and eta_muon < 2.4: csctfPt_all_eta3.Fill(pt_muon)
        
                for ihist, thresh in enumerate(pt_thresh):

                    if csc.PtTrk[iCSCTrk] >= thresh:
                        
                        csctfPt[ihist].Fill(pt_muon)
                        
                        # fill eta regions
                        if eta_muon > 0.9 and eta_muon <= 1.2: csctfPt_eta1[ihist].Fill(pt_muon)
                        if eta_muon > 1.2 and eta_muon <= 2.1: csctfPt_eta2[ihist].Fill(pt_muon)
                        if eta_muon > 2.1 and eta_muon < 2.4: csctfPt_eta3[ihist].Fill(pt_muon)
            '''                    
            # ===================================

        # end if track list

    # end muon loop
        
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



print '\n =========== Analysis Results ============= ' \
      '\n Denominator(Muons with 2 matched Segs)   = ', muon_count['denominator'], \
      '\n Numerator(when track has a matched Lct ) = ', muon_count['numerator'], \
      '\n Two Hit EMTF Tracks            : ', gen_count['2hit_tracks'],\
      '\n Three Hit EMTF Tracks : ', gen_count['3hit_tracks'],\
      '\n Four Hit EMTF Tracks : ', gen_count['4hit_tracks']


# ==============================================================================================
# export counter values to .csv file for latex
# The .csv is in form for latex{tabular}.  Either import the file or copy/paste contents inside tabular region

'''
# Row headers.  Change these titles as you see fit.
row = ['Denominator', 'Numerator', 'Different Sectors', 'Same Station', 'Eta/Phi Windows', 'Sector Edge', 'Unaccounted']

table = np.array([

    #first row is column headers of eta regions 
    [' ', 'All Eta', '$0.9 < \eta < 1.3$', '$1.3 < \eta < 1.7$', '$1.7 < \eta < 2.1$', '$2.1 < \eta < 2.4$'],

    [row[0], final_count['denominator'], final_count['denominator_0.9_1.3'], final_count['denominator_1.3_1.7'], final_count['denominator_1.7_2.1'], \
     final_count['denominator_2.1_2.4'] ],
    
    [row[1], final_count['numerator'], final_count['numerator_0.9_1.3'], final_count['numerator_1.3_1.7'], final_count['numerator_1.7_2.1'], \
     final_count['numerator_2.1_2.4'] ],

    [row[2], final_count['fail_diff_sector'], final_count['fail_diff_sector_0.9_1.3'], final_count['fail_diff_sector_1.3_1.7'], final_count['fail_diff_sector_1.7_2.1'], \
          final_count['fail_diff_sector_2.1_2.4'] ],

    [row[3], final_count['fail_same_station'], final_count['fail_same_station_0.9_1.3'], final_count['fail_same_station_1.3_1.7'], final_count['fail_same_station_1.7_2.1'], \
     final_count['fail_same_station_2.1_2.4'] ],

    [row[4], final_count['fail_windows'], final_count['fail_windows_0.9_1.3'], final_count['fail_windows_1.3_1.7'], final_count['fail_windows_1.7_2.1'], \
     final_count['fail_windows_2.1_2.4'] ],

    [row[5], final_count['fail_sector_edge'], final_count['fail_sector_edge_0.9_1.3'], final_count['fail_sector_edge_1.3_1.7'], final_count['fail_sector_edge_1.7_2.1'], \
          final_count['fail_sector_edge_2.1_2.4'] ],

    [row[6], final_count['fail_unaccounted'], final_count['fail_unaccounted_0.9_1.3'], final_count['fail_unaccounted_1.3_1.7'], final_count['fail_unaccounted_1.7_2.1'], \
               final_count['fail_unaccounted_2.1_2.4'] ],
        
    ])

np.savetxt("myTable.csv", table, delimiter=' & ', fmt="%s", newline=' \\\\\n')

# ==============================================================================================


# Table Debugging
# Assuming my current table is size 7 x 5 (7 rows, 5 columns).   
# Add rows and columns to make sure all final counts are conserved.
test_table = table[1:, 1:].astype(np.int)

print '\n\n Final Table:\n', test_table

for col in range(5):
    if test_table[1:, col].sum() != test_table[0,col]:  print '----> Column', col, 'has an error !!!!! '
    
for row in range(7):    
    if test_table[row, 1:].sum() != test_table[row, 0]: print '----> Row', col, 'has an error !!!!! '

'''

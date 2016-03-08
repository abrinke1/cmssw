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
from eff_EMTF_analysis import *


# Set the print level. Default = 0
if len(sys.argv) is 1: printLevel = 0
else: printLevel = sys.argv[1]

print '------> Importing Root File'

# SingleMuon
filename = 'root://eoscms//eos/cms/store/user/dcurry/EMTF/TEST_EMTF_v5.root'
#filename = '/afs/cern.ch/work/d/dcurry/private/rpc_mtf8/CMSSW_8_0_0_pre5/src/L1Trigger/L1TMuonEndCap/test/TEST_EMTF.root'

file = TFile.Open(filename)

# Histogram filename
newfile = TFile("plots/EMFT_analysis_singleMu.root","recreate")

# Set the branch address of TTree in Tfile
tree = file.Get("ntuple/tree")

# A more efficient way to count
muon_counter  = Counter()



# ================ Histograms ===================

hgbl_pt   = TH1F('hgbl_pt', '', 50 , 0, 100)
hgbl_eta  = TH1F('hgbl_eta', '', 50 , -2.5, 2.5)
hgbl_phi  = TH1F('hgbl_phi', '', 50 , -3.14, 3.14)

htrk_pt = TH1F('htrk_pt', '', 50 , 0, 100)
htrk_mode = TH1F('htrk_mode', '', 15 , 0, 15)

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


phi_max = 0.3
eta_max = 1

phi_bins = 30
eta_bins = 30

h2dphi_trk15 = TH2F('h2dphi_trk15', '', 6, 1, 7, phi_bins, 0 , phi_max)
h2deta_trk15 = TH2F('h2deta_trk15', '', 6, 1, 7, eta_bins, 0 , eta_max)

h2dphi_trk10 = TH2F('h2dphi_trk10', '', 6, 1, 7, phi_bins, 0 , phi_max)
h2deta_trk10 = TH2F('h2deta_trk10', '', 6, 1, 7, eta_bins, 0 , eta_max)

h2dphi_trk10_noEvtLCTs = TH2F('h2dphi_trk10_noEvtLCTs', '', 6, 1, 7, phi_bins, 0 , phi_max)

h2dphi_trk15_leg = TH2F('h2dphi_trk15_leg', '', 6, 1, 7, phi_bins, 0 , phi_max)
h2deta_trk15_leg = TH2F('h2deta_trk15_leg', '', 6, 1, 7, eta_bins, 0 , eta_max)

h2dphi_trk10_leg = TH2F('h2dphi_trk10_leg', '', 6, 1, 7, phi_bins, 0 , phi_max)
h2deta_trk10_leg = TH2F('h2deta_trk10_leg', '', 6, 1, 7, eta_bins, 0 , eta_max)


hist_list = [
    hdphi12, hdphi13, hdphi14, hdphi23, hdphi24, hdphi34,\
        hdphi12_trk, hdphi13_trk, hdphi14_trk, hdphi23_trk, hdphi24_trk, hdphi34_trk,\
        hdphi12_trk15, hdphi13_trk15, hdphi14_trk15, hdphi23_trk15, hdphi24_trk15, hdphi34_trk15,\
        h2dphi_trk15, h2deta_trk15, h2dphi_trk15_leg, h2deta_trk15_leg, h2dphi_trk10, h2deta_trk10, h2dphi_trk10_noEvtLCTs,\
        htrk_pt, htrk_mode
    ]



# ================================================

# Loop over over events in TFile
for iEvt in range(tree.GetEntries()):

    # for testing
    #if iEvt > 10: break
    
    tree.GetEntry(iEvt)
    
    if iEvt % 1000 is 0: print 'Event #', iEvt
    
    if printLevel > 3:
        print '\n============== New Event # ', tree.event, ' =================\n'\
              '\n  Run             = ', tree.run,  \
              '\n  Muons in Event  = ', tree.numGblRecoMuons,   \
              '\n  EMTF Tracks in Event   = ', tree.numTrks, \
              '\n  Legacy Tracks in Event = ', tree.numLegTrks

    # Loop over All LCTs
    for iLct in range(tree.numLCTs):
        if printLevel > 3:
            print '\nEvent Lct #', iLct, \
                '\n=======',\
                '\n LctEndcap  = ', tree.lctEndcap[iLct], \
                '\n LctSector  = ', tree.lctSector[iLct], \
                '\n LctRing    = ', tree.lctRing[iLct], \
                '\n LctChamber = ', tree.lctChamber[iLct], \
                '\n LctWire    = ', tree.lctWire[iLct], \
                '\n LctStrip   = ', tree.lctStrip[iLct], \
                '\n LctglobalEta  = ', tree.lctGlobalEta[iLct], \
                '\n LctglobalPhi  = ', tree.lctGlobalPhi[iLct]
            


    # Loop over EMTF tracks
    for iTrk in range(tree.numTrks):
        
        if iTrk > 3: continue
        
        if printLevel > 3:
            print '\n\nEMTF Track # ', iTrk, \
                ' trkPt: ', tree.trkPt[iTrk], \
                ' trkEta: ', tree.trkEta[iTrk], \
                ' trkPhi: ', tree.trkPhi[iTrk], \
                ' trkMode:  ', tree.trkMode[iTrk], \
                
        # dPhi Plots
        dphi_plots(tree, iTrk)

        # fill EMTF plots
        htrk_mode.Fill(tree.trkMode[iTrk])
        htrk_pt.Fill(tree.trkPt[iTrk])

        for iLct in range(tree.numTrkLCTs[iTrk]):
            
            if iLct > 3: continue

            if printLevel > 3:
                print '\nEMTF Lct #', iLct, \
                    '\n=======',\
                    '\n trLctStation = ', tree.trkLctStation[iTrk*4 + iLct], \
                    '\n trLctEndcap  = ', tree.trkLctEndcap[iTrk*4 + iLct], \
                    '\n trLctSector  = ', tree.trkLctSector[iTrk*4 + iLct], \
                    '\n trLctRing    = ', tree.trkLctRing[iTrk*4 + iLct], \
                    '\n trLctChamber = ', tree.trkLctChamber[iTrk*4 + iLct], \
                    '\n trLctWire    = ', tree.trkLctWire[iTrk*4 + iLct], \
                    '\n trLctStrip   = ', tree.trkLctStrip[iTrk*4 + iLct], \
                    '\n trLctglobalEta  = ', tree.trkLctGblEta[iTrk*4 + iLct], \
                    '\n trLctglobalPhi  = ', tree.trkLctGblPhi[iTrk*4 + iLct]


    # Loop over Legacy tracks
    for iTrk in range(tree.numLegTrks):
         
        if printLevel > 1:
            print '\n\nLegacy Track # ', iTrk, \
                ' trkPt: ', tree.leg_trkPt[iTrk], \
                ' trkEta: ', tree.leg_trkEta[iTrk], \
                ' trkPhi: ', tree.leg_trkPhi[iTrk], \
                ' trkMode:  ', tree.leg_trkMode[iTrk], \
                
        # dPhi Plots
        dphi_plots_leg(tree, iTrk)
        
        for iLct in range(tree.numLegTrkLCTs[iTrk]):
            
            if printLevel > 3:
                print '\nLegacy Lct #', iLct, \
                    '\n=======',\
                    '\n trLctStation = ', tree.leg_trkLctStation[iTrk*4 + iLct], \
                    '\n trLctEndcap  = ', tree.leg_trkLctEndcap[iTrk*4 + iLct], \
                    '\n trLctSector  = ', tree.leg_trkLctSector[iTrk*4 + iLct], \
                    '\n trLctRing    = ', tree.leg_trkLctRing[iTrk*4 + iLct], \
                    '\n trLctChamber = ', tree.leg_trkLctChamber[iTrk*4 + iLct], \
                    '\n trLctWire    = ', tree.leg_trkLctWire[iTrk*4 + iLct], \
                    '\n trLctStrip   = ', tree.leg_trkLctStrip[iTrk*4 + iLct], \
                    '\n trLctglobalEta  = ', tree.leg_trkLctGblEta[iTrk*4 + iLct], \
                    '\n trLctglobalPhi  = ', tree.leg_trkLctGblPhi[iTrk*4 + iLct]
        



        # Debug Printouts
        if tree.numTrks != 1: continue
        if tree.numLegTrks != 1: continue

        if tree.leg_trkMode[0] == 15 or tree.leg_trkMode[0] == 14 or tree.leg_trkMode[0] == 13 or tree.leg_trkMode[0] == 11:
            muon_counter['total_tracks'] +=1
        
        # mode to investigate
        debug_mode = 11

        if tree.trkMode[0] == debug_mode: continue
        
        for iLegTrk in range(tree.numLegTrks):
            if tree.leg_trkMode[iLegTrk] == debug_mode:
                
                muon_counter['numCSCTF_mode'+str(debug_mode)+'_tracks'] += 1
                
                if printLevel > 1:
                    print '\n ============================ EMTF DEBUG Mode 15 ====================================='
                    print '\nCSCTF Track # ', iLegTrk, \
                        ' trkPt: ', tree.leg_trkPt[iLegTrk], \
                        ' trkEta: ', tree.leg_trkEta[iLegTrk], \
                        ' trkPhi: ', tree.leg_trkPhi[iLegTrk], \
                        ' trkMode:  ', tree.leg_trkMode[iLegTrk]
                        
                for iLct in range(0, tree.numLegTrkLCTs[iLegTrk]):
                    if printLevel > 1:
                        print 'CSCTF  Lct #', iLct, \
                            'Station: ', tree.leg_trkLctStation[iLegTrk*4 + iLct], \
                            'Endcap: ', tree.leg_trkLctEndcap[iLegTrk*4 + iLct], \
                            'Sector: ', tree.leg_trkLctSector[iLegTrk*4 + iLct], \
                            'Ring: ', tree.leg_trkLctRing[iLegTrk*4 + iLct], \
                            'Wire: ', tree.leg_trkLctWire[iLegTrk*4 + iLct], \
                            'Strip: ', tree.leg_trkLctStrip[iLegTrk*4 + iLct], \
                            'Eta: ', tree.leg_trkLctGblEta[iLegTrk*4 + iLct], \
                            'Phi: ', tree.leg_trkLctGblPhi[iLegTrk*4 + iLct]
    
                for iTrk in range(tree.numTrks):
                    if tree.trkMode[iTrk] != debug_mode:
                        
                        for mode in range(0, 16):
                            if tree.trkMode[iTrk] == mode: muon_counter['numEMTF_mode'+str(mode)+'_tracks'] +=1
                        
                        if tree.trkMode[iTrk] == 7:
                            if printLevel > 1:
                                print '=========== EMTF MODE 7 DEBUG ========'
                                print 'Event: ', tree.event, ' Run: ', tree.run

                        if tree.trkMode[iTrk] == 12:
                            if printLevel > 1:
                                print '=========== EMTF MODE 12 DEBUG ========'
                                print 'Event: ', tree.event, ' Run: ', tree.run

                            
                        if printLevel > 1:
                            print '\nEMTF  Track # ', iTrk, \
                                ' trkPt: ', tree.trkPt[iTrk], \
                                ' trkEta: ', tree.trkEta[iTrk], \
                                ' trkPhi: ', tree.trkPhi[iTrk], \
                                ' trkMode:  ', tree.trkMode[iTrk]
                        
                        tphi1, tphi2, tphi3, tphi4 = -99, -99, -99, -99
                        teta1, teta2, teta3, teta4 = -99, -99, -99, -99
            
                        phi1, phi2, phi3, phi4 = -99, -99, -99, -99
                        eta1, eta2, eta3, eta4 = -99, -99, -99, -99
                            
                        for iLct in range(0, tree.numTrkLCTs[iTrk]):
                            
                            if tree.trkLctStation[iTrk*4 +iLct] == 1:
                                tphi1 = tree.trkLctGblPhi[iTrk*4 + iLct]
                                teta1 = tree.trkLctGblEta[iTrk*4 + iLct]

                            if tree.trkLctStation[iTrk*4 +iLct] == 2:
                                tphi2 = tree.trkLctGblPhi[iTrk*4 + iLct]
                                teta2 = tree.trkLctGblEta[iTrk*4 + iLct]

                            if tree.trkLctStation[iTrk*4 +iLct] == 3:
                                tphi3 = tree.trkLctGblPhi[iTrk*4 + iLct]
                                teta3 = tree.trkLctGblEta[iTrk*4 + iLct]

                            if tree.trkLctStation[iTrk*4 +iLct] == 4:
                                tphi4 = tree.trkLctGblPhi[iTrk*4 + iLct]
                                teta4 = tree.trkLctGblEta[iTrk*4 + iLct]
                            
                            if printLevel > 1:
                                print 'EMTF  Lct #', iLct, \
                                    'Station: ', tree.trkLctStation[iTrk*4 + iLct], \
                                    'Endcap: ', tree.trkLctEndcap[iTrk*4 + iLct], \
                                    'Sector: ', tree.trkLctSector[iTrk*4 + iLct], \
                                    'Ring: ', tree.trkLctRing[iTrk*4 + iLct], \
                                    'Wire: ', tree.trkLctWire[iTrk*4 + iLct], \
                                    'Strip: ', tree.trkLctStrip[iTrk*4 + iLct], \
                                    'Eta: ', tree.trkLctGblEta[iTrk*4 + iLct], \
                                    'Phi: ', tree.trkLctGblPhi[iTrk*4 + iLct]

                        if printLevel > 1: print '\nEvent LCTs'
                        for iLct in range(tree.numLCTs):
                            
                            if tree.lctStation[iLct] == 1:
                                phi1 = tree.lctGlobalPhi[iLct]
                                eta1 = tree.lctGlobalEta[iLct]
                                    
                            if tree.lctStation[iLct] == 2:
                                phi2 = tree.lctGlobalPhi[iLct]
                                eta2 = tree.lctGlobalEta[iLct]

                            if tree.lctStation[iLct] == 3:
                                phi3 = tree.lctGlobalPhi[iLct]
                                eta3 = tree.lctGlobalEta[iLct]

                            if tree.lctStation[iLct] == 4:
                                phi4 = tree.lctGlobalPhi[iLct]
                                eta4 = tree.lctGlobalEta[iLct]

                            if printLevel > 1:
                                print 'Event Lct #', iLct, \
                                    'Station: ', tree.lctStation[iLct], \
                                    'Endcap: ', tree.lctEndcap[iLct], \
                                    'Sector: ', tree.lctSector[iLct], \
                                    'Ring: ', tree.lctRing[iLct], \
                                    'Wire: ', tree.lctWire[iLct], \
                                    'Strip: ', tree.lctStrip[iLct], \
                                    'Eta: ', tree.lctGlobalEta[iLct], \
                                    'Phi: ', tree.lctGlobalPhi[iLct]

                        
                        # Find bending angles between EMTF track and event LCTs
                        if tphi1 != -99 and phi2 != -99:
                            dphi12 = abs(phi1-phi2)
                        if tphi1 != -99 and phi3 != -99:
                            dphi13 = abs(phi1-phi3)
                        if tphi1 != -99 and phi4 != -99:
                            dphi14 = abs(phi1-phi4)
                        if tphi2 != -99 and phi3 != -99:
                            dphi23 = abs(phi2-phi3)
                        if tphi2 != -99 and phi4 != -99:
                            dphi24 = abs(phi2-phi4)
                        if tphi3 != -99 and phi4 != -99:
                            dphi34 = abs(phi3-phi4)
        


# end event loop



# ================================

for hist in hist_list:
    if isinstance(hist, list):
        newfile.mkdir('%s' % hist[0].GetName()).cd()
        for i in hist: i.Write()
    else: hist.Write()

del newfile

# ================================


print '\n\n====== EMTF Debug Results ========'
print muon_counter

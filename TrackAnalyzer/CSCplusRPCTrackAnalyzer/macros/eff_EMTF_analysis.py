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

# SingleMuon
filename = 'root://eoscms//eos/cms/store/user/dcurry/EMTF/EMTF_MWGR_v3.root'

file = TFile.Open(filename)

# From the unpacker
filename2 = '/afs/cern.ch/work/a/abrinke1/public/EMTF/MWGR/Unpacked/2016_03_09/266423/EMTF_RawToRoot_2k.root'

file2 = TFile.Open(filename2)


# From L1TNtuples
filename3 = '/afs/cern.ch/work/d/dcurry/private/rpc_mtf8/CMSSW_8_0_0_pre6/src/L1Ntuple.root'

file3 = TFile.Open(filename3)

# Histogram filename
newfile = TFile("plots/EMFT_analysis_singleMu.root","recreate")

# Set the branch address of TTree in Tfile
tree = file.Get("ntuple/tree")

tree2 = file2.Get("Events")

tree3 = file3.Get("l1UpgradeEmuTree/L1UpgradeTree")
evtTree = file3.Get("l1EventTree/L1EventTree")

# A more efficient way to count
counter  = Counter()

# Eta Cuts
eta_min = 1.2
eta_max = 2.4

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
    #if iEvt > 100: break
    
    #if tree.numTrks < 1: continue
    
    
    tree.GetEntry(iEvt)

    tree2.GetEntry(iEvt)

    tree3.GetEntry(iEvt)
    
    if iEvt % 1000 is 0: print 'Event #', iEvt
    
    if printLevel > 1:
        print '\n============== New Event # ', tree.event, ' =================\n'\
              '\n  Run             = ', tree.run,  \
              '\n  EMTF Tracks in Event      = ', tree.numTrks, \
              '\n  Legacy Tracks in Event      = ', tree.numLegTrks, '\n'
                            #'\n  Unpacker tracks in Event  = ', len(tree2.l1tEMTFOutputs_unpack__EMTF), \

    # Loop over All LCTs
    for iLct in range(tree.numLCTs):
        if printLevel > 1:
            print 'Event Lct #', iLct,\
                'Endcap:', tree.lctEndcap[iLct],\
                'Sector:', tree.lctSector[iLct], \
                'Station:', tree.lctStation[iLct], \
                'Ring:', tree.lctRing[iLct], \
                'Chamber:', tree.lctChamber[iLct], \
                'Wire:', tree.lctWire[iLct], \
                'Strip:', tree.lctStrip[iLct], \
                'globalEta:', tree.lctGlobalEta[iLct], \
                'globalPhi:', tree.lctGlobalPhi[iLct],\
                'Bx:', tree.lctBx[iLct]
            
    
            
    # Loop over All Unpacker LCTs

    numUnpacked_tracks = 0
    
    if printLevel > 0: print '\n======== Unpacker =========\n'

    for iOut in range(tree2.l1tEMTFOutputs_unpack__EMTF.size()):
        
        EMTF_output = tree2.l1tEMTFOutputs_unpack__EMTF.at(iOut)
        
        header = EMTF_output.GetEventHeader()
        
        sector = header.Sector()
        endcap = header.Endcap()

        MeCollection = EMTF_output.GetMECollection()
        
        SpCollection = EMTF_output.GetSPCollection()
        
        for iTrk in range(SpCollection.size()):

            trk = SpCollection.at(iTrk)
            
            # Get the track mode
            #mode = trk.ME1_ID()*8 + trk.ME2_ID()*4 + trk.ME3_ID()*2 + trk.ME4_ID()*1
            

            if printLevel > 1:
                print '\nUnpacked Track #', numUnpacked_tracks,\
                    'Pt:', trk.Pt(),\
                    'Phi:', trk.Phi_global(),\
                    'Eta:', trk.Eta_GMT(),\
                    'Bx:', trk.TBIN_num()-3,\
                    'Mode', trk.Quality()

            if abs(trk.Eta_GMT()) < eta_min: continue
            if abs(trk.Eta_GMT()) > eta_max: continue
            
            if trk.Quality() != 11 and trk.Quality() != 13 and trk.Quality() != 14 and trk.Quality() != 15: continue

            if abs( (trk.TBIN_num()-3) ) != 1: continue

            numUnpacked_tracks += 1
            counter['num_unpacker_Tracks'] += 1
    

        for iLct in range(MeCollection.size()):

            lct  = MeCollection.at(iLct)

            if printLevel > 1:
                    print 'Unpacked Lct #', iLct,\
                        'Endcap:', endcap,\
                        'Sector:', sector,\
                        'Station:', lct.Station(),\
                        'Wire:', lct.Key_wire_group(),\
                        'Strip:', lct.CLCT_key_half_strip()


    if numUnpacked_tracks != tree.numTrks:
        if printLevel > 0: 
            print '\n======== ERROR!! UNPACKER DEBUG ========='
            print '# Unpacked Tracks:', numUnpacked_tracks
            
    
    # Ubnpackler Filter
    #if numUnpacked_tracks != 1: continue

    if printLevel > 0:  print '\n======== EMTF =========\n'

    numEMTF_tracks = 0
    # Loop over EMTF tracks
    for iTrk in range(tree.numTrks):
        
        if iTrk > 3: continue
        
        if printLevel > 3:
            print '\nEMTF Track # ', iTrk, \
                ' trkPt: ', tree.trkPt[iTrk], \
                ' trkEta: ', tree.trkEta[iTrk], \
                ' trkPhi: ', tree.trkPhi[iTrk], \
                ' trkMode:  ', tree.trkMode[iTrk],\
                ' trkBx:  ', tree.trkBx[iTrk]
            
        if abs(tree.trkEta[iTrk]) < eta_min: continue
        if abs(tree.trkEta[iTrk]) > eta_max: continue

        if tree.trkMode[iTrk] != 11 and tree.trkMode[iTrk] != 13 and tree.trkMode[iTrk] != 14 and tree.trkMode[iTrk] != 15: continue

        if tree.trkBx[iTrk] != 0: continue

        numEMTF_tracks += 1
        
        # dPhi Plots
        #dphi_plots(tree, iTrk)

        # fill EMTF plots
        #htrk_mode.Fill(tree.trkMode[iTrk])
        #htrk_pt.Fill(tree.trkPt[iTrk])

        for iLct in range(tree.numTrkLCTs[iTrk]):
            
            if iLct > 3: continue

            if printLevel > 1:
                print 'EMTF Lct #', iLct, \
                    'Station:', tree.trkLctStation[iTrk*4 + iLct], \
                    'Endcap:', tree.trkLctEndcap[iTrk*4 + iLct], \
                    'Sector:', tree.trkLctSector[iTrk*4 + iLct], \
                    'Ring:', tree.trkLctRing[iTrk*4 + iLct], \
                    'Chamber:', tree.trkLctChamber[iTrk*4 + iLct], \
                    'Wire:', tree.trkLctWire[iTrk*4 + iLct], \
                    'Strip:', tree.trkLctStrip[iTrk*4 + iLct], \
                    'globalEta:', tree.trkLctGblEta[iTrk*4 + iLct], \
                    'globalPhi:', tree.trkLctGblPhi[iTrk*4 + iLct]

    if printLevel > 0: print '\n======== L1TNtuple =========\n'
    
    numL1Trks = 0
    for iTrk in range(0,tree3.L1Upgrade.nMuons):
        
        trkPt = tree3.L1Upgrade.muonEt[iTrk]
        trkBx = tree3.L1Upgrade.muonBx[iTrk]

        if printLevel > 0:
            print '\nL1 Track #', iTrk,\
                'Pt:', trkPt,\
                'Eta:',  tree3.L1Upgrade.muonEta[iTrk],\
                'Phi:',  tree3.L1Upgrade.muonPhi[iTrk],\
                'Qual:',  tree3.L1Upgrade.muonQual[iTrk],\
                'Bx:',  tree3.L1Upgrade.muonBx[iTrk]
            
        if abs(tree3.L1Upgrade.muonEta[iTrk]) < eta_min: continue

        if abs(tree3.L1Upgrade.muonEta[iTrk]) > eta_max: continue

        if trkBx != 0: continue
            
        if tree3.L1Upgrade.muonQual[iTrk] < 12: continue

        numL1Trks += 1


        

    if printLevel > 0: print '\n======== CSCTF =========\n'

    # Loop over Legacy tracks
    for iTrk in range(tree.numLegTrks):
         
        if printLevel > 1:
            print '\nLegacy Track # ', iTrk, \
                ' trkPt:', tree.leg_trkPt[iTrk], \
                ' trkEta:', tree.leg_trkEta[iTrk], \
                ' trkPhi:', tree.leg_trkPhi[iTrk], \
                ' trkMode:', tree.leg_trkMode[iTrk]
                
        # dPhi Plots
        dphi_plots_leg(tree, iTrk)
        
        for iLct in range(tree.numLegTrkLCTs[iTrk]):
            
            if printLevel > 3:
                print 'Legacy Lct #', iLct, \
                    'Station:', tree.leg_trkLctStation[iTrk*4 + iLct], \
                    'Endcap:', tree.leg_trkLctEndcap[iTrk*4 + iLct], \
                    'Sector:', tree.leg_trkLctSector[iTrk*4 + iLct], \
                    'Ring:', tree.leg_trkLctRing[iTrk*4 + iLct], \
                    'Chamber:', tree.leg_trkLctChamber[iTrk*4 + iLct], \
                    'Wire:', tree.leg_trkLctWire[iTrk*4 + iLct], \
                    'Strip:', tree.leg_trkLctStrip[iTrk*4 + iLct], \
                    'globalEta:', tree.leg_trkLctGblEta[iTrk*4 + iLct], \
                    'globalPhi:', tree.leg_trkLctGblPhi[iTrk*4 + iLct]
        


    if numEMTF_tracks > numL1Trks: 
        if printLevel > 0: print '!!! L1T BUG !!!'
        counter['L1T_missing_EMTF_tracks'] += 1
            
    if numUnpacked_tracks > numL1Trks: 
        if printLevel > 0: print '!!! L1T Unpacker BUG !!!'
        counter['L1T_missing_Unpacker_tracks'] += 1

    if numUnpacked_tracks < numL1Trks:
        if printLevel > 0: print '!!! Unpacker L1T BUG !!!'
        counter['Unpacker_missing_L1T_tracks'] += 1

    if numEMTF_tracks < numL1Trks: 
        if printLevel > 0: print '!!! EMTF BUG !!!'
        counter['EMTF_missing_L1T_tracks'] += 1
             
    if numUnpacked_tracks > numEMTF_tracks:
        if printLevel > 0: print '!!! EMTF Unpacker BUG !!!'
        counter['EMTF_missing_Unpacker_tracks'] += 1

    if numUnpacked_tracks < numEMTF_tracks:
        if printLevel > 0: print '!!! Unpacker EMTF BUG !!!'
        counter['Unpacker_missing_EMTF_tracks'] += 1


        '''
        # Debug Printouts
        if tree.numTrks != 1: continue
        if tree.numLegTrks != 1: continue

        if tree.leg_trkMode[0] == 15 or tree.leg_trkMode[0] == 14 or tree.leg_trkMode[0] == 13 or tree.leg_trkMode[0] == 11:
            muon_counter['total_tracks'] +=1
        
        # mode to investigate
        debug_mode = 15

        if tree.trkMode[0] == debug_mode: continue
        
        for iLegTrk in range(tree.numLegTrks):
            if tree.leg_trkMode[iLegTrk] == debug_mode:
                
                muon_counter['numCSCTF_mode'+str(debug_mode)+'_tracks'] += 1
                
                if printLevel > 1:
                    print '\n ============================ EMTF DEBUG Mode 15 ====================================='
                    print 'Event: ', tree.event, ' Run: ', tree.run, '\n'
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
        

                            '''
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
print counter

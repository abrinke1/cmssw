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

# Input Data
#filename = 'root://eoscms.cern.ch//eos/cms/store/user/dcurry/SingleMuon/2015B_merged_test.root'
filename = 'root://eoscms//eos/cms/store/user/dcurry/trig/7_20_JSON/SingleMuon_merge.root'

#file = TFile('/afs/cern.ch/work/d/dcurry/public/trigEff/CMSSW_7_4_7/src/L1TriggerDPGUpgrade/L1TMuon/test/SingleMu_2015B_test.root')
file = TFile.Open(filename)


# Set the branch address of TTree in Tfile
csc  = file.Get("csctfTTree")
reco = file.Get("recoMuons")

# A more efficient way to count
muon_count  = Counter()
final_count = Counter() 
eta_count   = Counter() 
trk_count   = Counter()

# ================ Histograms ===================
newfile = TFile('trig_eff_plots_muonPhys_minusEta.root','recreate')

hgbl_pt = TH1F('hgbl_pt', '', 50 , 0, 200)
hcsctf_pt = TH1F('hcsctf_pt', '', 50 , 0, 200)


# efficiency(turn on)
pt_thresh = [7., 10., 12., 16.]
n_thresh = len(pt_thresh)

ptbin = [3, 4, 5, 6, 7, 8, 9, 10, 12, 16, 20, 50, 90]
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
    
hist_list = [csctfPt_all, csctfPt_all_eta1, csctfPt_all_eta2, csctfPt_all_eta3, csctfPt_all_eta4, \
                 hgbl_pt, hcsctf_pt \
             ]

# ================================================

# Loop over over events in TFile
for iEvt in range(csc.GetEntries()):
    
    # for testing
    #if iEvt > 10000: break
    
    csc.GetEntry(iEvt)
    reco.GetEntry(iEvt)
    
    if iEvt % 1000 is 0: print 'Event #', iEvt

    # Right now only works for single muon events.  Extension to multi muon events should not be too hard
    #if reco.muonSize > 1: continue

    # Test Filters
    #if reco.muonSize != 1: continue
    #if csc.SizeTrk != 1: continue
    if reco.Run == 251168: continue     

    if printLevel > 0:
        print '\n============== New Event # ', reco.Event, ' =================\n'\
              '\n  Run             = ', reco.Run,    \
              '\n  Tracks in Event = ', csc.SizeTrk, \
   
     
    # Now check each muon individually and fill hists
    for iReco in range(reco.muonSize):
        
        if printLevel > 0: print '\n===== Looping over Muon', iReco, '====='
        
        if not reco.isGlobalMuon[iReco]: continue
        
        if reco.gmrPt[iReco] < 3: continue
        
        if abs(reco.gmrEta[iReco]) > 2.4 or abs(reco.gmrEta[iReco]) < 0.9: continue
        
        #if reco.gmrEta[iReco] >= 0: continue  
        
        if printLevel > 0: print '-----> Muon is Global w/ pT > 3 and eta < 2.4 & > 0.9.  Continue on'
        
        muon_count['total_gbl_muons'] +=1
        
        # set gbl muon pt
        pt_muon  = reco.gmrPt[iReco]
        eta_muon = abs(reco.gmrEta[iReco])
        
        muon_count.clear()
        
        # =============================================================================================
        # Function that takes global and gives back is Matched to two Segs. Returns list[Bool, Lct id[] ]
        match_list = is_two_segs(iEvt, iReco, reco, csc, printLevel) 

        if not match_list[0]: continue 
        
        id_list = match_list[1]
            
        if printLevel > 0: print '\n-----> Muon has two Segs matched.  Fill denominator'
        
        muon_count['denominator'] += 1

        # fill histograms
        hgbl_pt.Fill(pt_muon)

        
        # =============================================================================================
        # Does a track have the same Lcts that segs matched to?  Returns list[Bool, track Id]
        track_list = is_track_match(iEvt, csc, id_list, printLevel)
        
        if csc.SizeTrk == 0: continue

        # track_list[0] is True for a match
        if track_list[0]: 

            if printLevel > 0: print '\n-----> Track has Lct matched to Segment.  Fill numerator'
          
            muon_count['numerator'] += 1
            
            iCSCTrk = track_list[1]

            hcsctf_pt.Fill(csc.PtTrk[iCSCTrk])
            

            # ======= Turn On Curves ========
            # choose only quality 3 tracks for turn on curves
            isQ3 = isQuality3(iCSCTrk, csc)
            #if isQ3:
            if True:

                # Fill histograms for turn on curves
                csctfPt_all.Fill(pt_muon)

                # Eta regions
                if eta_muon > 0.9 and eta_muon < 1.3: csctfPt_all_eta1.Fill(pt_muon)
                if eta_muon > 1.3 and eta_muon < 1.7: csctfPt_all_eta2.Fill(pt_muon)
                if eta_muon > 1.7 and eta_muon < 2.1: csctfPt_all_eta3.Fill(pt_muon)
                if eta_muon > 2.1 and eta_muon < 2.4: csctfPt_all_eta4.Fill(pt_muon)


                for ihist, thresh in enumerate(pt_thresh):

                    if csc.PtTrk[iCSCTrk] >= thresh:

                        csctfPt[ihist].Fill(pt_muon)
                    
                        # fill eta regions
                        if eta_muon > 0.9 and eta_muon < 1.3: csctfPt_eta1[ihist].Fill(pt_muon)
                        if eta_muon > 1.3 and eta_muon < 1.7: csctfPt_eta2[ihist].Fill(pt_muon)
                        if eta_muon > 1.7 and eta_muon < 2.1: csctfPt_eta3[ihist].Fill(pt_muon)
                        if eta_muon > 2.1 and eta_muon < 2.4: csctfPt_eta4[ihist].Fill(pt_muon)

            # ===================================

    

        # end if track is matched
                        
        # Begin failure tree for non matched tracks
        
        if not track_list[0]:
            
            if printLevel > 0: print '\n-----> Track Lcts are not matched to Segments. Find out why'
            
            muon_count['No Trigger'] += 1
            
            if printLevel > 1: print ' ======== Looping over Matched Segments ========'

            # Create local counter for segment pair failings
            local = Counter()
            
            # There is the occassional muon that has more than 2 matched segments with more than one failure reason for different seg pairs.
            # It is unclear the best way to handle this, as I'd like only one failure per muon.  For now take multiple failures in this priority:
            # Sectors, eta/phi windows, stations, edging
            # Loop over matched segments
            for iSeg in id_list:
                for jSeg in id_list:
                    if iSeg < jSeg:
                        
                        if printLevel > 1: print 'Looping over Seg', iSeg, 'and Seg', jSeg
                        
                        
                        # Exclude any seg pair from different sector, same station, different endcap
                        if csc.lctSector[iSeg] is not csc.lctSector[jSeg]:  
                            if printLevel > 1: print 'Seg', iSeg, 'and Seg', jSeg, 'are in different Sectors.  Skip further comparisons'
                            local['num_segs_diff_sectors'] += 1
                            continue
                            
                        if csc.lctStation[iSeg] is csc.lctStation[jSeg]:
                            if printLevel > 1: print 'Seg', iSeg, 'and Seg', jSeg, 'are in same Station.  Skip further comparisons.'
                            local['num_segs_same_station'] += 1
                            continue
                            
                        
                        if printLevel > 1: print 'Segments are in different stations, same sector.  Checking Dphi/eta windows.' 
                        
                        
                        in_dr_eta, in_dr_phi, in_window_too_close_edge = False, False, False
                        eta_bit = csc.lctglobalEta[jSeg] >> 1
                        
                        # First the eta windows. Different stations have different windows.
                        # Stations 1 and 2 or 1 and 3
                        if csc.lctStation[iSeg] + csc.lctStation[jSeg] is 3 or 4:
                            if abs(csc.lctglobalEta[iSeg] - csc.lctglobalEta[jSeg]) <= 4: in_dr_eta = True
                        
                        elif abs(csc.lctglobalEta[iSeg] - csc.lctglobalEta[jSeg]) <= 6: in_dr_eta = True
                        
                        # Phi windows depend on eta and station combination
                        if csc.lctStation[iSeg] + csc.lctStation[jSeg] is 3:
                            dphi_window = eta_dphi_ME1toME2[eta_bit]
                            if abs(csc.lctglobalPhi[iSeg] - csc.lctglobalPhi[jSeg]) <= dphi_window: in_dr_phi = True
                            
                        if csc.lctStation[iSeg] + csc.lctStation[jSeg] is 4:
                            dphi_window = eta_dphi_ME1toME3[eta_bit]
                            if abs(csc.lctglobalPhi[iSeg] - csc.lctglobalPhi[jSeg]) <= dphi_window: in_dr_phi = True

                        if csc.lctStation[iSeg] + csc.lctStation[jSeg] is 5:    
                            if csc.lctStation[iSeg] is 1 or csc.lctStation[iSeg] is 4:
                                dphi_window = eta_dphi_ME1toME3[eta_bit]
                                if abs(csc.lctglobalPhi[iSeg] - csc.lctglobalPhi[jSeg]) <= dphi_window: in_dr_phi = True

                        if csc.lctStation[iSeg] + csc.lctStation[jSeg] is 5:  
                            if csc.lctStation[iSeg] is 2 or csc.lctStation[iSeg] is 3:
                                if abs(csc.lctStation[iSeg]/4 - csc.lctStation[jSeg]/4) <= 127: in_dr_phi = True
                                
                        if csc.lctStation[iSeg] + csc.lctStation[jSeg] is 6 or csc.lctStation[iSeg] + csc.lctStation[jSeg] is 7:
                            if abs(csc.lctStation[iSeg]/4 - csc.lctStation[jSeg]/4) <= 127: in_dr_phi = True


                        if not in_dr_phi or not in_dr_eta:
                            if printLevel > 1: print 'Segments are not in eta/phi windows' 
                            local['num_segs_not_in_windows'] += 1

                        # if in windows we need to check of the segments would make a track to close to the sector edge.
                        # phi of potential track is taken from Lct 2,3,4, in that priority
                        # Sector edging depends on potential mode of the two segments. If mode is 5, 8, 9, 10, and too close to sector edge, cancel the track 

                        else:
                            
                            if (csc.lctStation[iSeg] is 2 or csc.lctStation[jSeg] is 2) and (csc.lctStation[iSeg] is 3 or csc.lctStation[jSeg] is 3):   pairMode = 8
                            
                            elif (csc.lctStation[iSeg] is 2 or csc.lctStation[jSeg] is 2) and (csc.lctStation[iSeg] is 4 or csc.lctStation[jSeg] is 4): pairMode = 9
                            
                            elif (csc.lctStation[iSeg] is 3 or csc.lctStation[jSeg] is 3) and (csc.lctStation[iSeg] is 4 or csc.lctStation[jSeg] is 4): pairMode = 10
                            
                            if csc.lctStation[iSeg] < csc.lctStation[jSeg] and csc.lctStation[iSeg] != 1:
                                sectorTrk_phi = csc.lctglobalPhi[iSeg]
                                
                            else: sectorTrk_phi = csc.lctglobalPhi[jSeg]
                            
                            if (sectorTrk_phi < 128 or sectorTrk_phi > (4095-128) ) and (pairMode is 10 or pairMode is 8 or pairMode is 9):
                                in_window_too_close_edge = True
                                local['num_segs_sector_edge'] += 1
                                if printLevel > 1: print 'This segment pair is in windows but track was cancelled due to track being to close to sector edge(128 phi bits)'
                                                            
                            elif printLevel > 1: print 'This segment pair was in eta/phi windows and not too close to sector edge'                            
                            

                            # If the muon made it all this way and still no reason for a failure is found, call this an unnaccounted failure.
                            if in_dr_eta and in_dr_phi and not in_window_too_close_edge:
                                if printLevel > 1: print 'This segment pair was in eta/phi windows and not too close to edge.  Should have made a track!'
                                local['num_unaccounted'] += 1
                            

            # end segment loop
            # Now find why these segments did not make a track
            if local['num_unaccounted'] > 0:
                muon_count['fail_unaccounted'] += 1
                local['num_fail'] += 1
                
            if local['num_segs_diff_sectors'] > 0 and local['num_fail'] < 1: 
                if printLevel > 1: print ' ---> Segments are in different sectors'
                muon_count['fail_diff_sector'] += 1
                local['num_fail'] += 1
       
            if local['num_segs_same_station'] > 0 and local['num_fail'] < 1:     
                if printLevel > 1: print ' ---> Segments are in same station'
                muon_count['fail_same_station'] += 1
                local['num_fail'] += 1
                                
            if local['num_segs_not_in_windows'] > 0 and local['num_fail'] < 1:
                if printLevel > 1: print ' ---> Segments are not in phi/eta windows'
                muon_count['fail_windows'] += 1
                local['num_fail'] += 1
                

            if local['num_segs_sector_edge'] > 0 and local['num_fail'] < 1:
                if printLevel > 1: print ' ---> Segments are in phi/eta windows, but too close to sector edge'
                muon_count['fail_sector_edge'] += 1
                local['num_fail'] += 1
                
                
                
            if local['num_fail'] > 1: print ' !!!!!! Overcounting Seg Failures !!!!!!'

            if local['num_fail'] < 1: print ' !!!!!! Undercounting Seg Failures !!!!!!'    


            
        # end if not track matched

        # Take all counts and split them up by eta region
        # 1 = 0.9 - 1.3
        # 2 = 1.3 - 1.7 
        # 3 = 1.7 - 2.1
        # 4 = 2.1 - 2.4
        eta = abs(reco.gmrEta[iReco])

        #print '\nBefore Count =', muon_count
        
        eta_count.clear()
        
        for name in muon_count:
            if eta >= 2.1:
                eta_count[name+'%s' % ('_2.1_2.4')] += 1
                
            if eta > 1.7 and eta < 2.1:     
                eta_count[name+'%s' % ('_1.7_2.1')] += 1

            if eta > 1.3 and eta < 1.7:
                eta_count[name+'%s' % ('_1.3_1.7')] += 1

            if eta <= 1.3:
                eta_count[name+'%s' % ('_0.9_1.3')] += 1

        # append the final count with this muons count
        for name in muon_count: final_count[name] += 1
        for name in eta_count:  final_count[name] += 1

        
    # end muon loop
        
# end event loop 

#  ======== Write Hists ==========

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
      '\n Denominator(Muons with 2 matched Segs)   = ', final_count['denominator'], \
      '\n Numerator(when track has a matched Lct ) = ', final_count['numerator'], \
      #'\n Total Global Muons                       = ', muon_count['total_gbl_muons'], \

# ==============================================================================================
# export counter values to .csv file for latex
# The .csv is in form for latex{tabular}.  Either import the file or copy/paste contents inside tabular region

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


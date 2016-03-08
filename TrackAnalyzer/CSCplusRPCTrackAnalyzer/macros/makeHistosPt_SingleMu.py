#! /usr/bin/env python                                                                                                                                                                           
from argparse import ArgumentParser
from ROOT import *
gROOT.SetBatch(False)
from array import *


## Get number of track hits matched to segment LCTs from one RECO muon
def GetNumRecoMatched( iTag, nTagLcts, tagStation, tagStrip, tagWire, nSegs, lctId, lctIsMatched, probeStation, probeStrip, probeWire ): 

    nRecoMatched = 0
    if (nSegs > 16):  ## Unphysical situation, produces errors
        return 0

    station_has_hit = {}
    for iTagHit in range(nTagLcts[iTag]):
        station_has_hit[iTagHit] = 0
        for iSeg in range(nSegs):
            if lctId[iSeg] < 0 or lctIsMatched[iSeg] != 1:
                continue
            if (tagStation[iTag*4 + iTagHit] == probeStation[lctId[iSeg]]
                and tagStrip[iTag*4 + iTagHit] == probeStrip[lctId[iSeg]] 
                and tagWire[iTag*4 + iTagHit] == probeWire[lctId[iSeg]]
                and tagStrip[iTag*4 + iTagHit] > -1 and tagWire[iTag*4 + iTagHit] > -1):
                station_has_hit[iTagHit] = 1
                continue

        nRecoMatched += station_has_hit[iTagHit]

    return nRecoMatched

## Get number of LCTs shared between two tracks, return index of track with most shared
def GetNumMatched( iTag, nTagLcts, tagStation, tagStrip, tagWire, nProbes, nProbeLcts, probeStation, probeStrip, probeWire ):

    maxMatched = 0
    iProbeOut = -99
    for iProbe in range(nProbes):
        if nProbeLcts[iProbe] < 2:
            continue
        nMatched = 0
        for iTagHit in range(nTagLcts[iTag]):
            for iProbeHit in range(nProbeLcts[iProbe]):
                if (tagStation[iTag*4 + iTagHit] == probeStation[iProbe*4 + iProbeHit]
                    and tagStrip[iTag*4 + iTagHit] == probeStrip[iProbe*4 + iProbeHit] 
                    and tagWire[iTag*4 + iTagHit] == probeWire[iProbe*4 + iProbeHit]
                    and tagStrip[iTag*4 + iTagHit] > -1 and tagWire[iTag*4 + iTagHit] > -1):
                    nMatched += 1

        if nMatched > maxMatched:
            maxMatched = nMatched
            iProbeOut = iProbe
            
    return [maxMatched, iProbeOut]

###########################################################

def main():

    print 'Inside makeHistosPt_SingleMu'
    
    parser = ArgumentParser(description='Make histograms from NTuple')
    parser.add_argument('rate_file_dir', nargs='?', default='/afs/cern.ch/work/a/abrinke1/public/EMTF/Emulator/trees/2016_02_28', 
                        help='Rate NTuple root file dir')
    parser.add_argument('rate_file_name', nargs='?', default='EMTF_RATE_ZeroBias4_259626.root', 
                        help='Rate NTuple root file name')
    parser.add_argument('eff_file_dir', nargs='?', default='/afs/cern.ch/work/a/abrinke1/public/EMTF/Emulator/trees/2016_03_07', 
                        help='Eff NTuple root file dir')
    parser.add_argument('eff_file_name', nargs='?', default='EMTF_EFF_SingleMuon_ZMu_Fills_4467_4479_4485_4569.root', 
                        help='Eff NTuple root file name')
    parser.add_argument('tree_name', nargs='?', default='ntuple/tree', help='TTree name')
    ## parser.add_argument('--cd', help='cd into a particular directory')
    args = parser.parse_args()

    # rate_file = TFile.Open(args.rate_file_dir+'/'+args.rate_file_name)
    # rate_tree = rate_file.Get(args.tree_name)
    eff_file = TFile.Open(args.eff_file_dir+'/'+args.eff_file_name)
    eff_tree = eff_file.Get(args.tree_name)
    out_file = TFile('plots/histosPt_SingleMu.root','recreate')


    ## Binnings for pT 10-12, 16-18
    pT_bins = [23, array('d', [0, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 6, 7, 8, 10, 12, 14, 16, 18, 20, 25, 30, 35, 40, 45, 50])]
    dPt_EMTF_CSCTF_bins = [30, -15, 15]
    dPt_EMTF_RECO_bins = [30, -20, 40]
    dPt_CSCTF_RECO_bins = [30, -20, 40]
    dPt_EMTF_SAM_bins = [30, -20, 40]
    dPt_CSCTF_SAM_bins = [30, -20, 40]

    # ## Binnings for pT 1-3
    # pT_bins = [17, array('d', [0, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 6, 7, 8, 10, 12, 14, 16, 18, 20])]
    # dPt_EMTF_CSCTF_bins = [30, -15, 15]
    # dPt_EMTF_RECO_bins = [40, -2, 18]
    # dPt_CSCTF_RECO_bins = [40, -2, 18]
    # dPt_EMTF_SAM_bins = [40, -2, 18]
    # dPt_CSCTF_SAM_bins = [40, -2, 18]

    ## Common binnings
    mode_bins = [16, -0.5, 15.5]
    pT_shift = 0.01  ## Apply to all CSCTF pT values to get in correct pT bin
    pT_max = pT_bins[1][pT_bins[0]] - pT_shift ## Include overflow in pT distributions

    ## Dictionaries of histograms
    h_EMTF_vs_CSCTF_mode = {'all hits shared' : 0, 
                            '1 hit not shared' : 1,
                            '>=2 hits not shared' : 2}
    h_RECO_pT = {}
    h_SAM_pT = {}
    h_EMTF_pT = {}
    h_CSCTF_pT = {}
    h_dPt_EMTF_CSCTF = {}
    h_dPt_EMTF_RECO = {}
    h_dPt_CSCTF_RECO = {}
    h_dPt_EMTF_SAM = {}
    h_dPt_CSCTF_SAM = {}
    for key in h_EMTF_vs_CSCTF_mode.keys():
        iKey = h_EMTF_vs_CSCTF_mode[key]
        print 'Key: %s gets number: %d' % (key, iKey)
        h_EMTF_vs_CSCTF_mode[key] = TH2D('h_EMTF_vs_CSCTF_mode_%d' % iKey, 'EMTF vs. CSCTF mode, %s' % key,
                                         mode_bins[0], mode_bins[1], mode_bins[2], mode_bins[0], mode_bins[1], mode_bins[2])
        h_EMTF_vs_CSCTF_mode[key].GetXaxis().SetTitle('CSCTF mode')
        h_EMTF_vs_CSCTF_mode[key].GetYaxis().SetTitle('EMTF mode')
        h_EMTF_vs_CSCTF_mode[key].GetZaxis().SetTitle('% of tracks')

        h_RECO_pT[key] = {}
        h_SAM_pT[key] = {}
        h_EMTF_pT[key] = {}
        h_CSCTF_pT[key] = {}
        h_dPt_EMTF_CSCTF[key] = {}
        h_dPt_EMTF_RECO[key] = {}
        h_dPt_CSCTF_RECO[key] = {}
        h_dPt_EMTF_SAM[key] = {}
        h_dPt_CSCTF_SAM[key] = {}
        for mode in range(16):
            h_RECO_pT[key][mode] = TH1D('h_RECO_pT_%d_%d' % (iKey, mode), '', pT_bins[0], pT_bins[1])
            h_SAM_pT[key][mode] = TH1D('h_SAM_pT_%d_%d' % (iKey, mode), '', pT_bins[0], pT_bins[1])
            h_EMTF_pT[key][mode] = TH1D('h_EMTF_pT_%d_%d' % (iKey, mode), '', pT_bins[0], pT_bins[1])
            h_CSCTF_pT[key][mode] = TH1D('h_CSCTF_pT_%d_%d' % (iKey, mode), '', pT_bins[0], pT_bins[1])
            h_dPt_EMTF_CSCTF[key][mode] = TH1D('h_dPt_EMTF_CSCTF_%d_%d' % (iKey, mode), '', 
                                               dPt_EMTF_CSCTF_bins[0], dPt_EMTF_CSCTF_bins[1], dPt_EMTF_CSCTF_bins[2])
            h_dPt_EMTF_RECO[key][mode] = TH1D('h_dPt_EMTF_RECO_%d_%d' % (iKey, mode), '', 
                                              dPt_EMTF_RECO_bins[0], dPt_EMTF_RECO_bins[1], dPt_EMTF_RECO_bins[2])
            h_dPt_CSCTF_RECO[key][mode] = TH1D('h_dPt_CSCTF_RECO_%d_%d' % (iKey, mode), '', 
                                               dPt_CSCTF_RECO_bins[0], dPt_CSCTF_RECO_bins[1], dPt_CSCTF_RECO_bins[2])
            h_dPt_EMTF_SAM[key][mode] = TH1D('h_dPt_EMTF_SAM_%d_%d' % (iKey, mode), '', 
                                             dPt_EMTF_SAM_bins[0], dPt_EMTF_SAM_bins[1], dPt_EMTF_SAM_bins[2])
            h_dPt_CSCTF_SAM[key][mode] = TH1D('h_dPt_CSCTF_SAM_%d_%d' % (iKey, mode), '', 
                                              dPt_CSCTF_SAM_bins[0], dPt_CSCTF_SAM_bins[1], dPt_CSCTF_SAM_bins[2])

            if (mode == 0):
                h_RECO_pT[key][mode].SetTitle('RECO pT, all modes, %s' % key)
                h_SAM_pT[key][mode].SetTitle('SAM pT, all modes, %s' % key)
                h_EMTF_pT[key][mode].SetTitle('EMTF pT, all modes, %s' % key)
                h_CSCTF_pT[key][mode].SetTitle('CSCTF pT, all modes, %s' % key)
                h_dPt_EMTF_CSCTF[key][mode].SetTitle('EMTF - CSCTF pT, all modes, %s' % key)
                h_dPt_EMTF_RECO[key][mode].SetTitle('EMTF - RECO pT, all modes, %s' % key)
                h_dPt_CSCTF_RECO[key][mode].SetTitle('CSCTF - RECO pT, all modes, %s' % key)
                h_dPt_EMTF_SAM[key][mode].SetTitle('EMTF - SAM pT, all modes, %s' % key)
                h_dPt_CSCTF_SAM[key][mode].SetTitle('CSCTF - SAM pT, all modes, %s' % key)
            elif (mode == 1):
                h_RECO_pT[key][mode].SetTitle('RECO pT, 3 hit tracks, %s' % key)
                h_SAM_pT[key][mode].SetTitle('SAM pT, 3 hit tracks, %s' % key)
                h_EMTF_pT[key][mode].SetTitle('EMTF pT, 3 hit tracks, %s' % key)
                h_CSCTF_pT[key][mode].SetTitle('CSCTF pT, 3 hit tracks, %s' % key)
                h_dPt_EMTF_CSCTF[key][mode].SetTitle('EMTF - CSCTF pT, 3 hit tracks, %s' % key)
                h_dPt_EMTF_RECO[key][mode].SetTitle('EMTF - RECO pT, 3 hit tracks, %s' % key)
                h_dPt_CSCTF_RECO[key][mode].SetTitle('CSCTF - RECO pT, 3 hit tracks, %s' % key)
                h_dPt_EMTF_SAM[key][mode].SetTitle('EMTF - SAM pT, 3 hit tracks, %s' % key)
                h_dPt_CSCTF_SAM[key][mode].SetTitle('CSCTF - SAM pT, 3 hit tracks, %s' % key)
            elif (mode == 2):
                h_RECO_pT[key][mode].SetTitle('RECO pT, 2 hit tracks, %s' % key)
                h_SAM_pT[key][mode].SetTitle('SAM pT, 2 hit tracks, %s' % key)
                h_EMTF_pT[key][mode].SetTitle('EMTF pT, 2 hit tracks, %s' % key)
                h_CSCTF_pT[key][mode].SetTitle('CSCTF pT, 2 hit tracks, %s' % key)
                h_dPt_EMTF_CSCTF[key][mode].SetTitle('EMTF - CSCTF pT, 2 hit tracks, %s' % key)
                h_dPt_EMTF_RECO[key][mode].SetTitle('EMTF - RECO pT, 2 hit tracks, %s' % key)
                h_dPt_CSCTF_RECO[key][mode].SetTitle('CSCTF - RECO pT, 2 hit tracks, %s' % key)
                h_dPt_EMTF_SAM[key][mode].SetTitle('EMTF - SAM pT, 2 hit tracks, %s' % key)
                h_dPt_CSCTF_SAM[key][mode].SetTitle('CSCTF - SAM pT, 2 hit tracks, %s' % key)
            else:
                h_RECO_pT[key][mode].SetTitle('RECO pT, mode %d, %s' % (mode, key))
                h_SAM_pT[key][mode].SetTitle('SAM pT, mode %d, %s' % (mode, key))
                h_EMTF_pT[key][mode].SetTitle('EMTF pT, mode %d, %s' % (mode, key))
                h_CSCTF_pT[key][mode].SetTitle('CSCTF pT, mode %d, %s' % (mode, key))
                h_dPt_EMTF_CSCTF[key][mode].SetTitle('EMTF - CSCTF pT, mode %d, %s' % (mode, key))
                h_dPt_EMTF_RECO[key][mode].SetTitle('EMTF - RECO pT, mode %d, %s' % (mode, key))
                h_dPt_CSCTF_RECO[key][mode].SetTitle('CSCTF - RECO pT, mode %d, %s' % (mode, key))
                h_dPt_EMTF_SAM[key][mode].SetTitle('EMTF - SAM pT, mode %d, %s' % (mode, key))
                h_dPt_CSCTF_SAM[key][mode].SetTitle('CSCTF - SAM pT, mode %d, %s' % (mode, key))

            h_RECO_pT[key][mode].GetXaxis().SetTitle('RECO pT')
            h_SAM_pT[key][mode].GetXaxis().SetTitle('SAM pT')
            h_EMTF_pT[key][mode].GetXaxis().SetTitle('EMTF pT')
            h_CSCTF_pT[key][mode].GetXaxis().SetTitle('CSCTF pT')
            h_dPt_EMTF_CSCTF[key][mode].GetXaxis().SetTitle('EMTF - CSCTF pT')
            h_dPt_EMTF_RECO[key][mode].GetXaxis().SetTitle('EMTF - RECO pT')
            h_dPt_CSCTF_RECO[key][mode].GetXaxis().SetTitle('CSCTF - RECO pT')
            h_dPt_EMTF_SAM[key][mode].GetXaxis().SetTitle('EMTF - SAM pT')
            h_dPt_CSCTF_SAM[key][mode].GetXaxis().SetTitle('CSCTF - SAM pT')

    nEvents = 0
    nTracks = 0

    print 'There are %d events in the tree' % eff_tree.GetEntries()

    ## Main event loop
    for iEvt in range(eff_tree.GetEntries()):

        # if iEvt > 100000: break
        eff_tree.GetEntry(iEvt)
        if iEvt % 1000 is 0: print 'Event #', iEvt
        
        nReco = eff_tree.numGblRecoMuons
        nTrks = eff_tree.numTrks
        nLegTrks = eff_tree.numLegTrks
        maxLegLcts = 0

        ## Only keep events with RECO muon in tight pT window
        if nReco != 1:
            continue
        if (eff_tree.gmrPt[0] < 10):
            continue
        # if (eff_tree.gmrPt[0] < 1 or eff_tree.gmrPt[0] > 3):
        #     continue
        recoPt = eff_tree.gmrPt[0]
        samPt = eff_tree.gmrSamPt[0]

        ## The LCT matching throws "out of range" errors for some such events, reason unknown
        if (nTrks > 3 or nLegTrks > 3):
            print 'In event %d, nTrks = %d and nLegTrks = %d' % (iEvt, nTrks, nLegTrks)
            continue

        ## Don't process events w/o valid tracks
        for iTrk in range(nLegTrks):
            if eff_tree.numLegTrkLCTs[iTrk] > maxLegLcts:
                maxLegLcts = eff_tree.numLegTrkLCTs[iTrk]
        if (nTrks == 0 and (nLegTrks == 0 or maxLegLcts < 2)):
            continue
        nEvents += 1

        ## Loop over EMTF tracks
        for iTrk in range(nTrks):

            if eff_tree.trkBx[iTrk] != 0:
                continue

            nRecoMatchedLCTs = GetNumRecoMatched(iTrk, eff_tree.numTrkLCTs, eff_tree.trkLctStation, 
                                                 eff_tree.trkLctStrip, eff_tree.trkLctWire,
                                                 eff_tree.muonNsegs[0], eff_tree.muon_cscsegs_lctId, eff_tree.muon_cscsegs_ismatched,
                                                 eff_tree.lctStation, eff_tree.lctStrip, eff_tree.lctWire)
            if nRecoMatchedLCTs < 2:
                continue

            [nMatchedLCTs, iLegTrk] = GetNumMatched(iTrk, eff_tree.numTrkLCTs, eff_tree.trkLctStation,
                                                    eff_tree.trkLctStrip, eff_tree.trkLctWire,
                                                    nLegTrks, eff_tree.numLegTrkLCTs, eff_tree.leg_trkLctStation,
                                                    eff_tree.leg_trkLctStrip, eff_tree.leg_trkLctWire)

            if (nRecoMatchedLCTs > 4 or nMatchedLCTs > 4):
                print 'Fatal error: %d and %d matched LCTs' % (nRecoMatchedLCTs, nMatchedLCTs)
                return 0

            nTrkLcts = eff_tree.numTrkLCTs[iTrk]
            trkMode = eff_tree.trkMode[iTrk]
            trkPt = eff_tree.trkPt[iTrk]

            if nMatchedLCTs > 0:
                nLegTrkLcts = eff_tree.numLegTrkLCTs[iLegTrk]
                leg_trkMode = eff_tree.leg_trkMode[iLegTrk]
                leg_trkPt = eff_tree.leg_trkPtGmt[iLegTrk] + pT_shift
            else:
                nLegTrkLcts = 0
                leg_trkMode = 0
            
            if (nTrkLcts == nLegTrkLcts and nTrkLcts == nMatchedLCTs):
                key = 'all hits shared'
            elif ( max(nTrkLcts - nMatchedLCTs, nLegTrkLcts - nMatchedLCTs) == 1 ):
                key = '1 hit not shared'
            elif ( max(nTrkLcts - nMatchedLCTs, nLegTrkLcts - nMatchedLCTs) > 1 ):
                key = '>=2 hits not shared'
            else:
                print 'Logic error! Neither 0, nor 1, nor >=2 hits not shared! Breaking ...'
                print 'nTrkLcts = %d, nLegTrkLcts = %d, nMatchedLCTs = %d' % (nTrkLcts, nLegTrkLcts, nMatchedLCTs)
                break

            if (key == 'all hits shared' and trkMode != leg_trkMode):
                print 'All hits shared but trkMode = %d and leg_trkMode = %d? Skipping.' % (trkMode, leg_trkMode)
                continue

            if ( not (nTrkLcts == 4 and (trkMode == 15)) and
                 not (nTrkLcts == 3 and (trkMode == 7 or trkMode == 11 or trkMode >= 13)) and
                 not (nTrkLcts == 2 and (trkMode == 3 or trkMode == 5 or trkMode == 6 or trkMode == 9 or trkMode == 10 or trkMode == 12)) ):
                print 'nTrkLcts = %d but trkMode = %d. Skipping.' % (nTrkLcts, trkMode)
                continue
            if ( not (nLegTrkLcts == 4 and (leg_trkMode == 15)) and
                 not (nLegTrkLcts == 3 and (leg_trkMode == 7 or leg_trkMode == 11 or leg_trkMode >= 13)) and
                 not (nLegTrkLcts == 2 and (leg_trkMode == 3 or leg_trkMode == 5 or leg_trkMode == 6 or leg_trkMode == 9 or leg_trkMode == 10 or leg_trkMode == 12)) and
                 not (nLegTrkLcts == 0 and (leg_trkMode == 0)) ):
                ## print 'nLegTrkLcts = %d but leg_trkMode = %d. Skipping.' % (nLegTrkLcts, leg_trkMode)
                continue

            nTracks += 1
            h_EMTF_vs_CSCTF_mode[key].Fill(leg_trkMode, trkMode)

            h_RECO_pT[key][trkMode].Fill(min(pT_max, recoPt))
            h_SAM_pT[key][trkMode].Fill(min(pT_max, samPt))
            h_EMTF_pT[key][trkMode].Fill(min(pT_max, trkPt))
            h_RECO_pT[key][0].Fill(min(pT_max, recoPt))
            h_SAM_pT[key][0].Fill(min(pT_max, samPt))
            h_EMTF_pT[key][0].Fill(min(pT_max, trkPt))
            if (nTrkLcts == 3):
                h_RECO_pT[key][1].Fill(min(pT_max, recoPt))
                h_SAM_pT[key][1].Fill(min(pT_max, samPt))
                h_EMTF_pT[key][1].Fill(min(pT_max, trkPt))
            if (nTrkLcts == 2):
                h_RECO_pT[key][2].Fill(min(pT_max, recoPt))
                h_SAM_pT[key][2].Fill(min(pT_max, samPt))
                h_EMTF_pT[key][2].Fill(min(pT_max, trkPt))

            if (nMatchedLCTs < 1): 
                continue

            h_CSCTF_pT[key][leg_trkMode].Fill(min(pT_max, leg_trkPt))
            h_CSCTF_pT[key][0].Fill(min(pT_max, leg_trkPt))
            if (nLegTrkLcts == 3):
                h_CSCTF_pT[key][1].Fill(min(pT_max, leg_trkPt))
            if (nLegTrkLcts == 2):
                h_CSCTF_pT[key][2].Fill(min(pT_max, leg_trkPt))

            this_dPt = max(dPt_EMTF_CSCTF_bins[1]+0.01, min(dPt_EMTF_CSCTF_bins[2]-0.01, trkPt - leg_trkPt) )
            h_dPt_EMTF_CSCTF[key][trkMode].Fill(this_dPt)
            h_dPt_EMTF_CSCTF[key][0].Fill(this_dPt)
            if (nTrkLcts == 3):
                h_dPt_EMTF_CSCTF[key][1].Fill(this_dPt)
            if (nTrkLcts == 2):
                h_dPt_EMTF_CSCTF[key][2].Fill(this_dPt)

            this_dPt = max(dPt_EMTF_RECO_bins[1]+0.01, min(dPt_EMTF_RECO_bins[2]-0.01, trkPt - recoPt) )
            h_dPt_EMTF_RECO[key][trkMode].Fill(this_dPt)
            h_dPt_EMTF_RECO[key][0].Fill(this_dPt)
            if (nTrkLcts == 3):
                h_dPt_EMTF_RECO[key][1].Fill(this_dPt)
            if (nTrkLcts == 2):
                h_dPt_EMTF_RECO[key][2].Fill(this_dPt)

            this_dPt = max(dPt_CSCTF_RECO_bins[1]+0.01, min(dPt_CSCTF_RECO_bins[2]-0.01, leg_trkPt - recoPt) )
            h_dPt_CSCTF_RECO[key][trkMode].Fill(this_dPt)
            h_dPt_CSCTF_RECO[key][0].Fill(this_dPt)
            if (nTrkLcts == 3):
                h_dPt_CSCTF_RECO[key][1].Fill(this_dPt)
            if (nTrkLcts == 2):
                h_dPt_CSCTF_RECO[key][2].Fill(this_dPt)

            this_dPt = max(dPt_EMTF_SAM_bins[1]+0.01, min(dPt_EMTF_SAM_bins[2]-0.01, trkPt - samPt) )
            h_dPt_EMTF_SAM[key][trkMode].Fill(this_dPt)
            h_dPt_EMTF_SAM[key][0].Fill(this_dPt)
            if (nTrkLcts == 3):
                h_dPt_EMTF_SAM[key][1].Fill(this_dPt)
            if (nTrkLcts == 2):
                h_dPt_EMTF_SAM[key][2].Fill(this_dPt)

            this_dPt = max(dPt_CSCTF_SAM_bins[1]+0.01, min(dPt_CSCTF_SAM_bins[2]-0.01, leg_trkPt - samPt) )
            h_dPt_CSCTF_SAM[key][trkMode].Fill(this_dPt)
            h_dPt_CSCTF_SAM[key][0].Fill(this_dPt)
            if (nTrkLcts == 3):
                h_dPt_CSCTF_SAM[key][1].Fill(this_dPt)
            if (nTrkLcts == 2):
                h_dPt_CSCTF_SAM[key][2].Fill(this_dPt)

        ## End loop: for iTrk in range(nTrks)

        ## Loop over CSCTF tracks with no matching LCTs
        for iLegTrk in range(nLegTrks):

            if eff_tree.leg_trkBx[iLegTrk] != 0:
                continue

            ## The LCT matching throws "out of range" errors for some such events, reason unknown
            if (nTrks > 3 or nLegTrks > 3):
                print 'In event %d, nTrks = %d and nLegTrks = %d' % (iEvt, nTrks, nLegTrks)
                continue 

            nRecoMatchedLCTs = GetNumRecoMatched(iLegTrk, eff_tree.numLegTrkLCTs, eff_tree.leg_trkLctStation, 
                                                 eff_tree.leg_trkLctStrip, eff_tree.leg_trkLctWire,
                                                 eff_tree.muonNsegs[0], eff_tree.muon_cscsegs_lctId, eff_tree.muon_cscsegs_ismatched,
                                                 eff_tree.lctStation, eff_tree.lctStrip, eff_tree.lctWire)
            if nRecoMatchedLCTs < 2:
                continue

            [nMatchedLCTs, iTrk] = GetNumMatched(iLegTrk, eff_tree.numLegTrkLCTs, eff_tree.leg_trkLctStation, 
                                                 eff_tree.leg_trkLctStrip, eff_tree.leg_trkLctWire,
                                                 nTrks, eff_tree.numTrkLCTs, eff_tree.trkLctStation, 
                                                 eff_tree.trkLctStrip, eff_tree.trkLctWire)

            if (nRecoMatchedLCTs > 4 or nMatchedLCTs > 4):
                print 'Fatal error: %d and %d matched LCTs' % (nRecoMatchedLCTs, nMatchedLCTs)
                return 0

            if nMatchedLCTs > 0:
                continue

            nLegTrkLcts = eff_tree.numLegTrkLCTs[iLegTrk]
            leg_trkMode = eff_tree.leg_trkMode[iLegTrk]
            leg_trkPt = eff_tree.leg_trkPtGmt[iLegTrk] + pT_shift

            if ( not (nLegTrkLcts == 4 and (leg_trkMode == 15)) and
                 not (nLegTrkLcts == 3 and (leg_trkMode == 7 or leg_trkMode == 11 or leg_trkMode >= 13)) and
                 not (nLegTrkLcts == 2 and (leg_trkMode == 3 or leg_trkMode == 5 or leg_trkMode == 6 or leg_trkMode == 9 or leg_trkMode == 10 or leg_trkMode == 12)) ):
                ## print 'nLegTrkLcts = %d but leg_trkMode = %d. Skipping.' % (nLegTrkLcts, leg_trkMode)
                continue

            nTracks += 1
            
            key = '>=2 hits not shared'
            
            h_EMTF_vs_CSCTF_mode[key].Fill(leg_trkMode, 0)

            h_RECO_pT[key][leg_trkMode].Fill(min(pT_max, recoPt))
            h_SAM_pT[key][leg_trkMode].Fill(min(pT_max, samPt))
            h_CSCTF_pT[key][leg_trkMode].Fill(min(pT_max, leg_trkPt))
            h_CSCTF_pT[key][0].Fill(min(pT_max, leg_trkPt))
            h_RECO_pT[key][0].Fill(min(pT_max, recoPt))
            h_SAM_pT[key][0].Fill(min(pT_max, samPt))
            if (nLegTrkLcts == 3):
                h_RECO_pT[key][1].Fill(min(pT_max, recoPt))
                h_SAM_pT[key][1].Fill(min(pT_max, samPt))
                h_CSCTF_pT[key][1].Fill(min(pT_max, leg_trkPt))
            if (nLegTrkLcts == 2):
                h_RECO_pT[key][2].Fill(min(pT_max, recoPt))
                h_SAM_pT[key][2].Fill(min(pT_max, samPt))
                h_CSCTF_pT[key][2].Fill(min(pT_max, leg_trkPt))

            this_dPt = max(dPt_CSCTF_RECO_bins[1]+0.01, min(dPt_CSCTF_RECO_bins[2]-0.01, leg_trkPt - recoPt) )
            h_dPt_CSCTF_RECO[key][leg_trkMode].Fill(this_dPt)
            h_dPt_CSCTF_RECO[key][0].Fill(this_dPt)
            if (nLegTrkLcts == 3):
                h_dPt_CSCTF_RECO[key][1].Fill(this_dPt)
            if (nLegTrkLcts == 2):
                h_dPt_CSCTF_RECO[key][2].Fill(this_dPt)

            this_dPt = max(dPt_CSCTF_SAM_bins[1]+0.01, min(dPt_CSCTF_SAM_bins[2]-0.01, leg_trkPt - samPt) )
            h_dPt_CSCTF_SAM[key][leg_trkMode].Fill(this_dPt)
            h_dPt_CSCTF_SAM[key][0].Fill(this_dPt)
            if (nLegTrkLcts == 3):
                h_dPt_CSCTF_SAM[key][1].Fill(this_dPt)
            if (nLegTrkLcts == 2):
                h_dPt_CSCTF_SAM[key][2].Fill(this_dPt)

        ## End loop: for iLegTrk in range(nLegTrks)
    ## End loop: for iEvt in range(eff_tree.GetEntries())
                
    for key in h_EMTF_vs_CSCTF_mode.keys():
        h_EMTF_vs_CSCTF_mode[key].Scale(100.0/nTracks)
        h_EMTF_vs_CSCTF_mode[key].SetMarkerColor(kWhite)
        h_EMTF_vs_CSCTF_mode[key].SetMarkerSize(1.8)
        h_EMTF_vs_CSCTF_mode[key].GetZaxis().SetTitleOffset(0.7)
        h_EMTF_vs_CSCTF_mode[key].Write()

        for mode in range(16):
            h_RECO_pT[key][mode].SetLineWidth(2)
            h_SAM_pT[key][mode].SetLineWidth(2)
            h_EMTF_pT[key][mode].SetLineWidth(2)
            h_CSCTF_pT[key][mode].SetLineWidth(2)
            h_dPt_EMTF_CSCTF[key][mode].SetLineWidth(2)
            h_dPt_EMTF_RECO[key][mode].SetLineWidth(2)
            h_dPt_CSCTF_RECO[key][mode].SetLineWidth(2)
            h_dPt_EMTF_SAM[key][mode].SetLineWidth(2)
            h_dPt_CSCTF_SAM[key][mode].SetLineWidth(2)

            h_RECO_pT[key][mode].SetLineColor(kBlack)
            h_SAM_pT[key][mode].SetLineColor(kViolet)
            h_EMTF_pT[key][mode].SetLineColor(kRed)
            h_CSCTF_pT[key][mode].SetLineColor(kBlue)
            h_dPt_EMTF_CSCTF[key][mode].SetLineColor(kBlack)
            h_dPt_EMTF_RECO[key][mode].SetLineColor(kRed)
            h_dPt_CSCTF_RECO[key][mode].SetLineColor(kBlue)
            h_dPt_EMTF_SAM[key][mode].SetLineColor(kRed)
            h_dPt_CSCTF_SAM[key][mode].SetLineColor(kBlue)

            h_RECO_pT[key][mode].Write()
            h_SAM_pT[key][mode].Write()
            h_EMTF_pT[key][mode].Write()
            h_CSCTF_pT[key][mode].Write()
            h_dPt_EMTF_CSCTF[key][mode].Write()
            h_dPt_EMTF_RECO[key][mode].Write()
            h_dPt_CSCTF_RECO[key][mode].Write()
            h_dPt_EMTF_SAM[key][mode].Write()
            h_dPt_CSCTF_SAM[key][mode].Write()

    # can1 = TCanvas('can1')
    # can1.cd()
    # can1.Update()
    # can1.SaveAs('plots/can1.png')
    
    print 'There are %d events and %d tracks in the tree' % (nEvents, nTracks)

    # del rate_tree
    del eff_tree
    # rate_file.Close()
    eff_file.Close()
    

if __name__ == '__main__':
    main()

    

#! /usr/bin/env python                                                                                                                                                                           
from argparse import ArgumentParser
from ROOT import *
gROOT.SetBatch(False)
from array import *

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

    print 'Inside makeHistosPt_ZeroBias'
    
    parser = ArgumentParser(description='Make histograms from NTuple')
    parser.add_argument('rate_file_dir', nargs='?', default='/afs/cern.ch/work/a/abrinke1/public/EMTF/Emulator/trees/2016_02_28', help='NTuple root file dir')
    parser.add_argument('rate_file_name', nargs='?', default='EMTF_RATE_ZeroBias4_259626.root', help='NTuple root file name')
    parser.add_argument('tree_name', nargs='?', default='ntuple/tree', help='TTree name')
    ## parser.add_argument('--cd', help='cd into a particular directory')
    args = parser.parse_args()

    rate_file = TFile.Open(args.rate_file_dir+'/'+args.rate_file_name)
    rate_tree = rate_file.Get(args.tree_name)
    # eff_file = TFile.Open(args.eff_file_dir+'/'+args.eff_file_name)
    # eff_tree = eff_file.Get(args.tree_name)
    out_file = TFile('plots/histosPt_ZeroBias.root','recreate')

    ## Common binnings
    mode_bins = [16, -0.5, 15.5]
    pT_bins = [19, array('d', [0, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 6, 7, 8, 10, 12, 14, 16, 18, 20, 25, 30])] 
    pT_shift = 0.01  ## Apply to all CSCTF pT values to get in correct pT bin 
    dPt_bins = [42, -4.2, 4.2]

    ## Dictionaries of histograms
    h_EMTF_vs_CSCTF_mode = {'all hits shared' : 0, 
                            '1 hit not shared' : 1,
                            '>=2 hits not shared' : 2}
    h_EMTF_pT = {}
    h_CSCTF_pT = {}
    h_dPt = {}
    for key in h_EMTF_vs_CSCTF_mode.keys():
        iKey = h_EMTF_vs_CSCTF_mode[key]
        print 'Key: %s gets number: %d' % (key, iKey)
        h_EMTF_vs_CSCTF_mode[key] = TH2D('h_EMTF_vs_CSCTF_mode_%d' % iKey, 'EMTF vs. CSCTF mode, %s' % key,
                                         mode_bins[0], mode_bins[1], mode_bins[2], mode_bins[0], mode_bins[1], mode_bins[2])
        h_EMTF_vs_CSCTF_mode[key].GetXaxis().SetTitle('CSCTF mode')
        h_EMTF_vs_CSCTF_mode[key].GetYaxis().SetTitle('EMTF mode')
        h_EMTF_vs_CSCTF_mode[key].GetZaxis().SetTitle('% of tracks')

        h_EMTF_pT[key] = {}
        h_CSCTF_pT[key] = {}
        h_dPt[key] = {}
        for mode in range(16):
            h_EMTF_pT[key][mode] = TH1D('h_EMTF_pT_%d_%d' % (iKey, mode), '', pT_bins[0], pT_bins[1])
            h_CSCTF_pT[key][mode] = TH1D('h_CSCTF_pT_%d_%d' % (iKey, mode), '', pT_bins[0], pT_bins[1])
            h_dPt[key][mode] = TH1D('h_dPt_%d_%d' % (iKey, mode), '', dPt_bins[0], dPt_bins[1], dPt_bins[2])

            if (mode == 0):
                h_EMTF_pT[key][mode].SetTitle('EMTF pT, all modes, %s' % key)
                h_CSCTF_pT[key][mode].SetTitle('CSCTF pT, all modes, %s' % key)
                h_dPt[key][mode].SetTitle('EMTF - CSCTF pT, all modes, %s' % key)
            elif (mode == 1):
                h_EMTF_pT[key][mode].SetTitle('EMTF pT, 3 hit tracks, %s' % key)
                h_CSCTF_pT[key][mode].SetTitle('CSCTF pT, 3 hit tracks, %s' % key)
                h_dPt[key][mode].SetTitle('EMTF - CSCTF pT, 3 hit tracks, %s' % key)
            elif (mode == 2):
                h_EMTF_pT[key][mode].SetTitle('EMTF pT, 2 hit tracks, %s' % key)
                h_CSCTF_pT[key][mode].SetTitle('CSCTF pT, 2 hit tracks, %s' % key)
                h_dPt[key][mode].SetTitle('EMTF - CSCTF pT, 2 hit tracks, %s' % key)
            else:
                h_EMTF_pT[key][mode].SetTitle('EMTF pT, mode %d, %s' % (mode, key))
                h_CSCTF_pT[key][mode].SetTitle('CSCTF pT, mode %d, %s' % (mode, key))
                h_dPt[key][mode].SetTitle('EMTF - CSCTF pT, mode %d, %s' % (mode, key))

            h_EMTF_pT[key][mode].GetXaxis().SetTitle('EMTF pT')
            h_CSCTF_pT[key][mode].GetXaxis().SetTitle('CSCTF pT')
            h_dPt[key][mode].GetXaxis().SetTitle('EMTF - CSCTF pT')

    nEvents = 0
    nTracks = 0

    print 'There are %d events in the tree' % rate_tree.GetEntries()

    ## Main event loop
    for iEvt in range(rate_tree.GetEntries()):

        ## if iEvt > 10000: break
        rate_tree.GetEntry(iEvt)
        if iEvt % 1000 is 0: print 'Event #', iEvt
        
        nTrks = rate_tree.numTrks
        nLegTrks = rate_tree.numLegTrks
        maxLegLcts = 0

        ## The LCT matching throws "out of range" errors for some such events, reason unknown
        if (nTrks > 3 or nLegTrks > 3):
            print 'In event %d, nTrks = %d and nLegTrks = %d' % (iEvt, nTrks, nLegTrks)
            continue

        ## Don't process events w/o valid tracks
        for iTrk in range(nLegTrks):
            if rate_tree.numLegTrkLCTs[iTrk] > maxLegLcts:
                maxLegLcts = rate_tree.numLegTrkLCTs[iTrk]
        if (nTrks == 0 and (nLegTrks == 0 or maxLegLcts < 2)):
            continue
        nEvents += 1

        ## Loop over EMTF tracks
        for iTrk in range(nTrks):

            if rate_tree.trkBx[iTrk] != 0:
                continue

            [nMatchedLCTs, iLegTrk] = GetNumMatched(iTrk, rate_tree.numTrkLCTs, rate_tree.trkLctStation, 
                                                    rate_tree.trkLctStrip, rate_tree.trkLctWire,
                                                    nLegTrks, rate_tree.numLegTrkLCTs, rate_tree.leg_trkLctStation, 
                                                    rate_tree.leg_trkLctStrip, rate_tree.leg_trkLctWire)

            nTrkLcts = rate_tree.numTrkLCTs[iTrk]
            trkMode = rate_tree.trkMode[iTrk]
            trkPt = rate_tree.trkPt[iTrk]

            if nMatchedLCTs > 0:
                nLegTrkLcts = rate_tree.numLegTrkLCTs[iLegTrk]
                leg_trkMode = rate_tree.leg_trkMode[iLegTrk]
                leg_trkPt = rate_tree.leg_trkPtGmt[iLegTrk] + pT_shift
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

            h_EMTF_pT[key][trkMode].Fill(trkPt)
            h_EMTF_pT[key][0].Fill(trkPt)
            if (nTrkLcts == 3):
                h_EMTF_pT[key][1].Fill(trkPt)
            if (nTrkLcts == 2):
                h_EMTF_pT[key][2].Fill(trkPt)

            if (nMatchedLCTs < 1): 
                continue

            h_CSCTF_pT[key][leg_trkMode].Fill(leg_trkPt)
            h_CSCTF_pT[key][0].Fill(leg_trkPt)
            if (nLegTrkLcts == 3):
                h_CSCTF_pT[key][1].Fill(leg_trkPt)
            if (nLegTrkLcts == 2):
                h_CSCTF_pT[key][2].Fill(leg_trkPt)

            this_dPt = max(dPt_bins[1]+0.01, min(dPt_bins[2]-0.01, trkPt - leg_trkPt) )
            h_dPt[key][trkMode].Fill(this_dPt)
            h_dPt[key][0].Fill(this_dPt)
            if (nTrkLcts == 3):
                h_dPt[key][1].Fill(this_dPt)
            if (nTrkLcts == 2):
                h_dPt[key][2].Fill(this_dPt)

        ## End loop: for iTrk in range(nTrks)

        ## Loop over CSCTF tracks with no matching LCTs
        for iLegTrk in range(nLegTrks):

            if rate_tree.leg_trkBx[iLegTrk] != 0:
                continue

            ## The LCT matching throws "out of range" errors for some such events, reason unknown
            if (nTrks > 3 or nLegTrks > 3):
                print 'In event %d, nTrks = %d and nLegTrks = %d' % (iEvt, nTrks, nLegTrks)
                continue 

            [nMatchedLCTs, iTrk] = GetNumMatched(iLegTrk, rate_tree.numLegTrkLCTs, rate_tree.leg_trkLctStation, 
                                                 rate_tree.leg_trkLctStrip, rate_tree.leg_trkLctWire,
                                                 nTrks, rate_tree.numTrkLCTs, rate_tree.trkLctStation, 
                                                 rate_tree.trkLctStrip, rate_tree.trkLctWire)

            if nMatchedLCTs > 0:
                continue

            nLegTrkLcts = rate_tree.numLegTrkLCTs[iLegTrk]
            leg_trkMode = rate_tree.leg_trkMode[iLegTrk]
            leg_trkPt = rate_tree.leg_trkPtGmt[iLegTrk] + pT_shift

            if ( not (nLegTrkLcts == 4 and (leg_trkMode == 15)) and
                 not (nLegTrkLcts == 3 and (leg_trkMode == 7 or leg_trkMode == 11 or leg_trkMode >= 13)) and
                 not (nLegTrkLcts == 2 and (leg_trkMode == 3 or leg_trkMode == 5 or leg_trkMode == 6 or leg_trkMode == 9 or leg_trkMode == 10 or leg_trkMode == 12)) ):
                ## print 'nLegTrkLcts = %d but leg_trkMode = %d. Skipping.' % (nLegTrkLcts, leg_trkMode)
                continue

            nTracks += 1
            
            key = '>=2 hits not shared'
            
            h_EMTF_vs_CSCTF_mode[key].Fill(leg_trkMode, 0)

            h_CSCTF_pT[key][leg_trkMode].Fill(leg_trkPt)
            h_CSCTF_pT[key][0].Fill(leg_trkPt)
            if (nLegTrkLcts == 3):
                h_CSCTF_pT[key][1].Fill(leg_trkPt)
            if (nLegTrkLcts == 2):
                h_CSCTF_pT[key][2].Fill(leg_trkPt)

        ## End loop: for iLegTrk in range(nLegTrks)
    ## End loop: for iEvt in range(rate_tree.GetEntries())
                
    for key in h_EMTF_vs_CSCTF_mode.keys():
        h_EMTF_vs_CSCTF_mode[key].Scale(100.0/nTracks)
        h_EMTF_vs_CSCTF_mode[key].SetMarkerColor(kWhite)
        h_EMTF_vs_CSCTF_mode[key].SetMarkerSize(1.8)
        h_EMTF_vs_CSCTF_mode[key].GetZaxis().SetTitleOffset(0.7)
        h_EMTF_vs_CSCTF_mode[key].Write()

        for mode in range(16):
            h_EMTF_pT[key][mode].SetLineWidth(2)
            h_CSCTF_pT[key][mode].SetLineWidth(2)
            h_dPt[key][mode].SetLineWidth(2)

            h_EMTF_pT[key][mode].SetLineColor(kRed)
            h_CSCTF_pT[key][mode].SetLineColor(kBlack)
            h_dPt[key][mode].SetLineColor(kBlue)

            h_EMTF_pT[key][mode].Write()
            h_CSCTF_pT[key][mode].Write()
            h_dPt[key][mode].Write()

    # can1 = TCanvas('can1')
    # can1.cd()
    # can1.Update()
    # can1.SaveAs('plots/can1.png')
    
    print 'There are %d events and %d tracks in the tree' % (nEvents, nTracks)

    del rate_tree
    # del eff_tree
    rate_file.Close()
    # eff_file.Close()
    

if __name__ == '__main__':
    main()

    

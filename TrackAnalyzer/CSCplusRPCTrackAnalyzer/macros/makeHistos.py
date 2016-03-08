#! /usr/bin/env python                                                                                                                                                                           
from argparse import ArgumentParser
from ROOT import *
gROOT.SetBatch(False)
from array import *

def main():

    print 'Inside makeHistos'
    
    parser = ArgumentParser(description='Make histograms from NTuple')
    parser.add_argument('rate_file_dir', nargs='?', default='/afs/cern.ch/work/a/abrinke1/public/EMTF/Emulator/trees/2016_02_28', help='NTuple root file dir')
    parser.add_argument('rate_file_name', nargs='?', default='TEST_EMTF_RATE_ZeroBias4_259626.root', help='NTuple root file name')
    parser.add_argument('tree_name', nargs='?', default='ntuple/tree', help='TTree name')
    ## parser.add_argument('--cd', help='cd into a particular directory')
    args = parser.parse_args()

    rate_file = TFile.Open(args.rate_file_dir+'/'+args.rate_file_name)
    rate_tree = rate_file.Get(args.tree_name)
    # eff_file = TFile.Open(args.eff_file_dir+'/'+args.eff_file_name)
    # eff_tree = eff_file.Get(args.tree_name)
    out_file = TFile('plots/histos_AWB.root','recreate')

    mode_sets = {}
    mode_sets['7_11_13_14_15'] = [7, 11, 13, 14, 15]
    mode_sets['11_13_14_15'] = [11, 13, 14, 15]
    mode_sets['13_14_15'] = [13, 14, 15]
    mode_sets['14_15'] = [14, 15]
    mode_sets['15'] = [15]

    mode_colors = {}
    mode_colors['7_11_13_14_15'] = 1 ## Black
    mode_colors['11_13_14_15'] = 4 ## Blue
    mode_colors['13_14_15'] = 3 ## Green
    mode_colors['14_15'] = 2 ## Red
    mode_colors['15'] = 6 ## Pink

    mode_bins = [16, -0.5, 15.5]
    pT_bins = [18, array('d', [0, 2, 2.5, 3, 3.5, 4, 4.5, 5, 6, 7, 8, 10, 12, 14, 16,18, 20, 25, 30])] 

    ## Mode
    h_EMTF_mode = TH1D('h_EMTF_mode', 'EMTF track mode', 
                       mode_bins[0], mode_bins[1], mode_bins[2])
    h_CSCTF_mode = TH1D('h_CSCTF_mode', 'CSCTF track mode', 
                        mode_bins[0], mode_bins[1], mode_bins[2])
    
    h_EMTF_vs_CSCTF_mode = TH2D('h_EMTF_vs_CSCTF_mode', 'EMTF vs. CSCTF track mode', 
                                mode_bins[0], mode_bins[1], mode_bins[2],
                                mode_bins[0], mode_bins[1], mode_bins[2])
    h_EMTF_vs_CSCTF_mode.GetXaxis().SetTitle('CSCTF mode')
    h_EMTF_vs_CSCTF_mode.GetYaxis().SetTitle('EMTF mode')

    ## pT
    EMTF_rate_vs_pT_hists = {}
    CSCTF_rate_vs_pT_hists = {}
    for mode_key in mode_sets.keys():
        EMTF_rate_vs_pT_hists[mode_key] =  TH1D('h_EMTF_rate_vs_pT_modes_%s' % mode_key,
                                                'EMTF rate vs. pT for modes %s' % mode_key,
                                                pT_bins[0], pT_bins[1])
    for mode_key in mode_sets.keys():
        CSCTF_rate_vs_pT_hists[mode_key] =  TH1D('h_CSCTF_rate_vs_pT_modes_%s' % mode_key,
                                                'CSCTF rate vs. pT for modes %s' % mode_key,
                                                pT_bins[0], pT_bins[1])

    nEvents = 0

    nCSC = 0
    nEMT = 0
    nCSCOnly = 0
    nEMTOnly = 0
    nCSCAndEMT = 0

    nCSCA = 0
    nEMTA = 0
    nCSCAOnly = 0
    nEMTAOnly = 0
    nCSCAAndEMTA = 0

    nCSCB = 0
    nEMTB = 0
    nCSCBOnly = 0
    nEMTBOnly = 0
    nCSCBAndEMTB = 0

    nCSCC = 0
    nEMTC = 0
    nCSCCOnly = 0
    nEMTCOnly = 0
    nCSCCAndEMTC = 0

    print 'There are %d events in the tree' % rate_tree.GetEntries()

    ## Main event loop
    for iEvt in range(rate_tree.GetEntries()):

        # if iEvt > 100000: break
        rate_tree.GetEntry(iEvt)
        if iEvt % 1000 is 0: print 'Event #', iEvt
        
        nTrks = rate_tree.numTrks
        nLegTrks = rate_tree.numLegTrks

        if nTrks == 0 and nLegTrks == 0: continue

    #     trkModes = rate_tree.trkMode
    #     leg_trkModes = rate_tree.leg_trkMode
        
    #     trkPts = rate_tree.trkPt
    #     leg_trkPts = rate_tree.leg_trkPtGmt

        ## EMTF tracks
        nEvents += 1

        isEMT = 0
        isEMTA = 0
        isEMTB = 0
        isEMTC = 0
        for iTrk in range(nTrks):
            if (rate_tree.trkBx[iTrk] == 0 and (rate_tree.trkMode[iTrk] == 7 or rate_tree.trkMode[iTrk] == 11 or rate_tree.trkMode[iTrk] >= 13) ): 
                isEMT = 1
                if (rate_tree.trkPt[iTrk] >= 16):
                    isEMTA = 1
            if (rate_tree.trkBx[iTrk] == 0 and rate_tree.trkMode[iTrk] == 15):
                isEMTB = 1
                if (rate_tree.trkPt[iTrk] >= 16):
                    isEMTC = 1

        isCSC = 0
        isCSCA = 0
        isCSCB = 0
        isCSCC = 0
        for iTrk in range(nLegTrks):
            if (rate_tree.leg_trkBx[iTrk] == 0 and (rate_tree.leg_trkMode[iTrk] == 7 or rate_tree.leg_trkMode[iTrk] == 11 or rate_tree.leg_trkMode[iTrk] >= 13) ): 
                isCSC = 1
                if (rate_tree.leg_trkPtGmt[iTrk] >= 16):
                    isCSCA = 1
            if (rate_tree.leg_trkBx[iTrk] == 0 and rate_tree.leg_trkMode[iTrk] == 15):
                isCSCB = 1
                if (rate_tree.leg_trkPtGmt[iTrk] >= 16):
                    isCSCC = 1

        if (isEMT): nEMT += 1
        if (isCSC): nCSC += 1
        if (isCSC and not isEMT): nCSCOnly += 1
        if (isEMT and not isCSC): nEMTOnly += 1
        if (isEMT and isCSC): nCSCAndEMT += 1

        if (isEMTA): nEMTA += 1
        if (isCSCA): nCSCA += 1
        if (isCSCA and not isEMTA): nCSCAOnly += 1
        if (isEMTA and not isCSCA): nEMTAOnly += 1
        if (isEMTA and isCSCA): nCSCAAndEMTA += 1

        if (isEMTB): nEMTB += 1
        if (isCSCB): nCSCB += 1
        if (isCSCB and not isEMTB): nCSCBOnly += 1
        if (isEMTB and not isCSCB): nEMTBOnly += 1
        if (isEMTB and isCSCB): nCSCBAndEMTB += 1

        if (isEMTC): nEMTC += 1
        if (isCSCC): nCSCC += 1
        if (isCSCC and not isEMTC): nCSCCOnly += 1
        if (isEMTC and not isCSCC): nEMTCOnly += 1
        if (isEMTC and isCSCC): nCSCCAndEMTC += 1

    #         h_EMTF_mode.Fill(trkModes[iTrk])

    #         for mode_key in EMTF_rate_vs_pT_hists.keys():
    #             for mode in mode_sets[mode_key]:
    #                 if (trkModes[iTrk] == mode):
    #                     for iBin in range(pT_bins[0]+1):
    #                         if trkPts[iTrk] + 0.01 > EMTF_rate_vs_pT_hists[mode_key].GetXaxis().GetBinLowEdge(iBin):
    #                             EMTF_rate_vs_pT_hists[mode_key].Fill(EMTF_rate_vs_pT_hists[mode_key].GetXaxis().GetBinLowEdge(iBin) + 0.01)
                                
    #     ## CSCTF tracks
    #     for iTrk in range(nLegTrks):
    #         h_CSCTF_mode.Fill(leg_trkModes[iTrk])

    #         for mode_key in CSCTF_rate_vs_pT_hists.keys():
    #             for mode in mode_sets[mode_key]:
    #                 if (leg_trkModes[iTrk] == mode):
    #                     for iBin in range(pT_bins[0]+1):
    #                         if leg_trkPts[iTrk] + 0.01 > CSCTF_rate_vs_pT_hists[mode_key].GetXaxis().GetBinLowEdge(iBin):
    #                             CSCTF_rate_vs_pT_hists[mode_key].Fill(CSCTF_rate_vs_pT_hists[mode_key].GetXaxis().GetBinLowEdge(iBin) + 0.01)
                                
    #     if (nTrks >= 1 and nLegTrks >= 1):
    #         h_EMTF_vs_CSCTF_mode.Fill(leg_trkModes[0], trkModes[0])
    #     if (nTrks == 0 and nLegTrks >= 1):
    #         h_EMTF_vs_CSCTF_mode.Fill(leg_trkModes[0], 0)
    #     if (nTrks >= 1 and nLegTrks == 0):
    #         h_EMTF_vs_CSCTF_mode.Fill(0, trkModes[0])
    #     if (nTrks >= 2 and nLegTrks >= 2):
    #         h_EMTF_vs_CSCTF_mode.Fill(leg_trkModes[1], trkModes[1])
    #     if (nTrks <= 1 and nLegTrks >= 2):
    #         h_EMTF_vs_CSCTF_mode.Fill(leg_trkModes[1], 0)
    #     if (nTrks >= 2 and nLegTrks <= 1):
    #         h_EMTF_vs_CSCTF_mode.Fill(0, trkModes[1])


    # # can1 = TCanvas('can1')
    # # can1.cd()

    # h_EMTF_mode.Write()
    # h_CSCTF_mode.Write()
    # h_EMTF_vs_CSCTF_mode.Write()
    # for mode_key in EMTF_rate_vs_pT_hists.keys():
    #     EMTF_rate_vs_pT_hists[mode_key].SetLineColor(mode_colors[mode_key])
    #     # if (i == 0):
    #     #     EMTF_rate_vs_pT_hists[mode_key].Draw('same')
    #     # else:
    #     #     EMTF_rate_vs_pT_hists[mode_key].Draw('same')
    #     EMTF_rate_vs_pT_hists[mode_key].Write()
    # for mode_key in CSCTF_rate_vs_pT_hists.keys():
    #     CSCTF_rate_vs_pT_hists[mode_key].SetLineColor(mode_colors[mode_key])
    #     # if (i == 0):
    #     #     CSCTF_rate_vs_pT_hists[mode_key].Draw('same')
    #     # else:
    #     #     CSCTF_rate_vs_pT_hists[mode_key].Draw('same')
    #     CSCTF_rate_vs_pT_hists[mode_key].Write()

    # # can1.Update()
    # # can1.SaveAs('plots/can1.png')
    
    print 'There are %d nEvents in the tree' % nEvents

    print 'There are %d nCSC in the tree' % nCSC
    print 'There are %d nEMT in the tree' % nEMT
    print 'There are %d nCSCOnly in the tree' % nCSCOnly
    print 'There are %d nEMTOnly in the tree' % nEMTOnly
    print 'There are %d nCSCAndEMT in the tree' % nCSCAndEMT

    print 'There are %d nCSCA in the tree' % nCSCA
    print 'There are %d nEMTA in the tree' % nEMTA
    print 'There are %d nCSCAOnly in the tree' % nCSCAOnly
    print 'There are %d nEMTAOnly in the tree' % nEMTAOnly
    print 'There are %d nCSCAAndEMTA in the tree' % nCSCAAndEMTA

    print 'There are %d nCSCB in the tree' % nCSCB
    print 'There are %d nEMTB in the tree' % nEMTB
    print 'There are %d nCSCBOnly in the tree' % nCSCBOnly
    print 'There are %d nEMTBOnly in the tree' % nEMTBOnly
    print 'There are %d nCSCBAndEMTB in the tree' % nCSCBAndEMTB

    print 'There are %d nCSCC in the tree' % nCSCC
    print 'There are %d nEMTC in the tree' % nEMTC
    print 'There are %d nCSCCOnly in the tree' % nCSCCOnly
    print 'There are %d nEMTCOnly in the tree' % nEMTCOnly
    print 'There are %d nCSCCAndEMTC in the tree' % nCSCCAndEMTC

    del rate_tree
    # del eff_tree
    rate_file.Close()
    # eff_file.Close()
    

if __name__ == '__main__':
    main()
    

#! /usr/bin/env python                                                                                                                                                                           
from argparse import ArgumentParser
from ROOT import *
gROOT.SetBatch(False)
from array import *
import math

def main():

    print 'Inside computeRate'
    
    parser = ArgumentParser(description='Compute rate from NTuple')
    parser.add_argument('rate_file_dir', nargs='?', default='/afs/cern.ch/work/a/abrinke1/public/EMTF/Emulator/trees/2016_02_28', help='NTuple root file dir')
    parser.add_argument('rate_file_name', nargs='?', default='EMTF_RATE_ZeroBias4_259626.root', help='NTuple root file name')
    parser.add_argument('tree_name', nargs='?', default='ntuple/tree', help='TTree name')
    ## parser.add_argument('--cd', help='cd into a particular directory')
    args = parser.parse_args()

    rate_file = TFile.Open(args.rate_file_dir+'/'+args.rate_file_name)
    rate_tree = rate_file.Get(args.tree_name)
    # eff_file = TFile.Open(args.eff_file_dir+'/'+args.eff_file_name)
    # eff_tree = eff_file.Get(args.tree_name)

    base_rate = 11245.6  ## Fundamental ZeroBias rate
    run = 259626
    nBunches = 589

    pT_shift = 0.01  ## Apply to pT_threshold to get proper counts for GT/GMT/CSCTF 
    pT_threshold = 16.0 - pT_shift
    eta_threshold = 1.24
    qual_cuts = {}
    qual_cuts['GT'] = [5, 6, 7]
    qual_cuts['GMT'] = [5, 6, 7]
    qual_cuts['CSCTF'] = [7, 11, 13, 14, 15]
    qual_cuts['EMTF'] = [11, 13, 14, 15]

    rate = {}
    rate['GT'] = {}
    rate['GMT'] = {}
    rate['CSCTF'] = {}
    rate['EMTF'] = {}

    rate['GT']['GT'] = {}
    rate['GMT']['GMT'] = {}
    rate['CSCTF']['CSCTF'] = {}
    rate['CSCTF']['EMTF'] = {}
    rate['EMTF']['CSCTF'] = {}
    rate['EMTF']['EMTF'] = {}

    rate['GT']['GT']['filled'] = False
    rate['GMT']['GMT']['filled'] = False
    rate['CSCTF']['CSCTF']['filled'] = False
    rate['CSCTF']['EMTF']['filled'] = False
    rate['EMTF']['CSCTF']['filled'] = False
    rate['EMTF']['EMTF']['filled'] = False

    rate['GT']['GT']['counts'] = 0
    rate['GMT']['GMT']['counts'] = 0
    rate['CSCTF']['CSCTF']['counts'] = 0
    rate['CSCTF']['EMTF']['counts'] = 0
    rate['EMTF']['CSCTF']['counts'] = 0
    rate['EMTF']['EMTF']['counts'] = 0

    nEvents = 0

    print 'There are %d events in the tree' % rate_tree.GetEntries()

    ## Main event loop
    for iEvt in range(rate_tree.GetEntries()):

        ## if iEvt > 100000: break
        rate_tree.GetEntry(iEvt)
        if iEvt % 1000 is 0: print 'Event #', iEvt
        nEvents += 1
        
        nGtTrks = rate_tree.numGtTrks
        nGmtTrks = rate_tree.numGmtTrks
        nLegTrks = rate_tree.numLegTrks
        nTrks = rate_tree.numTrks

        ## Begin loop over GT tracks
        for iTrk in range(nGtTrks):

            if rate_tree.gt_trkPt[iTrk] < pT_threshold:
                continue
            if rate_tree.gt_trkBx[iTrk] != 0:
                continue

            if (rate_tree.gt_trkQual[iTrk] in qual_cuts['GT']) and not rate['GT']['GT']['filled']:
                rate['GT']['GT']['counts'] += 1
                rate['GT']['GT']['filled'] = True
        ## End loop over GT tracks

        ## Begin loop over GMT tracks
        for iTrk in range(nGmtTrks):

            if rate_tree.gmt_trkPt[iTrk] < pT_threshold:
                continue
            if abs(rate_tree.gmt_trkEta[iTrk]) < eta_threshold:
                continue
            if rate_tree.gmt_trkBx[iTrk] != 0:
                continue

            if (rate_tree.gmt_trkQual[iTrk] in qual_cuts['GMT']) and not rate['GMT']['GMT']['filled']:
                rate['GMT']['GMT']['counts'] += 1
                rate['GMT']['GMT']['filled'] = True
        ## End loop over GMT tracks

        ## Begin loop over CSCTF tracks
        for iTrk in range(nLegTrks):

            if rate_tree.leg_trkPtGmt[iTrk] < pT_threshold:
                continue
            if abs(rate_tree.leg_trkEta[iTrk]) < eta_threshold:
                continue
            if rate_tree.leg_trkBx[iTrk] != 0:
                continue

            if (rate_tree.leg_trkMode[iTrk] in qual_cuts['CSCTF']) and not rate['CSCTF']['CSCTF']['filled']:
                rate['CSCTF']['CSCTF']['counts'] += 1
                rate['CSCTF']['CSCTF']['filled'] = True
            if (rate_tree.leg_trkMode[iTrk] in qual_cuts['EMTF']) and not rate['CSCTF']['EMTF']['filled']:
                rate['CSCTF']['EMTF']['counts'] += 1
                rate['CSCTF']['EMTF']['filled'] = True
        ## End loop over CSCTF tracks

        ## Begin loop over EMTF tracks
        for iTrk in range(nTrks):

            if rate_tree.trkPt[iTrk] < pT_threshold:
                continue
            if abs(rate_tree.trkEta[iTrk]) < eta_threshold:
                continue
            if rate_tree.trkBx[iTrk] != 0:
                continue

            if (rate_tree.trkMode[iTrk] in qual_cuts['CSCTF']) and not rate['EMTF']['CSCTF']['filled']:
                rate['EMTF']['CSCTF']['counts'] += 1
                rate['EMTF']['CSCTF']['filled'] = True
            if (rate_tree.trkMode[iTrk] in qual_cuts['EMTF']) and not rate['EMTF']['EMTF']['filled']:
                rate['EMTF']['EMTF']['counts'] += 1
                rate['EMTF']['EMTF']['filled'] = True
        ## End loop over EMTF tracks

        ## Reset "filled" bit for next event
        for trigger in rate.keys():
            for quality in rate[trigger].keys():
                rate[trigger][quality]['filled'] = False

    ## End loop: for iEvt in range(rate_tree.GetEntries())
                
    print 'There are %d events in the tree' % nEvents

    print 'Listing rates for run %d, with %d bunches' % (run, nBunches)
    for trigger in rate.keys():
        for quality in rate[trigger].keys():
            this_rate = base_rate * nBunches * rate[trigger][quality]['counts'] / nEvents
            rel_err = math.sqrt(rate[trigger][quality]['counts']) / rate[trigger][quality]['counts']
            print '%6s rate with %6s quality cuts is %6d +/- %4d Hz' % (trigger, quality, this_rate, this_rate * rel_err)
    

    del rate_tree
    # del eff_tree
    rate_file.Close()
    # eff_file.Close()
    

if __name__ == '__main__':
    main()

    

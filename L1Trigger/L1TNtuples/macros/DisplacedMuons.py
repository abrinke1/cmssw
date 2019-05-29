#! /usr/bin/env python

## **************************************************************** ##
##  Look at properties of displaced muons from Kalman algo in BMTF  ##
## **************************************************************** ##

import os

import ROOT as R
R.gROOT.SetBatch(False)  ## Don't print histograms to screen while processing

PRT_EVT  =   1  ## Print every Nth event
MAX_EVT  = 100  ## Number of events to process
VERBOSE  = True  ## Verbose print-out


def main():

    print '\nInside DisplacedMuons\n'

    in_file_names = ['L1Ntuple.root']

    if not os.path.exists('plots'): os.makedirs('plots')

    out_file_str = 'DisplacedMuons'
    out_file_str += ('_%dk' % (MAX_EVT / 1000))
    out_file = R.TFile('plots/'+out_file_str+'.root','recreate')

    chains = {}
    chains['Evt'] = []  ## Event info
    chains['Unp'] = []  ## Unpacked legacy BMTF
    chains['Emu'] = []  ## Emulated Kalman BMTF
    for i in range(len(in_file_names)):
        print 'Adding file %s' % in_file_names[i]
        chains['Evt'].append( R.TChain('l1EventTree/L1EventTree') )
        chains['Unp'].append( R.TChain('l1UpgradeTfMuonTree/L1UpgradeTfMuonTree') )
        chains['Emu'].append( R.TChain('l1UpgradeTfMuonEmuTree/L1UpgradeTfMuonTree') )
        chains['Evt'][i].Add( in_file_names[i] )
        chains['Unp'][i].Add( in_file_names[i] )
        chains['Emu'][i].Add( in_file_names[i] )


    ###################
    ### Book histograms
    ###################

    pt_bins  = [150, 0, 150]
    chi_bins = [100, 0, 100]

    h_pt_vtx_unp   = R.TH1F('h_pt_vtx_unp',   'Legacy BMTF vertex-constrained pT spectrum',         pt_bins[0], pt_bins[1], pt_bins[2])
    h_pt_vtx_emu   = R.TH1F('h_pt_vtx_emu',   'Kalman BMTF vertex-constrained pT spectrum',         pt_bins[0], pt_bins[1], pt_bins[2])
    h_pt_displ_emu = R.TH1F('h_pt_displ_emu', 'Kalman BMTF non-vertex-constrained pT spectrum',     pt_bins[0], pt_bins[1], pt_bins[2])
    h_pt_displ_kmt = R.TH1F('h_pt_displ_kmt', 'Internal Kalman non-vertex-constrained pT spectrum', pt_bins[0], pt_bins[1], pt_bins[2])

    h_chi2_kmt = R.TH1F('h_chi2_kmt', 'Kalman BMTF track #chi^{2} distribution', chi_bins[0], chi_bins[1], chi_bins[2])

    iEvt = -1
    print '\nEntering loop over chains'
    for iCh in range(len(chains['Unp'])):

        if iEvt > MAX_EVT: break

        ## Faster tecnhique, inspired by https://github.com/thomreis/l1tMuonTools/blob/master/L1Analysis.py
        Evt_br = R.L1Analysis.L1AnalysisEventDataFormat()
        Unp_br = R.L1Analysis.L1AnalysisL1UpgradeTfMuonDataFormat()
        Emu_br = R.L1Analysis.L1AnalysisL1UpgradeTfMuonDataFormat()
        Kmt_br = R.L1Analysis.L1AnalysisBMTFOutputDataFormat()

        chains['Evt'][iCh].SetBranchAddress('Event',               R.AddressOf(Evt_br))
        chains['Unp'][iCh].SetBranchAddress('L1UpgradeBmtfMuon',   R.AddressOf(Unp_br))
        chains['Emu'][iCh].SetBranchAddress('L1UpgradeBmtfMuon',   R.AddressOf(Emu_br))
        chains['Emu'][iCh].SetBranchAddress('L1UpgradeBmtfOutput', R.AddressOf(Kmt_br))


        print '\nEntering loop over events for chain %d' % iCh
        for jEvt in range(chains['Unp'][iCh].GetEntries()):

            if iEvt > MAX_EVT: break
            iEvt += 1
            if iEvt % PRT_EVT is 0: print '\nEvent # %d (%dth in chain)' % (iEvt, jEvt)

            chains['Evt'][iCh].GetEntry(jEvt)
            chains['Unp'][iCh].GetEntry(jEvt)
            chains['Emu'][iCh].GetEntry(jEvt)

            # ## Use these lines if you don't explicitly define the DataFormat and then do SetBranchAddress above
            # Evt_br = chains['Evt'][iCh].Event
            # Unp_br = chains['Unp'][iCh].L1UpgradeBmtfMuon
            # Emu_br = chains['Emu'][iCh].L1UpgradeBmtfMuon

            if iEvt % PRT_EVT is 0: print '  * Run %d, LS %d, event %d' % (int(Evt_br.run), int(Evt_br.lumi), int(Evt_br.event))

            nUnpMu = int(Unp_br.nTfMuons)
            nEmuMu = int(Emu_br.nTfMuons)
            nKmtMu = int(Kmt_br.nTrks)

            if (VERBOSE and nUnpMu > 0 or nEmuMu > 0):
                print 'Unpacked = %d, emulated = %d (internal %d) total muons in collection' % (nUnpMu, nEmuMu, nKmtMu)
        
            #################################
            ###  Unpacked (legacy) muons  ###
            #################################
            for i in range(nUnpMu):
                BX      = int(Unp_br.tfMuonBx[i])
                qual    = int(Unp_br.tfMuonHwQual[i])
                ptVtx   = float(Unp_br.tfMuonHwPt[i] - 1)*0.5   ## Vertex-constrained (standard) pT is stored in 0.5 GeV steps
                ptDispl = float(Unp_br.tfMuonHwPtDispl[i] - 1)  ## Is there an offset by 1 for displaced muons? - AWB 2019.05.29
                eta     = float(Unp_br.tfMuonHwEta[i])*0.010875
                if VERBOSE: print 'Unpacked muon %d BX = %d, qual = %d, ptVtx = %.1f, ptDispl = %.1f, eta = %.2f' % (i, BX, qual, ptVtx, ptDispl, eta)
                
                if (BX  !=  0): continue
                if (qual < 12): continue

                h_pt_vtx_unp.Fill( min( max( ptVtx+0.01, pt_bins[1]+0.01), pt_bins[2]-0.01) )


            #################################
            ###  Emulated (Kalman) muons  ###
            #################################
            for i in range(nEmuMu):
                BX      = int(Emu_br.tfMuonBx[i])
                qual    = int(Emu_br.tfMuonHwQual[i])
                ptVtx   = float(Emu_br.tfMuonHwPt[i] - 1)*0.5  ## Vertex-constrained (standard) pT is stored in 0.5 GeV steps
                ptDispl = float(Emu_br.tfMuonHwPtDispl[i])     ## Is there an offset by 1 for displaced muons? - AWB 2019.05.29
                eta     = float(Emu_br.tfMuonHwEta[i])*0.010875
                if VERBOSE: print 'Emulated muon %d BX = %d, qual = %d, ptVtx = %.1f, ptDispl = %.1f, eta = %.2f' % (i, BX, qual, ptVtx, ptDispl, eta)
                
                if (BX  !=  0): continue
                if (qual < 12): continue

                h_pt_vtx_emu  .Fill( min( max( ptVtx+0.01,   pt_bins[1]+0.01), pt_bins[2]-0.01) )
                h_pt_displ_emu.Fill( min( max( ptDispl+0.01, pt_bins[1]+0.01), pt_bins[2]-0.01) )


            ######################################
            ###  Extra info from Kalman muons  ###
            ######################################
            for i in range(nKmtMu):
                BX      = int(Kmt_br.bx[i])
                qual    = int(Kmt_br.quality[i])
                ptVtx   = -1
                ptDispl = float(Kmt_br.ptUnconstrained[i])  ## Is there an offset by 1 for displaced muons? - AWB 2019.05.29
                eta     = float(Kmt_br.coarseEta[i])*0.010875
                chi2    = float(Kmt_br.approxChi2[i])
                if VERBOSE: print 'Internal muon %d BX = %d, qual = %d, ptVtx = %.1f, ptDispl = %.1f, eta = %.2f' % (i, BX, qual, ptVtx, ptDispl, eta)
                
                if (BX  !=  0): continue
                # if (qual < 12): continue  ## Quality assignment not the same as uGMT quality

                h_pt_displ_kmt.Fill( min( max( ptDispl, pt_bins[1]+0.01), pt_bins[2]-0.01) )
                h_chi2_kmt    .Fill( min( max( chi2,   chi_bins[1]+0.01), chi_bins[2]-0.01) )

        ## End loop: for jEvt in range(chains['Unp'][iCh].GetEntries()):
    ## End loop: for iCh in range(len(chains['Unp'])):

    print '\nFinished loop over chains'

    out_file.cd()

    h_pt_vtx_unp.SetLineWidth(2)
    h_pt_vtx_unp.SetLineColor(R.kBlack)
    h_pt_vtx_unp.Write()

    h_pt_vtx_emu.SetLineWidth(2)
    h_pt_vtx_emu.SetLineColor(R.kBlue)
    h_pt_vtx_emu.Write()

    h_pt_displ_emu.SetLineWidth(2)
    h_pt_displ_emu.SetLineColor(R.kRed)
    h_pt_displ_emu.Write()
    
    h_pt_displ_kmt.SetLineWidth(2)
    h_pt_displ_kmt.SetLineColor(R.kMagenta)
    h_pt_displ_kmt.Write()
    
    h_chi2_kmt.SetLineWidth(2)
    h_chi2_kmt.SetLineColor(R.kBlack)
    h_chi2_kmt.Write()
    
    out_file.Close()
    del chains

    print '\nWrote out file: plots/'+out_file_str+'.root'


if __name__ == '__main__':
    main()

#! /usr/bin/env python

## Look at rate of VBF seeds in ZeroBias data

import sys

from ROOT import *
gROOT.SetBatch(False)
import math
# from Helper import *
import subprocess

def main():

    print 'Inside ETT_rate'

    PRT_EVT  =   1  ## Print every Nth event
    MAX_EVT  = 100  ## Number of events to process
    MAX_FILE =   1  ## Number of files to process
    # GOOD_RUNS = [306041, 306037, 306121]
    # GOOD_RUNS = [306091]
    GOOD_RUNS = []
    MIN_PU = 50      ## Only process events with PU > XX
    ZBRATE = 28500.  ## ZeroBias rate ~21000 kHz with 8b4e, ~28500 kHz with 48b
    

    in_file_names = []
    
    # Reis_dir = '/eos/cms/store/group/dpg_trigger/comm_trigger/L1Trigger/treis/l1t-integration-v97p17v2-CMSSW-1000omtfNewGhostBuster/'
    # for dir1 in  subprocess.check_output(['ls', Reis_dir]).splitlines():
    #     if not ('ZeroBias' in dir1): continue
    #     for dir2 in subprocess.check_output(['ls', Reis_dir+dir1]).splitlines():
    #         if not ('crab_l1t-integration-v97p17v2-CMSSW-1000omtfNewGhostBuster__ZeroBias_Run2017F-v1' in dir2): continue
    #         for dir3 in subprocess.check_output(['ls', Reis_dir+dir1+'/'+dir2]).splitlines():
    #             if not ('180406_162254' in dir3): continue
    #             for dir4 in subprocess.check_output(['ls', Reis_dir+dir1+'/'+dir2+'/'+dir3]).splitlines():
    #                 print '\n'+Reis_dir+dir1+'/'+dir2+'/'+dir3+'/'+dir4
    #                 for f_name in subprocess.check_output(['ls', Reis_dir+dir1+'/'+dir2+'/'+dir3+'/'+dir4]).splitlines():
    #                     if not ('.root') in f_name: continue
    #                     in_file_names.append(Reis_dir+dir1+'/'+dir2+'/'+dir3+'/'+dir4+'/'+f_name)

    Aaron_dir = '/eos/cms/store/group/dpg_trigger/comm_trigger/L1Trigger/bundocka/ZeroBias/zbMET'
    # for idx in ['a', 'b', 'c', 'd', 'e']:
    #     in_file_names.append(Aaron_dir+idx+'/L1Ntuple_Skim_PU50.root')
    for idx in ['e']:
        in_file_names.append(Aaron_dir+idx+'/L1Ntuple_Skim_PU50_0.root')

    # Aaron_dir = '/eos/cms/store/group/dpg_trigger/comm_trigger/L1Trigger/bundocka/ZeroBias/zbMETe/181212_124839/0000/'
    # for f_name in subprocess.check_output(['ls', Aaron_dir]).splitlines():
    #     if not '.root' in f_name: continue
    #     in_file_names.append(Aaron_dir+f_name)


    out_file_str = 'ETT_rates_PU_%d' % MIN_PU
    out_file_str += ('_%dk' % (MAX_EVT / 1000))
    out_file = TFile('plots/'+out_file_str+'.root','recreate')
    out_file.cd()

    chains = {}
    chains['Evt'] = 0  ## Event info
    chains['Vtx'] = 0  ## Reconstructed vertices
    chains['Unp'] = 0  ## Unpacked L1T
    chains['Emu'] = 0  ## Emulated L1T
    for i in range(len(in_file_names)):
        if i >= MAX_FILE: continue
        print 'Adding file %s' % in_file_names[i]
        if i == 0:
            chains['Evt'] = TChain('l1EventTree/L1EventTree')
            chains['Vtx'] = TChain('l1RecoTree/RecoTree')
            chains['Unp'] = TChain('l1UpgradeTree/L1UpgradeTree')
            chains['Emu'] = TChain('l1UpgradeEmuTree/L1UpgradeTree')
        chains['Evt'].Add( in_file_names[i] )
        chains['Vtx'].Add( in_file_names[i] )
        chains['Unp'].Add( in_file_names[i] )
        chains['Emu'].Add( in_file_names[i] )


    # ###################
    # ### Book parameters
    # ###################

    # eta_cuts = [-5.0, 5.0]

    #################
    ### Book counters
    #################

    ## BX 0
    nEvtSingleMu0_unp  = 0
    nEvtSingleMu0_emu  = 0
    nEvtSingleMu22_unp = 0
    nEvtSingleMu22_emu = 0

    nEvtSingleJet60_unp  = 0
    nEvtSingleJet60_emu  = 0
    nEvtSingleJet180_unp = 0
    nEvtSingleJet180_emu = 0

    nEvtETMHF120_unp = 0
    nEvtETMHF120_emu = 0
    nEvtHTT320_unp = 0
    nEvtHTT320_emu = 0

    nEvtETT500_unp = 0
    nEvtETT500_emu = 0
    nEvtETT1000_unp = 0
    nEvtETT1000_emu = 0
    nEvtETT1500_unp = 0
    nEvtETT1500_emu = 0
    nEvtETT2000_unp = 0
    nEvtETT2000_emu = 0


    ###################
    ### Book histograms
    ###################

    ETM_bins = [40,  0,  200]
    HTT_bins = [285, 30, 600]
    ETT_bins = [50,  0, 2500]

    h_ETM_unp = TH1D('h_ETM_unp', 'Rate of unpacked L1 ETMHF vs. threshold', ETM_bins[0], ETM_bins[1], ETM_bins[2])
    h_ETM_emu = TH1D('h_ETM_emu', 'Rate of emulated L1 ETMHF vs. threshold', ETM_bins[0], ETM_bins[1], ETM_bins[2])
    h_HTT_unp = TH1D('h_HTT_unp', 'Rate of unpacked L1 HTT |#eta < 2.5| vs. threshold', HTT_bins[0], HTT_bins[1], HTT_bins[2])
    h_HTT_emu = TH1D('h_HTT_emu', 'Rate of emulated L1 HTT |#eta < 2.5| vs. threshold', HTT_bins[0], HTT_bins[1], HTT_bins[2])
    h_ETT_unp = TH1D('h_ETT_unp', 'Rate of unpacked L1 ETT |#eta < 3.0| vs. threshold', ETT_bins[0], ETT_bins[1], ETT_bins[2])
    h_ETT_emu = TH1D('h_ETT_emu', 'Rate of emulated L1 ETT |#eta < 3.0| vs. threshold', ETT_bins[0], ETT_bins[1], ETT_bins[2])

    h_Njet_emu  = []
    h_Njet_off  = []
    Njet_colors = [kGray, kMagenta, kRed, kOrange, kGreen, kBlue, kViolet] 
    for i in range(7):
        h_Njet_emu.append( TH1D('h_%djet_emu' % i, 'Rate of L1 sum of %d highest-ET |#eta < 2.4| jets vs. threshold' % i, HTT_bins[0], HTT_bins[1], HTT_bins[2]) )
        h_Njet_off.append( TH1D('h_%djet_off' % i, 'Threshold reduction for L1 sum of %d jets vs. HTTer threshold' % i,   HTT_bins[0], HTT_bins[1], HTT_bins[2]) )


    nPass = -1

    print '\nDefining vertex branch as L1AnalysisRecoVertexDataFormat'
    # ## Faster tecnhique, inspired by https://github.com/thomreis/l1tMuonTools/blob/master/L1Analysis.py
    # Evt_br = L1Analysis.L1AnalysisEventDataFormat()
    Vtx_br = L1Analysis.L1AnalysisRecoVertexDataFormat()
    # Unp_br = L1Analysis.L1AnalysisL1UpgradeDataFormat()
    # Emu_br = L1Analysis.L1AnalysisL1UpgradeDataFormat()

    print '\nSetting vertex branch address'
    # chains['Evt'].SetBranchAddress('Event',     AddressOf(Evt_br))
    chains['Vtx'].SetBranchAddress('Vertex',    AddressOf(Vtx_br))
    # chains['Unp'].SetBranchAddress('L1Upgrade', AddressOf(Unp_br))
    # chains['Emu'].SetBranchAddress('L1Upgrade', AddressOf(Emu_br))


    print '\nEntering loop over events:'
    print chains['Vtx'].GetEntries()
    for iEvt in range(chains['Vtx'].GetEntries()):

        print '\nAbout to get entry #%d for l1RecoTree/RecoTree tree' % iEvt
        # chains['Evt'].GetEntry(iEvt)
        chains['Vtx'].GetEntry(iEvt)

        # ## Do this if you don't explicitly define the DataFormat and do SetBranchAddress above
        # Evt_br = chains['Evt'].Event
        # Vtx_br = chains['Vtx'].Vertex
        # Unp_br = chains['Unp'].L1Upgrade
        # Emu_br = chains['Emu'].L1Upgrade

        print '  * Number of vertices in event:'
        print int(Vtx_br.nVtx)
        if int(Vtx_br.nVtx) < MIN_PU: continue

        if ( len(GOOD_RUNS) > 0 and not int(Evt_br.run) in GOOD_RUNS ):
            print '\nLooking at run %d, not in list below - skipping' % int(Evt_br.run)
            print GOOD_RUNS
            print ''
            break

        if nPass > MAX_EVT: break
        nPass += 1
        if nPass % PRT_EVT is 0: print 'Event # %dk (%dth in chain)' % (nPass/1000, iEvt)

        if nPass % PRT_EVT is 0: print '  * Run %d, LS %d, event %d, nPV = %d' % (int(Evt_br.run), int(Evt_br.lumi), int(Evt_br.event), int(Vtx_br.nVtx))

        chains['Unp'].GetEntry(iEvt)
        chains['Emu'].GetEntry(iEvt)

        nUnpMu  = int(Unp_br.nMuons)
        nEmuMu  = int(Emu_br.nMuons)
        nUnpJet = int(Unp_br.nJets)
        nEmuJet = int(Emu_br.nJets)
        nUnpSum = int(Unp_br.nSums)
        nEmuSum = int(Emu_br.nSums)

        nSingMu0_unp  = 0
        nSingMu0_emu  = 0
        nSingMu22_unp = 0
        nSingMu22_emu = 0
        
        nSingJet60_unp  = 0
        nSingJet60_emu  = 0
        nSingJet180_unp = 0
        nSingJet180_emu = 0

        # if (nUnpMu > 0 or nEmuMu > 0):
        #     print 'Unpacked = %d, emulated = %d total muons in collection' % (nUnpMu, nEmuMu)
        
        ########################
        ###  Unpacked muons  ###
        ########################
        for i in range(nUnpMu):
            BX   = int(Unp_br.muonBx[i])
            qual = int(Unp_br.muonQual[i])
            pt   = float(Unp_br.muonEt[i]) + 0.01
            eta  = float(Unp_br.muonEta[i])
            # print 'Muon %d BX = %d, qual = %d, pt = %.2f' % (i, BX, qual, pt)

            if (BX  !=  0): continue
            if (qual < 12): continue
            nSingMu0_unp  += 1
            if (pt >= 22): nSingMu22_unp += 1

        ########################
        ###  Emulated muons  ###
        ########################
        for i in range(nEmuMu):
            BX   = int(Emu_br.muonBx[i])
            qual = int(Emu_br.muonQual[i])
            pt   = float(Emu_br.muonEt[i]) + 0.01
            eta  = float(Emu_br.muonEta[i])
            # print 'Muon %d BX = %d, qual = %d, pt = %.2f' % (i, BX, qual, pt)

            if (BX  !=  0): continue
            if (qual < 12): continue
            nSingMu0_emu  += 1
            if (pt >= 22): nSingMu22_emu += 1

        if (nSingMu0_unp  > 0): nEvtSingleMu0_unp  += 1
        if (nSingMu0_emu  > 0): nEvtSingleMu0_emu  += 1
        if (nSingMu22_unp > 0): nEvtSingleMu22_unp += 1
        if (nSingMu22_emu > 0): nEvtSingleMu22_emu += 1


        #######################
        ###  Unpacked jets  ###
        #######################
        for i in range(nUnpJet):

            BX1  = int(Unp_br.jetBx[i])
            pt1  = float(Unp_br.jetEt[i]) + 0.01
            eta1 = float(Unp_br.jetEta[i])
            phi1 = float(Unp_br.jetPhi[i])
            # print 'Jet %d BX = %d, pt = %.2f, eta = %.2f' % (i, BX1, pt1, eta1)

            if (BX1 !=   0): continue
            if (pt1  <  30): continue 
            if (pt1 >=  60): nSingJet60_unp  += 1
            if (pt1 >= 180): nSingJet180_unp += 1


        #######################
        ###  Emulated jets  ###
        #######################
        jetSum   = [0,0,0,0,0,0,0,0]
        pt1      = 999999.
        nJetPass = 0
        for i in range(nEmuJet):

            if ( float(Emu_br.jetEt[i]) + 0.01 > pt1 ):
                print '\nBIZZARE ERROR! Emulated jet #%d has pt = %.1f, jet #%d has pT = %.1f. Quitting' % (i, pt1, i+1, float(Emu_br.jetEt[i]) + 0.01)
                sys.exit()

            BX1  = int(Emu_br.jetBx[i])
            pt1  = float(Emu_br.jetEt[i]) + 0.01
            eta1 = float(Emu_br.jetEta[i])
            phi1 = float(Emu_br.jetPhi[i])
            # print 'Jet %d BX = %d, pt = %.2f, eta = %.2f' % (i, BX1, pt1, eta1)

            if (BX1 !=   0): continue
            if (pt1  <  30): continue
            if (pt1 >=  60): nSingJet60_emu  += 1
            if (pt1 >= 180): nSingJet180_emu += 1

            if (abs(eta1) > 2.4): continue
            nJetPass += 1

            jetSum[0] += pt1
            for j in range(1, 7):
                if (nJetPass <= j): jetSum[j] += pt1

        for xBin in range(HTT_bins[0]):
            xVal = h_Njet_emu[0].GetXaxis().GetBinLowEdge(xBin+1)
            for j in range(7):
                if (jetSum[j]+0.01 >= xVal): h_Njet_emu[j].Fill(xVal+0.01)


        #############################
        ###  Fill jet quantities  ###
        #############################

        if (nSingJet60_unp  > 0): nEvtSingleJet60_unp  += 1
        if (nSingJet60_emu  > 0): nEvtSingleJet60_emu  += 1
        if (nSingJet180_unp > 0): nEvtSingleJet180_unp += 1
        if (nSingJet180_emu > 0): nEvtSingleJet180_emu += 1

        #######################
        ###  Unpacked sums  ###
        #######################
        for i in range(nUnpSum):
            BX    = int(Unp_br.sumBx[i])
            kType = int(Unp_br.sumType[i])
            pt    = float(Unp_br.sumEt[i]) + 0.01
            # print 'Sum %d BX = %d, type = %d, pt = %.2f' % (i, BX, kType, pt)

            if (BX !=   0): continue

            if (kType == 8):
                if (pt >=  120): nEvtETMHF120_unp += 1

                for xBin in range(ETM_bins[0]):
                    xVal = h_ETM_unp.GetXaxis().GetBinLowEdge(xBin+1)
                    if (pt >= xVal): h_ETM_unp.Fill(xVal+0.01)

            if (kType == 1):
                if (pt >=  320): nEvtHTT320_unp   += 1

                for xBin in range(HTT_bins[0]):
                    xVal = h_HTT_unp.GetXaxis().GetBinLowEdge(xBin+1)
                    if (pt >= xVal): h_HTT_unp.Fill(xVal+0.01)

            if (kType == 0):
                if (pt >=  500): nEvtETT500_unp   += 1 
                if (pt >= 1000): nEvtETT1000_unp  += 1 
                if (pt >= 1500): nEvtETT1500_unp  += 1 
                if (pt >= 2000): nEvtETT2000_unp  += 1

                for xBin in range(ETT_bins[0]):
                    xVal = h_ETT_unp.GetXaxis().GetBinLowEdge(xBin+1)
                    if (pt >= xVal): h_ETT_unp.Fill(xVal+0.01)



        #######################
        ###  Emulated sums  ###
        #######################
        for i in range(nEmuSum):
            BX    = int(Emu_br.sumBx[i])
            kType = int(Emu_br.sumType[i])
            pt    = float(Emu_br.sumEt[i]) + 0.01
            # print 'Sum %d BX = %d, type = %d, pt = %.2f' % (i, BX, kType, pt)

            if (BX !=   0): continue
            
            if (kType == 8):
                if (pt >=  120): nEvtETMHF120_emu += 1
                
                for xBin in range(ETM_bins[0]):
                    xVal = h_ETM_emu.GetXaxis().GetBinLowEdge(xBin+1)
                    if (pt >= xVal): h_ETM_emu.Fill(xVal+0.01)

            if (kType == 1):
                if (pt >=  320): nEvtHTT320_emu   += 1

                for xBin in range(HTT_bins[0]):
                    xVal = h_HTT_emu.GetXaxis().GetBinLowEdge(xBin+1)
                    if (pt >= xVal): h_HTT_emu.Fill(xVal+0.01)

            if (kType == 0):
                if (pt >=  500): nEvtETT500_emu   += 1 
                if (pt >= 1000): nEvtETT1000_emu  += 1 
                if (pt >= 1500): nEvtETT1500_emu  += 1 
                if (pt >= 2000): nEvtETT2000_emu  += 1

                for xBin in range(ETT_bins[0]):
                    xVal = h_ETT_emu.GetXaxis().GetBinLowEdge(xBin+1)
                    if (pt >= xVal): h_ETT_emu.Fill(xVal+0.01)
 

    print '\nFinished loop over events'

    print '\n*****************************'
    print '*******   TOTAL RATES   *******'
    print '*******************************'
    print 'Number of events              %6d    %6.1f kHz' % (nPass+1,                 (nPass+1)               * ZBRATE / (nPass+1))
    print 'Unpacked muons                %6d    %6.1f kHz' % (nEvtSingleMu0_unp,       nEvtSingleMu0_unp       * ZBRATE / (nPass+1))
    print '  * pT >= 22                  %6d    %6.1f kHz' % (nEvtSingleMu22_unp,      nEvtSingleMu22_unp      * ZBRATE / (nPass+1))
    print 'Emulated muons                %6d    %6.1f kHz' % (nEvtSingleMu0_emu,       nEvtSingleMu0_emu       * ZBRATE / (nPass+1)) 
    print '  * pT >= 22                  %6d    %6.1f kHz' % (nEvtSingleMu22_emu,      nEvtSingleMu22_emu      * ZBRATE / (nPass+1))
    print 'Unpacked jets (ET > 60)       %6d    %6.1f kHz' % (nEvtSingleJet60_unp,     nEvtSingleJet60_unp     * ZBRATE / (nPass+1))
    print '  * ET >= 180                 %6d    %6.1f kHz' % (nEvtSingleJet180_unp,    nEvtSingleJet180_unp    * ZBRATE / (nPass+1))
    print 'Emulated jets (ET > 60)       %6d    %6.1f kHz' % (nEvtSingleJet60_emu,     nEvtSingleJet60_emu     * ZBRATE / (nPass+1)) 
    print '  * ET >= 180                 %6d    %6.1f kHz' % (nEvtSingleJet180_emu,    nEvtSingleJet180_emu    * ZBRATE / (nPass+1))
    print 'Unpacked ETMHF > 120          %6d    %6.1f kHz' % (nEvtETMHF120_unp,        nEvtETMHF120_unp        * ZBRATE / (nPass+1))
    print 'Emulated ETMHF > 120          %6d    %6.1f kHz' % (nEvtETMHF120_emu,        nEvtETMHF120_emu        * ZBRATE / (nPass+1))
    print 'Unpacked HTTer > 320          %6d    %6.1f kHz' % (nEvtHTT320_unp,          nEvtHTT320_unp          * ZBRATE / (nPass+1))
    print 'Emulated HTTer > 320          %6d    %6.1f kHz' % (nEvtHTT320_emu,          nEvtHTT320_emu          * ZBRATE / (nPass+1))
    print 'Unpacked ETT (ET > 500)       %6d    %6.1f kHz' % (nEvtETT500_unp,          nEvtETT500_unp          * ZBRATE / (nPass+1))
    print '  * ET >= 1000                %6d    %6.1f kHz' % (nEvtETT1000_unp,         nEvtETT1000_unp         * ZBRATE / (nPass+1))
    print '  * ET >= 1500                %6d    %6.1f kHz' % (nEvtETT1500_unp,         nEvtETT1500_unp         * ZBRATE / (nPass+1))
    print '  * ET >= 2000                %6d    %6.1f kHz' % (nEvtETT2000_unp,         nEvtETT2000_unp         * ZBRATE / (nPass+1))
    print 'Emulated ETT (ET > 500)       %6d    %6.1f kHz' % (nEvtETT500_emu,          nEvtETT500_emu          * ZBRATE / (nPass+1)) 
    print '  * ET >= 1000                %6d    %6.1f kHz' % (nEvtETT1000_emu,         nEvtETT1000_emu         * ZBRATE / (nPass+1))
    print '  * ET >= 1500                %6d    %6.1f kHz' % (nEvtETT1500_emu,         nEvtETT1500_emu         * ZBRATE / (nPass+1))
    print '  * ET >= 2000                %6d    %6.1f kHz' % (nEvtETT2000_emu,         nEvtETT2000_emu         * ZBRATE / (nPass+1))

    out_file.cd()

    h_ETM_unp.SetLineWidth(2)
    h_ETM_emu.SetLineWidth(2)
    h_ETM_unp.SetLineColor(kBlack)
    h_ETM_emu.SetLineColor(kBlue)
    h_ETM_unp.GetXaxis().SetTitle('Threshold (GeV)')
    h_ETM_emu.GetXaxis().SetTitle('Threshold (GeV)')
    h_ETM_unp.GetYaxis().SetTitle('Rate (kHz)')
    h_ETM_emu.GetYaxis().SetTitle('Rate (kHz)')
    h_ETM_unp.Scale(ZBRATE / (nPass+1))
    h_ETM_emu.Scale(ZBRATE / (nPass+1))
    h_ETM_unp.Write()
    h_ETM_emu.Write()
    
    h_HTT_unp.SetLineWidth(2)
    h_HTT_emu.SetLineWidth(2)
    h_HTT_unp.SetLineColor(kBlack)
    h_HTT_emu.SetLineColor(kBlue)
    h_HTT_unp.GetXaxis().SetTitle('Threshold (GeV)')
    h_HTT_emu.GetXaxis().SetTitle('Threshold (GeV)')
    h_HTT_unp.GetYaxis().SetTitle('Rate (kHz)')
    h_HTT_emu.GetYaxis().SetTitle('Rate (kHz)')
    h_HTT_unp.Scale(ZBRATE / (nPass+1))
    h_HTT_emu.Scale(ZBRATE / (nPass+1))
    h_HTT_unp.Write()
    h_HTT_emu.Write()
    
    h_ETT_unp.SetLineWidth(2)
    h_ETT_emu.SetLineWidth(2)
    h_ETT_unp.SetLineColor(kBlack)
    h_ETT_emu.SetLineColor(kBlue)
    h_ETT_unp.GetXaxis().SetTitle('Threshold (GeV)')
    h_ETT_emu.GetXaxis().SetTitle('Threshold (GeV)')
    h_ETT_unp.GetYaxis().SetTitle('Rate (kHz)')
    h_ETT_emu.GetYaxis().SetTitle('Rate (kHz)')
    h_ETT_unp.Scale(ZBRATE / (nPass+1))
    h_ETT_emu.Scale(ZBRATE / (nPass+1))
    h_ETT_unp.Write()
    h_ETT_emu.Write()

    for i in range(7):
        h_Njet_emu[i].SetLineWidth(2)
        h_Njet_emu[i].SetLineColor(Njet_colors[i])
        h_Njet_emu[i].GetXaxis().SetTitle('Threshold (GeV)')
        h_Njet_emu[i].GetYaxis().SetTitle('Rate (kHz)')
        h_Njet_emu[i].Scale(ZBRATE / (nPass+1))
        h_Njet_emu[i].Write()

        for j in range(HTT_bins[0]):
            for k in range(HTT_bins[0]):
                if h_Njet_emu[i].GetBinContent(k) > h_HTT_emu.GetBinContent(j+1) and h_Njet_emu[i].GetBinContent(k+1) <= h_HTT_emu.GetBinContent(j+1):
                    h_Njet_off[i].SetBinContent(j+1, h_HTT_emu.GetBinLowEdge(j+1) - h_Njet_emu[i].GetBinLowEdge(k+1))
                    break
 
        h_Njet_off[i].SetLineWidth(2)
        h_Njet_off[i].SetLineColor(Njet_colors[i])
        h_Njet_off[i].GetXaxis().SetTitle('HTTer Threshold (GeV)')
        h_Njet_off[i].GetYaxis().SetTitle('Jet sum threshold reduction (GeV)')
        h_Njet_off[i].Write()

    
    
    out_file.Close()
    del chains


if __name__ == '__main__':
    main()

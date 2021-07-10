#! /usr/bin/env python

## Look at rate of gluon fusion HH --> 4b seeds in ZeroBias data

import ROOT as R
R.gROOT.SetBatch(True)  ## Don't print histograms to screen while processing

from subprocess import Popen,PIPE
import os
import json
import math


PRT_EVT  = 10000  ## Print every Nth event
MAX_EVT  = 100000 ## Number of events to process        (set to -1 for all events)
MAX_FILE = 50     ## Maximum number of files to process (set to -1 for all files)
VERBOSE  = False  ## Print extra information

TRG_FAIL = False  ## Require events to fail exactly one threshold in HTT320er_QuadJet_70_55_40_40_er2p4 (and fail HTT360er)


## Function to mask events using JSON file
def PassJSON(JSON, run, LS):
    Good_LS = False
    if not str(run) in JSON.keys():
        return Good_LS
    for iLS in range( len( JSON[str(run)] ) ):
        if int(LS) >= JSON[str(run)][iLS][0] and int(LS) <= JSON[str(run)][iLS][-1]:
            Good_LS = True
            break
        if Good_LS: break
    return Good_LS
## End function: PassJSON(JSON, run, LS)


def main():

    print '\nInside ggHH_4b_rate\n'

    ## Full set of high-pileup ZeroBias data from 2018
    top_dir = '/eos/cms/store/group/dpg_trigger/comm_trigger/L1Trigger/ssawant/ZeroBias/L1TNtuple_HCal_OOT_PUS_PFA2_wCaloOption_Run2018'
    in_dirs = ['A-PromptReco-v1', 'A-PromptReco-v2', 'B-PromptReco-v1', 'B-PromptReco-v2',
               'C-PromptReco-v1', 'C-PromptReco-v2', 'D-PromptReco-v2']

    in_file_names = []
    for in_dir in in_dirs:
        for dir1 in Popen(['ls', top_dir+in_dir], stdout=PIPE).communicate()[0].split():
            for dir2 in Popen(['ls', top_dir+in_dir+'/'+dir1], stdout=PIPE).communicate()[0].split():
                for f_name in Popen(['ls', top_dir+in_dir+'/'+dir1+'/'+dir2], stdout=PIPE).communicate()[0].split():
                    if len(in_file_names) >= MAX_FILE and MAX_FILE > 0: break
                    if not '.root' in f_name: continue
                    if not 'nVtxMin_50' in f_name: continue
                    ## Require input ROOT files to be > 2 MB (avoid ROOT "Too many open files" error)
                    if os.path.getsize(top_dir+in_dir+'/'+dir1+'/'+dir2+'/'+f_name) < 2*pow(1024,2): continue
                    in_file_names.append(top_dir+in_dir+'/'+dir1+'/'+dir2+'/'+f_name)


    out_file_str = 'ggHH_4b_rates_nVtxMin_50'
    if TRG_FAIL:
        out_file_str += '_TrgFail'
    out_file_str += '_2018'
    for in_file in in_file_names:
        for era in ['A','B','C','D']:
            if 'Run2018'+era in in_file and not era in out_file_str.split('2018')[1]:
                out_file_str += '%s' % era
    if MAX_EVT > 0:
        out_file_str += ('_%dk' % (MAX_EVT / 1000))

    ## Creat output png directory if it doesn't exist
    if not os.path.exists('plots/png/'+out_file_str):
        os.makedirs('plots/png/'+out_file_str)
    else:  ## Delete old png files
        for png in os.listdir('plots/png/'+out_file_str):
            os.remove(os.path.join('plots/png/'+out_file_str, png))

    ## Create output ROOT file
    out_file = R.TFile('plots/'+out_file_str+'.root','recreate')
    print 'Will output plots to plots/'+out_file_str+'.root\n'


    chains = {}
    chains['Evt'] = []  ## Event info
    chains['Unp'] = []  ## Unpacked L1T
    chains['Emu'] = []  ## Emulated L1T
    for f_name in in_file_names:
        print 'Adding file %s' % f_name
        chains['Evt'].append( R.TChain('l1EventTree/L1EventTree') )
        chains['Unp'].append( R.TChain('l1UpgradeTree/L1UpgradeTree') )
        chains['Emu'].append( R.TChain('l1UpgradeEmuTree/L1UpgradeTree') )
        chains['Evt'][-1].Add( f_name )
        chains['Unp'][-1].Add( f_name )
        chains['Emu'][-1].Add( f_name )

    ## Load 2018 Golden JSON file
    JSON_FILE = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions18/13TeV/Legacy_2018/Cert_314472-325175_13TeV_Legacy2018_Collisions18_JSON.txt'
    print '\nLoading 2018 Golden JSON from %s' % JSON_FILE
    with open(JSON_FILE) as json_file:
        JSON = json.load(json_file)


    ###################
    ### Book histograms
    ###################

    mpt_bins  = [20, 0,  20]      ## pT bins for muons
    jpt_bins  = [80, 0, 400]      ## pT bins for jets and HT
    eta_bins  = [60, -3.0, 3.0 ]  ## eta bins for muons and jets

    hst = {}  ## Book all histograms
    for src in ['unp', 'emu']:
        for obj in ['muon', 'jet1', 'jet2', 'jet3', 'jet4', 'HT']:
            for var in ['pt', 'eta']:
                ## Set binning
                if var == 'pt':
                    if obj == 'muon': bins = mpt_bins
                    else:             bins = jpt_bins
                if var == 'eta':
                    bins = eta_bins
                    if obj == 'HT': continue
                ## Book histogram
                hst['%s_%s_%s' % (obj, var, src)] = R.TH1D('h_%s_%s_%s' % (obj, var, src), '%s %s %s' % (src, obj, var), bins[0], bins[1], bins[2])
                
    hst['min_dR_muon_jet_unp'] = R.TH1D('h_min_dR_muon_jet_unp', 'unp min dR(muon, jet)', 23, -0.1, 1.05)
    hst['min_dR_muon_jet_emu'] = R.TH1D('h_min_dR_muon_jet_emu', 'emu min dR(muon, jet)', 23, -0.1, 1.05)

    hst['QuadJet_fail']         = R.TH1D('h_QuadJet_fail',         'QuadJet only threshold failed (HT 320, pT 70/55/40/40)', 6, -0.5, 5.5)
    hst['QuadJet_fail_low']     = R.TH1D('h_QuadJet_fail_low',     'QuadJet only threshold failed (HT 320, pT 50/45/40/40)', 6, -0.5, 5.5)
    hst['QuadJet_fail_pt40']    = R.TH1D('h_QuadJet_fail_pt40',    'QuadJet only threshold failed (HT 320, pT 40/40/40/40)', 6, -0.5, 5.5)
    hst['QuadJet_fail_PS']      = R.TH1D('h_QuadJet_fail_PS',      'QuadJet only threshold failed (HT 280, pT 70/55/40/35)', 6, -0.5, 5.5)
    hst['QuadJet_fail_PS_low']  = R.TH1D('h_QuadJet_fail_PS_low',  'QuadJet only threshold failed (HT 280, pT 45/40/35/35)', 6, -0.5, 5.5)
    hst['QuadJet_fail_PS_pt35'] = R.TH1D('h_QuadJet_fail_PS_pt35', 'QuadJet only threshold failed (HT 280, pT 35/35/35/35)', 6, -0.5, 5.5)


    ####################
    ### Loop over events
    ####################

    iEvt = 0    ## Total event counter
    nEvtZB = 0  ## Number of events considered (base "ZeroBias" rate)
    print '\nEntering loop over %d chains' % len(chains['Unp'])
    for iCh in range(len(chains['Unp'])):

        if iEvt >= MAX_EVT and MAX_EVT > 0: break

        ## Faster (maybe?) tecnhique, inspired by https://github.com/thomreis/l1tMuonTools/blob/master/L1Analysis.py
        Evt_br = R.L1Analysis.L1AnalysisEventDataFormat()
        Unp_br = R.L1Analysis.L1AnalysisL1UpgradeDataFormat()
        Emu_br = R.L1Analysis.L1AnalysisL1UpgradeDataFormat()

        chains['Evt'][iCh].SetBranchAddress('Event',     R.AddressOf(Evt_br))
        chains['Unp'][iCh].SetBranchAddress('L1Upgrade', R.AddressOf(Unp_br))
        chains['Emu'][iCh].SetBranchAddress('L1Upgrade', R.AddressOf(Emu_br))

        if chains['Unp'][iCh].GetEntries() < 100:
            print '\nChain %d has only %d events: skipping.' % (iCh, chains['Unp'][iCh].GetEntries())
            continue

        print '\nEntering loop over %d events for chain %d' % (chains['Unp'][iCh].GetEntries(), iCh)
        for jEvt in range(chains['Unp'][iCh].GetEntries()):

            if iEvt >= MAX_EVT and MAX_EVT > 0: break
            if iEvt % PRT_EVT is 0: print 'Event # %dk (%dth in chain)' % (iEvt/1000, jEvt)
            iEvt += 1

            chains['Evt'][iCh].GetEntry(jEvt)
            chains['Unp'][iCh].GetEntry(jEvt)
            chains['Emu'][iCh].GetEntry(jEvt)

            ## Define unique string listing event info
            evt_str = 'Run %d, LS %d, event %d' % (int(Evt_br.run), int(Evt_br.lumi), int(Evt_br.event))
            if VERBOSE: print evt_str
            
            ## Remove data events not in Golden JSON
            pass_JSON = PassJSON(JSON, int(Evt_br.run), int(Evt_br.lumi))
            if not pass_JSON:
                if VERBOSE: print '%s not in Golden JSON' % evt_str
                continue

            ## Events passing Golden JSON count towards "base" ZeroBias rate (28.6 MHz in 2018)
            nEvtZB += 1

            nUnpMu  = int(Unp_br.nMuons)
            nEmuMu  = int(Emu_br.nMuons)
            nUnpJet = int(Unp_br.nJets)
            nEmuJet = int(Emu_br.nJets)

            vec = {}  ## TLorentzVectors
            for src in ['unp', 'emu']:
                for obj in ['muon', 'jet1', 'jet2', 'jet3', 'jet4']:
                    vec['%s_%s' % (src, obj)] = R.TLorentzVector()
            ## HTTer sums
            HTTer_unp = 0
            HTTer_emu = 0
            ## Minimum dR between a jet and muon
            min_dR_muon_jet_unp = 999.
            min_dR_muon_jet_emu = 999.

        
            ########################
            ###  Unpacked muons  ###
            ########################
            for i in range(nUnpMu):
                BX   = int(Unp_br.muonBx[i])
                qual = int(Unp_br.muonQual[i])
                pt   = float(Unp_br.muonEt[i]) + 0.01
                eta  = float(Unp_br.muonEta[i])
                phi  = float(Unp_br.muonPhi[i])
                if VERBOSE: print 'Unpacked muon %d BX = %d, qual = %d, pt = %.2f' % (i, BX, qual, pt)

                if (BX  !=  0):      continue
                if (qual < 12):      continue
                if (abs(eta) > 2.4): continue
                vec['unp_muon'].SetPtEtaPhiM(pt, eta, phi, 0)
                break
            ## End loop: for i in range(nUnpMu)

            ########################
            ###  Emulated muons  ###
            ########################
            for i in range(nEmuMu):
                BX   = int(Emu_br.muonBx[i])
                qual = int(Emu_br.muonQual[i])
                pt   = float(Emu_br.muonEt[i]) + 0.01
                eta  = float(Emu_br.muonEta[i])
                phi  = float(Emu_br.muonPhi[i])
                if VERBOSE: print 'Emulated muon %d BX = %d, qual = %d, pt = %.2f' % (i, BX, qual, pt)

                if (BX  !=  0):      continue
                if (qual < 12):      continue
                if (abs(eta) > 2.4): continue
                vec['emu_muon'].SetPtEtaPhiM(pt, eta, phi, 0)
                break
            ## End loop: for i in range(nEmuMu)


            #######################
            ###  Unpacked jets  ###
            #######################
            iJet = 0  ## Count selected jets
            for i in range(nUnpJet):
                BX     = int(Unp_br.jetBx[i])
                pt     = float(Unp_br.jetEt[i]) + 0.01
                eta    = float(Unp_br.jetEta[i])
                phi    = float(Unp_br.jetPhi[i])
                if VERBOSE: print 'Unpacked jet %d BX = %d, pt = %.2f, eta = %.2f' % (i, BX, pt, eta)

                if (BX != 0):        continue
                if (abs(eta) > 2.5): continue
                if pt > 30: HTTer_unp += pt
                iJet += 1
                if iJet <= 4:
                    vec['unp_jet%d' % iJet].SetPtEtaPhiM(pt, eta, phi, 0)
                    if vec['unp_muon'].Pt() > 0.5:
                        min_dR_muon_jet_unp = min(min_dR_muon_jet_unp, vec['unp_jet%d' % iJet].DeltaR(vec['unp_muon']))
            ## End loop: for i in range(nUnpJet)

            #######################
            ###  Emulated jets  ###
            #######################
            iJet = 0  ## Count selected jets
            for i in range(nEmuJet):
                BX     = int(Emu_br.jetBx[i])
                pt     = float(Emu_br.jetEt[i]) + 0.01
                eta    = float(Emu_br.jetEta[i])
                phi    = float(Emu_br.jetPhi[i])
                if VERBOSE: print 'Emulated jet %d BX = %d, pt = %.2f, eta = %.2f' % (i, BX, pt, eta)

                if (BX != 0):        continue
                if (abs(eta) > 2.5): continue
                if pt > 30: HTTer_emu += pt
                iJet += 1
                if iJet <= 4:
                    vec['emu_jet%d' % iJet].SetPtEtaPhiM(pt, eta, phi, 0)
                    if vec['emu_muon'].Pt() > 0.5:
                        min_dR_muon_jet_unp = min(min_dR_muon_jet_unp, vec['emu_jet%d' % iJet].DeltaR(vec['emu_muon']))
            ## End loop: for i in range(nEmuJet)


            ################################
            ###  Existing trigger paths  ###
            ################################
            cuts = {}  ## Dictionary to store cuts, and which passed or failed
            cuts['']         = [[320,70,55,40,40], [0,0,0,0,0]]  ## HTT320er_QuadJet_70_55_40_40_er2p4
            cuts['_low']     = [[320,50,45,40,40], [0,0,0,0,0]]  ## HTT320er_QuadJet_50_45_40_40_er2p4
            cuts['_pt40']    = [[320,40,40,40,40], [0,0,0,0,0]]  ## HTT320er_QuadJet_40_40_40_40_er2p4
            cuts['_PS']      = [[280,70,55,40,35], [0,0,0,0,0]]  ## HTT280er_QuadJet_70_55_40_35_er2p4
            cuts['_PS_low']  = [[280,45,40,35,35], [0,0,0,0,0]]  ## HTT280er_QuadJet_45_40_35_35_er2p4
            cuts['_PS_pt35'] = [[280,35,35,35,35], [0,0,0,0,0]]  ## HTT280er_QuadJet_35_35_35_35_er2p4

            ## Check which thresholds failed for each trigger path
            for key in cuts.keys():
                ## Check HTTer cut
                if HTTer_unp < cuts[key][0][0]:
                    cuts[key][1][0] = 1
                ## Check all 4 jet pt cuts
                for i in range(1,5):
                    if HTTer_unp > 360: continue
                    if vec['unp_jet%d' % i].Pt() < cuts[key][0][i]:
                        cuts[key][1][i] = 1
                ## Fill histograms with passing events, and with failing thresholds
                if cuts[key][1].count(1) == 0:
                    hst['QuadJet_fail'+key].Fill(0)
                if cuts[key][1].count(1) == 1:
                    for j in range(5):
                        if cuts[key][1][j] == 1:
                            hst['QuadJet_fail'+key].Fill(j+1)
            ## End loop: for key in cuts.keys()

            ## Require event to fail exactly one cut in HTT320er_QuadJet_70_55_40_40_er2p4
            if TRG_FAIL and (HTTer_unp > 360 or cuts[''][1].count(1) != 1): continue


            #########################
            ###  Fill histograms  ###
            #########################
            for src in ['unp', 'emu']:
                for obj in ['muon', 'jet1', 'jet2', 'jet3', 'jet4']:
                    for var in ['pt', 'eta']:
                        ## Set binning
                        if var == 'pt':
                            if obj == 'muon': bins = mpt_bins
                            else:             bins = jpt_bins
                            hst['%s_%s_%s' % (obj, var, src)].Fill( max(bins[1]+0.01, min(bins[2]-0.01, vec['%s_%s' % (src, obj)].Pt()) ) )
                        if var == 'eta':
                            bins = eta_bins
                            if vec['%s_%s' % (src, obj)].Pt() < 0.5: continue
                            hst['%s_%s_%s' % (obj, var, src)].Fill( max(bins[1]+0.01, min(bins[2]-0.01, vec['%s_%s' % (src, obj)].Eta()) ) )
            ## End loop: for src in ['unp', 'emu']

            hst['HT_pt_unp'].Fill( max(jpt_bins[1]+0.01, min(jpt_bins[2]-0.01, HTTer_unp) ) )
            hst['HT_pt_emu'].Fill( max(jpt_bins[1]+0.01, min(jpt_bins[2]-0.01, HTTer_emu) ) )

            if min_dR_muon_jet_unp > 998: min_dR_muon_jet_unp = -0.099
            if min_dR_muon_jet_emu > 998: min_dR_muon_jet_emu = -0.099
            hst['min_dR_muon_jet_unp'].Fill( min(1.049, min_dR_muon_jet_unp) )
            hst['min_dR_muon_jet_emu'].Fill( min(1.049, min_dR_muon_jet_emu) )

        ## End loop: for jEvt in range(chains['Unp'][iCh].GetEntries())
    ## End loop: for iCh in range(len(chains['Unp'])):
    print '\nFinished loop over chains'


    out_file.cd()

    ## Write output histograms
    for key in hst.keys():
        hist = hst[key]
        hist.SetLineWidth(2)
        if 'unp' in key: hist.SetLineColor(R.kBlack)
        if 'emu' in key: hist.SetLineColor(R.kBlue)
        hist.GetXaxis().SetTitle( hist.GetTitle() )
        hist.GetYaxis().SetTitle( 'Events' )
        out_file.cd()
        hist.Write()

        ## Create "rate" version of each plot in kHz
        hist_rate = hist.Clone(hist.GetName()+'_rate')
        hist_rate.Scale(28600. / nEvtZB)  ## Scale by 28.6 MHz ZeroBias rate / # of events considered
        hist_rate.GetYaxis().SetTitle( 'Rate (kHz)' )
        hist_rate.Write()

        ## Create cumulative version of pT threshold plots
        isThresh = False
        for obj in ['muon', 'jet1', 'jet2', 'jet3', 'jet4', 'HT']:
            if (obj+'_pt') in key:
                isThresh = True
        if isThresh:
            hist_thresh = hist_rate.GetCumulative(False, '_thresh')
            hist_thresh.GetYaxis().SetTitle( 'Rate (kHz)' )
            hist_thresh.GetXaxis().SetTitle( hist.GetXaxis().GetTitle()+' threshold (GeV)' )
            hist_thresh.SetTitle( hist.GetTitle()+' cumulative rate vs. threshold' )
            hist_thresh.Write()

        if key.endswith('emu'): continue  ## Skip emulated plots for pngs

        can = R.TCanvas('can_'+key, 'can_'+key, 1)
        can.cd()
        can.Clear()
        hist.Draw('hist')
        if not TRG_FAIL and not 'QuadJet' in key: can.SetLogy()
        can.SaveAs('plots/png/'+out_file_str+'/'+key+'.png')

        can.Clear()
        hist_rate.Draw('hist')
        can.SaveAs('plots/png/'+out_file_str+'/'+key+'_rate.png')

        if isThresh:
            can.Clear()
            hist_thresh.Draw('hist')
            can.SaveAs('plots/png/'+out_file_str+'/'+key+'_rate_thresh.png')

    ## End loop: for key in hst.keys()

    
    print '\nWrote plots to plots/'+out_file_str+'.root'
    out_file.Close()
    del chains


if __name__ == '__main__':
    main()

#! /usr/bin/env python

## *************************************************************************** ##
##  Look at scale and resolution of L1T jets and MET with different input TPs  ##
## *************************************************************************** ##

import os

import ROOT as R
R.gROOT.SetBatch(False)  ## Don't print histograms to screen while processing

PRT_EVT  = 1000   ## Print every Nth event
MAX_EVT  = -1     ## Number of events to process
VERBOSE  = False  ## Verbose print-out

PT_MIN = 30   ## Minimum offline jet pT to consider
DR_MIN = 1.2  ## Minimum dR between offline jets considered for measurement
DR_MAX = 0.3  ## Maximum dR between L1T and offline jets for matching

PT_CAT = {}
PT_CAT['lowPt'] = [30,  60,   60]  ## Low pT, turn-on threshold, high pT
PT_CAT['medPt'] = [60,  90,   90]  ## Low pT, turn-on threshold, high pT
PT_CAT['hiPt']  = [90, 120, 9999]  ## Low pT, turn-on threshold, high pT

ETA_CAT = {}
ETA_CAT['HBEF'] = [0.000, 5.210]  ## Whole detector, 1 - 41
ETA_CAT['HB']   = [0.000, 1.392]  ## Trigger towers  1 - 16
ETA_CAT['HE1']  = [1.392, 1.740]  ## Trigger towers 17 - 20
ETA_CAT['HE2a'] = [1.740, 2.322]  ## Trigger towers 21 - 25
ETA_CAT['HE2b'] = [2.322, 3.000]  ## Trigger towers 26 - 28
ETA_CAT['HF']   = [3.000, 5.210]  ## Trigger towers 30 - 41



def main():

    print '\nInside L1T_JetMET_Res\n'

    in_file_names = []
    # in_file_names.append('output/L1Ntuple_HCAL_Original_nVtxMin_50_100k.root')
    # in_file_names.append('output/L1Ntuple_HCAL_TP_OOT_PUS_nVtxMax_12_nSamp_1_nPresamp_0_HB_1p0_HE1_1p0_HE2_1p0_100k.root')
    in_file_names.append('output/L1Ntuple_HCAL_TP_OOT_PUS_nVtxMin_40_nSamp_2_nPresamp_0_HB_1p0_1p0_HE1_1p0_1p0_HE2_1p0_1p0_100k.root')
    in_file_names.append('output/L1Ntuple_HCAL_TP_OOT_PUS_nVtxMin_40_nSamp_2_nPresamp_1_HB_n0p51_1p0_HE1_n0p49_1p0_HE2_n0p45_1p0_100k.root')

    if not os.path.exists('plots'): os.makedirs('plots')

    out_file_str = 'L1T_JetMET_Res'
    out_file_str += ('_%dk' % (MAX_EVT / 1000))
    out_file = R.TFile('plots/'+out_file_str+'.root','recreate')

    chains = {}
    chains['Evt'] = []  ## Event info
    chains['Vtx'] = []  ## RECO vertex info
    chains['Jet'] = []  ## RECO jet info
    chains['Unp'] = []  ## Unpacked Layer-2 info
    chains['Emu'] = []  ## Emulated Layer-2 info
    for i in range(len(in_file_names)):
        print 'Adding file %s' % in_file_names[i]
        chains['Evt'].append( R.TChain('l1EventTree/L1EventTree') )
        chains['Vtx'].append( R.TChain('l1RecoTree/RecoTree') )
        chains['Jet'].append( R.TChain('l1JetRecoTree/JetRecoTree') )
        chains['Unp'].append( R.TChain('l1UpgradeTree/L1UpgradeTree') )
        chains['Emu'].append( R.TChain('l1UpgradeEmuTree/L1UpgradeTree') )
        chains['Evt'][i].Add( in_file_names[i] )
        chains['Vtx'][i].Add( in_file_names[i] )
        chains['Jet'][i].Add( in_file_names[i] )
        chains['Unp'][i].Add( in_file_names[i] )
        chains['Emu'][i].Add( in_file_names[i] )


    ###################
    ### Book histograms
    ###################

    pt_bins  = [ 20,    0, 200]
    res_bins = [100, -1.5, 3.5]
    dR_bins  = [ 35,  0.0, 0.35]

    h_jet_den_unp = {}
    h_jet_den_emu = {}
    h_jet_num_unp = {}
    h_jet_num_emu = {}
    h_jet_res_unp = {}
    h_jet_res_emu = {}
    h_jet_res_unp = {}
    h_jet_res_emu = {}
    h_jet_dR_unp  = {}
    h_jet_dR_emu  = {}

    for iEta in ETA_CAT.keys():
        h_jet_den_unp[iEta] = {}
        h_jet_den_emu[iEta] = {}
        h_jet_num_unp[iEta] = {}
        h_jet_num_emu[iEta] = {}
        h_jet_res_unp[iEta] = {}
        h_jet_res_emu[iEta] = {}
        h_jet_dR_unp [iEta] = {}
        h_jet_dR_emu [iEta] = {}

        for iPt in PT_CAT.keys():
            h_jet_den_unp[iEta][iPt] = []
            h_jet_den_emu[iEta][iPt] = []
            h_jet_num_unp[iEta][iPt] = []
            h_jet_num_emu[iEta][iPt] = []
            h_jet_res_unp[iEta][iPt] = []
            h_jet_res_emu[iEta][iPt] = []
            h_jet_dR_unp [iEta][iPt] = []
            h_jet_dR_emu [iEta][iPt] = []

            ## Separate histogram for each input file (different TP reconstructions)
            for iTP in range(len(in_file_names)):

                h_jet_den_unp[iEta][iPt].append( R.TH1D( 'h_jet_den_%s_%s_%d_unp' % (iEta, iPt, iTP),
                                                         'L1T Unp jet p_{T} denominator in %s for %s' % (iEta, iPt),
                                                         pt_bins[0], pt_bins[1], pt_bins[2] ) )
                h_jet_den_emu[iEta][iPt].append( R.TH1D( 'h_jet_den_%s_%s_%d_emu' % (iEta, iPt, iTP),
                                                         'L1T Emu jet p_{T} denominator in %s for %s' % (iEta, iPt),
                                                         pt_bins[0], pt_bins[1], pt_bins[2] ) )

                h_jet_num_unp[iEta][iPt].append( R.TH1D( 'h_jet_num_%s_%s_%d_unp' % (iEta, iPt, iTP),
                                                         'L1T Unp jet p_{T} numerator in %s for %s' % (iEta, iPt),
                                                         pt_bins[0], pt_bins[1], pt_bins[2] ) )
                h_jet_num_emu[iEta][iPt].append( R.TH1D( 'h_jet_num_%s_%s_%d_emu' % (iEta, iPt, iTP),
                                                         'L1T Emu jet p_{T} numerator in %s for %s' % (iEta, iPt),
                                                         pt_bins[0], pt_bins[1], pt_bins[2] ) )

                h_jet_res_unp[iEta][iPt].append( R.TH1D( 'h_jet_res_%s_%s_%d_unp' % (iEta, iPt, iTP),
                                                         'L1T Unp jet p_{T} resolution in %s for %s' % (iEta, iPt),
                                                         res_bins[0], res_bins[1], res_bins[2] ) )
                h_jet_res_emu[iEta][iPt].append( R.TH1D( 'h_jet_res_%s_%s_%d_emu' % (iEta, iPt, iTP),
                                                         'L1T Emu jet p_{T} resolution in %s for %s' % (iEta, iPt),
                                                         res_bins[0], res_bins[1], res_bins[2] ) )

                h_jet_dR_unp[iEta][iPt].append( R.TH1D( 'h_jet_dR_%s_%s_%d_unp' % (iEta, iPt, iTP),
                                                        'dR(RECO, Unp L1T) jet in %s for %s' % (iEta, iPt),
                                                        dR_bins[0], dR_bins[1], dR_bins[2] ) )
                h_jet_dR_emu[iEta][iPt].append( R.TH1D( 'h_jet_dR_%s_%s_%d_emu' % (iEta, iPt, iTP),
                                                        'dR(RECO, Emu L1T) jet in %s for %s' % (iEta, iPt),
                                                        dR_bins[0], dR_bins[1], dR_bins[2] ) )

    iEvt = 0
    print '\nEntering loop over chains'
    for iCh in range(len(chains['Unp'])):

        if iEvt > MAX_EVT and MAX_EVT > 0: break

        ## Faster tecnhique, inspired by https://github.com/thomreis/l1tMuonTools/blob/master/L1Analysis.py
        Evt_br = R.L1Analysis.L1AnalysisEventDataFormat()
        Vtx_br = R.L1Analysis.L1AnalysisRecoVertexDataFormat()
        Jet_br = R.L1Analysis.L1AnalysisRecoJetDataFormat()
        Unp_br = R.L1Analysis.L1AnalysisL1UpgradeDataFormat()
        Emu_br = R.L1Analysis.L1AnalysisL1UpgradeDataFormat()

        chains['Evt'][iCh].SetBranchAddress('Event',     R.AddressOf(Evt_br))
        chains['Vtx'][iCh].SetBranchAddress('Vertex',    R.AddressOf(Vtx_br))
        chains['Jet'][iCh].SetBranchAddress('Jet',       R.AddressOf(Jet_br))
        chains['Unp'][iCh].SetBranchAddress('L1Upgrade', R.AddressOf(Unp_br))
        chains['Emu'][iCh].SetBranchAddress('L1Upgrade', R.AddressOf(Emu_br))

        print '\nEntering loop over events for chain %d' % iCh
        for jEvt in range(chains['Unp'][iCh].GetEntries()):

            iEvt += 1
            if iEvt > MAX_EVT and MAX_EVT > 0: break
            if iEvt % PRT_EVT is 0: print '\nEvent # %d (%dth in chain)' % (iEvt, jEvt+1)

            chains['Evt'][iCh].GetEntry(jEvt)
            chains['Vtx'][iCh].GetEntry(jEvt)
            chains['Jet'][iCh].GetEntry(jEvt)
            chains['Unp'][iCh].GetEntry(jEvt)
            chains['Emu'][iCh].GetEntry(jEvt)

            # ## Use these lines if you don't explicitly define the DataFormat and then do SetBranchAddress above
            # Evt_br = chains['Evt'][iCh].Event
            # Vtx_br = chains['Vtx'][iCh].Vertex
            # Jet_br = chains['Jet'][iCh].Vertex
            # Unp_br = chains['Unp'][iCh].L1Upgrade
            # Emu_br = chains['Emu'][iCh].L1Upgrade

            if iEvt % PRT_EVT is 0: print '  * Run %d, LS %d, event %d, nVtx %d' % (int(Evt_br.run), int(Evt_br.lumi), int(Evt_br.event), int(Vtx_br.nVtx))

            nOffJets = int(Jet_br.nJets)
            nUnpJets = int(Unp_br.nJets)
            nEmuJets = int(Emu_br.nJets)


            if VERBOSE:
                print 'Number of jets: RECO = %d, L1T Unpacked = %d, Emulated = %d' % (nOffJets, nUnpJets, nEmuJets)

            ## Create list of offfline RECO jets which are too close to other RECO jets
            bad_off_jets = []
            ## Loop over all offline RECO jets
            for iOff in range(nOffJets):
                iOff_vec = R.TLorentzVector()
                iOff_vec.SetPtEtaPhiM(Jet_br.et[iOff], Jet_br.eta[iOff], Jet_br.phi[iOff], 0)
                ## Loop over all offline RECO jets with higher pT
                for jOff in range(iOff):
                    jOff_vec = R.TLorentzVector()
                    jOff_vec.SetPtEtaPhiM(Jet_br.et[jOff], Jet_br.eta[jOff], Jet_br.phi[jOff], 0)

                    if iOff_vec.DeltaR(jOff_vec) < DR_MIN:
                        # print '\n  * Removing offline jet pT = %.1f, eta = %.2f, phi = %.2f' % (iOff_vec.Pt(), iOff_vec.Eta(), iOff_vec.Phi())
                        # print '  * Has dR = %.2f to jet pT = %.1f, eta = %.2f, phi = %.2f' % (iOff_vec.DeltaR(jOff_vec), jOff_vec.Pt(), jOff_vec.Eta(), jOff_vec.Phi())
                        bad_off_jets.append(iOff)
                        break

            ## Loop over all offline RECO jets
            for iOff in range(nOffJets):

                ## Remove offline jets which overlap other jets
                if iOff in bad_off_jets: continue
                
                vOff = R.TLorentzVector()
                vOff.SetPtEtaPhiM(Jet_br.et[iOff], Jet_br.eta[iOff], Jet_br.phi[iOff], 0)

                ## Apply selection cut(s) to offline jet
                if vOff.Pt() < PT_MIN: continue

                ## Pick the |eta| and pT categories
                iEta = 'None'
                for iCat in ETA_CAT.keys():
                    if iCat == 'HBEF': continue
                    if abs(vOff.Eta()) > ETA_CAT[iCat][0] and abs(vOff.Eta()) < ETA_CAT[iCat][1]:
                        iEta = iCat
                if iEta == 'None' or iEta == 'HBEF':
                    print '\n\nSUPER-BIZZARE JET THAT FALLS INTO NO ETA CATEGORIES!!!  eta = %.3f\n\n' % vOff.Eta()
                    continue

                iPt = 'None'
                for iCat in PT_CAT.keys():
                    if vOff.Pt() > PT_CAT[iCat][0] and vOff.Pt() < PT_CAT[iCat][2]:
                        iPt = iCat
                if iPt == 'None':
                    if vOff.Pt() > PT_CAT['lowPt'][0] and vOff.Pt() < PT_CAT['hiPt'][2]:
                        print '\n\nSUPER-BIZZARE JET THAT FALLS INTO NO PT CATEGORIES!!!  pT = %.3f\n\n' % vOff.Pt()
                    continue

                ## Find highest-pT Level-1 jet with good dR matching to unpacked jet
                max_pt_unp = -99
                max_pt_emu = -99
                vMaxUnp = R.TLorentzVector()
                vMaxEmu = R.TLorentzVector()

                ## Loop over all L1T unpacked jets
                for iUnp in range(nUnpJets):

                    vUnp = R.TLorentzVector()
                    vUnp.SetPtEtaPhiM(Unp_br.jetEt[iUnp], Unp_br.jetEta[iUnp], Unp_br.jetPhi[iUnp], 0)

                    if vUnp.DeltaR(vOff) < DR_MAX and vUnp.Pt() > max_pt_unp:
                        max_pt_unp = vUnp.Pt()
                        vMaxUnp = vUnp
                ## End loop: for iUnp in range(nUnpJets)

                ## Loop over all L1T emulated jets
                for iEmu in range(nEmuJets):

                    vEmu = R.TLorentzVector()
                    vEmu.SetPtEtaPhiM(Emu_br.jetEt[iEmu], Emu_br.jetEta[iEmu], Emu_br.jetPhi[iEmu], 0)

                    if vEmu.DeltaR(vOff) < DR_MAX and vEmu.Pt() > max_pt_emu:
                        max_pt_emu = vEmu.Pt()
                        vMaxEmu = vEmu
                ## End loop: for iEmu in range(nEmuJets)


                ## Re-set the |eta| categories based on emulated and unpacked L1T jet eta, if there is a match
                unpEta = 'None'
                emuEta = 'None'
                if max_pt_unp > 0:
                    for iCat in ETA_CAT.keys():
                        if abs(vMaxUnp.Eta()) > ETA_CAT[iCat][0] and abs(vMaxUnp.Eta()) < ETA_CAT[iCat][1]:
                            unpEta = iCat
                else:       unpEta = iEta
                if max_pt_emu > 0:
                    for iCat in ETA_CAT.keys():
                        if abs(vMaxEmu.Eta()) > ETA_CAT[iCat][0] and abs(vMaxEmu.Eta()) < ETA_CAT[iCat][1]:
                            emuEta = iCat
                else:       emuEta = iEta
                if unpEta == 'None' or emuEta == 'None':
                    print '\n\nSUPER-BIZZARE JET THAT FALLS INTO NO ETA CATEGORIES!!!  eta_unp = %.3f, eta_emu = %.3f\n\n' % (vMaxUnp.Eta(), vMaxEmu.Eta())
                    continue
                # if unpEta != iEta:
                #     print '  * L1T jet (eta = %.3f) not in same category as RECO jet (eta = %.3f)' % (vMaxUnp.Eta(), vOff.Eta())


                for jPt in PT_CAT.keys():
                    h_jet_den_unp[unpEta][jPt][iCh].Fill( vOff.Pt() )
                    h_jet_den_emu[emuEta][jPt][iCh].Fill( vOff.Pt() )
                    h_jet_den_unp['HBEF'][jPt][iCh].Fill( vOff.Pt() )
                    h_jet_den_emu['HBEF'][jPt][iCh].Fill( vOff.Pt() )
                    if vMaxUnp.Pt() > PT_CAT[jPt][1]:
                        h_jet_num_unp[unpEta][jPt][iCh].Fill( vOff.Pt() )
                        h_jet_num_unp['HBEF'][jPt][iCh].Fill( vOff.Pt() )
                    if vMaxEmu.Pt() > PT_CAT[jPt][1]:
                        h_jet_num_emu[emuEta][jPt][iCh].Fill( vOff.Pt() )
                        h_jet_num_emu['HBEF'][jPt][iCh].Fill( vOff.Pt() )

                if max_pt_unp > 0:
                    h_jet_res_unp[unpEta][iPt][iCh].Fill( (vMaxUnp.Pt() - vOff.Pt()) / vOff.Pt() )
                    h_jet_dR_unp [unpEta][iPt][iCh].Fill( vOff.DeltaR(vMaxUnp) )
                    h_jet_res_unp['HBEF'][iPt][iCh].Fill( (vMaxUnp.Pt() - vOff.Pt()) / vOff.Pt() )
                    h_jet_dR_unp ['HBEF'][iPt][iCh].Fill( vOff.DeltaR(vMaxUnp) )

                if max_pt_emu > 0:
                    h_jet_res_emu[emuEta][iPt][iCh].Fill( (vMaxEmu.Pt() - vOff.Pt()) / vOff.Pt() )
                    h_jet_dR_emu [emuEta][iPt][iCh].Fill( vOff.DeltaR(vMaxEmu) )
                    h_jet_res_emu['HBEF'][iPt][iCh].Fill( (vMaxEmu.Pt() - vOff.Pt()) / vOff.Pt() )
                    h_jet_dR_emu ['HBEF'][iPt][iCh].Fill( vOff.DeltaR(vMaxEmu) )

            ## End loop: for iOff in range(nOffJets):

        ## End loop: for jEvt in range(chains['Unp'][iCh].GetEntries()):
    ## End loop: for iCh in range(len(chains['Unp'])):

    print '\nFinished loop over chains'

    out_file.cd()

    colors = [R.kViolet, R.kBlue, R.kGreen, R.kRed]

    for iEta in ETA_CAT.keys():
        for iPt in PT_CAT.keys():
            for iTP in range(len(in_file_names)):

                h_jet_eff_unp = R.TEfficiency( h_jet_num_unp[iEta][iPt][iTP], h_jet_den_unp[iEta][iPt][iTP] )
                h_jet_eff_emu = R.TEfficiency( h_jet_num_emu[iEta][iPt][iTP], h_jet_den_emu[iEta][iPt][iTP] )
                h_jet_eff_unp.SetName( h_jet_num_unp[iEta][iPt][iTP].GetName().replace('num', 'eff') )
                h_jet_eff_emu.SetName( h_jet_num_emu[iEta][iPt][iTP].GetName().replace('num', 'eff') )

                h_jet_eff_unp                .SetLineWidth(2)
                h_jet_eff_emu                .SetLineWidth(2)
                h_jet_res_unp[iEta][iPt][iTP].SetLineWidth(2)
                h_jet_res_emu[iEta][iPt][iTP].SetLineWidth(2)
                h_jet_dR_unp [iEta][iPt][iTP].SetLineWidth(2)
                h_jet_dR_emu [iEta][iPt][iTP].SetLineWidth(2)

                h_jet_eff_unp                .SetLineColor(R.kBlack)
                h_jet_eff_emu                .SetLineColor(colors[iTP])
                h_jet_res_unp[iEta][iPt][iTP].SetLineColor(R.kBlack)
                h_jet_res_emu[iEta][iPt][iTP].SetLineColor(colors[iTP])
                h_jet_dR_unp [iEta][iPt][iTP].SetLineColor(R.kBlack)
                h_jet_dR_emu [iEta][iPt][iTP].SetLineColor(colors[iTP])

                h_jet_eff_unp                .Write()
                h_jet_eff_emu                .Write()
                h_jet_res_unp[iEta][iPt][iTP].Write()
                h_jet_res_emu[iEta][iPt][iTP].Write()
                h_jet_dR_unp [iEta][iPt][iTP].Write()
                h_jet_dR_emu [iEta][iPt][iTP].Write()

                del h_jet_eff_unp
                del h_jet_eff_emu
    
    out_file.Close()
    del chains

    print '\nWrote out file:  plots/'+out_file_str+'.root'


if __name__ == '__main__':
    main()

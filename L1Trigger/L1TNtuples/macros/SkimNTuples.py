#! /usr/bin/env python

## Skim NTuples based on nPV or other properties

import sys
import subprocess
import ROOT as R

def main():

    print '\nInside SkimNTuples\n'

    IDX = 0

    PRT_EVT  =       1000  ## Print every Nth event
    MAX_EVT  =    1000000  ## Number of events to process
    MIN_FILE =     IDX*2  ## Minimum input file index to process
    MAX_FILE = (IDX+1)*2  ## Maximum input file index to process
    MIN_PU = 50         ## Only save events with PU > XX

    in_file_names = []

    # Aaron_dir = '/eos/cms/store/group/dpg_trigger/comm_trigger/L1Trigger/bundocka/ZeroBias/zbMETa/181212_124635/0000/'
    # Aaron_dir = '/eos/cms/store/group/dpg_trigger/comm_trigger/L1Trigger/bundocka/ZeroBias/zbMETb/181212_124704/0000/'
    # Aaron_dir = '/eos/cms/store/group/dpg_trigger/comm_trigger/L1Trigger/bundocka/ZeroBias/zbMETc/181212_124734/0000/'
    # Aaron_dir = '/eos/cms/store/group/dpg_trigger/comm_trigger/L1Trigger/bundocka/ZeroBias/zbMETd/181212_124803/0000/'
    Aaron_dir = '/eos/cms/store/group/dpg_trigger/comm_trigger/L1Trigger/bundocka/ZeroBias/zbMETe/181212_124839/0000/'
    for f_name in  subprocess.check_output(['ls', Aaron_dir]).splitlines():
        if not ('.root') in f_name: continue
        in_file_names.append(Aaron_dir+f_name)    


    # out_file_str = 'plots/SkimNTuples_ZeroBias_PU_50'
    # out_file_str += ('_%dk.root' % (MAX_EVT / 1000))
    # out_file_str = '/eos/cms/store/group/dpg_trigger/comm_trigger/L1Trigger/bundocka/ZeroBias/zbMETa/L1Ntuple_Skim_PU50_%d.root' % IDX
    # out_file_str = '/eos/cms/store/group/dpg_trigger/comm_trigger/L1Trigger/bundocka/ZeroBias/zbMETb/L1Ntuple_Skim_PU50_%d.root' % IDX
    # out_file_str = '/eos/cms/store/group/dpg_trigger/comm_trigger/L1Trigger/bundocka/ZeroBias/zbMETc/L1Ntuple_Skim_PU50_%d.root' % IDX
    # out_file_str = '/eos/cms/store/group/dpg_trigger/comm_trigger/L1Trigger/bundocka/ZeroBias/zbMETd/L1Ntuple_Skim_PU50_%d.root' % IDX
    out_file_str = '/eos/cms/store/group/dpg_trigger/comm_trigger/L1Trigger/bundocka/ZeroBias/zbMETe/L1Ntuple_Skim_PU50_%d.root' % IDX
    out_file = R.TFile(out_file_str,'recreate')
    out_file.cd()


    chains = {}
    # chains['l1EventTree/L1EventTree']               = 0
    # chains['l1CaloTowerTree/L1CaloTowerTree']       = 0
    # chains['l1UpgradeTree/L1UpgradeTree']           = 0
    # # chains['l1uGTTree/L1uGTTree']  ## Data format no lonter available in L1Trigger/L1TNtuples
    # chains['l1CaloTowerEmuTree/L1CaloTowerTree']    = 0
    # chains['l1UpgradeEmuTree/L1UpgradeTree']        = 0
    chains['l1RecoTree/RecoTree']                   = 0
    # chains['l1JetRecoTree/JetRecoTree']             = 0
    # chains['l1MetFilterRecoTree/MetFilterRecoTree'] = 0
    # chains['l1ElectronRecoTree/ElectronRecoTree']   = 0
    # chains['l1TauRecoTree/TauRecoTree']             = 0

    out_trees = {}
    for key in chains.keys():
        out_trees[key] = 0
        dir1 = out_file.mkdir(key.split('/')[0])
        dir1.cd()
        dir1.mkdir(key.split('/')[1])

    for i in range(len(in_file_names)):
        if i < MIN_FILE or i >= MAX_FILE: continue
        print 'Adding file %s' % in_file_names[i]
        for key in chains.keys():
            if i == 0: chains[key] = R.TChain(key)
            chains[key].Add( in_file_names[i] )


    ## Faster tecnhique, inspired by https://github.com/thomreis/l1tMuonTools/blob/master/L1Analysis.py
    branches = {}
            
    # branches['CaloTP']           = R.L1Analysis.L1AnalysisCaloTPDataFormat()
    # branches['CaloTPEmu']        = R.L1Analysis.L1AnalysisCaloTPDataFormat()
    # branches['Event']            = R.L1Analysis.L1AnalysisEventDataFormat()
    # # branches['L1uGT']  ## Data format no lonter available in L1Trigger/L1TNtuples
    # branches['L1CaloTower']      = R.L1Analysis.L1AnalysisL1CaloTowerDataFormat()
    # branches['L1CaloTowerEmu']   = R.L1Analysis.L1AnalysisL1CaloTowerDataFormat()
    # branches['L1Upgrade']        = R.L1Analysis.L1AnalysisL1UpgradeDataFormat()
    # branches['L1UpgradeEmu']     = R.L1Analysis.L1AnalysisL1UpgradeDataFormat()
    # branches['L1CaloClusterEmu'] = R.L1Analysis.L1AnalysisL1CaloClusterDataFormat()
    # branches['Electron']         = R.L1Analysis.L1AnalysisRecoElectronDataFormat()
    # branches['Jet']              = R.L1Analysis.L1AnalysisRecoJetDataFormat()
    # branches['Sums']             = R.L1Analysis.L1AnalysisRecoMetDataFormat()
    # branches['MetFilters']       = R.L1Analysis.L1AnalysisRecoMetFilterDataFormat()
    # branches['Tau']              = R.L1Analysis.L1AnalysisRecoTauDataFormat()
    branches['Vertex']           = R.L1Analysis.L1AnalysisRecoVertexDataFormat()
    
    # ## Unused branches
    # branches[''] = R.L1Analysis.L1AnalysisBMTFInputsDataFormat()
    # branches[''] = R.L1Analysis.L1AnalysisBMTFOutputDataFormat()
    # branches[''] = R.L1Analysis.L1AnalysisCSCTFDataFormat()
    # branches[''] = R.L1Analysis.L1AnalysisDTTFDataFormat()
    # branches[''] = R.L1Analysis.L1AnalysisGCTDataFormat()
    # branches[''] = R.L1Analysis.L1AnalysisGMTDataFormat()
    # branches[''] = R.L1Analysis.L1AnalysisGTDataFormat()
    # branches[''] = R.L1Analysis.L1AnalysisGeneratorDataFormat()
    # branches[''] = R.L1Analysis.L1AnalysisL1ExtraDataFormat()
    # branches[''] = R.L1Analysis.L1AnalysisL1HODataFormat()
    # branches[''] = R.L1Analysis.L1AnalysisL1MenuDataFormat()
    # branches[''] = R.L1Analysis.L1AnalysisL1UpgradeTfMuonDataFormat()
    # branches[''] = R.L1Analysis.L1AnalysisRCTDataFormat()
    # branches[''] = R.L1Analysis.L1AnalysisRecoClusterDataFormat()
    # branches[''] = R.L1Analysis.L1AnalysisRecoMuon2DataFormat()
    # branches[''] = R.L1Analysis.L1AnalysisRecoMuonDataFormat()
    # branches[''] = R.L1Analysis.L1AnalysisRecoRpcHitDataFormat()
    # branches[''] = R.L1Analysis.L1AnalysisRecoTrackDataFormat()
    # branches[''] = R.L1Analysis.L1AnalysisSimulationDataFormat()
    

    nPass = 0
    print '\nEntering loop over chains'

    for iTree in chains.keys():
        for branch in chains[iTree].GetListOfBranches():
            iBr = branch.GetName()
            print 'Tree %s has branch %s' % (iTree, iBr)
            if 'EmuTree' in iTree:
                chains[iTree].SetBranchAddress( iBr, R.AddressOf(branches[iBr+'Emu']) )
            else:
                chains[iTree].SetBranchAddress( iBr, R.AddressOf(branches[iBr]) )
                    
        out_file.cd(iTree)
        out_trees[iTree] = chains[iTree].CloneTree(0)

    nEntries = chains['l1RecoTree/RecoTree'].GetEntries()
    print '\nEntering loop over %d events\n' % (nEntries)
    for iEvt in range(nEntries):

        chains['l1RecoTree/RecoTree'].GetEntry(iEvt)

        if int(branches['Vertex'].nVtx) < MIN_PU: continue

        for iTree in chains.keys():
            if not iTree == 'l1RecoTree/RecoTree':
                chains[iTree].GetEntry(iEvt)
                

        if nPass % PRT_EVT is 0: print 'Event # %dk (%dth in chain) with PU = %d' % (nPass/1000, iEvt, int(branches['Vertex'].nVtx))
        nPass += 1
        if nPass > MAX_EVT: break

        for iTree in chains.keys():
            out_trees[iTree].Fill()
                
    ## End loop: for iEvt in range(nEntries):

    print '\nFinished loop over chains'

    # for iTree in chains.keys():
        # out_trees[iTree].AutoSave()
        
    print '\nSaved trees to output file %s\n' % out_file_str

    out_file.Write()
    out_file.Close()


if __name__ == '__main__':
    main()

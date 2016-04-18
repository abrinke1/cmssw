## 11.02.16: Copied from https://raw.githubusercontent.com/dcurry09/EMTF8/master/L1Trigger/L1TMuonEndCap/test/runMuonEndCap.py

# -*- coding: utf-8 -*-

import FWCore.ParameterSet.Config as cms
import os
import sys
import commands
from Configuration.StandardSequences.Eras import eras

process = cms.Process("L1TMuonEmulation")


# OLD process lits
#process.load("FWCore.MessageLogger.MessageLogger_cfi")
#process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
#process.load('Configuration.StandardSequences.L1Emulator_cff')
#process.load("Configuration.StandardSequences.RawToDigi_cff")
#process.load('Configuration/StandardSequences/EndOfProcess_cff')
#process.load('Configuration/EventContent/EventContent_cff')
#process.load("Configuration.StandardSequences.Generator_cff")
#process.load( "HLTrigger.HLTcore.triggerSummaryAnalyzerAOD_cfi" )
#process.load('Configuration.Geometry.GeometryExtended2015Reco_cff')
#process.load('Configuration.Geometry.GeometryExtended2015_cff')
#process.load('Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff')

# NEW process list
# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('Configuration.Geometry.GeometryExtended2016Reco_cff')
process.load('Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff')
process.load('Configuration.StandardSequences.RawToDigi_Data_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

# Muons
process.load("RecoMuon.TrackingTools.MuonServiceProxy_cff")
process.load("RecoMuon.TrackingTools.MuonTrackLoader_cff")

# Lumi JSON tools
import FWCore.PythonUtilities.LumiList as LumiList
#process.source.lumisToProcess = LumiList.LumiList(filename = 'goodList.json').getVLuminosityBlockRange()

# Message Logger and Event range
process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(100)
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(100) )
process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(False))

process.options = cms.untracked.PSet(
#    SkipEvent = cms.untracked.vstring('ProductNotFound')
)


# Input Source
process.source = cms.Source('PoolSource',
                            #eventsToProcess = cms.untracked.lumisToProcess(''),
                            fileNames = cms.untracked.vstring(
        
        # For efficiencies
        #'/store/data/Run2015D/SingleMuon/RAW-RECO/ZMu-PromptReco-v4/000/258/159/00000/0EFE474F-D26B-E511-9618-02163E011F4B.root',
        #'file:/afs/cern.ch/work/a/abrinke1/public/EMTF/Emulator/samples/ZMu-PromptReco-v4/0EFE474F-D26B-E511-9618-02163E011F4B.root',
        #'file:/afs/cern.ch/work/a/abrinke1/public/EMTF/Emulator/samples/ZMu-PromptReco-v4/267ACC62-DD6B-E511-92AD-02163E011F4B.root',
        #'file:/afs/cern.ch/work/a/abrinke1/public/EMTF/Emulator/samples/ZMu-PromptReco-v4/2E3BE2CD-E86B-E511-A777-02163E01211D.root',
        #'file:/afs/cern.ch/work/a/abrinke1/public/EMTF/Emulator/samples/ZMu-PromptReco-v4/58353698-B56B-E511-9FFD-02163E011F32.root',
        #'file:/afs/cern.ch/work/a/abrinke1/public/EMTF/Emulator/samples/ZMu-PromptReco-v4/68266258-D26B-E511-BE87-02163E014126.root',
        #'file:/afs/cern.ch/work/a/abrinke1/public/EMTF/Emulator/samples/ZMu-PromptReco-v4/745C2AB6-B56B-E511-B15A-02163E01297A.root',
        #'file:/afs/cern.ch/work/a/abrinke1/public/EMTF/Emulator/samples/ZMu-PromptReco-v4/90BBED7C-DD6B-E511-973F-02163E0146B8.root',
        #'file:/afs/cern.ch/work/a/abrinke1/public/EMTF/Emulator/samples/ZMu-PromptReco-v4/94E134E9-D26B-E511-A2C2-02163E0143F8.root',
        #'file:/afs/cern.ch/work/a/abrinke1/public/EMTF/Emulator/samples/ZMu-PromptReco-v4/A81C747E-D26B-E511-BC71-02163E011A97.root',
        #'file:/afs/cern.ch/work/a/abrinke1/public/EMTF/Emulator/samples/ZMu-PromptReco-v4/C697122A-BD6B-E511-8B30-02163E01397A.root',
        #'file:/afs/cern.ch/work/a/abrinke1/public/EMTF/Emulator/samples/ZMu-PromptReco-v4/D64E75BB-C56B-E511-975F-02163E0143E4.root',
        #'file:/afs/cern.ch/work/a/abrinke1/public/EMTF/Emulator/samples/ZMu-PromptReco-v4/F006B63A-246C-E511-A0DC-02163E011FE7.root',
        #'file:/afs/cern.ch/work/a/abrinke1/public/EMTF/Emulator/samples/ZMu-PromptReco-v4/FCCAA76B-D26B-E511-A660-02163E01348B.root'
        
        # for rate
        
        #'/store/data/Commissioning2016/MinimumBias/RAW/v1/000/267/996/00000/2CAD531C-93F5-E511-801F-02163E01240F.root'

        #'file:/afs/cern.ch/work/a/abrinke1/public/EMTF/MWGR/RAW/2016_03_09/266423/106D48F5-71E6-E511-B4B6-02163E012236.root'

        '/store/data/Commissioning2016/ZeroBias1/RAW/v1/000/269/224/00000/94AEE783-E7FF-E511-B6ED-02163E01447F.root'
        
        # for PU checks
        #'/store/group/dpg_trigger/comm_trigger/L1Trigger/L1Menu2016/Stage2/l1-tsg-v4/SingleMuon/crab_l1-tsg-v4__SingleMuon_ZMu/160314_132813/0000/'
        #'/store/data/Run2015D/ZeroBias/RAW/',
        #'/store/data/Run2015D/ZeroBias/RAW',
        #'/store/data/Run2015D/ZeroBias/RAW',
        #'/store/data/Run2015D/ZeroBias/RAW',
        #'/store/data/Run2015D/ZeroBias/RAW'


        )
	                    )

# Global Tags
#process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_data', '')
#process.GlobalTag = GlobalTag(process.GlobalTag, 'GR_P_V56', '')


####Event Setup Producer
process.load('L1Trigger.L1TMuonEndCap.fakeEmtfParams_cff')
process.esProd = cms.EDAnalyzer("EventSetupRecordDataGetter",
   toGet = cms.VPSet(
        ## Apparently L1TMuonEndcapParamsRcd doesn't exist in CondFormats/DataRecord/src/
        cms.PSet(record = cms.string('L1TMuonEndcapParamsRcd'),
                 data = cms.vstring('L1TMuonEndcapParams'))
        ),
   verbose = cms.untracked.bool(True)
)

process.content = cms.EDAnalyzer("EventContentAnalyzer")

####EMTF Emulator
process.load('L1Trigger.L1TMuonEndCap.simEmtfDigis_cfi')

process.dumpED = cms.EDAnalyzer("EventContentAnalyzer")
process.dumpES = cms.EDAnalyzer("PrintEventSetupContent")

process.L1TMuonSeq = cms.Sequence( 
      process.csctfDigis +
      #process.esProd +          
      process.simEmtfDigis 
    )


# Load the Ntuplizer
process.ntuple = cms.EDAnalyzer('CSCplusRPCTrackAnalyzer',
                                process.MuonServiceProxy,
                                muonsTag     = cms.InputTag("muons", ""),
                                genTag       = cms.InputTag("genParticles"),
                                csctfTag     = cms.InputTag("simEmtfDigis", "EMTF"),
                                leg_csctfTag = cms.InputTag("csctfDigis"),
                                cscTPTag     = cms.InputTag("csctfDigis"),
                                cscSegTag    = cms.InputTag("cscSegments"),
                                #leg_gmtTag   = cms.InputTag("gtDigis"),
                                printLevel   = cms.untracked.int32(3),
                                NoTagAndProbe= cms.untracked.bool(True),
                                isMC         = cms.untracked.int32(0),
                                outputDIR    = cms.string('TEST')
                                 ) 


# Output File
process.TFileService = cms.Service(
    "TFileService",
    fileName = cms.string("TEST_v1.root")
    #fileName = cms.string("root://eoscms//eos/cms/store/user/dcurry/EMTF/TEST_v1.root")
    #fileName = cms.string("root://eoscms//eos/cms/store/user/dcurry/EMTF/EMTF_MWGR_v3.root")
    )


process.L1TMuonPath = cms.Path(
    process.L1TMuonSeq
    + process.ntuple
    )

## Keep only a few outputs - AWB 11.02.16
outCommands=cms.untracked.vstring(                                                                                             
    'keep *EMTF*_*_*_*',
    'keep *_*EMTF*_*_*',
    'keep *_*_*EMTF*_*',
    'keep *_*_*_*EMTF*',
    'keep *csctf*_*_*_*',
    'keep *_*csctf*_*_*',
    'keep *_*_*csctf*_*',
    'keep *_*_*_*csctf*',
    'keep *Csctf*_*_*_*',
    'keep *_*Csctf*_*_*',
    'keep *_*_*Csctf*_*',
    'keep *_*_*_*Csctf*',
    'keep *CSCTF*_*_*_*',
    'keep *_*CSCTF*_*_*',
    'keep *_*_*CSCTF*_*',
    'keep *_*_*_*CSCTF*',
    'keep l1tMuonBXVector_*_*_*',
    'keep l1tRegionalMuonCandBXVector_*_*_*'
    )

#outCommands = cms.untracked.vstring('keep *')


process.out = cms.OutputModule("PoolOutputModule", 
                               fileName = cms.untracked.string("l1temtf_superprimitives1.root"),
                               outputCommands = outCommands
                               )

#process.output_step = cms.EndPath(process.out)

process.schedule = cms.Schedule(process.L1TMuonPath)

#process.schedule.extend([process.output_step])

from SLHCUpgradeSimulations.Configuration.muonCustoms import customise_csc_PostLS1
process = customise_csc_PostLS1(process)

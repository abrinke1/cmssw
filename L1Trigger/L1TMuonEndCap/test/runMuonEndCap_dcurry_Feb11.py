## 11.02.16: Copied from https://raw.githubusercontent.com/dcurry09/EMTF8/master/L1Trigger/L1TMuonEndCap/test/runMuonEndCap.py

# -*- coding: utf-8 -*-

import FWCore.ParameterSet.Config as cms
import os
import sys
import commands

process = cms.Process("L1TMuonEmulation")

process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.load('Configuration.StandardSequences.SimL1Emulator_cff')
process.load("Configuration.StandardSequences.RawToDigi_cff")
#process.load('Configuration.StandardSequences.L1Emulator_cff')
#process.load("Configuration.StandardSequences.RawToDigi_Data_cff")
process.load('Configuration/StandardSequences/EndOfProcess_cff')
process.load('Configuration/EventContent/EventContent_cff')
process.load("Configuration.StandardSequences.Generator_cff")
process.load("RecoMuon.TrackingTools.MuonServiceProxy_cff")
process.load("RecoMuon.TrackingTools.MuonTrackLoader_cff")
process.load( "HLTrigger.HLTcore.triggerSummaryAnalyzerAOD_cfi" )


# PostLS1 geometry used
process.load('Configuration.Geometry.GeometryExtended2015Reco_cff')
process.load('Configuration.Geometry.GeometryExtended2015_cff')

# Muons
process.load("RecoMuon.TrackingTools.MuonServiceProxy_cff")
process.load("RecoMuon.TrackingTools.MuonTrackLoader_cff")

# Message Logger and Event range
process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(100)
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(10000) )
process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(False))


# Input Source
process.source = cms.Source('PoolSource',
                            fileNames = cms.untracked.vstring(
        '/store/data/Run2015D/SingleMuon/RAW-RECO/ZMu-PromptReco-v4/000/258/159/00000/0EFE474F-D26B-E511-9618-02163E011F4B.root',
        #'/cms/data/store/data/Run2015D/ZeroBias/RAW/v1/000/259/721/00000/0A2BA199-5878-E511-B77E-02163E01190D.root',
        #'/cms/data/store/mc/Fall13dr/MuPlus_Pt-1to150_PositiveEndcap-gun/GEN-SIM-RAW/tsg_PU40bx25_POSTLS162_V2-v1/20000/04643A9D-F382-E311-9D3C-0017A4770C34.root'
        )
	                    )

# Global Tags
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')
from Configuration.AlCa.GlobalTag_condDBv2 import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'GR_P_V56', '')


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


#process.L1ReEmulSeq = cms.Sequence(
#    process.csctfDigis
#    )

####EMTF Emulator
process.load('L1Trigger.L1TMuonEndCap.simMuonEndCapDigis_cfi')

process.dumpED = cms.EDAnalyzer("EventContentAnalyzer")
process.dumpES = cms.EDAnalyzer("PrintEventSetupContent")

process.L1TMuonSeq = cms.Sequence( 
      process.csctfDigis +
      process.esProd +          
      process.simEmtfDigis 
    )


# ## Don't load the Ntuplizer: AWB 11.02.16
# # Load the Ntuplizer
# process.ntuple = cms.EDAnalyzer('CSCplusRPCTrackAnalyzer',
#                                 process.MuonServiceProxy,
#                                 muonsTag     = cms.InputTag("muons", ""),
#                                 genTag       = cms.InputTag("genParticles"),
#                                 csctfTag     = cms.InputTag("L1TMuonEndcapTrackFinder", "DataITC"),
#                                 leg_csctfTag = cms.InputTag("simcsctfDigis"),
#                                 cscTPTag     = cms.InputTag("csctfDigis"),
#                                 cscSegTag    = cms.InputTag("cscSegments"),
#                                 printLevel   = cms.untracked.int32(4),
#                                 isMC         = cms.untracked.int32(0),
#                                 outputDIR   = cms.string('TEST')
#                                 )


# Output File
process.TFileService = cms.Service(
    "TFileService",
    fileName = cms.string("TEST_EMTF.root")
    )


process.L1TMuonPath = cms.Path(
    process.L1TMuonSeq  ## Don't run the Ntuplizer - AWB 11.02.16
    # process.L1TMuonSeq +
    # process.ntuple
    )

## Keep only a few outputs - AWB 11.02.16
outCommands=cms.untracked.vstring(                                                                                             
    'keep l1tRegionalMuonCandBXVector_simEmtfDigis_EMTF_L1TMuonEmulation', 
    'keep cscL1TrackCSCDetIdCSCCorrelatedLCTDigiMuonDigiCollectionstdpairs_simCsctfTrackDigis__L1TMuonEmulation',
    'keep cscL1TrackCSCDetIdCSCCorrelatedLCTDigiMuonDigiCollectionstdpairs_csctfDigis__L1TMuonEmulation',               
    'keep recoMuons_muons__RECO',
    'keep *_*_EMTF_*',
    'keep *_*_*_EMTF',
    )

# outCommands = cms.untracked.vstring('keep *')


process.out = cms.OutputModule("PoolOutputModule", 
                               fileName = cms.untracked.string("l1temtf_superprimitives1.root"),
                               outputCommands = outCommands
                               )

process.output_step = cms.EndPath(process.out)
process.schedule = cms.Schedule(process.L1TMuonPath)
process.schedule.extend([process.output_step])

from SLHCUpgradeSimulations.Configuration.muonCustoms import customise_csc_PostLS1
process = customise_csc_PostLS1(process)

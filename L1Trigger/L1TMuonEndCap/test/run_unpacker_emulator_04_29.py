## 11.02.16: Copied from https://raw.githubusercontent.com/dcurry09/EMTF8/master/L1Trigger/L1TMuonEndCap/test/runMuonEndCap.py

import FWCore.ParameterSet.Config as cms
import os
import sys
import commands
from Configuration.StandardSequences.Eras import eras

process = cms.Process("L1TMuonEmulation")

## Import standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('Configuration.Geometry.GeometryExtended2016Reco_cff') ## Is this appropriate for 2015 data/MC? - AWB 18.04.16
process.load('Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff') ## Will this work on 0T data? - AWB 18.04.16
process.load('Configuration.StandardSequences.RawToDigi_Data_cff') ## Will this work for MC? - AWB 18.04.16
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

## Import RECO muon configurations
process.load("RecoMuon.TrackingTools.MuonServiceProxy_cff")
process.load("RecoMuon.TrackingTools.MuonTrackLoader_cff")

## Lumi JSON tools
import FWCore.PythonUtilities.LumiList as LumiList
# process.source.lumisToProcess = LumiList.LumiList(filename = 'goodList.json').getVLuminosityBlockRange()

## Message Logger and Event range
process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(100)
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(200) )
process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(False))

process.options = cms.untracked.PSet(
    # SkipEvent = cms.untracked.vstring('ProductNotFound')
)


## Input Source
process.source = cms.Source('PoolSource',
                            # eventsToProcess = cms.untracked.lumisToProcess(''),
                            fileNames = cms.untracked.vstring(
        
        ## 2016 data for FW-emulator comparison
        ## eos ls /eos/cms/tier0/store/data/Run2016B/ZeroBias1/RAW/v1/000/272/011/00000/
        '/store/data/Run2016B/ZeroBias1/RAW/v1/000/272/011/00000/325A344A-870D-E611-ABE1-02163E01420A.root'
        
        # ## eos ls /store/user/abrinke1/EMTF/Commissioning2016/
        # '/store/user/abrinke1/EMTF/Commissioning2016/2016_04_20/RAW/ZeroBias1/270389/004496D5-A706-E611-93B6-02163E0144F0.root'
        
        ## 2015 data for efficiency studies
        #'/store/data/Run2015D/SingleMuon/RAW-RECO/ZMu-PromptReco-v4/000/258/159/00000/0EFE474F-D26B-E511-9618-02163E011F4B.root',
        #'file:/afs/cern.ch/work/a/abrinke1/public/EMTF/Emulator/samples/ZMu-PromptReco-v4/0EFE474F-D26B-E511-9618-02163E011F4B.root',
        #'file:/afs/cern.ch/work/a/abrinke1/public/EMTF/Emulator/samples/ZMu-PromptReco-v4/267ACC62-DD6B-E511-92AD-02163E011F4B.root',
        
        # ## 2015 data for rate studies
        #'/store/data/Run2015D/ZeroBias/RAW/',
        #'/store/data/Run2015D/ZeroBias/RAW',
        #'/store/data/Run2015D/ZeroBias/RAW',
        #'/store/data/Run2015D/ZeroBias/RAW',
        #'/store/data/Run2015D/ZeroBias/RAW'
        
        )
	                    )

## Global Tags
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_data', '') ## Good for 2015/2016 data/MC? - AWB 18.04.16
# process.GlobalTag = GlobalTag(process.GlobalTag, 'GR_P_V56', '') ## Used for anything? - AWB 18.04.16

## Event Setup Producer
process.load('L1Trigger.L1TMuonEndCap.fakeEmtfParams_cff') ## Why does this file have "fake" in the name? - AWB 18.04.16
process.esProd = cms.EDAnalyzer("EventSetupRecordDataGetter",
                                toGet = cms.VPSet(
        ## Apparently L1TMuonEndcapParamsRcd doesn't exist in CondFormats/DataRecord/src/ (Important? - AWB 18.04.16)
        cms.PSet(record = cms.string('L1TMuonEndcapParamsRcd'),
                 data = cms.vstring('L1TMuonEndcapParams'))
        ),
                                verbose = cms.untracked.bool(True)
                                )

process.content = cms.EDAnalyzer("EventContentAnalyzer")

## EMTF Emulator
process.load('EventFilter.L1TRawToDigi.emtfStage2Digis_cfi')
process.load('L1Trigger.L1TMuonEndCap.simEmtfDigis_cfi') 
process.simEmtfDigis.CSCInput = cms.InputTag('emtfStage2Digis') ## Can also use ('csctfDigis') or ('simCscTriggerPrimitiveDigis', 'MPCSORTED')

process.dumpED = cms.EDAnalyzer("EventContentAnalyzer")
process.dumpES = cms.EDAnalyzer("PrintEventSetupContent")


process.L1TMuonSeq = cms.Sequence(
    process.csctfDigis + ## Necessary for legacy studies, or if you use csctfDigis as input
    ## process.esProd + ## What do we loose by not having this? - AWB 18.04.16
    process.emtfStage2Digis +
    process.simEmtfDigis 
    )

process.L1TMuonPath = cms.Path(
    process.L1TMuonSeq
    )

# outCommands = cms.untracked.vstring('keep *')
outCommands = cms.untracked.vstring(
    'keep *EMTF*_*_*_*',
    'keep *_*_*EMTF*_*',
    'keep *_*csctf*_*_*',
    'keep l1tMuonBXVector_*_*_*',
    'keep l1tRegionalMuonCandBXVector_*_*_*'
    )


process.out = cms.OutputModule("PoolOutputModule", 
                               fileName = cms.untracked.string("l1temtf_unpacker_emulator_04_22.root"),
                               outputCommands = outCommands
                               )

process.output_step = cms.EndPath(process.out)

process.schedule = cms.Schedule(process.L1TMuonPath)

process.schedule.extend([process.output_step])

## What does this do? Necessary? - AWB 29.04.16
from SLHCUpgradeSimulations.Configuration.muonCustoms import customise_csc_PostLS1
process = customise_csc_PostLS1(process)

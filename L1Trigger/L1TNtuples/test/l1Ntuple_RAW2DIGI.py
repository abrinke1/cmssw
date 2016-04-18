# Auto generated configuration file
# using: 
# Revision: 1.19 
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v 
# with command line options: l1Ntuple -s RAW2DIGI --era=Run2_2016 --geometry=Extended2016,Extended2016Reco --customise=L1Trigger/Configuration/customiseReEmul.L1TEventSetupForHF1x1TPs --customise=L1Trigger/Configuration/customiseReEmul.L1TReEmulFromRAW --customise=L1Trigger/L1TNtuples/customiseL1Ntuple.L1NtupleEMU --customise=L1Trigger/Configuration/customiseUtils.L1TTurnOffUnpackStage2GtGmtAndCalo --conditions=auto:run2_data -n 100 --data --no_exec
import FWCore.ParameterSet.Config as cms

from Configuration.StandardSequences.Eras import eras

process = cms.Process('RAW2DIGI',eras.Run2_2016)

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

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(100)
)


infiles = [

    ## eos ls /eos/cms/tier0/store/data/Commissioning2016/ZeroBias1/RAW/v1/000/269/224/00000/
    # '/store/data/Commissioning2016/ZeroBias1/RAW/v1/000/269/224/00000/14D05088-E7FF-E511-A237-02163E0119DB.root',
    # '/store/data/Commissioning2016/ZeroBias1/RAW/v1/000/269/224/00000/1C108881-E7FF-E511-8943-02163E012381.root',
    # '/store/data/Commissioning2016/ZeroBias1/RAW/v1/000/269/224/00000/1C113074-E7FF-E511-9A87-02163E01411D.root',
    # '/store/data/Commissioning2016/ZeroBias1/RAW/v1/000/269/224/00000/3AF21C28-E8FF-E511-8923-02163E0146DB.root',
    # '/store/data/Commissioning2016/ZeroBias1/RAW/v1/000/269/224/00000/7A691281-E7FF-E511-AB15-02163E013922.root',
    '/store/data/Commissioning2016/ZeroBias1/RAW/v1/000/269/224/00000/94AEE783-E7FF-E511-B6ED-02163E01447F.root'
    ]




# Input source
# Input source
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(infiles), ## Modified to point to MWGR data - AWB 03.28.16
    secondaryFileNames = cms.untracked.vstring()
)
process.options = cms.untracked.PSet(

)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    annotation = cms.untracked.string('l1Ntuple nevts:100'),
    name = cms.untracked.string('Applications'),
    version = cms.untracked.string('$Revision: 1.19 $')
)

# Output definition

process.RECOSIMoutput = cms.OutputModule("PoolOutputModule",
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string(''),
        filterName = cms.untracked.string('')
    ),
    eventAutoFlushCompressedSize = cms.untracked.int32(5242880),
                                         
    fileName = cms.untracked.string('l1Ntuple_RAW2DIGI.root'),
    #fileName = cms.untracked.string("root://eoscms//eos/cms/store/user/dcurry/EMTF_L1T/ZeroBias_csctfDigis_v1.root"),                                     
                                         
    outputCommands = cms.untracked.vstring(
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
        'keep l1tRegionalMuonCandBXVector_*_*_*',
        ), ## Only keep muon output

    # outputCommands = process.RECOSIMEventContent.outputCommands,
   splitLevel = cms.untracked.int32(0)
)

# Additional output definition

# Other statements
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_data', '')

# Path and EndPath definitions
process.raw2digi_step = cms.Path(process.RawToDigi)
process.endjob_step = cms.EndPath(process.endOfProcess)
process.RECOSIMoutput_step = cms.EndPath(process.RECOSIMoutput)

# Schedule definition
process.schedule = cms.Schedule(process.raw2digi_step,process.endjob_step,process.RECOSIMoutput_step)

# customisation of the process.

# Automatic addition of the customisation function from L1Trigger.Configuration.customiseReEmul
from L1Trigger.Configuration.customiseReEmul import L1TEventSetupForHF1x1TPs,L1TReEmulFromRAW 

#call to customisation function L1TEventSetupForHF1x1TPs imported from L1Trigger.Configuration.customiseReEmul
process = L1TEventSetupForHF1x1TPs(process)

#call to customisation function L1TReEmulFromRAW imported from L1Trigger.Configuration.customiseReEmul
process = L1TReEmulFromRAW(process)

# Automatic addition of the customisation function from L1Trigger.L1TNtuples.customiseL1Ntuple
from L1Trigger.L1TNtuples.customiseL1Ntuple import L1NtupleEMU 

#call to customisation function L1NtupleEMU imported from L1Trigger.L1TNtuples.customiseL1Ntuple
process = L1NtupleEMU(process)

# Automatic addition of the customisation function from L1Trigger.Configuration.customiseUtils
from L1Trigger.Configuration.customiseUtils import L1TTurnOffUnpackStage2GtGmtAndCalo 

#call to customisation function L1TTurnOffUnpackStage2GtGmtAndCalo imported from L1Trigger.Configuration.customiseUtils
process = L1TTurnOffUnpackStage2GtGmtAndCalo(process)

# End of customisation functions


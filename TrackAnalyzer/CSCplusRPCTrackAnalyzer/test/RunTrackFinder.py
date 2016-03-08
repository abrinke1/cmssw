import FWCore.ParameterSet.Config as cms

process = cms.Process('L1EMTF')

process.load("FWCore.MessageService.MessageLogger_cfi")
process.load("L1TriggerConfig.L1ScalesProducers.L1MuTriggerScalesConfig_cff")
process.load("L1TriggerConfig.L1ScalesProducers.L1MuTriggerPtScaleConfig_cff")
process.load('Configuration.StandardSequences.SimL1Emulator_cff')
#process.load("Configuration.StandardSequences.L1Emulator_cff")
#process.load("Configuration.StandardSequences.RawToDigi_Data_cff")
process.load("Configuration.StandardSequences.RawToDigi_cff")
process.load('Configuration.Geometry.GeometryExtended2015Reco_cff')
process.load('Configuration.Geometry.GeometryExtended2015_cff')
process.load("Configuration.StandardSequences.Generator_cff")


process.load('Configuration/StandardSequences/EndOfProcess_cff')
process.load('Configuration/EventContent/EventContent_cff')


process.load("RecoMuon.TrackingTools.MuonServiceProxy_cff")
process.load("RecoMuon.TrackingTools.MuonTrackLoader_cff")

process.load( "HLTrigger.HLTcore.triggerSummaryAnalyzerAOD_cfi" )

process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')
from Configuration.AlCa.GlobalTag_condDBv2 import GlobalTag

# for MC 
#process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_mc', '')
# for Data
process.GlobalTag.globaltag ='GR_P_V56'

process.options = cms.untracked.PSet(
    SkipEvent = cms.untracked.vstring('ProductNotFound'),
    wantSummary = cms.untracked.bool(True)
    )

process.MessageLogger.cerr.FwkReport.reportEvery = 1
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(10))

process.content = cms.EDAnalyzer("EventContentAnalyzer")


# Load the Ntuplizer
process.ntuple = cms.EDAnalyzer('CSCplusRPCTrackAnalyzer',
                                muonsTag     = cms.InputTag("muons"),
                                genTag       = cms.InputTag("genParticles"),
                                csctfTag     = cms.InputTag("L1TMuonEndcapTrackFinder", "DataITC"),
                                RPC_csctfTag = cms.InputTag("L1TMuonEndcapTrackFinder", "DataITCrpc"),
                                leg_csctfTag = cms.InputTag("simCsctfTrackDigis"),
                                #leg_csctfTag = cms.InputTag("csctfDigis"),
                                cscTPTag     = cms.InputTag("L1TMuonTriggerPrimitives","CSC"),
                                rpcTPTag     = cms.InputTag("L1TMuonTriggerPrimitives","RPC"),
                                cscSegTag    = cms.InputTag("cscSegments"),
                                printLevel   = cms.untracked.int32(-1),
                                isMC         = cms.untracked.int32(-1),
                                outputDIR   = cms.string('TEST')
                                )

# For debugging
process.ntuple.verbose = cms.untracked.bool(True)


readFiles = cms.untracked.vstring()
secFiles  = cms.untracked.vstring()
process.source = cms.Source(
    'PoolSource',
    fileNames = readFiles,
    secondaryFileNames= secFiles
    #, eventsToProcess = cms.untracked.VEventRange('201196:265380261')
    )

readFiles.extend([
        'root://eoscms//eos/cms/store/data/Run2015B/SingleMuon/RECO/PromptReco-v1/000/251/168/00000/360D09C5-C726-E511-8DD4-02163E01194E.root'
        ])

secFiles.extend([
        'root://eoscms//eos/cms/store/data/Run2015B/SingleMuon/RAW/v1/000/251/168/00000/382EE8DB-2825-E511-B3E0-02163E013597.root'
        ])


# Output File
process.TFileService = cms.Service(
    "TFileService",
    fileName = cms.string("TEST_EMTF.root")
    )

outCommands = cms.untracked.vstring('keep *')

# For debugging
process.FEVTDEBUGoutput = cms.OutputModule(
    "PoolOutputModule",
    splitLevel = cms.untracked.int32(0),
    eventAutoFlushCompressedSize = cms.untracked.int32(5242880),
    outputCommands = outCommands,
    fileName = cms.untracked.string('Emulator_EDM_Out.root'),
    dataset = cms.untracked.PSet(
        filterName = cms.untracked.string(''),
        dataTier = cms.untracked.string('')
    )
)


process.L1TMuonSequence = cms.Sequence(
    process.csctfDigis +
    process.SimL1Emulator +
    process.ntuple
    )

process.L1TMuonPath = cms.Path(process.L1TMuonSequence)

process.outPath = cms.EndPath(process.FEVTDEBUGoutput)

process.schedule = cms.Schedule(process.L1TMuonPath)

#process.schedule.extend([process.outPath])

import FWCore.ParameterSet.Config as cms

process = cms.Process('L1EMTFtuple')
process.load("FWCore.MessageService.MessageLogger_cfi")
process.SimpleMemoryCheck = cms.Service("SimpleMemoryCheck",ignoreTotal = cms.untracked.int32(1))
process.load("L1TriggerConfig.L1ScalesProducers.L1MuTriggerScalesConfig_cff")
process.load("L1TriggerConfig.L1ScalesProducers.L1MuTriggerPtScaleConfig_cff")
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.load('L1Trigger.L1TMuonTrackFinderEndCap.L1TMuonTriggerPrimitiveProducer_cfi')
#process.load('Configuration.Geometry.GeometryIdeal_cff')
process.load('Configuration.Geometry.GeometryExtended2015Reco_cff')
process.load('Configuration.Geometry.GeometryExtended2015_cff')

from Configuration.AlCa.GlobalTag import GlobalTag
# for MC
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_mc', '')
# for Data
#process.GlobalTag.globaltag ='GR_P_V56::All'

process.options = cms.untracked.PSet(
        SkipEvent = cms.untracked.vstring('ProductNotFound'),
            wantSummary = cms.untracked.bool(True)
        )


process.MessageLogger.cerr.FwkReport.reportEvery = 10
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(50))

process.content = cms.EDAnalyzer("EventContentAnalyzer")

process.ntuple = cms.EDAnalyzer('CSCplusRPCTrackAnalyzer',
                                muonsTag     = cms.InputTag("muons"),
                                genTag       = cms.InputTag("genParticles"),
                                csctfTag     = cms.InputTag("L1TMuonEndcapTrackFinder", "DataITC"),
                                cscTPTag     = cms.InputTag("L1TMuonTriggerPrimitives","CSC"),
                                rpcTPTag     = cms.InputTag("L1TMuonTriggerPrimitives","RPC"),
                                cscSegTag    = cms.InputTag("cscSegments"),
                                printLevel   = cms.untracked.int32(2),
                                isMC         = cms.untracked.int32(1),
                                outputDIR   = cms.string('TEST')
                                )

# For debugging
process.ntuple.verbose = cms.untracked.bool(True)

process.TFileService = cms.Service("TFileService", 
                                   fileName = cms.string("TEST.root"),
                                   closeFileFast = cms.untracked.bool(True)
                                   )

infile = [
    'file:Emulator_EDM_Out_CMSSW8_2015RAW.root'
    #'file:SingleMuLowPt_5GeVto200GeV_GEN_SIM_DIGI_L1.root'
    ]

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(infile)
    )

process.L1TMuonSequence = cms.Sequence(process.ntuple)

process.L1TMuonPath = cms.Path(process.L1TMuonSequence)

process.schedule = cms.Schedule(process.L1TMuonPath)

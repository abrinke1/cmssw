import FWCore.ParameterSet.Config as cms

process = cms.Process('L1EMTF')
process.load("FWCore.MessageService.MessageLogger_cfi")
#process.SimpleMemoryCheck = cms.Service("SimpleMemoryCheck",ignoreTotal = cms.untracked.int32(1))
process.load("L1TriggerConfig.L1ScalesProducers.L1MuTriggerScalesConfig_cff")
process.load("L1TriggerConfig.L1ScalesProducers.L1MuTriggerPtScaleConfig_cff")
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.load('L1Trigger.L1TMuonTrackFinderEndCap.L1TMuonTriggerPrimitiveProducer_cfi')
process.load("Configuration.StandardSequences.RawToDigi_Data_cff")
#process.load('Configuration.Geometry.GeometryIdeal_cff')
process.load('Configuration.Geometry.GeometryExtended2015Reco_cff')
process.load('Configuration.Geometry.GeometryExtended2015_cff')

from Configuration.AlCa.GlobalTag import GlobalTag
# for MC 
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_mc', '')
# for Data
##process.GlobalTag.globaltag ='GR_P_V56'

process.options = cms.untracked.PSet(
    SkipEvent = cms.untracked.vstring('ProductNotFound'),
    wantSummary = cms.untracked.bool(True)
)


process.MessageLogger.cerr.FwkReport.reportEvery = 1000
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1))

# Load the Emulator Track Producer
process.L1TMuonEndcapTrackFinder = cms.EDProducer('L1TMuonUpgradedTrackFinder',
                                                  primitiveSrcs = cms.VInputTag( 
        cms.InputTag('L1TMuonTriggerPrimitives','CSC'),
        cms.InputTag('L1TMuonTriggerPrimitives','DT'),
        cms.InputTag('L1TMuonTriggerPrimitives','RPC')
        ),
                                                  )

process.content = cms.EDAnalyzer("EventContentAnalyzer")


# Load the Ntuplizer
process.ntuple = cms.EDAnalyzer('CSCplusRPCTrackAnalyzer',
                                muonsTag     = cms.InputTag("muons"),
                                genTag       = cms.InputTag("genParticles"),
                                csctfTag     = cms.InputTag("L1TMuonEndcapTrackFinder", "DataITC"),
                                leg_csctfTag = cms.InputTag("simCsctfTrackDigis"),
                                cscTPTag     = cms.InputTag("L1TMuonTriggerPrimitives","CSC"),
                                rpcTPTag     = cms.InputTag("L1TMuonTriggerPrimitives","RPC"),
                                cscSegTag    = cms.InputTag("cscSegments"),
                                printLevel   = cms.untracked.int32(-1),
                                isMC         = cms.untracked.int32(1),
                                outputDIR   = cms.string('TEST')
                                )

# For debugging
process.ntuple.verbose = cms.untracked.bool(True)


infile = [

    'file:SingleMuLowPt_5GeVto200GeV_GEN_SIM_DIGI_L1.root'
#    'root://eoscms//eos/cms/store/data/Run2015B/SingleMuon/RAW/v1/000/251/168/00000/382EE8DB-2825-E511-B3E0-02163E013597.root'
    #'/store/mc/Fall13dr/MuPlus_Pt-1to20_NegativeEndcap-gun/GEN-SIM-RAW/tsg_PU20bx25_POSTLS162_V2-v1/00000/'
#    '/store/relval/CMSSW_7_5_0_pre1/RelValSingleMuPt100_UP15/GEN-SIM-DIGI-RECO/MCRUN2_74_V7_FastSim-v1/00000/04DB6E17-72E2-E411-8311-0025905964BA.root',
#    '/store/relval/CMSSW_7_5_0_pre1/RelValSingleMuPt100_UP15/GEN-SIM-DIGI-RECO/MCRUN2_74_V7_FastSim-v1/00000/24978F06-72E2-E411-8346-0025905A6084.root',
#    '/store/relval/CMSSW_7_5_0_pre1/RelValSingleMuPt100_UP15/GEN-SIM-DIGI-RECO/MCRUN2_74_V7_FastSim-v1/00000/469C811A-72E2-E411-B1EF-0025905A6118.root',
#    '/store/relval/CMSSW_7_5_0_pre1/RelValSingleMuPt100_UP15/GEN-SIM-DIGI-RECO/MCRUN2_74_V7_FastSim-v1/00000/AAD41A17-72E2-E411-A617-0025905A607E.root',
#    '/store/relval/CMSSW_7_5_0_pre1/RelValSingleMuPt100_UP15/GEN-SIM-DIGI-RECO/MCRUN2_74_V7_FastSim-v1/00000/C4F4E747-71E2-E411-8305-0026189438AB.root' 
 
   ]


process.source = cms.Source(
    'PoolSource',
    fileNames = cms.untracked.vstring(infile)
    )

# Output File
process.TFileService = cms.Service("TFileService",
                                   fileName = cms.string("TEST.root")
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
#    process.csctfDigis *
    process.L1TMuonTriggerPrimitives * 
    process.L1TMuonEndcapTrackFinder +
    process.ntuple
    )

process.L1TMuonPath = cms.Path(process.L1TMuonSequence)

process.outPath = cms.EndPath(process.FEVTDEBUGoutput)

process.schedule = cms.Schedule(process.L1TMuonPath, process.outPath)


## Initial script to convert from .dat files to root output with EDMCollections - AWB 29.01.16

import FWCore.ParameterSet.Config as cms

process = cms.Process("EMTF")
process.load("FWCore.MessageLogger.MessageLogger_cfi")

process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(1000)
process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(True))

infiles = [

    ## eos ls store/express/Commissioning2016/ExpressCosmics/FEVT/Express-v1/000/264/374/00000/ - MWGR #1, 10.02.16
    ## eos ls store/express/Commissioning2016/ExpressCosmics/FEVT/Express-v1/000/264/479/00000/ - MWGR #1, 11.02.16
    ## eos ls store/express/Commissioning2016/ExpressCosmics/FEVT/Express-v1/000/264/593/00000/ - MWGT #1, 12.02.16

    ## DAS: dataset=/*/Commissioning2016*/RAW
    ## DAS: dataset=/*/Commissioning2016*/FEVT

    'root://eoscms//store/express/Commissioning2016/ExpressCosmics/FEVT/Express-v1/000/264/593/00000/002BAC1F-EBD1-E511-A705-02163E0144B7.root',
    'root://eoscms//store/express/Commissioning2016/ExpressCosmics/FEVT/Express-v1/000/264/593/00000/004B8353-10D2-E511-B539-02163E0136DC.root',
    'root://eoscms//store/express/Commissioning2016/ExpressCosmics/FEVT/Express-v1/000/264/593/00000/00545D78-30D2-E511-8295-02163E013703.root',
    'root://eoscms//store/express/Commissioning2016/ExpressCosmics/FEVT/Express-v1/000/264/593/00000/00B9326E-0AD2-E511-8C9A-02163E0136F8.root',
]

fNames = cms.untracked.vstring('file:/afs/cern.ch/work/a/abrinke1/public/EMTF/miniDAQ/dat_dumps/2015_12_13/263758/run263758_ls0025_streamA_StorageManager.dat')


process.source = cms.Source(
    "PoolSource",
    # fileNames = fNames,
    fileNames = cms.untracked.vstring(infiles)
    )


# process.source = cms.Source(
#     "NewEventStreamFileReader",
#     # fileNames = fNames,
#     fileNames = cms.untracked.vstring(infiles),
#     skipEvents=cms.untracked.uint32(123)
# )

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(10000))

# PostLS1 geometry used
process.load('Configuration.Geometry.GeometryExtended2015Reco_cff')
process.load('Configuration.Geometry.GeometryExtended2015_cff')
############################
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')
from Configuration.AlCa.GlobalTag_condDBv2 import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_mc', '')

# ## Debug / error / warning message output
# process.MessageLogger = cms.Service(
#     "MessageLogger",
#     threshold  = cms.untracked.string('DEBUG'),
#     categories = cms.untracked.vstring('L1T'),
#     debugModules = cms.untracked.vstring('*'),
#     )


# Dump raw data of payload as text
process.dump = cms.EDAnalyzer( 
    "DumpFEDRawDataProduct",
    label = cms.untracked.string("rawDataCollector"),
    # feds = cms.untracked.vint32(1402,813),
    # feds = cms.untracked.vint32(1402),
    ## Dump payload as text
    dumpPayload = cms.untracked.bool ( True )
)

process.unpack = cms.EDProducer("L1TRawToDigi",
        Setup           = cms.string("stage2::EMTFSetup"),
        InputLabel      = cms.InputTag("rawDataCollector"),
        FedIds          = cms.vint32( 1384, 1385 ),
        FWId            = cms.uint32(0),
        debug = cms.untracked.bool(False), ## More debugging output
        MTF7 = cms.untracked.bool(True)
)


# process.out = cms.OutputModule("PoolOutputModule", 
#    outputCommands=cms.untracked.vstring(
#        'keep *_unpack_*_*',
#        'keep *_*_*_EMTF',
#        'keep *l1t*_*_*_*',
#        'keep recoMuons_muons__RECO',
#        'keep *_*osmic*_*_*',
#        'keep edmTriggerResults_*_*_*',
#        'keep *CSC*_*_*_*',
#        'keep *_*csc*_*_*',
#        'keep *_*_*csc*_*',
#    ),
#    fileName = cms.untracked.string("EMTF_RAWToRoot_v0.root")
# )

process.out = cms.OutputModule("PoolOutputModule", 
   outputCommands=cms.untracked.vstring(
       'keep *_unpack_*_*',
       'keep *_*_*_EMTF',
       'keep *l1t*_*_*_*',
       'keep recoMuons_muons__RECO',
       'keep *_*osmic*_*_*',
       'keep edmTriggerResults_*_*_*',
       'keep *CSC*_*_*_*',
       'keep *_*CSC*_*_*',
       'keep *_*_*CSC*_*',
       'keep *_*_*_*CSC*',
       'keep *Csc*_*_*_*',
       'keep *_*Csc*_*_*',
       'keep *_*_*Csc*_*',
       'keep *_*_*_*Csc*',
       'keep *csc*_*_*_*',
       'keep *_*csc*_*_*',
       'keep *_*_*csc*_*',
       'keep *_*_*_*csc*',
   ),
   fileName = cms.untracked.string("EMTF_RAWToRoot_v0.root")
)

## process.p = cms.Path(process.dump * process.unpack)
process.p = cms.Path(process.unpack)
process.end = cms.EndPath(process.out)

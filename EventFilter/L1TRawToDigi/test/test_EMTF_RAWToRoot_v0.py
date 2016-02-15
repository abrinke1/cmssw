## Initial script to convert from .dat files to root output with EDMCollections - AWB 29.01.16

import FWCore.ParameterSet.Config as cms

process = cms.Process("EMTF")
process.load("FWCore.MessageLogger.MessageLogger_cfi")

process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(100)
process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(True))

infiles = [

    ## eos ls /eos/cms/tier0/store/express/Commissioning2016/ExpressCosmics/FEVT/Express-v1/000/264/374/00000/ - MWGR #1, 10.02.16
    ## eos ls /eos/cms/tier0/store/express/Commissioning2016/ExpressCosmics/FEVT/Express-v1/000/264/479/00000/ - MWGR #1, 11.02.16
    ## eos ls /eos/cms/tier0/store/express/Commissioning2016/ExpressCosmics/FEVT/Express-v1/000/264/593/00000/ - MWGT #1, 12.02.16

    'root://eoscms//eos/cms/tier0/store/express/Commissioning2016/ExpressCosmics/FEVT/Express-v1/000/264/593/00000/002BAC1F-EBD1-E511-A705-02163E0144B7.root',
    'root://eoscms//eos/cms/tier0/store/express/Commissioning2016/ExpressCosmics/FEVT/Express-v1/000/264/593/00000/004B8353-10D2-E511-B539-02163E0136DC.root',
    'root://eoscms//eos/cms/tier0/store/express/Commissioning2016/ExpressCosmics/FEVT/Express-v1/000/264/593/00000/00545D78-30D2-E511-8295-02163E013703.root',
    'root://eoscms//eos/cms/tier0/store/express/Commissioning2016/ExpressCosmics/FEVT/Express-v1/000/264/593/00000/00B9326E-0AD2-E511-8C9A-02163E0136F8.root',
    'root://eoscms//eos/cms/tier0/store/express/Commissioning2016/ExpressCosmics/FEVT/Express-v1/000/264/593/00000/00E369CD-F4D1-E511-89EF-02163E01469D.root',

    # 'root://eoscms//eos/cms/tier0/store/express/Commissioning2016/ExpressCosmics/FEVT/Express-v1/000/264/479/00000/00506EEE-12D1-E511-BEF4-02163E011875.root',
    # 'root://eoscms//eos/cms/tier0/store/express/Commissioning2016/ExpressCosmics/FEVT/Express-v1/000/264/479/00000/02540E25-4AD1-E511-91D5-02163E011E70.root',
    # 'root://eoscms//eos/cms/tier0/store/express/Commissioning2016/ExpressCosmics/FEVT/Express-v1/000/264/479/00000/02CAA00F-2AD1-E511-923A-02163E01420C.root',
    # 'root://eoscms//eos/cms/tier0/store/express/Commissioning2016/ExpressCosmics/FEVT/Express-v1/000/264/479/00000/02D52A4F-55D1-E511-B66A-02163E014453.root',
    # 'root://eoscms//eos/cms/tier0/store/express/Commissioning2016/ExpressCosmics/FEVT/Express-v1/000/264/479/00000/04165790-45D1-E511-8DF4-02163E0144EB.root',

    # 'root://eoscms//eos/cms/tier0/store/express/Commissioning2016/ExpressCosmics/FEVT/Express-v1/000/264/374/00000/0096B0C7-5CD0-E511-9FFE-02163E012622.root',
    # 'root://eoscms//eos/cms/tier0/store/express/Commissioning2016/ExpressCosmics/FEVT/Express-v1/000/264/374/00000/00D85196-3CD0-E511-BFB4-02163E01472C.root',
    # 'root://eoscms//eos/cms/tier0/store/express/Commissioning2016/ExpressCosmics/FEVT/Express-v1/000/264/374/00000/02353427-97D0-E511-AC72-02163E01398E.root',
    # 'root://eoscms//eos/cms/tier0/store/express/Commissioning2016/ExpressCosmics/FEVT/Express-v1/000/264/374/00000/028EF0C4-7AD0-E511-9A9F-02163E01431B.root',
    # 'root://eoscms//eos/cms/tier0/store/express/Commissioning2016/ExpressCosmics/FEVT/Express-v1/000/264/374/00000/02FDE524-98D0-E511-84C5-02163E0118A5.root',

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


process.out = cms.OutputModule("PoolOutputModule", 
   outputCommands=cms.untracked.vstring(
       'keep *_unpack_*_*',
       'keep *_*_*_EMTF',
       'keep *l1t*_*_*_*',
       'keep recoMuons_muons__RECO',
       'keep *_*osmic*_*_*',
       'keep edmTriggerResults_*_*_*',
       'keep *CSC*_*_*_*',
       'keep *_*csc*_*_*',
       'keep *_*_*csc*_*',
   ),
   fileName = cms.untracked.string("EMTF_RAWToRoot_v0.root")
)

## process.p = cms.Path(process.dump * process.unpack)
process.p = cms.Path(process.unpack)
process.end = cms.EndPath(process.out)

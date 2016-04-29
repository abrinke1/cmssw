## Initial script to convert from .dat files to root output with EDMCollections - AWB 29.01.16

import FWCore.ParameterSet.Config as cms

process = cms.Process("EMTF")
process.load("FWCore.MessageLogger.MessageLogger_cfi")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(100000))
process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(100)
process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(True))

infiles = [

    ## DAS: dataset=/*/Commissioning2016*/RAW
    ## DAS: dataset=/*/Commissioning2016*/FEVT

    # ## 2016 data for FW-emulator comparison
    # ## eos ls /eos/cms/tier0/store/data/Commissioning2016/ZeroBias1/RAW/v1/000/270/389/00000/
    # '/store/data/Commissioning2016/ZeroBias1/RAW/v1/000/270/389/00000/004496D5-A706-E611-93B6-02163E0144F0.root'
    
    # eos ls /store/user/abrinke1/EMTF/Commissioning2016/
    '/store/user/abrinke1/EMTF/Commissioning2016/2016_04_20/RAW/ZeroBias1/270389/004496D5-A706-E611-93B6-02163E0144F0.root'

    ## eos ls /eos/cms/tier0/store/data/Run2016A/ZeroBias1/RAW/v1/000/271/084/00000/
    # '/store/data/Run2016A/ZeroBias1/RAW/v1/000/271/084/00000/0441FA0C-4509-E611-BFDC-02163E0145DC.root',
    # '/store/data/Run2016A/ZeroBias1/RAW/v1/000/271/084/00000/063E2EDA-4409-E611-8418-02163E01413C.root',
    # '/store/data/Run2016A/ZeroBias1/RAW/v1/000/271/084/00000/081DFBC9-3D09-E611-85A9-02163E0142CD.root',
    # '/store/data/Run2016A/ZeroBias1/RAW/v1/000/271/084/00000/0C9008C9-4609-E611-ABB9-02163E011D1F.root',
    # '/store/data/Run2016A/ZeroBias1/RAW/v1/000/271/084/00000/0EC2DCDB-4409-E611-A71F-02163E01183A.root',
    # '/store/data/Run2016A/ZeroBias1/RAW/v1/000/271/084/00000/0EFA26CC-4F09-E611-9E87-02163E013710.root',
    # '/store/data/Run2016A/ZeroBias1/RAW/v1/000/271/084/00000/107B09B7-4F09-E611-B8D2-02163E011DB6.root',
    # '/store/data/Run2016A/ZeroBias1/RAW/v1/000/271/084/00000/14AF66CC-4F09-E611-A796-02163E011D1E.root',
    # '/store/data/Run2016A/ZeroBias1/RAW/v1/000/271/084/00000/1853A2D5-4409-E611-9CAB-02163E0133C2.root',
    # '/store/data/Run2016A/ZeroBias1/RAW/v1/000/271/084/00000/1A3059DB-4409-E611-8526-02163E013745.root',
    # '/store/data/Run2016A/ZeroBias1/RAW/v1/000/271/084/00000/1E709C4D-3C09-E611-8058-02163E0133C2.root',
    # '/store/data/Run2016A/ZeroBias1/RAW/v1/000/271/084/00000/206DBBAD-4F09-E611-913A-02163E01190C.root',
    # '/store/data/Run2016A/ZeroBias1/RAW/v1/000/271/084/00000/20EE4C25-4809-E611-8D4C-02163E014598.root',
    # '/store/data/Run2016A/ZeroBias1/RAW/v1/000/271/084/00000/26107CC3-4309-E611-BD91-02163E013955.root',
    # '/store/data/Run2016A/ZeroBias1/RAW/v1/000/271/084/00000/28B6DF6F-4509-E611-8654-02163E01452B.root',
    # '/store/data/Run2016A/ZeroBias1/RAW/v1/000/271/084/00000/28FF3BD9-4F09-E611-80B7-02163E0133D0.root',
    # '/store/data/Run2016A/ZeroBias1/RAW/v1/000/271/084/00000/32686E0C-4509-E611-BFAD-02163E012489.root',
    # '/store/data/Run2016A/ZeroBias1/RAW/v1/000/271/084/00000/342FC7CC-4409-E611-85CB-02163E011CEE.root',
    # '/store/data/Run2016A/ZeroBias1/RAW/v1/000/271/084/00000/3A5ACBF6-4409-E611-8A49-02163E011F58.root',
    # '/store/data/Run2016A/ZeroBias1/RAW/v1/000/271/084/00000/3E0A3C3D-4309-E611-AEC5-02163E013843.root',
    # '/store/data/Run2016A/ZeroBias1/RAW/v1/000/271/084/00000/3ED77F4C-3C09-E611-A71F-02163E011A71.root',
    # '/store/data/Run2016A/ZeroBias1/RAW/v1/000/271/084/00000/4851A70B-4509-E611-B1FC-02163E01367D.root',
    # '/store/data/Run2016A/ZeroBias1/RAW/v1/000/271/084/00000/48BDECC2-4F09-E611-A731-02163E0146D7.root',
    # '/store/data/Run2016A/ZeroBias1/RAW/v1/000/271/084/00000/4EEF63D8-4409-E611-9AEA-02163E014255.root',
    # '/store/data/Run2016A/ZeroBias1/RAW/v1/000/271/084/00000/667547CE-4F09-E611-BD29-02163E01377D.root',
    # '/store/data/Run2016A/ZeroBias1/RAW/v1/000/271/084/00000/6889BDD8-4F09-E611-AABD-02163E0140E2.root',
    # '/store/data/Run2016A/ZeroBias1/RAW/v1/000/271/084/00000/6A1AD060-4509-E611-906F-02163E011C45.root',
    # '/store/data/Run2016A/ZeroBias1/RAW/v1/000/271/084/00000/70C643B8-4F09-E611-A5E0-02163E014771.root',
    # '/store/data/Run2016A/ZeroBias1/RAW/v1/000/271/084/00000/70E5EE59-4309-E611-8D1C-02163E01383A.root',
    # '/store/data/Run2016A/ZeroBias1/RAW/v1/000/271/084/00000/70F03632-4509-E611-BD20-02163E0135C0.root',
    # '/store/data/Run2016A/ZeroBias1/RAW/v1/000/271/084/00000/746C70A0-4509-E611-A48C-02163E0145EC.root',
    # '/store/data/Run2016A/ZeroBias1/RAW/v1/000/271/084/00000/747046CB-4F09-E611-BB92-02163E014377.root',
    # '/store/data/Run2016A/ZeroBias1/RAW/v1/000/271/084/00000/784461D3-4F09-E611-96F8-02163E01355D.root',
    # '/store/data/Run2016A/ZeroBias1/RAW/v1/000/271/084/00000/784F16B9-4F09-E611-B5FC-02163E0133B8.root',
    # '/store/data/Run2016A/ZeroBias1/RAW/v1/000/271/084/00000/7C28EFB7-4F09-E611-8B2E-02163E0145B3.root',
    # '/store/data/Run2016A/ZeroBias1/RAW/v1/000/271/084/00000/7C472A09-4509-E611-BD8C-02163E0144C3.root',
    # '/store/data/Run2016A/ZeroBias1/RAW/v1/000/271/084/00000/84E7DDD5-4409-E611-82EF-02163E014469.root',
    # '/store/data/Run2016A/ZeroBias1/RAW/v1/000/271/084/00000/868FE91A-4509-E611-95EA-02163E0144C1.root',
    # '/store/data/Run2016A/ZeroBias1/RAW/v1/000/271/084/00000/8C64FD12-4509-E611-9C5D-02163E014179.root',
    # '/store/data/Run2016A/ZeroBias1/RAW/v1/000/271/084/00000/92233421-4509-E611-AADC-02163E0137BB.root',
    # '/store/data/Run2016A/ZeroBias1/RAW/v1/000/271/084/00000/96BEF8F4-4409-E611-850C-02163E01387F.root',
    # '/store/data/Run2016A/ZeroBias1/RAW/v1/000/271/084/00000/980B234A-5309-E611-8270-02163E014406.root',
    # '/store/data/Run2016A/ZeroBias1/RAW/v1/000/271/084/00000/98203DFC-4409-E611-9F9B-02163E012259.root',
    # '/store/data/Run2016A/ZeroBias1/RAW/v1/000/271/084/00000/988E8649-4509-E611-AB8E-02163E0133CE.root',
    # '/store/data/Run2016A/ZeroBias1/RAW/v1/000/271/084/00000/9AE6990D-5009-E611-A32C-02163E0128EB.root',
    # '/store/data/Run2016A/ZeroBias1/RAW/v1/000/271/084/00000/9E768AAC-4F09-E611-955B-02163E01383A.root',
    # '/store/data/Run2016A/ZeroBias1/RAW/v1/000/271/084/00000/9ECEE8DD-4409-E611-BD86-02163E011A81.root',
    # '/store/data/Run2016A/ZeroBias1/RAW/v1/000/271/084/00000/AA0052FF-4409-E611-B654-02163E013841.root',
    # '/store/data/Run2016A/ZeroBias1/RAW/v1/000/271/084/00000/ACC5E548-3C09-E611-9EFD-02163E011DD6.root',
    # '/store/data/Run2016A/ZeroBias1/RAW/v1/000/271/084/00000/AEB94AEF-4409-E611-92B0-02163E0143A0.root',
    # '/store/data/Run2016A/ZeroBias1/RAW/v1/000/271/084/00000/B640990C-4509-E611-AC39-02163E0142CD.root',
    # '/store/data/Run2016A/ZeroBias1/RAW/v1/000/271/084/00000/BED50B96-3D09-E611-8D4C-02163E011F71.root',
    # '/store/data/Run2016A/ZeroBias1/RAW/v1/000/271/084/00000/C03A75FE-4F09-E611-A117-02163E0140F8.root',
    # '/store/data/Run2016A/ZeroBias1/RAW/v1/000/271/084/00000/C2BB4A06-4509-E611-920C-02163E013921.root',
    # '/store/data/Run2016A/ZeroBias1/RAW/v1/000/271/084/00000/C415959E-3D09-E611-89EF-02163E0134E0.root',
    # '/store/data/Run2016A/ZeroBias1/RAW/v1/000/271/084/00000/CA02DFB8-4F09-E611-940B-02163E01278D.root',
    # '/store/data/Run2016A/ZeroBias1/RAW/v1/000/271/084/00000/CC8594C4-4F09-E611-A1B4-02163E0123E8.root',
    # '/store/data/Run2016A/ZeroBias1/RAW/v1/000/271/084/00000/CEA3FAF7-4F09-E611-AEA1-02163E014410.root',
    # '/store/data/Run2016A/ZeroBias1/RAW/v1/000/271/084/00000/CEF463F8-4409-E611-82E2-02163E014238.root',
    # '/store/data/Run2016A/ZeroBias1/RAW/v1/000/271/084/00000/D2F291C2-4F09-E611-B236-02163E0138D8.root',
    # '/store/data/Run2016A/ZeroBias1/RAW/v1/000/271/084/00000/D81E0109-4509-E611-83B4-02163E0145DD.root',
    # '/store/data/Run2016A/ZeroBias1/RAW/v1/000/271/084/00000/D89BA906-4509-E611-8AAC-02163E01278D.root',
    # '/store/data/Run2016A/ZeroBias1/RAW/v1/000/271/084/00000/DC1F5B7C-4509-E611-8D6B-02163E0140F9.root',
    # '/store/data/Run2016A/ZeroBias1/RAW/v1/000/271/084/00000/FAAF6CEF-4409-E611-9EF8-02163E014338.root',
    # '/store/data/Run2016A/ZeroBias1/RAW/v1/000/271/084/00000/FC51E009-4509-E611-B802-02163E0139BA.root',


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
#     ## categories = cms.untracked.vstring('EMTF'),
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

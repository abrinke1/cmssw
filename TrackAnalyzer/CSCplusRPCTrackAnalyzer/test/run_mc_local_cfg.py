
import FWCore.ParameterSet.Config as cms

process = cms.Process("CSCplusRPCTrackAnalyzer")
#from TrackAnalyzer.CSCplusRPCTrackAnalyzer.CSCplusRPCTrackAnalyzer_cfi import *
process.load('TrackAnalyzer.CSCplusRPCTrackAnalyzer.CSCplusRPCTrackAnalyzer_cfi')
process.CSCplusRPCTrackAnalyzer.isMC = cms.bool(True)

process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 5000
process.options = cms.untracked.PSet( wantSummary = cms.untracked.bool(True),
                                        SkipEvent = cms.untracked.vstring('ProductNotFound')
                                        )



#load run conditions
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.load('Configuration.Geometry.GeometryIdeal_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')


# Global Tag to specify the "good" events to run over
#from Configuration.AlCa.GlobalTag import GlobalTag
#process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:mc', '')
# Global Tags
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag.globaltag = 'GR_P_V41::All'

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(5000) )

process.source = cms.Source("PoolSource",
    #duplicateCheckMode = cms.untracked.string('noDuplicateCheck'),
    fileNames = cms.untracked.vstring(
	'file:SingleMuLowPt_5GeVto200GeV_GEN_SIM_DIGI_L1.root'
#	'file:SingleMu_FlatPt2_100_V2.root'
#	'file:/mnt/3TB/rewang/rpc/MC_SingleMu_FlatPt2_100_GENSIM_DIGI_L1_0.root',
#	'file:/mnt/3TB/rewang/rpc/MC_SingleMu_FlatPt2_100_GENSIM_DIGI_L1_1.root',
#	'file:/mnt/3TB/rewang/rpc/MC_SingleMu_FlatPt2_100_GENSIM_DIGI_L1_2.root',
#	'file:/mnt/3TB/rewang/rpc/MC_SingleMu_FlatPt2_100_GENSIM_DIGI_L1_3.root',
#	'file:/mnt/3TB/rewang/rpc/MC_SingleMu_FlatPt2_100_GENSIM_DIGI_L1_4.root',
#	'file:/mnt/3TB/rewang/rpc/MC_SingleMu_FlatPt2_100_GENSIM_DIGI_L1_5.root',
#	'file:/mnt/3TB/rewang/rpc/MC_SingleMu_FlatPt2_100_GENSIM_DIGI_L1_6.root',
#	'file:/mnt/3TB/rewang/rpc/MC_SingleMu_FlatPt2_100_GENSIM_DIGI_L1_7.root',
#	'file:/mnt/3TB/rewang/rpc/MC_SingleMu_FlatPt2_100_GENSIM_DIGI_L1_8.root',
#	'file:/mnt/3TB/rewang/rpc/MC_SingleMu_FlatPt2_100_GENSIM_DIGI_L1_9.root',
    ),
)

process.TFileService = cms.Service("TFileService",
				   fileName = cms.string("output_Files_run_mc_local/TEST_allQ_output.root")
                                  )



# standard unpacking sequence
#process.load("Configuration.StandardSequences.RawToDigi_Data_cff")

#process.RawToDigi = cms.Sequence(process.csctfDigis
#                    )


process.load('L1TriggerDPGUpgrade.L1TMuon.L1TMuonTriggerPrimitiveProducer_cfi')
process.load('L1TriggerDPGUpgrade.L1TMuon.L1CSCTFTrackConverter_cfi')
process.load('L1TriggerDPGUpgrade.L1TMuon.L1DTTFTrackConverter_cfi')
process.load('L1TriggerDPGUpgrade.L1TMuon.L1RPCTFTrackConverter_cfi')

process.p = cms.Path(#process.RawToDigi *
                                   process.L1TMuonTriggerPrimitives *
                                   process.L1CSCTFTrackConverter    *
                                   process.L1DTTFTrackConverter     *
                                   process.L1RPCTFTrackConverters   *
			process.CSCplusRPCTrackAnalyzer)


### local run
process.CSCplusRPCTrackAnalyzer.verbose = cms.untracked.bool(False)

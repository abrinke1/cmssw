import FWCore.ParameterSet.Config as cms

###EMTF emulator configuration
simEmtfDigis = cms.EDProducer("L1TMuonEndCapTrackProducer",
                              ## CSCInput = cms.InputTag('simCscTriggerPrimitiveDigis','MPCSORTED')
                              ## CSCInput = cms.InputTag('simCscTriggerPrimitiveDigis','')
                              CSCInput = cms.InputTag('csctfDigis') ## Crucial fix? red herring? - AWB 04.04.16
                              )



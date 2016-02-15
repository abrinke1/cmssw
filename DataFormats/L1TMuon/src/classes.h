#include "DataFormats/Common/interface/Wrapper.h"
#include "DataFormats/Common/interface/RefToBase.h"

#include "DataFormats/L1TMuon/interface/MuonCaloSumFwd.h"
#include "DataFormats/L1TMuon/interface/MuonCaloSum.h"
#include "DataFormats/L1TMuon/interface/RegionalMuonCandFwd.h"
#include "DataFormats/L1TMuon/interface/RegionalMuonCand.h"
#include "DataFormats/L1TMuon/interface/EMTFOutput.h"
#include "DataFormats/L1TMuon/interface/EMTF/InternalTrack.h"
/* #include "DataFormats/L1TMuon/interface/MuonInternalTrack.h" */

namespace {
  struct dictionary {
    l1t::MuonCaloSumBxCollection caloSum;
    edm::Wrapper<l1t::MuonCaloSumBxCollection> caloSumWrap;

    l1t::RegionalMuonCandBxCollection regCand;
    edm::Wrapper<l1t::RegionalMuonCandBxCollection> regCandWrap;
   
    l1t::EMTFOutputCollection emtfOutput;
    edm::Wrapper<l1t::EMTFOutputCollection> emtfOutputWrap;
   
    l1t::emtf::InternalTrackCollection internalTrack;
    edm::Wrapper<l1t::emtf::InternalTrackCollection> internalTrackWrap;

    /* L1TMuon::InternalTrackCollection internalTrackMu; */
    /* edm::Wrapper<L1TMuon::InternalTrackCollection> internalTrackMuWrap; */

    /* std::vector<L1TMuon::InternalTrack> internalTrackVect; */
    /* edm::Wrapper< std::vector<L1TMuon::InternalTrack> > internalTrackVectWrap; */

    /* L1TMuon::TriggerPrimitiveCollection triggerPrimitive; */
    /* edm::Wrapper<L1TMuon::TriggerPrimitiveCollection> triggerPrimitiveWrap; */
   
  };
}



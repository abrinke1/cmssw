// Class for muon tracks in EMTF
// Mostly copied from L1Trigger/L1TMuonEndCap/src/MuonInternalTrack.cc

#include "DataFormats/L1TMuon/interface/EMTF/InternalTrack.h"

// // Begin MuonInternalTrack.cc includes. Should cull. -AWB 08.02.16
// #include "L1Trigger/L1TMuonEndCap/interface/MuonInternalTrack.h"

// #include "DataFormats/L1CSCTrackFinder/interface/L1Track.h"

// #include "DataFormats/MuonDetId/interface/RPCDetId.h"
// #include "DataFormats/MuonDetId/interface/CSCDetId.h"
// // End MuonInternalTrack.cc includes. Should cull. -AWB 08.02.16

namespace l1t {
  namespace emtf {

    // // Can this be used anymore?  Are there csc::L1Track objects still around? - AWB 08.02.16
    // InternalTrack::InternalTrack(const csc::L1Track& csctrack):
    //   L1MuRegionalCand(csctrack) {
    //   _mode = 0;
    //   _endcap = (csctrack.endcap() == 2) ? -1 : 1;
    //   _wheel = (_endcap < 0) ? -4 : 4;
    //   _sector = csctrack.sector();
    // }

    // // Can this be used anymore?  Are there L1MuRegionalCand objects still around? - AWB 08.02.16
    // unsigned InternalTrack::type_idx() const {
    //   if( _parent.isNonnull() ) return L1MuRegionalCand::type_idx();
    //   return _type;
    // }

    // void InternalTrack::add_stub(const L1TMuon::TriggerPrimitive& _stub) { 
      
    //   unsigned station;
    //   subsystem_offset offset;
    //   // L1TMuon::TriggerPrimitive::subsystem_type type = _stub.subsystem();

    //   // switch(type) {
    //   // case TriggerPrimitive::kCSC:    
    //   offset = kCSC;
    //   station = _stub.detId<CSCDetId>().station();
    //   // break;
    //   // case TriggerPrimitive::kRPC:    
    //   // 	offset = kRPCb;
    //   // 	if(_stub.detId<RPCDetId>().region() != 0) 
    //   // 	  offset = kRPCf;
    //   // 	station = _stub.detId<RPCDetId>().station(); 
    //   // 	break;
    //   // default:
    //   // 	throw cms::Exception("Invalid Subsytem") 
    //   // 	  << "The specified subsystem for this track stub is out of range"
    //   // 	  << std::endl;
    //   // } // End switch(type)  
      
    //   const unsigned shift = 4*offset + station - 1;
    //   const unsigned bit = 1 << shift;
      
    //   // Add this track to the mode
    //   mode = mode | bit;

    //   // if( stubs.count(shift) == 0 ) 
    //   // 	stubs[shift] = L1TMuon::TriggerPrimitiveCollection();
         
    //   // stubs[shift].push_back(_stub);

    // } // End void InternalTrack::add_stub()

    
  } // End namespace emtf
} // End namespace l1t

// Class for muon tracks in EMTF
// Mostly copied from L1Trigger/L1TMuonEndCap/interface/MuonInternalTrack.h

#ifndef __l1t_emtf_InternalTrack_h__
#define __l1t_emtf_InternalTrack_h__

#include <vector>
#include <boost/cstdint.hpp> 

#include "DataFormats/L1TMuon/interface/EMTF/CSCPrimitive.h"

/* // Used for add_stub and Stubs() */
/* #include "L1Trigger/L1TMuon/interface/deprecate/MuonTriggerPrimitive.h" */
/* #include "L1Trigger/L1TMuon/interface/deprecate/MuonTriggerPrimitiveFwd.h" */

/* // Used for CSC and RPC stub station */
/* #include "DataFormats/MuonDetId/interface/RPCDetId.h" */
/* #include "DataFormats/MuonDetId/interface/CSCDetId.h" */

/* // Begin MuonInternalTrack.h includes. Should cull. -AWB 08.02.16 */
/* #include <iostream> */

/* #include "DataFormats/L1GlobalMuonTrigger/interface/L1MuRegionalCand.h" */
/* #include "L1Trigger/L1TMuonEndCap/interface/MuonInternalTrackFwd.h" */

/* #include "DataFormats/RPCDigi/interface/RPCDigiL1Link.h" */
/* #include "DataFormats/L1CSCTrackFinder/interface/L1CSCTrackCollection.h" */
/* #include "DataFormats/L1DTTrackFinder/interface/L1MuDTTrackContainer.h" */
/* #include "DataFormats/L1GlobalMuonTrigger/interface/L1MuRegionalCand.h" */
/* // End MuonInternalTrack.h includes. Should cull. -AWB 08.02.16 */

namespace l1t {
  namespace emtf {
    class InternalTrack {
    public:
      
    InternalTrack() :
      endcap(-99), sector(-99), type(-99), mode(-99), rank(-99), 
	pt(-99), theta_loc(-99), theta_deg(-99), theta_rad(-99), eta(-99), phi_local(-99), phi_global(-99), numCSCPrimitives(0)
	{};
      
      virtual ~InternalTrack() {};

      void push_CSCPrimitive(CSCPrimitive bits)  { _CSCPrimitiveCollection.push_back(bits); numCSCPrimitives += 1; };

      int NumCSCPrimitives()  { return numCSCPrimitives; };

      CSCPrimitiveCollection GetCSCPrimitiveCollection()  { return _CSCPrimitiveCollection; };


      enum subsystem_offset{ kRPCb, kCSC, kRPCf };

      /* void add_stub (const L1TMuon::TriggerPrimitive& _stub); */

      /* const L1TMuon::TriggerPrimitiveStationMap& Stubs()  const { return stubs; } */

      /* InternalTrack(const csc::L1Track &); */
      /* InternalTrack(const L1MuRegionalCand &, const RPCL1LinkRef &); */
      
      
      /* RegionalCandBaseRef parent() const { return _parent; } */
      /* void setParent(const RegionalCandBaseRef& parent) { _parent = parent; } */
      
      /* RPCL1LinkRef parentRPCLink() const { return _parentlink; } */

      // Can't have a vector of vectors of vectors in ROOT files
      /* void set_deltas (std::vector< std::vector<int> > _deltas) { deltas = _deltas; } */
      void set_phis   (std::vector<int>                _phis)   { phis   = _phis; }
      void set_thetas (std::vector<int>                _thetas) { thetas = _thetas; }
            
      void set_endcap    (int           bits) { endcap    = bits; };
      void set_sector    (int           bits) { sector    = bits; };
      void set_type      (unsigned      bits) { type      = bits; };
      void set_mode      (unsigned long bits) { mode      = bits; };
      void set_rank      (int           bits) { rank      = bits; };
      void set_pt        (float         val ) { pt        = val;  };
      void set_theta_loc (float         val ) { theta_loc = val;  };
      void set_theta_deg (float         val ) { theta_deg = val;  };
      void set_theta_rad (float         val ) { theta_rad = val;  };
      void set_eta       (float         val ) { eta       = val;  };
      void set_phi_local (float         val ) { phi_local = val;  };
      void set_phi_global(float         val ) { phi_global= val;  };
      
      const int           Endcap()     { return  endcap;    };
      const int           Sector()     { return  sector;    };
      const unsigned      Type()       { return  type;      };
      const unsigned long Mode()       { return  mode;      };
      const int           Rank()       { return  rank;      };
      const float         Pt()         { return  pt;        };
      const float         Theta_loc()  { return  theta_loc; };
      const float         Theta_deg()  { return  theta_deg; };
      const float         Theta_rad()  { return  theta_rad; };
      const float         Eta()        { return  eta;       };
      const float         Phi_local()  { return  phi_local; };
      const float         Phi_global() { return  phi_global;};
      
      
    private:

      CSCPrimitiveCollection _CSCPrimitiveCollection;

      /* L1TMuon::TriggerPrimitiveStationMap stubs; */
      /* RegionalCandBaseRef _parent; */
      /* RPCL1LinkRef _parentlink; */
      
      // Can't have a vector of vectors of vectors in ROOT files
      /* std::vector< std::vector<int> > deltas; */
      std::vector<int> phis;
      std::vector<int> thetas;
      
      int           endcap; 
      int           sector; 
      unsigned      type; 
      unsigned long mode; 
      int           rank;
      float         pt;
      float         theta_loc; // This is some bizzare local definition of theta
      float         theta_deg; // This is the true global theta in degrees
      float         theta_rad; // This is the true global theta in radians
      float         eta;
      float         phi_local;
      float         phi_global;
      int           numCSCPrimitives;

    }; // End of class InternalTrack
    
    // Define a vector of InternalTrack
    typedef std::vector<InternalTrack> InternalTrackCollection;

  } // End of namespace emtf
} // End of namespace l1t

#endif /* define __l1t_emtf_InternalTrack_h__ */

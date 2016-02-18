// Class for input trigger primitives to EMTF
// Based on L1Trigger/L1TMuon/interface/deprecate/MuonTriggerPrimitive.h
// In particular, see struct CSCData

#ifndef __l1t_emtf_CSCPrimitive_h__
#define __l1t_emtf_CSCPrimitive_h__

#include <vector>
#include <boost/cstdint.hpp> 

/* #include "DataFormats/DetId/interface/DetId.h" */
/* class CSCCorrelatedLCTDigi; */
/* class CSCDetId; */

namespace l1t {
  namespace emtf {
    class CSCPrimitive {
    public:

    CSCPrimitive() :

      endcap(-99), station(-99), ring(-99), sector(-99), chamber(-99), layer(-99),
	csc_ID(-99), mpc_link(-99), wire(-99), strip(-99), track_num(-99), 
	phi_local_deg(-99), phi_local_rad(-99), phi_global_deg(-99), phi_global_rad(-99),
	theta_loc(-99), theta_deg(-99), theta_rad(-99), eta(-99), 
	quality(-99), pattern(-99), bend(-99), 
	valid(-99), sync_err(-99), bx0(-99), bx(-99) 
	{};
      
      virtual ~CSCPrimitive() {};

      void set_endcap         (int  bits) { endcap        = bits; };
      void set_station        (int  bits) { station       = bits; };
      void set_ring           (int  bits) { ring          = bits; };
      void set_sector         (int  bits) { sector        = bits; };
      void set_chamber        (int  bits) { chamber       = bits; };
      void set_layer          (int  bits) { layer         = bits; };
      void set_csc_ID         (int  bits)  { csc_ID       = bits; };
      void set_mpc_link       (int  bits) { mpc_link      = bits; };
      void set_wire           (int  bits) { wire          = bits; };
      void set_strip          (int  bits) { strip         = bits; };
      void set_track_num      (int  bits) { track_num     = bits; };
      void set_phi_local_deg  (float val) { phi_local_deg  = val; };
      void set_phi_local_rad  (float val) { phi_local_rad  = val; };
      void set_phi_global_deg (float val) { phi_global_deg = val; };
      void set_phi_global_rad (float val) { phi_global_rad = val; };
      void set_theta_loc      (float val) { theta_loc      = val; };
      void set_theta_deg      (float val) { theta_deg      = val; };
      void set_theta_rad      (float val) { theta_rad      = val; };
      void set_eta            (float val) { eta            = val; };
      void set_quality        (int  bits) { quality       = bits; };
      void set_pattern        (int  bits) { pattern       = bits; };
      void set_bend           (int  bits) { bend          = bits; };
      void set_valid          (int  bits) { valid         = bits; };
      void set_sync_err       (int  bits) { sync_err      = bits; };
      void set_bx0            (int  bits) { bx0           = bits; };
      void set_bx             (int  bits) { bx            = bits; };

      const int   Endcap         ()  const { return endcap   ;      };
      const int   Station        ()  const { return station  ;      };
      const int   Ring           ()  const { return ring     ;      };
      const int   Sector         ()  const { return sector   ;      };
      const int   Chamber        ()  const { return chamber  ;      };
      const int   Layer          ()  const { return layer    ;      };
      const int   CSC_ID         ()  const { return csc_ID   ;      };
      const int   MPC_link       ()  const { return mpc_link ;      };
      const int   Wire           ()  const { return wire     ;      };
      const int   Strip          ()  const { return strip    ;      };
      const int   Track_num      ()  const { return track_num;      };
      const float Phi_local_deg  ()  const { return phi_local_deg;  };
      const float Phi_local_rad  ()  const { return phi_local_rad;  };
      const float Phi_global_deg ()  const { return phi_global_deg; };
      const float Phi_global_rad ()  const { return phi_global_rad; };
      const float Theta_loc      ()  const { return theta_loc;      };
      const float Theta_deg      ()  const { return theta_deg;      };
      const float Theta_rad      ()  const { return theta_rad;      };
      const float Eta            ()  const { return eta      ;      };
      const int   Quality        ()  const { return quality  ;      };
      const int   Pattern        ()  const { return pattern  ;      };
      const int   Bend           ()  const { return bend     ;      };
      const int   Valid          ()  const { return valid    ;      };
      const int   Sync_err       ()  const { return sync_err ;      };
      const int   BX0            ()  const { return bx0      ;      };
      const int   BX             ()  const { return bx       ;      };

      /* CSCPrimitive(const CSCDetId&, */
      /* 		const CSCCorrelatedLCTDigi&); */

    private:

      int   endcap;
      int   station;
      int   ring;
      int   sector;
      int   chamber;
      int   layer;
      int   csc_ID;
      int   mpc_link;
      int   wire;
      int   strip;
      int   track_num;
      float phi_local_deg;
      float phi_local_rad;
      float phi_global_deg;
      float phi_global_rad;
      float theta_loc; // This is some bizzare local definition of theta
      float theta_deg; // This is the true global theta in degrees
      float theta_rad; // This is the true global theta in radians
      float eta;
      int   quality;
      int   pattern;
      int   bend;
      int   valid;
      int   sync_err;
      int   bx0;
      int   bx;
      
      /* void calculateCSCGlobalSector(const CSCDetId& chid, */
      /* 				    unsigned& global_sector, */
      /* 				    unsigned& subsector ); */

    }; // End of class CSCPrimitive

    // Define a vector of CSCPrimitive
    typedef std::vector<CSCPrimitive> CSCPrimitiveCollection;

  } // End of namespace emtf
} // End of namespace l1t

#endif /* define __l1t_emtf_CSCPrimitive_h__ */

// Class for muon tracks in EMTF - AWB 04.01.16
// Mostly copied from L1Trigger/L1TMuonEndCap/interface/MuonInternalTrack.h

#ifndef __l1t_EMTFTrack_h__
#define __l1t_EMTFTrack_h__

#include <vector>
#include <boost/cstdint.hpp> 

#include "DataFormats/L1TMuon/interface/EMTFHit.h"

namespace l1t {
  class EMTFTrack {
  public:
    
  EMTFTrack() :
    // Using -999 instead of -99 b/c this seems most common in the emulator.  Unfortunate. - AWB 17.03.16
    endcap(-999), sector(-999), sector_GMT(-999), type(-999), mode(-999), mode_LUT(-999), quality(-999), rank(-999), layer(-999), 
      straightness(-999), strip(-999), first_bx(-999), second_bx(-999), pt(-999), pt_GMT(-999), pt_XML(-999), pt_LUT(0),
      theta_int(-999), theta_deg(-999), theta_rad(-999), eta(-999), eta_GMT(-999), eta_LUT_int(-999), 
      phi_loc_int(-999), phi_loc_deg(-999), phi_loc_rad(-999), phi_glob_deg(-999), phi_glob_rad(-999), 
      phi_GMT(-999), charge(-999), charge_GMT(-999), isGMT(0),
      dPhi_12(-999), dPhi_13(-999), dPhi_14(-999), dPhi_23(-999), dPhi_24(-999), dPhi_34(-999),
      dTheta_12(-999), dTheta_13(-999), dTheta_14(-999), dTheta_23(-999), dTheta_24(-999), dTheta_34(-999),
      clct_1(-999), clct_2(-999), clct_3(-999), clct_4(-999), fr_1(-999), fr_2(-999), fr_3(-999), fr_4(-999),
      numHits(0)
	{};
    
    virtual ~EMTFTrack() {};

    float pi = 3.141592653589793238;

    std::vector<int> Convert_pT_LUT(int _mode, unsigned long _address);

    void set_Hits(EMTFHitCollection bits)       { _Hits = bits;                numHits = _Hits.size(); }
    void push_Hit(EMTFHit bits)                 { _Hits.push_back(bits);       numHits = _Hits.size(); }
    void set_HitIndices(std::vector<uint> bits) { _HitIndices = bits;          numHits = _HitIndices.size(); }
    void push_HitIndex(uint bits)               { _HitIndices.push_back(bits); numHits = _HitIndices.size(); }
    int NumHits()            const { return numHits; }
    EMTFHitCollection Hits()       { return _Hits; }
    std::vector<uint> HitIndices() { return _HitIndices; }
    const EMTFHitCollection * PtrHits()      const { return &_Hits; }
    const std::vector<uint> * PtrHitIndices() const { return &_HitIndices; }
    
    /* // Can't have a vector of vectors of vectors in ROOT files */
    /* void set_deltas (vector< vector<int> > _deltas) { deltas = _deltas; } */
    void set_phis   (std::vector<int> _phis)   { phis   = _phis; }
    void set_thetas (std::vector<int> _thetas) { thetas = _thetas; }
    
    void set_endcap        (int  bits) { endcap       = bits; }
    void set_sector        (int  bits) { sector       = bits; }
    void set_sector_GMT    (int  bits) { sector_GMT   = bits; }
    void set_type          (int  bits) { type         = bits; }
    void set_mode          (int  bits) { mode         = bits; }
    void set_mode_LUT      (int  bits) { mode_LUT     = bits; }
    void set_quality       (int  bits) { quality      = bits; }
    void set_rank          (int  bits) { rank         = bits; }
    void set_layer         (int  bits) { layer        = bits; }
    void set_straightness  (int  bits) { straightness = bits; }
    void set_strip         (int  bits) { strip        = bits; }
    void set_first_bx      (int  bits) { first_bx     = bits; }
    void set_second_bx     (int  bits) { second_bx    = bits; }
    void set_pt            (float val) { pt           = val;  }
    void set_pt_GMT        (int  bits) { pt_GMT       = bits; }
    void set_pt_XML        (float val) { pt_XML       = val;  }
    void set_pt_LUT (unsigned long  bits)  { pt_LUT   = bits; }
    void set_theta_int     (int  bits) { theta_int    = bits; }
    void set_theta_deg     (float val) { theta_deg    = val;  }
    void set_theta_rad     (float val) { theta_rad    = val;  }
    void set_eta           (float val) { eta          = val;  }
    void set_eta_GMT       (int  bits) { eta_GMT      = bits; }
    void set_eta_LUT_int   (int  bits) { eta_LUT_int  = bits; }
    void set_phi_loc_int   (int  bits) { phi_loc_int  = bits; }
    void set_phi_loc_deg   (float val) { phi_loc_deg  = val;  }
    void set_phi_loc_rad   (float val) { phi_loc_rad  = val;  }
    void set_phi_glob_deg  (float val) { (val < 180) ? phi_glob_deg = val : phi_glob_deg = val - 360;  }
    void set_phi_glob_rad  (float val) { (val < pi ) ? phi_glob_rad = val : phi_glob_rad = val - 2*pi; }
    void set_phi_GMT       (int  bits) { phi_GMT      = bits; }
    void set_charge        (int  bits) { charge       = bits; }
    void set_charge_GMT    (int  bits) { charge_GMT   = bits; }
    void set_isGMT         (int  bits) { isGMT        = bits; }
    void set_dPhi_12       (int  bits) { dPhi_12      = bits; }
    void set_dPhi_13       (int  bits) { dPhi_13      = bits; }
    void set_dPhi_14       (int  bits) { dPhi_14      = bits; }
    void set_dPhi_23       (int  bits) { dPhi_23      = bits; }
    void set_dPhi_24       (int  bits) { dPhi_24      = bits; }
    void set_dPhi_34       (int  bits) { dPhi_34      = bits; }
    void set_dTheta_12     (int  bits) { dTheta_12    = bits; }
    void set_dTheta_13     (int  bits) { dTheta_13    = bits; }
    void set_dTheta_14     (int  bits) { dTheta_14    = bits; }
    void set_dTheta_23     (int  bits) { dTheta_23    = bits; }
    void set_dTheta_24     (int  bits) { dTheta_24    = bits; }
    void set_dTheta_34     (int  bits) { dTheta_34    = bits; }
    void set_clct_1        (int  bits) { clct_1       = bits; }
    void set_clct_2        (int  bits) { clct_2       = bits; }
    void set_clct_3        (int  bits) { clct_3       = bits; }
    void set_clct_4        (int  bits) { clct_4       = bits; }
    void set_fr_1          (int  bits) { fr_1         = bits; }
    void set_fr_2          (int  bits) { fr_2         = bits; }
    void set_fr_3          (int  bits) { fr_3         = bits; }
    void set_fr_4          (int  bits) { fr_4         = bits; }
    
    
    int   Endcap()        const { return  endcap;       }
    int   Sector()        const { return  sector;       }
    int   Sector_GMT()    const { return  sector_GMT;   }
    int   Type()          const { return  type;         }
    int   Mode()          const { return  mode;         }
    int   Mode_LUT()      const { return  mode_LUT;     }
    int   Quality()       const { return  quality;      }
    int   Rank()          const { return  rank;         }
    int   Layer()         const { return  layer;        }
    int   Straightness()  const { return  straightness; }
    int   Strip()         const { return  strip;        }
    int   First_BX()      const { return  first_bx;     }
    int   Second_BX()     const { return  second_bx;    }
    float Pt()            const { return  pt;           }
    int   Pt_GMT()        const { return  pt_GMT;       }
    float Pt_XML()        const { return  pt_XML;       }
    unsigned long Pt_LUT() const { return  pt_LUT;      }
    int   Theta_int()     const { return  theta_int;    }
    float Theta_deg()     const { return  theta_deg;    }
    float Theta_rad()     const { return  theta_rad;    }
    float Eta()           const { return  eta;          }
    int   Eta_GMT()       const { return  eta_GMT;      }
    int   Eta_LUT_int()   const { return  eta_LUT_int;  }
    int   Phi_loc_int()   const { return  phi_loc_int;  }
    float Phi_loc_deg()   const { return  phi_loc_deg;  }
    float Phi_loc_rad()   const { return  phi_loc_rad;  }
    float Phi_glob_deg()  const { return  phi_glob_deg; }
    float Phi_glob_rad()  const { return  phi_glob_rad; }
    int   Phi_GMT()       const { return  phi_GMT;      }
    int   Charge()        const { return  charge;       }
    int   Charge_GMT()    const { return  charge_GMT;   }
    int   IsGMT()         const { return  isGMT;        }
    int   DPhi_12()       const { return dPhi_12;       }
    int   DPhi_13()       const { return dPhi_13;       }
    int   DPhi_14()       const { return dPhi_14;       }
    int   DPhi_23()       const { return dPhi_23;       }
    int   DPhi_24()       const { return dPhi_24;       }
    int   DPhi_34()       const { return dPhi_34;       }
    int   DTheta_12()     const { return dTheta_12;     }
    int   DTheta_13()     const { return dTheta_13;     }
    int   DTheta_14()     const { return dTheta_14;     }
    int   DTheta_23()     const { return dTheta_23;     }
    int   DTheta_24()     const { return dTheta_24;     }
    int   DTheta_34()     const { return dTheta_34;     }
    int   CLCT_1()        const { return clct_1;        }
    int   CLCT_2()        const { return clct_2;        }
    int   CLCT_3()        const { return clct_3;        }
    int   CLCT_4()        const { return clct_4;        }
    int   FR_1()          const { return fr_1;          }
    int   FR_2()          const { return fr_2;          }
    int   FR_3()          const { return fr_3;          }
    int   FR_4()          const { return fr_4;          }

    
    
  private:
    
    EMTFHitCollection _Hits;
    std::vector<uint>  _HitIndices;

    /* // Can't have a vector of vectors of vectors in ROOT files */
    /* std::vector< std::vector<int> > deltas; */
    std::vector<int> phis;
    std::vector<int> thetas;
    
    int   endcap;       // -1 or 1.  Filled in emulator from hit. 
    int   sector;       //  1 -  6.  Filled in emulator from hit.
    int   sector_GMT;   //  0 - 11.  Filled in emulator from hit.
    int   type;         //  Don't remember what this is - AWB 06.04.16
    int   mode;         //  0 - 15.  Filled in emulator.
    int   mode_LUT;     //  0 - 15.  Filled in emulator.
    int   quality;      //  0 - 15.  Filled in emultaor.
    int   rank;         //  ? -  ?.  Filled in emulator.
    int   layer;        //  ? -  ?.  Computed in BXAnalyzer.h.  How can we access?
    int   straightness; //  ? -  ?.  Filled in emulator.
    int   strip;        //  ? -  ?.  Computed in SortSector.h.  How can we access?
    int   first_bx;     //  ? -  ?.  Filled in emulator.
    int   second_bx;    //  ? -  ?.  Filled in emulator.
    float pt;           //  ? -  ?.  Filled in emulator.
    int   pt_GMT;       //  ? -  ?.  Filled in emulator.
    float pt_XML;       //  ? -  ?.  Filled in emulator.
    unsigned long pt_LUT; // ? - ?.  Filled in emulator.
    int   theta_int;    //  ? -  ?.  Filled in emulator.
    float theta_deg;    //  ? -  ?.  Filled in emulator.
    float theta_rad;    //  ? -  ?.  Filled in emulator.
    float eta;          //  ? -  ?.  Filled in emulator.
    int   eta_GMT;      //  ? -  ?.  Filled in emulator.
    int   eta_LUT_int;  //  ? -  ?.  Filled in emulator.
    int   phi_loc_int;  //  ? -  ?.  Filled in emulator.
    float phi_loc_deg;  //  ? -  ?.  Filled in emulator.
    float phi_loc_rad;  //  ? -  ?.  Filled in emulator.
    float phi_glob_deg; //  ? -  ?.  Filled in emulator.
    float phi_glob_rad; //  ? -  ?.  Filled in emulator.
    int   phi_GMT;      //  ? -  ?.  Filled in emulator.
    int   charge;       // -1 or 1.  Filled in emulator.
    int   charge_GMT;   //  0 or 1.  Filled in emulator.
    int   isGMT;        //  0 or 1.  Filled in emulator.
    int   dPhi_12;
    int   dPhi_13;
    int   dPhi_14;
    int   dPhi_23;
    int   dPhi_24;
    int   dPhi_34;
    int   dTheta_12;
    int   dTheta_13;
    int   dTheta_14;
    int   dTheta_23;
    int   dTheta_24;
    int   dTheta_34;
    int   clct_1;
    int   clct_2;
    int   clct_3;
    int   clct_4;
    int   fr_1;
    int   fr_2;
    int   fr_3;
    int   fr_4;
    int   numHits;
    
  }; // End of class EMTFTrack
  
  // Define a vector of EMTFTrack
  typedef std::vector<EMTFTrack> EMTFTrackCollection;
  
} // End of namespace l1t

#endif /* define __l1t_EMTFTrack_h__ */

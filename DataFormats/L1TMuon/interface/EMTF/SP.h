// Class for Sector Processor (SP) Output Data Record

#ifndef __l1t_emtf_SP_h__
#define __l1t_emtf_SP_h__

#include <boost/cstdint.hpp> 

namespace l1t {
  namespace emtf {
    class SP {
    public:
      
      explicit SP(uint64_t dataword);
    
    SP() :
      pt_lut_address(-99), phi_local_int(-99), phi_GMT_int(-99), eta_GMT_int(-99), eta_LUT_int(-99), pt_int(-99), 
	quality(-99), mode(-99), mode_LUT(-99), bx(-99), me1_subsector(-99), me1_CSC_ID(-99), me1_sector(-99),
	me1_neighbor(-99), me1_trk_stub_num(-99), me2_CSC_ID(-99), me2_sector(-99), me2_neighbor(-99),
	me2_trk_stub_num(-99), me3_CSC_ID(-99), me3_sector(-99), me3_neighbor(-99), me3_trk_stub_num(-99), 
	me4_CSC_ID(-99), me4_sector(-99), me4_neighbor(-99), me4_trk_stub_num(-99), me1_delay(-99), 
	me2_delay(-99), me3_delay(-99), me4_delay(-99), tbin_num(-99), hl(-99), c(-99), vc(-99), 
	vt(-99), se(-99), bc0(-99), pt(-99), phi_local(-99), phi_local_rad(-99), phi_global(-99), 
	phi_GMT(-99), phi_GMT_corr(-99), phi_GMT_rad(-99), phi_GMT_global(-99), eta_GMT(-99),  
	dPhi_12(-99), dPhi_13(-99), dPhi_14(-99), dPhi_23(-99), dPhi_24(-99), dPhi_34(-99),
	dTheta_12(-99), dTheta_13(-99), dTheta_14(-99), dTheta_23(-99), dTheta_24(-99), dTheta_34(-99),
	clct_1(-99), clct_2(-99), clct_3(-99), clct_4(-99), fr_1(-99), fr_2(-99), fr_3(-99), fr_4(-99),
	format_errors(0), dataword(-99) 
	{};

      virtual ~SP() {};

      float pi = 3.141592653589793238;

      // phi_local gives the exact phi value (marked "phi_full" in the format document)
      // phi_GMT (the value used by GMT) is a rough estimate, with offsets of 1-2 degrees for some phi values
      // The conversion used is: phi_GMT =        (360/576)*phi_GMT_int +        (180/576)
      // More accurate would be: phi_GMT = 1.0208*(360/576)*phi_GMT_int + 1.0208*(180/576) + 0.552

      float calc_pt(int bits)                    { return (bits - 1) * 0.5;                                  };
      int   calc_pt_int(float val)               { return (val * 2) + 1;                                     };
      float calc_phi_local(int bits)             { return (bits / 60.0) - 2.0;                               };
      float calc_phi_local_rad(int bits)         { return (bits * pi / 10800) - (pi / 90);                   };
      int   calc_phi_local_int(float val)        { return (val + 2) * 60;                                    };
      float calc_phi_GMT(int bits)               { return (bits * 0.625) + 0.3125;                           }; /* x (360/576) + (180/576) */
      float calc_phi_GMT_corr(int bits)          { return (bits * 0.625 * 1.0208) + 0.3125 * 1.0208 + 0.552; }; /* AWB mod 09.02.16 */
      float calc_phi_GMT_rad(int bits)           { return (bits * pi / 288) + (pi / 576);                    }; /* x (2*pi/576) + (pi/576) */
      int   calc_phi_GMT_int(float val)          { return (val - 0.3125) / 0.625;                            }; /* - (180/576) / (360/576) */
      float calc_eta_GMT(int bits)               { return bits * 0.010875;                                   };
      int   calc_eta_GMT_int(float val)          { return val / 0.010875;                                    };
      float calc_phi_global(float loc, int sect) { return loc + 15 + (sect - 1) * 60;                        };
      int   calc_mode()                          { return 8*me1_trk_stub_num + 4*me2_trk_stub_num + 2*me3_trk_stub_num + me4_trk_stub_num; };

      // Converts CSC_ID, sector, subsector, and neighbor
      std::vector<int> convert_chamber_SP(int _csc_ID, int _sector, int _subsector, int _station) {
	int new_sector = _sector;
	if (_station == 1) {
	  if      (_csc_ID <  0) { int arr[] = {-99, -99, -99, -99}; std::vector<int> vec(arr, arr+4); return vec; }
	  else if (_csc_ID == 0) { int arr[] = { -1,  -1,  -1,  -1}; std::vector<int> vec(arr, arr+4); return vec; }
	  else if (_csc_ID <= 9) { int arr[] = {_csc_ID, new_sector, _subsector, 0}; std::vector<int> vec(arr, arr+4); return vec; }
	  else new_sector = (_sector != 6) ? _sector+1 : 1;

	  if      (_csc_ID == 10) { int arr[] = {3, new_sector, 2, 1}; std::vector<int> vec(arr, arr+4); return vec; }
	  else if (_csc_ID == 11) { int arr[] = {6, new_sector, 2, 1}; std::vector<int> vec(arr, arr+4); return vec; }
	  else if (_csc_ID == 12) { int arr[] = {9, new_sector, 2, 1}; std::vector<int> vec(arr, arr+4); return vec; }
	  else { int arr[] = {-99, -99, -99, -99}; std::vector<int> vec(arr, arr+4); return vec; }
	}
	else if (_station == 2 || _station == 3 || _station == 4) {
	  if      (_csc_ID <  0) { int arr[] = {-99, -99, -99, -99}; std::vector<int> vec(arr, arr+4); return vec; }
	  else if (_csc_ID == 0) { int arr[] = { -1,  -1,  -1,  -1}; std::vector<int> vec(arr, arr+4); return vec; }
	  else if (_csc_ID <= 9) { int arr[] = {_csc_ID, new_sector, -1, 0}; std::vector<int> vec(arr, arr+4); return vec; }
	  else new_sector = (_sector != 6) ? _sector+1 : 1;

	  if      (_csc_ID == 10) { int arr[] = {3, new_sector, -1, 1}; std::vector<int> vec(arr, arr+4); return vec; }
	  else if (_csc_ID == 11) { int arr[] = {6, new_sector, -1, 1}; std::vector<int> vec(arr, arr+4); return vec; }
	  else { int arr[] = {-99, -99, -99, -99}; std::vector<int> vec(arr, arr+4); return vec; }
	}
	else { int arr[] = {-99, -99, -99, -99}; std::vector<int> vec(arr, arr+4); return vec; }
      }

      // Setting pt, phi_local, phi_GMT, or eta_GMT automatically sets all formats (integer, degrees, radians) 
      void set_pt_int(int bits)                    { pt_int = bits;
                                                     set_pt_only(calc_pt(pt_int));                              };
      void set_pt(float val)                       { pt = val;
                                                     set_pt_int_only(calc_pt_int(pt));                          };
      void set_phi_local_int(int bits)             { phi_local_int = bits;
	                                             set_phi_local_only(calc_phi_local(phi_local_int));
                                                     set_phi_local_rad_only(calc_phi_local_rad(phi_local_int)); };
      void set_phi_local(float val)                { phi_local = val;
	                                             set_phi_local_int_only(calc_phi_local_int(phi_local));
                                                     set_phi_local_rad_only(calc_phi_local_rad(phi_local_int)); };
      void set_phi_local_rad(float val)            { phi_local_rad = val;
	                                             set_phi_local_only(val * 180 / pi);
                                                     set_phi_local_int_only(calc_phi_local_int(phi_local));     };
      void set_phi_GMT_int(int bits)               { phi_GMT_int = bits;
	                                             set_phi_GMT_only(calc_phi_GMT(phi_GMT_int));
	                                             set_phi_GMT_corr_only(calc_phi_GMT_corr(phi_GMT_int));
                                                     set_phi_GMT_rad_only(calc_phi_GMT_rad(phi_GMT_int));       };
      void set_phi_GMT(float val)                  { phi_GMT = val;
	                                             set_phi_GMT_int_only(calc_phi_GMT_int(phi_GMT));
	                                             set_phi_GMT_corr_only(calc_phi_GMT_corr(phi_GMT_int));
                                                     set_phi_GMT_rad_only(calc_phi_GMT_rad(phi_GMT_int));       };
      void set_phi_GMT_rad(float val)              { phi_GMT_rad = val;
	                                             set_phi_GMT_only(val * 180 / pi);
                                                     set_phi_GMT_int_only(calc_phi_GMT_int(phi_GMT));
                                                     set_phi_GMT_corr_only(calc_phi_GMT_corr(phi_GMT_int));     };
      void set_phi_global(float loc, int sect)     { set_phi_global_only(calc_phi_global(loc, sect));           };
      void set_phi_GMT_global(float loc, int sect) { set_phi_GMT_global_only(calc_phi_global(loc, sect));       };
      void set_eta_GMT_int(int  bits)              { eta_GMT_int = bits;
                                                     set_eta_GMT_only(calc_eta_GMT(eta_GMT_int));               };
      void set_eta_GMT(float val)                  { eta_GMT= val;
                                                      set_eta_GMT_int_only(calc_eta_GMT_int(eta_GMT));          };

      void set_pt_lut_address(unsigned long bits) { pt_lut_address = bits;   };
      void set_eta_LUT_int(int bits)      { eta_LUT_int = bits;      };
      void set_quality(int bits)          { quality = bits;          };
      void set_mode(int bits)             { mode = bits;             };
      void set_mode_LUT(int bits)         { mode_LUT = bits;         };
      void set_bx(int bits)               { bx = bits;               };
      void set_me1_subsector(int bits)    { me1_subsector = bits;    };
      void set_me1_CSC_ID(int bits)       { me1_CSC_ID = bits;       };
      void set_me1_sector(int bits)       { me1_sector = bits;       };
      void set_me1_neighbor(int bits)     { me1_neighbor = bits;     };
      void set_me1_trk_stub_num(int bits) { me1_trk_stub_num = bits; };      
      void set_me2_CSC_ID(int bits)       { me2_CSC_ID = bits;       };
      void set_me2_sector(int bits)       { me2_sector = bits;       };
      void set_me2_neighbor(int bits)     { me2_neighbor = bits;     };
      void set_me2_trk_stub_num(int bits) { me2_trk_stub_num = bits; };
      void set_me3_CSC_ID(int bits)       { me3_CSC_ID = bits;       };
      void set_me3_sector(int bits)       { me3_sector = bits;       };
      void set_me3_neighbor(int bits)     { me3_neighbor = bits;     };
      void set_me3_trk_stub_num(int bits) { me3_trk_stub_num = bits; };
      void set_me4_CSC_ID(int bits)       { me4_CSC_ID = bits;       };
      void set_me4_sector(int bits)       { me4_sector = bits;       };
      void set_me4_neighbor(int bits)     { me4_neighbor = bits;     };
      void set_me4_trk_stub_num(int bits) { me4_trk_stub_num = bits; };
      void set_me1_delay(int bits)         { me1_delay = bits;         };
      void set_me2_delay(int bits)         { me2_delay = bits;         };
      void set_me3_delay(int bits)         { me3_delay = bits;         };
      void set_me4_delay(int bits)         { me4_delay = bits;         };
      void set_TBIN_num(int bits)         { tbin_num = bits;         };
      void set_hl(int bits)               { hl = bits;               };
      void set_c(int bits)                { c = bits;                };
      void set_vc(int bits)               { vc = bits;               };
      void set_vt(int bits)               { vt = bits;               };
      void set_se(int bits)               { se = bits;               };
      void set_bc0(int bits)              { bc0 = bits;              };
      void set_dPhi_12(int bits)          { dPhi_12 = bits;          };
      void set_dPhi_13(int bits)          { dPhi_13 = bits;          };
      void set_dPhi_14(int bits)          { dPhi_14 = bits;          };
      void set_dPhi_23(int bits)          { dPhi_23 = bits;          };
      void set_dPhi_24(int bits)          { dPhi_24 = bits;          };
      void set_dPhi_34(int bits)          { dPhi_34 = bits;          };
      void set_dTheta_12(int bits)        { dTheta_12 = bits;        };
      void set_dTheta_13(int bits)        { dTheta_13 = bits;        };
      void set_dTheta_14(int bits)        { dTheta_14 = bits;        };
      void set_dTheta_23(int bits)        { dTheta_23 = bits;        };
      void set_dTheta_24(int bits)        { dTheta_24 = bits;        };
      void set_dTheta_34(int bits)        { dTheta_34 = bits;        };
      void set_clct_1(int bits)           { clct_1 = bits;           };
      void set_clct_2(int bits)           { clct_2 = bits;           };
      void set_clct_3(int bits)           { clct_3 = bits;           };
      void set_clct_4(int bits)           { clct_4 = bits;           };
      void set_fr_1(int bits)             { fr_1 = bits;             };
      void set_fr_2(int bits)             { fr_2 = bits;             };
      void set_fr_3(int bits)             { fr_3 = bits;             };
      void set_fr_4(int bits)             { fr_4 = bits;             };
      void add_format_error()             { format_errors += 1;      };
      void set_dataword(uint64_t bits)    { dataword = bits;         };

      unsigned long Pt_lut_address() const { return pt_lut_address;   };
      int      Phi_local_int()    const { return phi_local_int;    };
      int      Phi_GMT_int()      const { return phi_GMT_int;      };
      int      Eta_GMT_int()      const { return eta_GMT_int;      };
      int      Eta_LUT_int()      const { return eta_LUT_int;      };
      int      Pt_int()           const { return pt_int;           };
      int      Quality()          const { return quality;          };
      int      Mode()             const { return mode;             };
      int      Mode_LUT()         const { return mode_LUT;         };
      int      BX()               const { return bx;               };
      int      ME1_subsector()    const { return me1_subsector;    };
      int      ME1_CSC_ID()       const { return me1_CSC_ID;       };
      int      ME1_sector()       const { return me1_sector;       };
      int      ME1_neighbor()     const { return me1_neighbor;     };
      int      ME1_trk_stub_num() const { return me1_trk_stub_num; };      
      int      ME2_CSC_ID()       const { return me2_CSC_ID;       };
      int      ME2_sector()       const { return me2_sector;       };
      int      ME2_neighbor()     const { return me2_neighbor;     };
      int      ME2_trk_stub_num() const { return me2_trk_stub_num; };
      int      ME3_CSC_ID()       const { return me3_CSC_ID;       };  
      int      ME3_sector()       const { return me3_sector;       };  
      int      ME3_neighbor()     const { return me3_neighbor;     };  
      int      ME3_trk_stub_num() const { return me3_trk_stub_num; };
      int      ME4_CSC_ID()       const { return me4_CSC_ID;       };
      int      ME4_sector()       const { return me4_sector;       };
      int      ME4_neighbor()     const { return me4_neighbor;     };
      int      ME4_trk_stub_num() const { return me4_trk_stub_num; };
      int      ME1_delay()         const { return me1_delay;         };
      int      ME2_delay()         const { return me2_delay;         };
      int      ME3_delay()         const { return me3_delay;         };
      int      ME4_delay()         const { return me4_delay;         };
      int      TBIN_num()         const { return tbin_num;         };
      int      HL()               const { return hl;               };
      int      C()                const { return c;                };
      int      VC()               const { return vc;               };
      int      VT()               const { return vt;               };
      int      SE()               const { return se;               };
      int      BC0()              const { return bc0;              };
      float    Pt()               const { return pt;               };
      float    Phi_local()        const { return phi_local;        };
      float    Phi_local_rad()    const { return phi_local_rad;    };
      float    Phi_global()       const { return phi_global;       };
      float    Phi_GMT()          const { return phi_GMT;          };
      float    Phi_GMT_corr()     const { return phi_GMT_corr;     };
      float    Phi_GMT_rad()      const { return phi_GMT_rad;      };
      float    Phi_GMT_global()   const { return phi_GMT_global;   };
      float    Eta_GMT()          const { return eta_GMT;          };
      int      DPhi_12()          const { return dPhi_12;          };
      int      DPhi_13()          const { return dPhi_13;          };
      int      DPhi_14()          const { return dPhi_14;          };
      int      DPhi_23()          const { return dPhi_23;          };
      int      DPhi_24()          const { return dPhi_24;          };
      int      DPhi_34()          const { return dPhi_34;          };
      int      DTheta_12()        const { return dTheta_12;        };
      int      DTheta_13()        const { return dTheta_13;        };
      int      DTheta_14()        const { return dTheta_14;        };
      int      DTheta_23()        const { return dTheta_23;        };
      int      DTheta_24()        const { return dTheta_24;        };
      int      DTheta_34()        const { return dTheta_34;        };
      int      CLCT_1()           const { return clct_1;           };
      int      CLCT_2()           const { return clct_2;           };
      int      CLCT_3()           const { return clct_3;           };
      int      CLCT_4()           const { return clct_4;           };
      int      FR_1()             const { return fr_1;             };
      int      FR_2()             const { return fr_2;             };
      int      FR_3()             const { return fr_3;             };
      int      FR_4()             const { return fr_4;             };
      int      Format_Errors()    const { return format_errors;    };
      uint64_t Dataword()         const { return dataword;         }; 
      
    private:
      // Set only specific formats of values
      void set_pt_only(float val)             { pt = val;             };
      void set_pt_int_only(int  bits)         { pt_int = bits;        };
      void set_phi_local_only(float val)      { phi_local = val;      };
      void set_phi_local_rad_only(float val)  { phi_local_rad = val;  };
      void set_phi_local_int_only(int  bits)  { phi_local_int = bits; };
      void set_phi_global_only(float val)     { phi_global = val;     };
      void set_phi_GMT_only(float val)        { phi_GMT = val;        };
      void set_phi_GMT_corr_only(float val)   { phi_GMT_corr = val;   };
      void set_phi_GMT_rad_only(float val)    { phi_GMT_rad = val;    };
      void set_phi_GMT_int_only(int  bits)    { phi_GMT_int = bits;   };
      void set_phi_GMT_global_only(float val) { phi_GMT_global = val; };
      void set_eta_GMT_only(float val)        { eta_GMT = val;        };
      void set_eta_GMT_int_only(int  bits)    { eta_GMT_int = bits;   };

      unsigned long pt_lut_address;
      int phi_local_int;
      int phi_GMT_int;
      int eta_GMT_int;
      int eta_LUT_int;
      int pt_int;
      int quality;
      int mode;
      int mode_LUT;
      int bx;
      int me1_subsector;
      int me1_CSC_ID;      
      int me1_sector;      
      int me1_neighbor;      
      int me1_trk_stub_num;      
      int me2_CSC_ID;
      int me2_sector;
      int me2_neighbor;
      int me2_trk_stub_num;
      int me3_CSC_ID;
      int me3_sector;
      int me3_neighbor;
      int me3_trk_stub_num;
      int me4_CSC_ID;      
      int me4_sector;      
      int me4_neighbor;      
      int me4_trk_stub_num;
      int me1_delay;
      int me2_delay;
      int me3_delay;
      int me4_delay;
      int tbin_num;
      int hl;
      int c;
      int vc;
      int vt;
      int se;
      int bc0;
      float pt;
      float phi_local;
      float phi_local_rad;
      float phi_global;
      float phi_GMT;
      float phi_GMT_corr;
      float phi_GMT_rad;
      float phi_GMT_global;
      float eta_GMT;
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
      int format_errors;
      uint64_t dataword;
      
    }; // End of class SP

    // Define a vector of SP
    typedef std::vector<SP> SPCollection;

  } // End of namespace emtf
} // End of namespace l1t

#endif /* define __l1t_emtf_SP_h__ */

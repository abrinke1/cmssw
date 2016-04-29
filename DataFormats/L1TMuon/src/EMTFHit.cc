#include "DataFormats/L1TMuon/interface/EMTFHit.h"

namespace l1t {

  // Based on L1Trigger/L1TMuon/src/MuonTriggerPrimitive.cc
  // TriggerPrimitive::TriggerPrimitive(const CSCDetId& detid, const CSCCorrelatedLCTDigi& digi)
  void EMTFHit::ImportCSCDetId( const CSCDetId& _detId) {

    SetCSCDetId ( _detId ); 
    // It appears the following function *actually does literally nothing* - AWB 17.03.16
    // calculateCSCGlobalSector(detid,_globalsector,_subsector);

    // Based on L1Trigger/L1TMuonEndCap/interface/PrimitiveConverter.h
    set_endcap  ( (_detId.endcap() == 2) ? -1 : _detId.endcap() ); // Convert from {+,-} = {1,2} to {1,-1}
    set_station ( _detId.station()       );
    set_sector  ( _detId.triggerSector() );
    set_ring    ( _detId.ring()          );
    set_chamber ( _detId.chamber()       );

    set_sector_GMT ( calc_sector_GMT( endcap, sector ) );
    set_is_CSC_hit ( true  );
    set_is_RPC_hit ( false );

  } // End EMTFHit::ImportCSCDetId

  CSCDetId EMTFHit::CreateCSCDetId() {

    return CSCDetId( (endcap == 1) ? 1 : 2, station,    // For now, leave "layer" unfilled, defaults to 0.
		     (ring == 4) ? 1 : ring, chamber ); // Not sure if this is correct, or what "layer" does. - AWB 27.04.16
  }

  // Based on L1Trigger/L1TMuon/src/MuonTriggerPrimitive.cc
  // TriggerPrimitive::TriggerPrimitive(const CSCDetId& detid, const CSCCorrelatedLCTDigi& digi)
  // This is what gets filled when "getCSCData()" is called in
  // L1Trigger/L1TMuonEndCap/interface/PrimitiveConverter.h
  void EMTFHit::ImportCSCCorrelatedLCTDigi( const CSCCorrelatedLCTDigi& _digi) {

    SetCSCLCTDigi ( _digi );

    set_track_num ( _digi.getTrknmb()  );
    set_valid     ( _digi.isValid()    );
    set_quality   ( _digi.getQuality() );
    set_wire      ( _digi.getKeyWG()   );
    set_strip     ( _digi.getStrip()   );
    set_pattern   ( _digi.getPattern() );
    set_bend      ( _digi.getBend()    );
    set_bx        ( _digi.getBX() - 6  ); // Standard for csctfDigis in data, simCscTriggerPrimitiveDigis in MC
    set_mpc_link  ( _digi.getMPCLink() );
    set_bx0       ( _digi.getBX0()     );
    set_sync_err  ( _digi.getSyncErr() );
    set_csc_ID    ( _digi.getCSCID()   );

    set_subsector ( calc_subsector( station, chamber ) ); 

  } // End EMTFHit::ImportCSCCorrelatedLCTDigi

  CSCCorrelatedLCTDigi EMTFHit::CreateCSCCorrelatedLCTDigi() {

    return CSCCorrelatedLCTDigi( 1, valid, quality, wire, strip, 
				 pattern, (bend == 1) ? 1 : 0,   
				 bx + 6, 0, 0, sync_err, csc_ID );  
    // Unsure of how to fill "trknmb" or "bx0" - for now filling with 1 and 0. - AWB 27.04.16
    // Appear to be unused in the emulator code. mpclink = 0 (after bx) indicates unsorted.
  }

  void EMTFHit::ImportME( const emtf::ME _ME) {

    set_wire       ( _ME.Wire() );
    set_strip      ( _ME.Strip() );
    set_quality    ( _ME.Quality() );
    set_pattern    ( _ME.CLCT_pattern() );
    set_bend       ( (_ME.LR() == 1) ? 1 : -1 );
    set_valid      ( _ME.VP() );
    set_sync_err   ( _ME.SE() );
    set_bx         ( _ME.TBIN() - 3 );
    set_bc0        ( _ME.BC0() ); 
    set_is_CSC_hit ( true  );
    set_is_RPC_hit ( false );

    // Station, CSC_ID, Sector, Subsector, Neighbor, Sector_GMT, Ring, and Chamber filled in
    // EventFilter/L1TRawToDigi/src/implementations_stage2/EMTFBlockME.cc
    // "set_layer()" is not invoked, so Layer is not yet filled - AWB 21.04.16

  } // End EMTFHit::ImportME

  int EMTFHit::calc_ring (int _station, int _csc_ID, int _strip) {
    if (_station > 1) {
      if      (_csc_ID <  4) return 1;
      else if (_csc_ID < 10) return 2;
      else return -999;
    }
    else if (_station == 1) {
      if      (_csc_ID < 4 && _strip > 127) return 4;
      else if (_csc_ID < 4 && _strip >=  0) return 1;
      else if (_csc_ID > 3 && _csc_ID <  7) return 2;
      else if (_csc_ID > 6 && _csc_ID < 10) return 3;
      else return -999;
    }
    else return -999;
  } // End EMTFHit::calc_ring

  int EMTFHit::calc_chamber (int _station, int _sector, int _subsector, int _ring, int _csc_ID) {
    int tmp_chamber = -999;
    if (_station == 1) {
      tmp_chamber = ((_sector-1) * 6) + _csc_ID + 2; // Chamber offset of 2: First chamber in sector 1 is chamber 3
      if (_ring == 2)       tmp_chamber -= 3;
      if (_ring == 3)       tmp_chamber -= 6;
      if (_subsector == 2)  tmp_chamber += 3;
      if (tmp_chamber > 36) tmp_chamber -= 36;
    }
    else if (_ring == 1) { 
      tmp_chamber = ((_sector-1) * 3) + _csc_ID + 1; // Chamber offset of 1: First chamber in sector 1 is chamber 2
      if (tmp_chamber > 18) tmp_chamber -= 18;
    }
    else if (_ring == 2) {
      tmp_chamber = ((_sector-1) * 6) + _csc_ID - 3 + 2; // Chamber offset of 2: First chamber in sector 1 is chamber 3
      if (tmp_chamber > 36) tmp_chamber -= 36;
    }
    return tmp_chamber;
  } // End EMTFHit::calc_chamber
    
} // End namespace l1t

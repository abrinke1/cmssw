// -*- C++ -*-
//=============================================================
// Fill all LCTs in the event record for: 
// Package:    CSCplusRPCTrackAnalyzer
// Class:      CSCplusRPCTrackAnalyzer
//
// Written by David Curry
// ============================================================

#include <string.h>
#include <iomanip>
#include <iostream>
#include <fstream>
#include <set>
#include <cmath>
#include <vector>


using namespace std;

void fillEMTFTracks(DataEvtSummary_t &ev, edm::Handle<std::vector<l1t::emtf::InternalTrack>> tracks, int printLevel) {
  
    // loop over CSCTF tracks
  int nTrk=0;
  for( auto trk = tracks->cbegin(); trk < tracks->cend(); trk++,nTrk++) {
    
    // Access the track variables
    float trPt     = trk -> Pt();
    float trGblEta = trk -> Eta();
    float trGblPhi = trk -> Phi_global_rad();
    int trMode     = trk -> Mode();
    int trBx       = trk -> BX();

    if (printLevel > 0) {
      cout << " CSC Track # " << nTrk << endl;
      cout << "===========================" << endl;
      cout << " Track Pt        = " << trPt << endl ;
      cout << " Track mode      = " << trMode << endl;
      cout << " Track Eta       = " << trGblEta  << endl;
      cout << " Track Phi       = " << trGblPhi  << endl;
    }

    // Fill Track Branches
    ev.trkPt   -> push_back(trPt);
    ev.trkEta  -> push_back(trGblEta);
    ev.trkPhi  -> push_back(trGblPhi);
    ev.trkMode -> push_back(trMode);
    ev.trkBx  -> push_back(trBx);
    ev.trkRank -> push_back( trk->Rank() );
    ev.trkStraight -> push_back( trk->Straightness() );

    int trBx_beg = -99;
    int trBx_end = 99;

    // Fill Track LCTs  
    int LctTrkId_ = 0;
    for( auto lct = trk->GetCSCPrimitiveCollection().cbegin(); lct < trk->GetCSCPrimitiveCollection().cend(); lct++, LctTrkId_++) {
      
      int trlct_endcap   = lct->Endcap();
      int trlct_sector   = lct->Sector();
      int trlct_station  = lct->Station();
      int trlct_ring     = lct->Ring();
      int trlct_wire     = lct->Wire();
      int trlct_strip    = lct->Strip();
      int trlct_chamber  = lct->Chamber();
      int trlct_cscID    = lct->CSC_ID();
      float trlct_gblphi = lct->Phi_global_rad();
      float trlct_geomphi = lct->Phi_geom_rad();
      float trlct_gbleta = lct->Eta();
      int trlct_locphi   = lct->Phi_local_rad();
      int trlct_loctheta = lct->Theta_loc();
      int trlct_bx       = lct->BX();
      if (trlct_bx > trBx_beg) trBx_beg = trlct_bx;
      if (trlct_bx < trBx_end) trBx_end = trlct_bx;
      
      // for consistency with LCT collection
      if (trlct_endcap<0) trlct_endcap = 2;
      
      if (printLevel > 0) {
	cout << "   === CSC LCT # "<< LctTrkId_ << endl;
	cout << "   Phi       = "  << trlct_gblphi << endl;
	cout << "   Eta       = "  << trlct_gbleta << endl;
	cout << "   Sector    = "  << trlct_sector  << endl;
	cout << "   Endcap    = "  << trlct_endcap  << endl;
	cout << "   Station   = "  << trlct_station  << endl;
	cout << "   Ring      = "  << trlct_ring  << endl;
	cout << "   Chamber   = "  << trlct_chamber  << endl;
	cout << "   cscID     = "  << trlct_cscID  << endl ;
	cout << "   Wire      = "  << trlct_wire  << endl;
	cout << "   Strip     = "  << trlct_strip  << endl << endl;
      }

      // Do not FIll array over their given size!!
      if (nTrk > MAXTRK-1) {
	if (printLevel > 1) cout << "-----> nTrks is greater than MAXTRK-1.  Skipping this Track..." << endl;
	continue;
      }
      
      if (LctTrkId_ > MAXTRKLCTS-1) {
	if (printLevel > 1)cout << "-----> LctTrkId_ is greater than MAXTRKLCTS-1.  Skipping this Track..." << endl;
	continue;
      }
      	

      ev.trkLctEndcap[nTrk][LctTrkId_] = trlct_endcap;
            
      // sector (end 1: 1->6, end 2: 7 -> 12)
      //if ( trlct_endcap == 1)
      ev.trkLctSector[nTrk][LctTrkId_] = trlct_sector;
      //else
      //	trLctSector[nTrk][LctTrkId_] = 6+trlct_sector;
      
      ev.trkLctStation[nTrk][LctTrkId_] = trlct_station;
      
      ev.trkLctRing[nTrk][LctTrkId_] = trlct_ring;
      
      ev.trkLctChamber[nTrk][LctTrkId_] = trlct_chamber;
      
      ev.trkLctCSCID[nTrk][LctTrkId_] = trlct_cscID;
      
      ev.trkLctWire[nTrk][LctTrkId_] = trlct_wire;
      
      ev.trkLctStrip[nTrk][LctTrkId_] = trlct_strip;
      
      ev.trkLctGblPhi[nTrk][LctTrkId_] = trlct_gblphi;
      
      ev.trkLctGeomPhi[nTrk][LctTrkId_] = trlct_geomphi;
      
      ev.trkLctGblEta[nTrk][LctTrkId_] = trlct_gbleta;

      ev.trkLctLocPhi[nTrk][LctTrkId_] = trlct_locphi;
      
      ev.trkLctLocTheta[nTrk][LctTrkId_] = trlct_loctheta;
      
      ev.trkLctBx[nTrk][LctTrkId_] = trlct_bx;

      ev.trkLctQual[nTrk][LctTrkId_] = lct->Quality();

      ev.trkLctPattern[nTrk][LctTrkId_] = lct->Pattern();
      
    } // end track LCT loop
    
    ev.trkBxBeg  -> push_back(trBx_beg);
    ev.trkBxEnd  -> push_back(trBx_end);
    ev.numTrkLCTs -> push_back(LctTrkId_);
    
  } // end track loop

  ev.numTrks = nTrk;


} // end fill Tracks

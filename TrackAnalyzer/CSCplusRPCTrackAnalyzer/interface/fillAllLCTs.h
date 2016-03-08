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
#include "L1Trigger/L1TMuonEndCap/plugins/L1TMuonEndCapTrackProducer.h"
#include "L1Trigger/CSCCommonTrigger/interface/CSCPatternLUT.h"
#include "L1Trigger/CSCTrackFinder/test/src/RefTrack.h"

#include "L1Trigger/L1TMuon/interface/deprecate/SubsystemCollectorFactory.h"

#include "DataFormats/HepMCCandidate/interface/GenParticleFwd.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include <TMath.h>
#include <TCanvas.h>
#include <TLorentzVector.h>

#include <TStyle.h>
#include <TLegend.h>
#include <TF1.h>
#include <TH2.h>
#include <TH1F.h>
#include <TFile.h>
#include "L1Trigger/L1TMuon/interface/deprecate/GeometryTranslator.h"
#include "L1Trigger/L1TMuon/interface/deprecate/MuonTriggerPrimitive.h"

#include "L1Trigger/L1TMuonEndCap/interface/MuonInternalTrack.h"
//#include "L1Trigger/L1TMuonEndCap/interface/MuonInternalTrackFwd.h"

//#include "L1Trigger/L1TMuonEndCap/interface/PrimitiveConverter.h"
#include "L1Trigger/L1TMuonEndCap/interface/PhiMemoryImage.h"
#include "L1Trigger/L1TMuonEndCap/interface/EmulatorClasses.h"
#include "L1Trigger/CSCTrackFinder/interface/CSCTFPtLUT.h"
#include "L1Trigger/CSCTrackFinder/interface/CSCSectorReceiverLUT.h"
#include "DataFormats/CSCDigi/interface/CSCCorrelatedLCTDigiCollection.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "L1Trigger/L1TMuon/interface/deprecate/MuonTriggerPrimitive.h"
#include <L1Trigger/CSCTrackFinder/interface/CSCTFSPCoreLogic.h>

using namespace std;
using namespace edm;
using namespace reco;
using namespace csc;


/*
void fillAllLCTs(DataEvtSummary_t &ev, edm::Handle<CSCCorrelatedLCTDigiCollection> LCTs, int printLevel, 
		 CSCSectorReceiverLUT* srLUTs_[5][2],
		 const L1MuTriggerScales  *ts,
		 const L1MuTriggerPtScale *tpts) {
  
  std::vector<L1TMuon::TriggerPrimitive> LCT_collection;
  
  auto chamber = LCTs->begin();
  auto chend  = LCTs->end();
  for( ; chamber != chend; ++chamber ) {
    auto digi = (*chamber).second.first;
    auto dend = (*chamber).second.second;
    for( ; digi != dend; ++digi ) {
      LCT_collection.push_back(TriggerPrimitive((*chamber).first,*digi));
    }
  }
  */

void fillAllLCTs(DataEvtSummary_t &ev, std::vector<L1TMuon::TriggerPrimitive> LCT_collection, int printLevel) {
  
  int lctId = 0; // count number of lcts in event
  
  auto Lct = LCT_collection.cbegin();
  auto Lctend = LCT_collection.cend();
  for( ; Lct != Lctend; Lct++) {

    if(Lct->subsystem() != 1) continue;

    if (printLevel>1) cout << "\nLCT CSC " << lctId << endl;
    
    CSCDetId id                = Lct->detId<CSCDetId>();
    auto lct_station           = id.station();
    auto lct_endcap            = id.endcap();
    auto lct_chamber           = id.chamber();
    uint16_t lct_bx            = Lct->getCSCData().bx;
    int lct_ring               = id.ring();
    int lct_sector             = CSCTriggerNumbering::triggerSectorFromLabels(id);
    int lct_subSector          = CSCTriggerNumbering::triggerSubSectorFromLabels(id);
    uint16_t lct_bx0           = Lct->getCSCData().bx0;
    uint16_t lct_cscID         = Lct->getCSCData().cscID;
    uint16_t lct_strip         = Lct->getCSCData().strip;
    uint16_t lct_pattern       = Lct->getCSCData().pattern;
    uint16_t lct_bend          = Lct->getCSCData().bend;
    uint16_t lct_quality       = Lct->getCSCData().quality;
    uint16_t lct_keywire       = Lct->getCSCData().keywire;
    //int fpga    = ( lct_subSector ? lct_subSector-1 : lct_station);
    
    
    double lct_phi             = Lct->getCMSGlobalPhi();
    double lct_eta             = Lct->getCMSGlobalEta();

    if ( printLevel > 0 ) {
      //cout << "\nLCT CSC " << lctId
      cout << "\n======\n";
      cout <<"lctEndcap       = " << lct_endcap << endl;
      cout <<"lctSector       = " << lct_sector<< endl;
      cout <<"lctSubSector    = " << lct_subSector << endl;
      cout <<"lctStation      = " << lct_station << endl;
      cout <<"lctRing         = " << lct_ring << endl;
      cout <<"lctChamber      = " << lct_chamber << endl;
      cout <<"lctTriggerCSCID = " << lct_cscID << endl;
      cout <<"lctBx           = " << lct_bx << endl;
      cout <<"lctBx0          = " << lct_bx0 << endl;
      cout <<"lctKeyWire      = " << lct_keywire << endl;
      cout <<"lctStrip        = " << lct_strip << endl;
      cout <<"lctBend         = " << lct_bend << endl;
      cout <<"lctQuality      = " << lct_quality << endl;
      cout <<"lct_pattern     = " << lct_pattern << endl;
      //cout <<"lct fpga        = " << fpga << endl;
      cout <<"phi global      = " << lct_phi << endl;
      cout <<"eta global      = " << lct_eta << endl;
    }

    ev.lctEndcap -> push_back(lct_endcap);
    ev.lctSector -> push_back(lct_sector);
    ev.lctSubSector -> push_back(lct_subSector);
    ev.lctStation -> push_back(lct_station);
    ev.lctRing -> push_back(lct_ring);
    ev.lctChamber -> push_back(lct_chamber);
    ev.lctTriggerCSCID -> push_back(lct_cscID);
    ev.lctBx -> push_back(lct_bx);
    ev.lctBx0 -> push_back(lct_bx0);
    ev.lctWire -> push_back(lct_keywire);
    ev.lctStrip -> push_back(lct_strip);
    ev.lctGlobalPhi -> push_back(lct_phi);
    ev.lctGlobalEta -> push_back(lct_eta);


    /*
    int EndCapLUT = 1;
    if(lct_endcap==2) EndCapLUT= 0; 
    
    //    Check if DetId is within range
    if( lct_sector < 1   || lct_sector > 12 ||
	lct_station < 1  || lct_station >  4 ||
	lct_cscID < 1    || lct_cscID >  9 ||
	EndCapLUT > 2    || EndCapLUT < 0 ||
	fpga > 5         || fpga < 0 )
      {
	if (printLevel > 1) cout << "  LCT ERROR: CSC digi are out of range! " << endl;;
	continue;
      }
    
    lclphidat lclPhi;
    try {
      lclPhi = srLUTs_[fpga][EndCapLUT] -> localPhi(lct_strip, lct_pattern, lct_quality, lct_bend);
    } 
    catch(cms::Exception &) {
      bzero(&lclPhi,sizeof(lclPhi));
    }
    
    gblphidat gblPhi;
    try {
      gblPhi = srLUTs_[fpga][EndCapLUT] -> globalPhiME(lclPhi.phi_local, lct_keywire, lct_cscID);
    } 
    catch(cms::Exception &) {
      bzero(&gblPhi,sizeof(gblPhi));
    }

    gbletadat gblEta;
    try {
      gblEta = srLUTs_[fpga][EndCapLUT] -> globalEtaME(lclPhi.phi_bend_local, lclPhi.phi_local, lct_keywire, lct_cscID);
    } 
    catch(cms::Exception &) {
      bzero(&gblEta,sizeof(gblEta));
    }
    
    
    // in global form
    float lct_gbleta = ts->getRegionalEtaScale(2)->getCenter(gblEta.global_eta);

    if (lct_endcap == 1) lct_gbleta = abs(lct_gbleta);

    //float lct_gblphi = fmod( gblPhi.global_phi +14.0*M_PI/180+(lct_sector-1)*60.0*M_PI/180, 2.*M_PI );
    float lct_gblphi = fmod(gblPhi.global_phi + ((lct_sector-1)*TMath::Pi()/3) + //sector 1 starts at 15 degrees
	 (TMath::Pi()/12) , 2*TMath::Pi());

    if (lct_gblphi > M_PI) lct_gblphi -= 2.*M_PI;

    if (printLevel>1) {
      cout <<"phi packed      = " << gblPhi.global_phi << endl;
      cout <<"eta packed      = " << gblEta.global_eta << endl;
      //cout <<"phi global      = " << ev.lctGlobalPhi[lctId] << endl;
      //cout <<"eta global      = " << ev.lctGlobalEta[lctId] << endl;
    }
    
    // Fill the branch vectors
    //ev.lctGlobalPhi -> push_back(lct_gblphi);
    //ev.lctGlobalEta -> push_back(lct_gbleta);
    ev.lctLocPhi -> push_back(gblPhi.global_phi);
    ev.lctLocEta -> push_back(gblEta.global_eta);
    */


    
    lctId++;

  } // end LCT loop
  
  ev.numLCTs = lctId;
  
} // end fillAllLCTs



/*
  for(CSCCorrelatedLCTDigiCollection::DigiRangeIterator csc=LCTs.product()->begin(); csc!=LCTs.product()->end(); csc++) {
  CSCCorrelatedLCTDigiCollection::Range range1 = LCTs.product()->get((*csc).first);
  for(CSCCorrelatedLCTDigiCollection::const_iterator Lct = range1.first; Lct != range1.second; Lct++, lctId++) {
  
  int lct_endcap    = (*csc).first.endcap()-1;
  int lct_station   = (*csc).first.station()-1;
  int lct_sector    = (*csc).first.triggerSector()-1;
  int lct_subSector = CSCTriggerNumbering::triggerSubSectorFromLabels((*csc).first);
  int lct_ring      = (*csc).first.ring();
  int lct_cscId     = (*csc).first.triggerCscId()-1;
  int lct_chamber   = (*csc).first.chamber()-1;
*/

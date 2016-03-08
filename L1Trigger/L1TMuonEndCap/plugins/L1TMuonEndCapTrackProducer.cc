///////////////////////////////////////////////////////////////
// Upgraded Encdap Muon Track Finding Algorithm		     //
//							     //
// Info: A human-readable version of the firmware based      //
//       track finding algorithm which will be implemented   //
//       in the upgraded endcaps of CMS. DT and RPC inputs   //
//	     are not considered in this algorithm.           //
//							     //
// Author: M. Carver (UF)				     //
///////////////////////////////////////////////////////////////

// Which of these includes are really needed?  Should try to cull - AWB 15.02.16

#include "L1Trigger/L1TMuonEndCap/plugins/L1TMuonEndCapTrackProducer.h"
#include "L1Trigger/CSCCommonTrigger/interface/CSCPatternLUT.h"
#include "L1Trigger/CSCTrackFinder/test/src/RefTrack.h"

#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#include "L1Trigger/L1TMuonEndCap/interface/PrimitiveConverter.h"
#include "L1Trigger/L1TMuonEndCap/interface/BXAnalyzer.h"
#include "L1Trigger/L1TMuonEndCap/interface/ZoneCreation.h"
#include "L1Trigger/L1TMuonEndCap/interface/PatternRecognition.h"
#include "L1Trigger/L1TMuonEndCap/interface/SortSector.h"
#include "L1Trigger/L1TMuonEndCap/interface/Matching.h"
#include "L1Trigger/L1TMuonEndCap/interface/Deltas.h"
#include "L1Trigger/L1TMuonEndCap/interface/BestTracks.h"
#include "L1Trigger/L1TMuonEndCap/interface/PtAssignment.h"
#include "L1Trigger/L1TMuonEndCap/interface/MakeRegionalCand.h"

#include "DataFormats/L1TMuon/interface/EMTF/InternalTrack.h"

// Can we move out of the L1TMuon namespace? Should we? - AWB 15.02.16
using namespace L1TMuon;


// Any collection you want to save in the output root file must be declared here.
// Additionally, you must declare the collection class in
// DataFormats/L1TMuon/src/classes.h and DataFormats/L1TMuon/src/classes_def.xml
L1TMuonEndCapTrackProducer::L1TMuonEndCapTrackProducer(const PSet& p) {
  
  inputTokenCSC = consumes<CSCCorrelatedLCTDigiCollection>(p.getParameter<edm::InputTag>("CSCInput"));
  
  produces< l1t::RegionalMuonCandBxCollection >("EMTF");
  // produces< std::vector<L1TMuon::InternalTrack> >("EMTF");
  // produces< L1TMuon::InternalTrackCollection >("EMTF");
  produces< l1t::emtf::InternalTrackCollection >("EMTF");
  
  // To set the phi and eta values of the LCTs
  // Following the example of plugins/deprecate/L1TMuonTriggerPrimitiveProducer.cc
  geom.reset(new GeometryTranslator());
}


// This is the main function which runs the emulator
void L1TMuonEndCapTrackProducer::produce(edm::Event& ev,
					 const edm::EventSetup& es) {

  // es.get<MuonGeometryRecord>().get(cscGeom);
  geom->checkAndUpdateGeometry(es);
  
  // Should implement proper error-checking, with options in python cfg file - AWB 15.02.16
  // bool verbose = false;
  // Should perhaps include a "Helper" class to define basic quantities like pi - AWB 15.02.16
  float pi = 3.14159265359;
  
  //std::cout<<"Start Upgraded Track Finder Producer::::: event = "<<ev.id().event()<<"\n\n";
  
  // Is this still at all useful? - AWB 15.02.16
  //fprintf (write,"12345\n"); //<-- part of printing text file to send verilog code, not needed if George's package is included
  
  // Create pointers to the collections you want to output
  // These collections should also be declared in L1TMuonEndCapTrackProducer::L1TMuonEndCapTrackProducer
  std::auto_ptr<l1t::RegionalMuonCandBxCollection > OutputCands (new l1t::RegionalMuonCandBxCollection);
  // std::auto_ptr<L1TMuon::InternalTrackCollection> FoundTracks (new L1TMuon::InternalTrackCollection);
  // std::auto_ptr< std::vector<L1TMuon::InternalTrack> > FoundTracks (new std::vector< L1TMuon::InternalTrack> );
  std::auto_ptr<l1t::emtf::InternalTrackCollection> FoundTracksNew (new l1t::emtf::InternalTrackCollection);
  
  
  // BTrack is a struct defined in interface/EmulatorClasses.h
  // It only contains Winner winner, int phi, int theta, int clctpattern, 
  // std::vector<std::vector<int>> deltas, and std::vector<ConvertedHit> AHits
  // BTracks are presumably used internally, since they are integer-defined
  // Should deprecate and simply use an InternalTrack class object - AWB 15.02.16
  // Also, why are there only 12? - AWB 15.02.16
  std::vector<BTrack> PTracks[12];

  // ConvertedHit is a class also defined in interface/EmulatorClasses.h
  // Again, this functionality should be folded into CSCPrimitive

  // TriggerPrimitive is a class defined in L1Trigger/L1TMuon/interface/deprecate/MuonTriggerPrimitive.h
  // It has functions defined in L1Trigger/L1TMuon/src/MuonTriggerPrimitive.cc
  // "tester" seems to be all the TriggerPrimitives in the event
  // It is converted into vec<ConvertedHits> ConvHits
  // These functionalities should be imported into CSCPrimitive - AWB 15.02.16
  std::vector<TriggerPrimitive> tester;
  
  //////////////////////////////////////////////
  ///////// Make Trigger Primitives ////////////
  //////////////////////////////////////////////
  
  // CSCCorrelatedLCTDigi defined in DataFormats/CSCDigi/interface/CSCCorrelatedLCTDigi.h
  // Functions defined in DataFormats/CSCDigi/src/CSCCorrelatedLCTDigi.cc
  edm::Handle<CSCCorrelatedLCTDigiCollection> MDC;
  ev.getByToken(inputTokenCSC, MDC);
  // It's not clear why we need both "out" and "tester" - AWB 15.02.16
  std::vector<TriggerPrimitive> out;
  
  // CSCCorrelatedLCTDigiCollection defined in DataFormats/CSCDigi/interface/CSCCorrelatedLCTDigiCollection.h, as
  // typedef MuonDigiCollection<CSCDetId,CSCCorrelatedLCTDigi> CSCCorrelatedLCTDigiCollection;
  // CSCDetId is defined in DataFormats/MuonDetId/interface/CSCDetId.h
  // Why do we only loop from second.first to second.second, and not second.last? - AWB 15.02.16
  // All we are storing in each "out" TriggerPrimitive is "first, second" from the CSCCorrelatedLCTDigiCollection object -
  // i.e., all there is of the object.  Why do we save it as a TriggerPrimitive, and not just pass the 
  // (CSCDetId, CSCCorrelatedLCTDigi)? - AWB 15.02.16
  for (auto chamber = MDC->begin(); chamber != MDC->end(); ++chamber) {
    for (auto digi = (*chamber).second.first; digi != (*chamber).second.second; ++digi) {
      out.push_back( TriggerPrimitive((*chamber).first, *digi) );
    }
  }
  

  // Is it true that this block "currently does nothing"? - AWB 15.02.16
  //////////////////////////////////////////////
  ///////// Get Trigger Primitives /////////////  Retrieve TriggerPrimitives from the event record: Currently does nothing because we don't take RPC's
  //////////////////////////////////////////////

  // auto tpsrc = _tpinputs.cbegin();
  // auto tpend = _tpinputs.cend();
  // for( ; tpsrc != tpend; ++tpsrc ) {
  //   edm::Handle<TriggerPrimitiveCollection> tps;
  //   ev.getByLabel(*tpsrc,tps);
    
  // Loop over the trigger primitives
  for (auto tp = out.cbegin(); tp != out.cend(); ++tp) {
    // subsystem() returns a subsystem_type: kDT, kCSC, kRPC, or kNSubsystems
    // Not sure what a value of "1" means - maybe just that there is some subsystem_type?
    // Is substem_type defined somewhere? - AWB 15.02.16
    if (tp->subsystem() == 1) {
	tester.push_back(*tp);
	// if(verbose) std::cout<<"\ntrigger prim found station:"<<tp->detId<CSCDetId>().station()<<std::endl;
      }
  }
  // }

  std::vector<ConvertedHit> CHits[12];
  MatchingOutput MO[12];

  // Loop over all 12 sectors
  // Sectors 1-6 in the positive endcap have SectIndex 0-5; in the negative endcap, 6-11
  for (int SectIndex=0; SectIndex < 12; SectIndex++) {

    //////////////////////////////////////////////////////  Input is raw hit information from ___? - AWB 15.02.16
    ///////////////// TP Conversion //////////////////////  Output is vector of Converted Hits
    //////////////////////////////////////////////////////
    
    // PrimConv is defined in interface/PrimitiveConverter.h
    // It does an immense amount of work
    // Should be left untouched for now, except that the output should be CSCPrimitive instead of ConvertedHit - AWB 15.02.16
    std::vector<ConvertedHit> ConvHits = PrimConv(tester,SectIndex);
    CHits[SectIndex] = ConvHits;


    //////////////////////////////////////////////////////  Takes the vector of converted hits and groups into 3 groups of hits
    ////////////////////// BX Grouper ////////////////////  which are 3 BX's wide. Effectively looking 2 BX's into the future and
    //////////////////////////////////////////////////////  past from the central BX, this analyzes a total of 5 BX's.
    
    // GroupBX defined in interface/BXAnalyzer.h
    std::vector<std::vector<ConvertedHit>> GroupedHits = GroupBX(ConvHits);

    
    ////////////////////////////////////////////////////////  Creates a zone for each of the three groups created in the BX Grouper module.
    ////////// Create Zones for pattern Recognition ////////  The output of this module not only contains the zones but also the
    ////////////////////////////////////////////////////////  reference back to the TriggerPrimitives that went into making them.

    // Zones defined in interface/ZoneCreation.h
    // struct ZonesOutput defined in interface/EmulatorClasses.h - contains
    // vectors of PhiMemoryImage and ConvertedHit
    std::vector<ZonesOutput> Zout = Zones(GroupedHits);


    ///////////////////////////////
    ///// Pattern Recognition /////  Applies pattern recognition logic on each of the 3 BX groups and assigns a quality to each keystrip in the zone.
    ///// & quality assinment /////  The delete duplicate patterns function looks at the 3 BX groups and deletes duplicate patterns found from the
    ///////////////////////////////  same hits. This is where the BX analysis ends; Only 1 list of found patterns is given to the next module.


    // Patterns defined in interface/PatternRecognition.h
    // struct PatternOutput defined in interface/EmulatorClasses.h - contains
    // a QualityOutput and a vector of ConvertedHit
    std::vector<PatternOutput> Pout = Patterns(Zout);
  
    // DeleteDuplicatePatterns defined in interface/BXAnalyzer.h
    PatternOutput Test = DeleteDuplicatePatterns(Pout);

    // PrintQuality defined in interface/PatternRecognition.h
    // PrintQuality(Test.detected);


    ///////////////////////////////
    //////Sector Sorting/////////// Sorts through the patterns found in each zone and selects the best three per zone to send to the next module.
    ///////Finding 3 Best Pattern//
    ///////////////////////////////

    // SortSect defined in interface/SortSector.h - contains
    // class SortingOutput defined in interface/EmulatorClasses.h - contains
    // vectors of Winner and ConvertedHit
    SortingOutput Sout = SortSect(Test);
    

    //////////////////////////////////
    ///////// Match phi patterns ///// Loops over each sorted pattern and then loops over all possible triggerprimitives which could have made 
    ////// to segment inputs ///////// the pattern and matches the associated full precision triggerprimitives to the detected pattern.
    //////////////////////////////////

    // PhiMatching defined in interface/Matching.h
    // class MathchingOutput defined in interface/EmulatorClasses.h - contains
    // ThOutput, PhOutput, and vectors of ConvertedHit, Winner, and int segment
    MatchingOutput Mout = PhiMatching(Sout);
    MO[SectIndex] = Mout;

    /////////////////////////////////
    //////// Calculate delta //////// Once we have matched the hits we calculate the delta phi and theta between all
    //////// phi and theta   //////// stations present.
    /////////////////////////////////

    // CalcDeltas defined in interface/Deltas.h
    // class DeltaOutput defined in interface/EmulatorClasses.h - contains
    // MatchingOutput, vec<vec<int>> Deltas, int Phi, int Theta, and a Winner
    std::vector<std::vector<DeltaOutput>> Dout = CalcDeltas(Mout);////


    /////////////////////////////////
    /////// Sorts and gives /////////  Loops over all of the found tracks (looking across zones) and selects the best three per sector.
    ////// Best 3 tracks/sector /////  Here ghost busting is done to delete tracks which are comprised of the same associated stubs.
    /////////////////////////////////

    // BestTracks defined in interface/BestTracks.h
    std::vector<BTrack> Bout = BestTracks(Dout);
    PTracks[SectIndex] = Bout;


  } // End for (int SectIndex=0; SectIndex < 12; SectIndex++)


  ////////////////////////////////////
  /// Sorting through all sectors ////
  ///   to find 4 best muons      ////
  ////////////////////////////////////

  // Leftover from CSCTF with Muon Sorter
  // No longer just four tracks, but as many as are there - AWB 15.02.16
  // BTrack FourBest[4];
  BTrack AllBest[36];
  std::vector<BTrack> PTemp[12] = PTracks;
  // int windex[4] = {-1,-1,-1,-1};
  int windex[36] = {-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,
		    -1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1};
  
  // for (int i = 0; i < 4; i++) {
  for (int i = 0; i < 36; i++) {
    for (int j = 0; j < 36; j++) {

      if (!PTemp[j/3][j%3].phi) // No track
	continue;
      
      // if ( (windex[0] == j) || (windex[1] == j) || (windex[2] == j) || (windex[3] == j) ) // Already picked
      // 	continue;
      
      if ( ( windex[0] == j) ||  (windex[1] == j) ||  (windex[2] == j) ||  (windex[3] == j) ||  (windex[4] == j) ||  (windex[5] == j) || 
	   ( windex[6] == j) ||  (windex[7] == j) ||  (windex[8] == j) ||  (windex[9] == j) || (windex[10] == j) || (windex[11] == j) ||
	   (windex[12] == j) || (windex[13] == j) || (windex[14] == j) || (windex[15] == j) || (windex[16] == j) || (windex[17] == j) ||
	   (windex[18] == j) || (windex[19] == j) || (windex[20] == j) || (windex[21] == j) || (windex[22] == j) || (windex[23] == j) ||
	   (windex[24] == j) || (windex[25] == j) || (windex[26] == j) || (windex[27] == j) || (windex[28] == j) || (windex[29] == j) ||
	   (windex[30] == j) || (windex[31] == j) || (windex[32] == j) || (windex[33] == j) || (windex[34] == j) || (windex[35] == j) ) 
	continue; // Already picked
      
      if (PTracks[j/3][j%3].winner.Rank() > AllBest[i].winner.Rank()) {
	AllBest[i] = PTemp[j/3][j%3];
	windex[i] = j;
      }
    }
  }

  ///////////////////////////////////
  /// Make Internal track if ////////
  /////// tracks are found //////////
  ///////////////////////////////////

  // for (int fbest=0; fbest < 4; fbest++) {
  for (int all_best=0; all_best < 36; all_best++) {
    
    if (AllBest[all_best].phi) {
      
      InternalTrack tempTrack;
      tempTrack.setType(2);
      tempTrack.phi = AllBest[all_best].phi;
      tempTrack.theta = AllBest[all_best].theta;
      tempTrack.rank = AllBest[all_best].winner.Rank();
      tempTrack.deltas = AllBest[all_best].deltas;
      
      l1t::emtf::InternalTrack tempTrackNew;
      tempTrackNew.set_type          (  2                                          );
      tempTrackNew.set_phi_local_deg ( (AllBest[all_best].phi / 60.0) - 2.0        ); // The "phi_full" conversion. Right? - AWB 13.02.16
      tempTrackNew.set_phi_local_rad (  tempTrackNew.Phi_local_deg() * (pi/180)    ); 
      tempTrackNew.set_theta_loc     (  AllBest[all_best].theta                    ); // This is some bizzare local definition of theta
      tempTrackNew.set_theta_deg     ( (AllBest[all_best].theta * 0.2851562) + 8.5 ); // This is the true global |theta| in degrees; set to theta later
      tempTrackNew.set_theta_rad     (  tempTrackNew.Theta_deg() * (pi/180)        ); // This is the true global |theta| in radians; set to theta later
      tempTrackNew.set_eta           ( -1 * log( tan( tempTrackNew.Theta_rad()/2 ) ) ); // This is the global |eta|; set to eta later
      tempTrackNew.set_rank          (  AllBest[all_best].winner.Rank() );

      int tempStraightness = 0;
      int tempRank = tempTrackNew.Rank();
      if(tempRank & 64)
	tempStraightness |= 4;
      if(tempRank & 16)
	tempStraightness |= 2;
      if(tempRank & 4)
	tempStraightness |= 1;

      tempTrackNew.set_straightness ( tempStraightness );

      // Can't have a vector of vectors of vectors in ROOT files
      // tempTrackNew.set_deltas(AllBest[all_best].deltas);
      
      std::vector<int> ps, ts;
      
      int sector = -1;
      bool ME13 = false;
      int me1address = 0, me2address = 0, CombAddress = 0, mode = 0;
      
      int first_lct_bx = -99;
      int second_lct_bx = -99;
      for (std::vector<ConvertedHit>::iterator A = AllBest[all_best].AHits.begin(); A != AllBest[all_best].AHits.end(); A++) {
	
	l1t::emtf::CSCPrimitive tempStub;

	if (A->Phi() != -999) {
	  
	  int station = A->TP().detId<CSCDetId>().station();
	  int id = A->TP().getCSCData().cscID;
	  int trknm = A->TP().getCSCData().trknmb;
	  
	  tempTrack.addStub(A->TP());
	  // tempTrackNew.add_stub(); // AWB TODO
	  ps.push_back(A->Phi());
	  ts.push_back(A->Theta());
	  sector = (A->TP().detId<CSCDetId>().endcap() -1)*6 + A->TP().detId<CSCDetId>().triggerSector() - 1;

	  // std::cout << "In track " << all_best << ", station " << station << ", A->Theta() = " << A->Theta() << ", A->Phi() = " << A->Phi() << std::endl;
	  // std::cout << "A->Quality() =  "<< A->Quality() <<", A->Wire() = "<< A->Wire() << ", A->Strip() = " << A->Strip() << std::endl;
	  
	  // CSCDetId variables defined in: 
	  // https://github.com/cms-l1t-offline/cmssw/blob/l1t-muon-pass2-CMSSW_8_0_0_pre5/DataFormats/MuonDetId/interface/CSCDetId.h
	  // ConvertedHit values defined in interface/EmulatorClasses.h
	  tempStub.set_endcap        ( ( A->TP().detId<CSCDetId>().endcap() == 1 ) ? 1 : -1 );
	  tempStub.set_station       ( A->TP().detId<CSCDetId>().station()       );
	  tempStub.set_ring          ( A->TP().detId<CSCDetId>().ring()          );
	  tempStub.set_sector        ( A->TP().detId<CSCDetId>().triggerSector() ); // Using the +/- 1-6 convention, rather than 0-11, for now
	  tempStub.set_chamber       ( A->TP().detId<CSCDetId>().chamber()       );
	  tempStub.set_layer         ( A->TP().detId<CSCDetId>().layer()         );
	  tempStub.set_csc_ID        ( A->TP().getCSCData().cscID                );
	  tempStub.set_mpc_link      ( A->TP().getCSCData().mpclink              );
	  tempStub.set_wire          ( A->TP().getCSCData().keywire              );
	  tempStub.set_strip         ( A->TP().getCSCData().strip                );
	  tempStub.set_track_num     ( A->TP().getCSCData().trknmb               );
	  tempStub.set_phi_local_deg ( (A->Phi() / 60.0) - 2.0                   ); // The "phi_full" conversion. Right? - AWB 13.02.16
	  tempStub.set_phi_local_rad ( tempStub.Phi_local_deg() * (pi/180)       ); 
	  tempStub.set_phi_global_deg( tempStub.Phi_local_deg() + 60 * (tempStub.Sector() - 1) ); // Only holds using 1-6 sector convention
	  // Correct for 15 deg. offset, set range to -180 to 180
	  tempStub.set_phi_global_deg( (tempStub.Phi_global_deg() < 345) ? tempStub.Phi_global_deg() + 15 : tempStub.Phi_global_deg() - 345 ); 
	  tempStub.set_phi_global_deg( (tempStub.Phi_global_deg() < 180) ? tempStub.Phi_global_deg()      : tempStub.Phi_global_deg() - 360 );
	  tempStub.set_phi_global_rad( tempStub.Phi_global_deg() * (pi/180)      ); 
	  tempStub.set_theta_loc     ( A->Theta()                                ); // This is some bizzare local definition of theta
	  tempStub.set_theta_deg     ( (tempStub.Endcap() == 1)  * ( (A->Theta() * 0.2851562) + 8.5) + // This is the true global theta in degrees
				       (tempStub.Endcap() == -1) * (180 - ( (A->Theta() * 0.2851562) + 8.5) ) ); 
	  tempStub.set_theta_rad     ( tempStub.Theta_deg() * (pi/180)           ); // This is the true global theta in radians
	  tempStub.set_eta           ( -1 * log( tan( tempStub.Theta_rad()/2 ) ) );
	  tempStub.set_quality       ( A->TP().getCSCData().quality              );
	  tempStub.set_pattern       ( A->TP().getCSCData().pattern              );
	  tempStub.set_bend          ( A->TP().getCSCData().bend                 );
	  tempStub.set_valid         ( A->TP().getCSCData().valid                );
	  tempStub.set_sync_err      ( A->TP().getCSCData().syncErr              );
	  tempStub.set_bx0           ( A->TP().getCSCData().bx0                  );
	  tempStub.set_bx            ( A->TP().getCSCData().bx - 6               ); // Offset so center BX is at 0
	  if (tempStub.BX() >= 725444449) {
	    std::cout << "Why does tempStub.BX() == " << tempStub.BX() << " ?  Resetting to -99." << std::endl;
	    tempStub.set_bx(-99);
	  }
	  
	  if ( tempStub.BX() >= first_lct_bx ) {
	    second_lct_bx = first_lct_bx;
	    first_lct_bx = tempStub.BX();
	  }

	  if ( tempStub.Quality() != A->Quality() )
	    std::cout << "A->TP().getCSCData().quality == " <<  A->TP().getCSCData().quality << " but A->Quality() == " << A->Quality() << std::endl;
	  if ( A->TP().getCSCData().pattern != A->Pattern() )
	    std::cout << "A->TP().getCSCData().pattern == " << A->TP().getCSCData().pattern << " but A->Pattern() == " << A->Pattern() << std::endl;


	  // if ( ev.id().event() == 205987364 ||
	  //      ev.id().event() == 208080931 ||
	  //      ev.id().event() == 207364106 ||
	  //      ev.id().event() == 208851566 ||
	  //      ev.id().event() == 208568537 ||
	  //      ev.id().event() == 210559179 ||
	  //      ev.id().event() == 209911185 ||
	  //      ev.id().event() == 357576086 ||
	  //      ev.id().event() == 370173370 ||
	  //      ev.id().event() == 433124505 ||
	  //      ev.id().event() == 445076529 ||
	  //      ev.id().event() == 451674044 ||
	  //      ev.id().event() == 463482814 ||
	  //      ev.id().event() == 469847518 )

      // 	  TriggerPrimitive tempPrim = A->TP();
      // 	  CSCDetId tempDetId = tempPrim.detId<CSCDetId>();
      // 	  // if (tempDetId.station() == 1 && tempDetId.ring() == 1 && tempPrim.getCSCData().strip > 127) {
      // 	    // Set ring to 4
      // 	    tempDetId = CSCDetId( tempDetId.endcap(), tempDetId.station(), 4, tempDetId.chamber(), tempDetId.layer() );
      // 	    // const CSCLayer* tempLayer = cscGeom->layer( tempDetId );
      // 	    // GlobalPoint tempGPstrip = tempLayer->centerOfStrip( tempPrim.getCSCData().strip );
      // 	    GlobalPoint tempGPstrip = cscGeom->layer( tempDetId )->centerOfStrip( tempPrim.getCSCData().strip );
      // 	    // GlobalPoint tempGPwire = tempLayer->centerOfWireGroup( tempStub.Wire() );

      // 	    std::cout << tempGPstrip.eta() << std::endl;
      // 	    // std::cout << tempGPwire.phi() << std::endl;
      // 	    // // How do we access the CSCCorrelatedLCTDigi from A->TP()?
      // 	    // tempPrim = TriggerPrimitive(tempDetId, CSCCorrelatedLCTDigi);
      // 	    // }
	    
      	  tempStub.set_phi_geom_rad ( geom->calculateGlobalPhi(A->TP()) );

      // 	  // // tempStub.set_phi_geom_rad ( geom->calculateGlobalPhi(tempPrim) );
	  
      // 	  // // if ( abs(tempStub.Phi_global_rad() - tempStub.Phi_geom_rad()) > 0.05 && abs(tempStub.Phi_global_rad()) < 3.1 ) {
      // 	  //   std::cout << "In event " << ev.id().event() << ", Emu phi = " << tempStub.Phi_global_rad() << 
      // 	  //     ", new Geom phi = " << tempGPstrip.phi() << " / " << tempGPwire.phi() << ", and old Geom phi = " << tempStub.Phi_geom_rad() << std::endl;
      // 	  //   std::cout << "Emu eta = " << tempStub.Eta() << ", new Geom eta = " << tempGPstrip.eta() << " / " << tempGPwire.eta() << std::endl;
      // 	  //   std::cout << "Endcap " << tempStub.Endcap() << ", station " << tempStub.Station() << ", ring " << tempStub.Ring() << ", sector " << tempStub.Sector() << std::endl;
      // 	  //   std::cout << "Chamber " << tempStub.Chamber() << ", layer " << tempStub.Layer() << ", wire " << tempStub.Wire() << ", strip " << tempStub.Strip() << std::endl;
      // 	  //   // std::cout << "tempPrim.detId<CSCDetId>().ring() == " << tempPrim.detId<CSCDetId>().ring() << std::endl;
      // 	  //   // }	      

      // // std::cout << "Trigger Primitive phi = " << geom->calculateGlobalPhi( TriggerPrimitive((*chamber).first, *digi) ) << std::endl;
      // // std::cout << "Trigger Primitive eta = " << geom->calculateGlobalEta( TriggerPrimitive((*chamber).first, *digi) ) << std::endl;

	  
	  if (tempTrackNew.NumCSCPrimitives() == 0) {
	    tempTrackNew.set_endcap( tempStub.Endcap() );
	    tempTrackNew.set_sector( tempStub.Sector() ); // Using the +/- 1-6 convention, rather than 0-11, for now
	    if (tempStub.Endcap() == -1) {
	      tempTrackNew.set_theta_deg( 180 - tempTrackNew.Theta_deg() ); // This is the true global theta in degrees
	      tempTrackNew.set_theta_rad( pi  - tempTrackNew.Theta_rad() ); // This is the true global theta in radians
	      tempTrackNew.set_eta      ( -1  * tempTrackNew.Eta()       );
	    }
	  }
	  
	  tempTrackNew.push_CSCPrimitive ( tempStub );
	  
	  switch (station) {
	  case 1: mode |= 8; break;
	  case 2: mode |= 4; break;
	  case 3: mode |= 2; break;
	  case 4: mode |= 1; break;
	  default: mode |= 0;
	  }

	  if (A->TP().detId<CSCDetId>().station() == 1 && A->TP().detId<CSCDetId>().ring() == 3)
	    ME13 = true;
	  
	  if (station == 1 && id > 3 && id < 7) {
	    
	    int sub = 2;
	    if(A->TP().detId<CSCDetId>().chamber()%6 > 2)
	      sub = 1;
	    
	    me1address = id;
	    me1address -= 3;
	    me1address += 3*(sub - 1);
	    me1address = id << 1;
	    me1address |= trknm-1;
	  }
	  
	  if (station == 2 && id > 3) {
	    me2address = id;
	    me2address -= 3;
	    me2address = me2address<<1;
	    me2address |= trknm-1;
	  }
	} // End if (A->Phi() != -999)
      } // End loop for (std::vector<ConvertedHit>::iterator A = AllBest[all_best].AHits.begin(); A != AllBest[all_best].AHits.end(); A++)
      
      tempTrack.phis = ps;
      tempTrack.thetas = ts;
      tempTrackNew.set_phis(ps); 
      tempTrackNew.set_thetas(ts); 
      
      float xmlpt = CalculatePt(tempTrack,es);
      tempTrack.pt = xmlpt*1.4;
      tempTrackNew.set_pt(xmlpt*1.4); // Is this the "right" pT Defined how? - AWB 13.02.16
      tempTrackNew.set_pt_int( floor( (xmlpt*1.4)*2 + 1) ); // Convert to integer-stored value  
      
      CombAddress = (me2address<<4) | me1address;
      
      // Why do we send the local theta value to MakeRegionalCand?  Is xmlpt or 1.4*xmlpt the "accurate" value? - AWB 13.02.16
      l1t::RegionalMuonCand outCand = MakeRegionalCand(xmlpt*1.4,AllBest[all_best].phi,AllBest[all_best].theta,
						       CombAddress,mode,1,sector);
      // std::cout << "mode =  " << mode << std::endl;
      tempTrackNew.set_mode  ( mode );

      tempTrackNew.set_bx ( (second_lct_bx > -99) ? second_lct_bx : first_lct_bx );
      // tempTrackNew.set_sector( sector );  // Commented b/c we're using the +/- 1-6 convention (above), rather than 0-11, for now
      tempTrackNew.set_phi_global_deg ( tempTrackNew.Phi_local_deg() + 60 * (tempTrackNew.Sector() - 1) );
      // Correct for 15 deg. offset, set range to -180 to 180
      tempTrackNew.set_phi_global_deg ( (tempTrackNew.Phi_global_deg() < 345) ? tempTrackNew.Phi_global_deg() + 15 : tempTrackNew.Phi_global_deg() - 345 ); 
      tempTrackNew.set_phi_global_deg ( (tempTrackNew.Phi_global_deg() < 180) ? tempTrackNew.Phi_global_deg()      : tempTrackNew.Phi_global_deg() - 360 );
      tempTrackNew.set_phi_global_rad ( tempTrackNew.Phi_global_deg() * (pi/180) ); 
      
      // FoundTracks->push_back(tempTrack);
      FoundTracksNew->push_back(tempTrackNew);
      
      // NOTE: assuming that all candidates come from the central BX:
      int bx = 0;
      float theta_angle = (AllBest[all_best].theta*0.2851562 + 8.5)*(pi/180);
      float eta = (-1)*log(tan(theta_angle/2));
      if(!ME13 && fabs(eta) > 1.1)
	OutputCands->push_back(bx, outCand);
      
    } // End if (AllBest[all_best].phi)
  } // End for (int all_best=0; all_best < ; all_best++)
  
  ev.put( OutputCands, "EMTF");
  // ev.put( FoundTracks, "EMTF");
  ev.put( FoundTracksNew, "EMTF");
  //std::cout<<"End Upgraded Track Finder Prducer:::::::::::::::::::::::::::\n:::::::::::::::::::::::::::::::::::::::::::::::::\n\n";
  
} // End void L1TMuonEndCapTrackProducer::produce

void L1TMuonEndCapTrackProducer::beginJob()
{
  
}
void L1TMuonEndCapTrackProducer::endJob()
{

}
#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(L1TMuonEndCapTrackProducer);

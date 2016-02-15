///////////////////////////////////////////////////////////////
// Upgraded Encdap Muon Track Finding Algorithm		    	//
//							   								//
// Info: A human-readable version of the firmware based     //
//       track finding algorithm which will be implemented  //
//       in the upgraded endcaps of CMS. DT and RPC inputs  //
//	     are not considered in this algorithm.      		//
//								   							//
// Author: M. Carver (UF)				    				//
//////////////////////////////////////////////////////////////


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

using namespace L1TMuon;


L1TMuonEndCapTrackProducer::L1TMuonEndCapTrackProducer(const PSet& p) {

  inputTokenCSC = consumes<CSCCorrelatedLCTDigiCollection>(p.getParameter<edm::InputTag>("CSCInput"));
  
  produces< l1t::RegionalMuonCandBxCollection >("EMTF");
  // produces< std::vector<L1TMuon::InternalTrack> >("EMTF");
  // produces< L1TMuon::InternalTrackCollection >("EMTF");
  produces< l1t::emtf::InternalTrackCollection >("EMTF");
}


void L1TMuonEndCapTrackProducer::produce(edm::Event& ev,
			       const edm::EventSetup& es) {

  //bool verbose = false;
  float pi = 3.14159265359;


  //std::cout<<"Start Upgraded Track Finder Producer::::: event = "<<ev.id().event()<<"\n\n";

  //fprintf (write,"12345\n"); //<-- part of printing text file to send verilog code, not needed if George's package is included

  std::auto_ptr<l1t::RegionalMuonCandBxCollection > OutputCands (new l1t::RegionalMuonCandBxCollection);
  // std::auto_ptr<L1TMuon::InternalTrackCollection> FoundTracks (new L1TMuon::InternalTrackCollection);
  // std::auto_ptr< std::vector<L1TMuon::InternalTrack> > FoundTracks (new std::vector< L1TMuon::InternalTrack> );
  std::auto_ptr<l1t::emtf::InternalTrackCollection> FoundTracksNew (new l1t::emtf::InternalTrackCollection);

  std::vector<BTrack> PTracks[12];

  std::vector<TriggerPrimitive> tester;
  
  //////////////////////////////////////////////
  ///////// Make Trigger Primitives ////////////
  //////////////////////////////////////////////
  
  edm::Handle<CSCCorrelatedLCTDigiCollection> MDC;
  ev.getByToken(inputTokenCSC, MDC);
  std::vector<TriggerPrimitive> out;
  
  auto chamber = MDC->begin();
  auto chend  = MDC->end();
  for( ; chamber != chend; ++chamber ) {
    auto digi = (*chamber).second.first;
    auto dend = (*chamber).second.second;
    for( ; digi != dend; ++digi ) {
      out.push_back(TriggerPrimitive((*chamber).first,*digi));
    }
  }
  

  //////////////////////////////////////////////
  ///////// Get Trigger Primitives /////////////  Retrieve TriggerPrimitives from the event record: Currently does nothing because we don't take RPC's
  //////////////////////////////////////////////

 // auto tpsrc = _tpinputs.cbegin();
  //auto tpend = _tpinputs.cend();
 // for( ; tpsrc != tpend; ++tpsrc ) {
   // edm::Handle<TriggerPrimitiveCollection> tps;
   // ev.getByLabel(*tpsrc,tps);
    auto tp = out.cbegin();
    auto tpend = out.cend();

    for( ; tp != tpend; ++tp ) {
      if(tp->subsystem() == 1)
      {
		//TriggerPrimitiveRef tpref(out,tp - out.cbegin());

		tester.push_back(*tp);

		//if(verbose) std::cout<<"\ntrigger prim found station:"<<tp->detId<CSCDetId>().station()<<std::endl;
      }

     }
   //}
  std::vector<ConvertedHit> CHits[12];
  MatchingOutput MO[12];

for(int SectIndex=0;SectIndex<12;SectIndex++){//perform TF on all 12 sectors



  //////////////////////////////////////////////////////  Input is raw hit information from
  ///////////////// TP Conversion //////////////////////  Output is vector of Converted Hits
  //////////////////////////////////////////////////////


 	std::vector<ConvertedHit> ConvHits = PrimConv(tester,SectIndex);
	CHits[SectIndex] = ConvHits;


/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////print values for input into Alex's emulator code/////////////////////////////////////////////////////
	//for(std::vector<ConvertedHit>::iterator h = ConvHits.begin();h != ConvHits.end();h++){

		//if((h->Id()) > 9){h->SetId(h->Id() - 9);h->SetStrip(h->Strip() + 128);}
		//fprintf (write,"0	1	1 	%d	%d\n",h->Sub(),h->Station());
		//fprintf (write,"1	%d	%d 	%d\n",h->Quality(),h->Pattern(),h->Wire());
		//fprintf (write,"%d	0	%d\n",h->Id(),h->Strip());
	//}
////////////////////////////////print values for input into Alex's emulator code/////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////



 //////////////////////////////////////////////////////
 //////////////////////////////////////////////////////  Takes the vector of converted hits and groups into 3 groups of hits
 ////////////////////// BX Grouper ////////////////////  which are 3 BX's wide. Effectively looking 2 BX's into the future and
 //////////////////////////////////////////////////////  past from the central BX, this analyzes a total of 5 BX's.
 //////////////////////////////////////////////////////


 std::vector<std::vector<ConvertedHit>> GroupedHits = GroupBX(ConvHits);


////////////////////////////////////////////////////////  Creates a zone for each of the three groups created in the BX Grouper module.
////////// Creat Zones for pattern Recognition /////////  The output of this module not only contains the zones but also the
////////////////////////////////////////////////////////  reference back to the TriggerPrimitives that went into making them.

 std::vector<ZonesOutput> Zout = Zones(GroupedHits);


  ///////////////////////////////
  ///// Pattern Recognition /////  Applies pattern recognition logic on each of the 3 BX groups and assigns a quality to each keystrip in the zone.
  ///// & quality assinment /////  The delete duplicate patterns function looks at the 3 BX groups and deletes duplicate patterns found from the
  ///////////////////////////////  same hits. This is where the BX analysis ends; Only 1 list of found patterns is given to the next module.


  std::vector<PatternOutput> Pout = Patterns(Zout);

  PatternOutput Test = DeleteDuplicatePatterns(Pout);

  //PrintQuality(Test.detected);


  ///////////////////////////////
  //////Sector Sorting/////////// Sorts through the patterns found in each zone and selects the best three per zone to send to the next module.
  ///////Finding 3 Best Pattern//
  ///////////////////////////////


  SortingOutput Sout = SortSect(Test);


  //////////////////////////////////
  ///////// Match ph patterns ////// Loops over each sorted pattern and then loops over all possible triggerprimitives which could have made the pattern
  ////// to segment inputs ///////// and matches the associated full precision triggerprimitives to the detected pattern.
  //////////////////////////////////


  MatchingOutput Mout = PhiMatching(Sout);
  MO[SectIndex] = Mout;

  /////////////////////////////////
  //////// Calculate delta //////// Once we have matched the hits we calculate the delta phi and theta between all
  ////////    ph and th    //////// stations present.
  /////////////////////////////////


 std::vector<std::vector<DeltaOutput>> Dout = CalcDeltas(Mout);////


  /////////////////////////////////
  /////// Sorts and gives /////////  Loops over all of the found tracks(looking across zones) and selects the best three per sector.
  ////// Best 3 tracks/sector /////  Here ghost busting is done to delete tracks which are comprised of the same associated stubs.
  /////////////////////////////////


  std::vector<BTrack> Bout = BestTracks(Dout);
   PTracks[SectIndex] = Bout;



  }

 ////////////////////////////////////
 /// Sorting through all sectors ////
 ///   to find 4 best muons      ////
 ////////////////////////////////////


 BTrack FourBest[4];//ok
 std::vector<BTrack> PTemp[12] = PTracks;
 int windex[4] = {-1,-1,-1,-1};



 for(int i=0;i<4;i++){

 	for(int j=0;j<36;j++){


			if(!PTemp[j/3][j%3].phi)//no track
				continue;

			if((windex[0] == j) || (windex[1] == j) || (windex[2] == j) || (windex[3] == j))//already picked
				continue;

			if(PTracks[j/3][j%3].winner.Rank() > FourBest[i].winner.Rank()){

				FourBest[i] = PTemp[j/3][j%3];
				windex[i] = j;

			}

 	}
}

  ///////////////////////////////////
  /// Make Internal track if ////////
  /////// tracks are found //////////
  ///////////////////////////////////

  for(int fbest=0;fbest<4;fbest++){

  	if(FourBest[fbest].phi){


		InternalTrack tempTrack;
  		tempTrack.setType(2);
		tempTrack.phi = FourBest[fbest].phi;
		tempTrack.theta = FourBest[fbest].theta;
		tempTrack.rank = FourBest[fbest].winner.Rank();
		tempTrack.deltas = FourBest[fbest].deltas;

		l1t::emtf::InternalTrack tempTrackNew;
		tempTrackNew.set_type      (  2                                        );
		tempTrackNew.set_phi_local ( (FourBest[fbest].phi / 60) - 2            ); // The "phi_full" conversion. Right? - AWB 13.02.16
		tempTrackNew.set_theta_loc (  FourBest[fbest].theta                    ); // This is some bizzare local definition of theta
		tempTrackNew.set_theta_deg ( (FourBest[fbest].theta * 0.2851562) + 8.5 ); // This is the true global |theta| in degrees; set to theta later
		tempTrackNew.set_theta_rad (  tempTrackNew.Theta_deg() * (pi/180)      ); // This is the true global |theta| in radians; set to theta later
		tempTrackNew.set_eta       ( -1 * log( tan( tempTrackNew.Theta_rad()/2 ) ) ); // This is the global |eta|; set to eta later
		tempTrackNew.set_rank      (  FourBest[fbest].winner.Rank() );
		// Can't have a vector of vectors of vectors in ROOT files
 		// tempTrackNew.set_deltas(FourBest[fbest].deltas);

		std::vector<int> ps, ts;

		int sector = -1;
		bool ME13 = false;
		int me1address = 0, me2address = 0, CombAddress = 0, mode = 0;

		for(std::vector<ConvertedHit>::iterator A = FourBest[fbest].AHits.begin();A != FourBest[fbest].AHits.end();A++){

		  l1t::emtf::CSCPrimitive tempStub;

			if(A->Phi() != -999){

				int station = A->TP().detId<CSCDetId>().station();
				int id = A->TP().getCSCData().cscID;
				int trknm = A->TP().getCSCData().trknmb;

				tempTrack.addStub(A->TP());
				// tempTrackNew.add_stub(); // AWB TODO
				ps.push_back(A->Phi());
				ts.push_back(A->Theta());
				sector = (A->TP().detId<CSCDetId>().endcap() -1)*6 + A->TP().detId<CSCDetId>().triggerSector() - 1;
				//std::cout<<"Q: "<<A->Quality()<<", keywire: "<<A->Wire()<<", strip: "<<A->Strip()<<std::endl;

				// CSCDetId variables defined in: 
			        // https://github.com/cms-l1t-offline/cmssw/blob/l1t-muon-pass2-CMSSW_8_0_0_pre5/DataFormats/MuonDetId/interface/CSCDetId.h
				// ConvertedHit values defined in interface/EmulatorClasses.h
				tempStub.set_endcap    ( ( A->TP().detId<CSCDetId>().endcap() == 1 ) ? 1 : -1 );
				tempStub.set_station   ( A->TP().detId<CSCDetId>().station()       );
				tempStub.set_ring      ( A->TP().detId<CSCDetId>().ring()          );
				tempStub.set_sector    ( A->TP().detId<CSCDetId>().triggerSector() ); // Using the +/- 1-6 convention, rather than 0-11, for now
				tempStub.set_chamber   ( A->TP().detId<CSCDetId>().chamber()       );
				tempStub.set_layer     ( A->TP().detId<CSCDetId>().layer()         );
				tempStub.set_csc_ID    ( A->TP().getCSCData().cscID                );
				tempStub.set_mpc_link  ( A->TP().getCSCData().mpclink              );
				tempStub.set_wire      ( A->TP().getCSCData().keywire              );
				tempStub.set_strip     ( A->TP().getCSCData().strip                );
				tempStub.set_track_num ( A->TP().getCSCData().trknmb               );
				tempStub.set_phi_local ( (A->Phi() / 60) - 2                       ); // The "phi_full" conversion. Right? - AWB 13.02.16
				tempStub.set_phi_global( tempStub.Phi_local() + 60 * (tempStub.Sector() - 1) ); // Only holds using 1-6 sector convention
				tempStub.set_theta_loc ( A->Theta()                                ); // This is some bizzare local definition of theta
				tempStub.set_theta_deg ( (tempStub.Endcap() == 1)  * ( (A->Theta() * 0.2851562) + 8.5) + // This is the true global theta in degrees
							(tempStub.Endcap() == -1) * (180 - ( (A->Theta() * 0.2851562) + 8.5) ) ); 
				tempStub.set_theta_rad ( tempStub.Theta_deg() * (pi/180)           ); // This is the true global theta in radians
				tempStub.set_eta       ( -1 * log( tan( tempStub.Theta_rad()/2 ) ) );
				tempStub.set_quality   ( A->TP().getCSCData().quality              );
				tempStub.set_pattern   ( A->TP().getCSCData().pattern              );
				tempStub.set_bend      ( A->TP().getCSCData().bend                 );
				tempStub.set_valid     ( A->TP().getCSCData().valid                );
				tempStub.set_sync_err  ( A->TP().getCSCData().syncErr              );
				tempStub.set_bx0       ( A->TP().getCSCData().bx0                  );
				tempStub.set_bx        ( A->TP().getCSCData().bx                   );

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

				switch(station){
					case 1: mode |= 8;break;
					case 2: mode |= 4;break;
					case 3: mode |= 2;break;
					case 4: mode |= 1;break;
					default: mode |= 0;
				}


				if(A->TP().detId<CSCDetId>().station() == 1 && A->TP().detId<CSCDetId>().ring() == 3)
					ME13 = true;

				if(station == 1 && id > 3 && id < 7){

					int sub = 2;
					if(A->TP().detId<CSCDetId>().chamber()%6 > 2)
						sub = 1;

					me1address = id;
					me1address -= 3;
					me1address += 3*(sub - 1);
					me1address = id<<1;//
					me1address |= trknm-1;

				}

				if(station == 2 && id > 3){

					me2address = id;
					me2address -= 3;
					me2address = me2address<<1;
					me2address |= trknm-1;

				}


			}

		} // End loop for(std::vector<ConvertedHit>::iterator A = FourBest[fbest].AHits.begin();A != FourBest[fbest].AHits.end();A++)
		tempTrack.phis = ps;
		tempTrack.thetas = ts;
		tempTrackNew.set_phis(ps); 
		tempTrackNew.set_thetas(ts); 

		float xmlpt = CalculatePt(tempTrack,es);
		tempTrack.pt = xmlpt*1.4;
		tempTrackNew.set_pt(xmlpt*1.4); // Is this the "right" pT Defined how? - AWB 13.02.16

		CombAddress = (me2address<<4) | me1address;

		// Why do we send the local theta value to MakeRegionalCand?  Is xmlpt or 1.4*xmlpt the "accurate" value? - AWB 13.02.16
		l1t::RegionalMuonCand outCand = MakeRegionalCand(xmlpt*1.4,FourBest[fbest].phi,FourBest[fbest].theta,
														         CombAddress,mode,1,sector);
		tempTrackNew.set_mode  ( mode );
		// tempTrackNew.set_sector( sector );  // Commented b/c we're using the +/- 1-6 convention (above), rather than 0-11, for now
		tempTrackNew.set_phi_global ( tempTrackNew.Phi_local() + 60 * (tempTrackNew.Sector() - 1) );

		// FoundTracks->push_back(tempTrack);
		FoundTracksNew->push_back(tempTrackNew);

        // NOTE: assuming that all candidates come from the central BX:
        int bx = 0;
		float theta_angle = (FourBest[fbest].theta*0.2851562 + 8.5)*(pi/180);
		float eta = (-1)*log(tan(theta_angle/2));
		if(!ME13 && fabs(eta) > 1.1)
			OutputCands->push_back(bx, outCand);
	} // End if(FourBest[fbest].phi)
  } // End for(int fbest=0;fbest<4;fbest++)

ev.put( OutputCands, "EMTF");
// ev.put( FoundTracks, "EMTF");
ev.put( FoundTracksNew, "EMTF");
  //std::cout<<"End Upgraded Track Finder Prducer:::::::::::::::::::::::::::\n:::::::::::::::::::::::::::::::::::::::::::::::::\n\n";

}//analyzer

void L1TMuonEndCapTrackProducer::beginJob()
{

}
void L1TMuonEndCapTrackProducer::endJob()
{

}
#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(L1TMuonEndCapTrackProducer);

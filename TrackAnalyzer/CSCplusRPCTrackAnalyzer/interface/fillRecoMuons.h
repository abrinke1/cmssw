//=============================================================
// Fill all REco Muons in the event record for:
// Package:    CSCplusRPCTrackAnalyzer
// Class:      CSCplusRPCTrackAnalyzer
//
// Written by David Curry
// ============================================================

#include <iostream>
#include <fstream>
#include <set>
#include <cmath>
#include <vector>
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/MuonReco/interface/Muon.h"
#include "DataFormats/MuonReco/interface/MuonFwd.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "DataFormats/MuonReco/interface/MuonSelectors.h"
#include "DataFormats/RecoCandidate/interface/RecoChargedCandidate.h"
#include "DataFormats/RecoCandidate/interface/RecoChargedCandidateFwd.h"

using namespace std;
using namespace edm;
using namespace reco;


bool fillRecoMuons(DataEvtSummary_t &ev, edm::Handle<reco::MuonCollection> muons, int printLevel) {
  
  bool tagExists = false;
  bool probeExists = false;

  int numMuons = 0;
  for (MuonCollection::const_iterator muon=muons->begin(); muon!=muons->end(); muon++) {


    /*
    // StandAlone Muons
    if (muon->isGlobalMuon() ) {
    ev.samPt -> push_back( muon->standAloneMuon()->pt() );
    ev.samPhi -> push_back( muon->standAloneMuon()->phi() );
    ev.samEta -> push_back( muon->standAloneMuon()->eta() );
    ev.samCharge -> push_back( muon->standAloneMuon()->charge() );
    }
    */

    
    // global muon
    if (muon->isGlobalMuon() && muon->combinedMuon().isNonnull()) {
      
      TrackRef trackRef = muon->combinedMuon();
      
      if (printLevel > 4 ) {
	printf("************************************************\n");
	printf("GBL RECO MOUN # %d\n", numMuons);
	printf("************************************************\n\n");
	printf("%s\n"    , "--------------------------------");
	printf("%s: %d\n", "isGlobalMuon    ()", muon->isGlobalMuon    ());
	printf("%s: %d\n", "isTrackerMuon   ()", muon->isTrackerMuon   ());
	printf("%s: %d\n", "isStandAloneMuon()", muon->isStandAloneMuon());
	printf("%s: %d\n", "combinedMuon    ().isNonnull()", muon->combinedMuon  ().isNonnull());
	printf("%s: %d\n", "track           ().isNonnull()", muon->track         ().isNonnull());
	printf("%s: %d\n", "standAloneMuon  ().isNonnull()", muon->standAloneMuon().isNonnull());
	printf("%s\n\n"  , "--------------------------------");
      
        printf("(GBL) muon->pt(): %10.5f, muon->eta(): %10.5f, muon->phi(): %10.5f\n",
               trackRef->pt(), trackRef->eta(), trackRef->phi());
      }
      
      if ( abs(trackRef->eta()) < 1.1 && trackRef->pt() > 30 ) tagExists = true;

      // Only fill for known CSC eta range
      if ( abs(trackRef->eta()) < 1.1 || abs(trackRef->eta()) > 2.4) continue;
      
      ev.gmrPt       -> push_back(trackRef->pt    ());
      ev.gmrSamPt    -> push_back(muon->standAloneMuon()->pt() );
      ev.gmrPhi      -> push_back(trackRef->phi   ());
      ev.gmrEta      -> push_back(trackRef->eta   ());
      ev.gmrChi2Norm -> push_back(trackRef->normalizedChi2());
      ev.gmrD0       -> push_back(trackRef->d0());
      ev.gmrValHits  -> push_back(trackRef->numberOfValidHits());
      ev.gmrCharge   -> push_back(trackRef->charge());

      probeExists = true;
      
      numMuons++;
    }
    
  } // end muon loop

  ev.numGblRecoMuons = numMuons;
  
  return (tagExists && probeExists);

}

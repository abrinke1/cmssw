// -*- C++ -*-
//=============================================================
// Fill all Gen Muons in the event record for: 
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

using namespace std;
using namespace edm;
using namespace reco;


void fillGenMuons(DataEvtSummary_t &ev, edm::Handle<std::vector<reco::GenParticle>> genParticles, int printLevel) {
  

  ev.numGenMuons = 0;
 
  if(genParticles.isValid()) {
    for(size_t i=0; i<genParticles->size(); i++) {
    
      const Candidate * genParticle = &(*genParticles)[i];
      int status=genParticle->status();
      int pid=genParticle->pdgId();
      if(status!=1 || abs(pid)!=13) continue; // PYTHIA 6 based
      
      float mu_eta = genParticle->eta();
      //if(fabs(mu_eta)<1.3 || fabs(mu_eta)>1.6) continue;
      //if(fabs(mu_eta)<0.9 || fabs(mu_eta)>1.9) continue;
      //if(fabs(mu_eta)<1.0 || fabs(mu_eta)>1.3) continue;
      
      float genphi = genParticle->phi();
      //if(genphi<0) genphi += 2*M_PI;
      
      if (printLevel > 0) {
	cout << "Gen Muon --> PT: " << genParticle->pt()
	     << " Eta: " << mu_eta
	     << " Phi: " << genphi<< endl;
	     
      }
      
      ev.gen_eta -> push_back(mu_eta);
      ev.gen_phi -> push_back(genphi);
      ev.gen_pt  -> push_back(genParticle->pt());
      ev.gen_id  -> push_back(genParticle->pdgId());
      
      ev.numGenMuons++;
      
    }
  }



} // end fillGen

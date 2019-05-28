#include "L1Trigger/L1TNtuples/interface/L1AnalysisBMTFOutput.h"
#include <FWCore/ParameterSet/interface/ParameterSet.h>

#include <sstream>
#include <string>

using namespace std;

L1Analysis::L1AnalysisBMTFOutput::L1AnalysisBMTFOutput()
{
}


L1Analysis::L1AnalysisBMTFOutput::~L1AnalysisBMTFOutput()
{
}

void L1Analysis::L1AnalysisBMTFOutput::SetL1MuKBMTrack(const edm::Handle<L1MuKBMTrackBxCollection> tracks, unsigned int maxTrk)
{

  // Loop over BX
  for (int iBX = tracks->getFirstBX(); iBX <= tracks->getLastBX(); ++iBX) {
    // Loop over tracks in each BX
    for ( L1MuKBMTrackBxCollection::const_iterator iTrk = tracks->begin(iBX);
	  iTrk != tracks->end(iBX) && (uint) bmtf_.nTrks < maxTrk; iTrk++) {
      
      bmtf_.nTrks = bmtf_.nTrks + 1;

      // BX
      bmtf_.bx.push_back ( iTrk->bx() );
      // Unconstrained pt
      bmtf_.ptUnconstrained.push_back ( iTrk->ptUnconstrained() );
      // Unconstrained curvature at station 1
      bmtf_.curvatureAtMuon.push_back ( iTrk->curvatureAtMuon() ); 
      // Unconstrained phi at station 1
      bmtf_.phiAtMuon.push_back ( iTrk->phiAtMuon() );
      // Unconstrained phiB at station 1
      bmtf_.phiBendAtMuon.push_back ( iTrk->phiBAtMuon() );
      // Constrained curvature at vertex
      bmtf_.curvatureAtVertex.push_back ( iTrk->curvatureAtVertex() ); 
      // Constrained phi at the vertex
      bmtf_.phiAtVertex.push_back ( iTrk->phiAtVertex() );
      // Impact parameter as calculated from the muon track 
      bmtf_.dxy.push_back ( iTrk->dxy() );
      // Unconstrained curvature at the muon systen 
      bmtf_.curvature.push_back ( iTrk->curvature() );
      // Unconstrained phi at the muon systen 
      bmtf_.positionAngle.push_back ( iTrk->positionAngle() );
      // Unconstrained bending angle at the muon systen 
      bmtf_.bendingAngle.push_back ( iTrk->bendingAngle() );
      // Fine eta
      bmtf_.fineEta.push_back ( iTrk->fineEta() );
      bmtf_.hasFineEta.push_back( iTrk->hasFineEta() );
      // Coarse eta caluclated only using phi segments 
      bmtf_.coarseEta.push_back ( iTrk->coarseEta() );
      // Approximate Chi2 metric
      bmtf_.approxChi2.push_back ( iTrk->approxChi2() );
      // Hit pattern (?)
      bmtf_.hitPattern.push_back ( iTrk->hitPattern() );
      // Step (?)
      bmtf_.step.push_back ( iTrk->step() );
      // Sector;
      bmtf_.sector.push_back ( iTrk->sector() );
      // Wheel
      bmtf_.wheel.push_back ( iTrk->wheel() );
      // Quality
      bmtf_.quality.push_back ( iTrk->quality() );
      // Rank (?)
      bmtf_.rank.push_back ( iTrk->rank() );
      
    } // End loop: for ( MuonBxCollection::const_iterator iTrk = tracks->begin(iBX); ...)
  }  // End loop: for (int iBX = tracks->getFirstBX(); iBX <= tracks->getLastBX(); ++iBX)

} // End function: void L1Analysis::L1AnalysisBMTFOutput::SetL1MuKBMTrack()

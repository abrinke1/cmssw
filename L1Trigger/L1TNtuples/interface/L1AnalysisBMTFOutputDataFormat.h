#ifndef __L1Analysis_L1AnalysisBMTFOutputDataFormat_H__
#define __L1Analysis_L1AnalysisBMTFOutputDataFormat_H__

#include <vector>

namespace L1Analysis
{
  struct L1AnalysisBMTFOutputDataFormat
  {
    
    L1AnalysisBMTFOutputDataFormat(){Reset();};
    ~L1AnalysisBMTFOutputDataFormat(){};
    
    void Reset()
    {
      
      nTrks = 0;
      
      bx.clear();
      ptUnconstrained.clear();
      curvatureAtMuon.clear();
      phiAtMuon.clear();
      phiBendAtMuon.clear();
      curvatureAtVertex.clear();
      phiAtVertex.clear();
      dxy.clear();
      curvature.clear();
      positionAngle.clear();
      bendingAngle.clear();
      fineEta.clear();
      hasFineEta.clear();
      coarseEta.clear();
      approxChi2.clear();
      hitPattern.clear();
      step.clear();
      sector.clear();
      wheel.clear();
      quality.clear();
      rank.clear();
      
    }
    
    // ---- L1AnalysisBMTFOutputDataFormat information.
    // ---- Directly copied from DataFormats/L1TMuon/interface/L1MuKBMTrack.h
    
    int nTrks;

    std::vector<int>    bx;
    std::vector<float>  ptUnconstrained;
    std::vector<int>    curvatureAtMuon;
    std::vector<int>    phiAtMuon;
    std::vector<int>    phiBendAtMuon;
    std::vector<int>    curvatureAtVertex;
    std::vector<int>    phiAtVertex;
    std::vector<int>    dxy;
    std::vector<int>    curvature;
    std::vector<int>    positionAngle;
    std::vector<int>    bendingAngle;
    std::vector<int>    fineEta;
    std::vector<bool>   hasFineEta;
    std::vector<int>    coarseEta;
    std::vector<int>    approxChi2;
    std::vector<int>    hitPattern;
    std::vector<int>    step;
    std::vector<int>    sector;
    std::vector<int>    wheel;
    std::vector<int>    quality;
    std::vector<int>    rank;

  };
}
#endif

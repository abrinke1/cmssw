#ifndef __L1Analysis_L1AnalysisRecoMuon2DataFormat_H__
#define __L1Analysis_L1AnalysisRecoMuon2DataFormat_H__

//-------------------------------------------------------------------------------
// Created 20/04/2010 - E. Conte, A.C. Le Bihan
//
//
// Original code : L1Trigger/L1TNtuples/L1RecoMuon2NtupleProducer - Jim Brooke
//-------------------------------------------------------------------------------

#include <vector>

namespace L1Analysis
{
  struct L1AnalysisRecoMuon2DataFormat
  {
    L1AnalysisRecoMuon2DataFormat(){Reset();};
    ~L1AnalysisRecoMuon2DataFormat(){Reset();};

    void Reset()
    {
    nMuons=0;

    e.clear();
    et.clear();
    pt.clear();
    ptSAM.clear();
    eta.clear();
    etaSAM.clear();
    phi.clear();
    phiSAM.clear();
    isLooseMuon.clear();
    isMediumMuon.clear();
    isTightMuon.clear();
    iso.clear();
    hlt_isomu.clear();
    hlt_mu.clear();
    hlt_isoDeltaR.clear();
    hlt_deltaR.clear();
    passesSingleMuon.clear();
    charge.clear();
    chargeSAM.clear();
    chi2.clear();
    chi2SAM.clear();
    dxy.clear();
    dxySAM.clear();
    dz.clear();
    dzSAM.clear();
    mt.clear();
    met.clear();
    etaSt1.clear();
    phiSt1.clear();
    etaSt2.clear();
    phiSt2.clear();
    }

    unsigned short nMuons;
    std::vector<float> e;
    std::vector<float> et;
    std::vector<float> pt;
    std::vector<float> ptSAM;
    std::vector<float> eta;
    std::vector<float> etaSAM;
    std::vector<float> phi;
    std::vector<float> phiSAM;
    std::vector<bool> isLooseMuon;
    std::vector<bool> isMediumMuon;
    std::vector<bool> isTightMuon;
    std::vector<float> iso;
    std::vector<short> hlt_isomu;
    std::vector<short> hlt_mu;
    std::vector<float> hlt_isoDeltaR;
    std::vector<float> hlt_deltaR;
    std::vector<int> passesSingleMuon;
    std::vector<int> charge;
    std::vector<int> chargeSAM;
    std::vector<float> chi2;
    std::vector<float> chi2SAM;
    std::vector<float> dxy;
    std::vector<float> dxySAM;
    std::vector<float> dz;
    std::vector<float> dzSAM;
    std::vector<float> met;
    std::vector<float> mt;
    std::vector<float> etaSt1;
    std::vector<float> phiSt1;
    std::vector<float> etaSt2;
    std::vector<float> phiSt2;
  };
}
#endif




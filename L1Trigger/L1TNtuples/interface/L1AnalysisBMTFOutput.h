#ifndef __L1Analysis_L1AnalysisBMTFOutput_H__
#define __L1Analysis_L1AnalysisBMTFOutput_H__

#include "DataFormats/L1TMuon/interface/L1MuKBMTrack.h"
#include "DataFormats/Common/interface/Handle.h"

#include <vector>

#include "L1AnalysisBMTFOutputDataFormat.h"

namespace L1Analysis
{
  class L1AnalysisBMTFOutput
  {
  public:
    L1AnalysisBMTFOutput();
    ~L1AnalysisBMTFOutput();
    
    void SetL1MuKBMTrack(const edm::Handle<L1MuKBMTrackBxCollection> tracks, unsigned int maxTrk);

    void Reset() {bmtf_.Reset();}
    L1AnalysisBMTFOutputDataFormat * getData() {return &bmtf_;}

  private :
    L1AnalysisBMTFOutputDataFormat bmtf_;
  };
}

#endif

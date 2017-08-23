//
// L1TMuonEndcapForests: Collection of Decision Tree Forests used to fill EMTF LUTs.
//

#ifndef l1t_L1TMuonEndcapForest_h
#define l1t_L1TMuonEndcapForest_h

#include <memory>
#include <iostream>
#include <vector>
#include <map>

#include "CondFormats/Serialization/interface/Serializable.h"

class L1TMuonEndcapForest {
 public:

  class DTreeNode {
  public:
    DTreeNode(){splitVar = ileft = iright = 0; splitVal = fitVal = 0.0;}
    int splitVar;
    double splitVal;
    double fitVal;
    unsigned ileft;
    unsigned iright;

    COND_SERIALIZABLE;
  };
  typedef std::vector<DTreeNode> DTree;
  typedef std::vector<DTree> DForest;
  typedef std::vector<DForest> DForestColl;
  typedef std::map<int,int> DForestMap;

  unsigned version_;
  DForestColl forest_coll_;
  DForestMap forest_map_;
  		
  L1TMuonEndcapForest() { version_=0; }
  ~L1TMuonEndcapForest() {}
  
  COND_SERIALIZABLE;
};
#endif

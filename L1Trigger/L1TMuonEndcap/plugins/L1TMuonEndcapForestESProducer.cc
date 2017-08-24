#include <iostream>
#include <memory>

#include "FWCore/Framework/interface/ModuleFactory.h"
#include "FWCore/Framework/interface/ESProducer.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Framework/interface/ESProducts.h"

#include "CondFormats/L1TObjects/interface/L1TMuonEndcapForest.h"
#include "CondFormats/DataRecord/interface/L1TMuonEndcapForestRcd.h"

#include "L1Trigger/L1TMuonEndcap/interface/PtAssignmentEngine.h"
#include "L1Trigger/L1TMuonEndcap/interface/PtAssignmentEngine2016.h"
#include "L1Trigger/L1TMuonEndcap/interface/PtAssignmentEngine2017.h"
#include "L1Trigger/L1TMuonEndcap/interface/bdt/Node.h"
#include "L1Trigger/L1TMuonEndcap/interface/bdt/Tree.h"
#include "L1Trigger/L1TMuonEndcap/interface/bdt/Forest.h"

using namespace std;

// class declaration

class L1TMuonEndcapForestESProducer : public edm::ESProducer {
public:
  L1TMuonEndcapForestESProducer(const edm::ParameterSet&);
  ~L1TMuonEndcapForestESProducer() {}

  typedef std::shared_ptr<L1TMuonEndcapForest> ReturnType;

  ReturnType produce(const L1TMuonEndcapForestRcd&);

private:
  int ptLUTVersion;
  string bdtXMLDir;

  L1TMuonEndcapForest::DTree traverse(emtf::Node* tree);
};

// constructor

L1TMuonEndcapForestESProducer::L1TMuonEndcapForestESProducer(const edm::ParameterSet& iConfig)
{
   setWhatProduced(this);

   ptLUTVersion = iConfig.getParameter<int>("PtAssignVersion");
   bdtXMLDir    = iConfig.getParameter<string>("bdtXMLDir");
}

// member functions

L1TMuonEndcapForest::DTree L1TMuonEndcapForestESProducer::traverse(emtf::Node* node){
    // original implementation use 0 ptr for non-existing children nodes, return empty cond tree (vector of nodes)
    if( !node ) return L1TMuonEndcapForest::DTree();
    // recur on left and then right child
    L1TMuonEndcapForest::DTree left_subtree  = traverse( node->getLeftDaughter() );
    L1TMuonEndcapForest::DTree right_subtree = traverse( node->getRightDaughter() );
    // allocate tree
    L1TMuonEndcapForest::DTree cond_tree(1 + left_subtree.size() + right_subtree.size());
    // copy the local root node
    L1TMuonEndcapForest::DTreeNode &local_root = cond_tree[0];
    local_root.splitVar = node->getSplitVariable();
    local_root.splitVal = node->getSplitValue();
    local_root.fitVal   = node->getFitValue();
    // shift children indicies and place the subtrees into the newly allocated tree
    local_root.ileft    = (left_subtree.size()?1:0); // left subtree (if exists) is placed right after the root -> index=1
    transform(left_subtree.cbegin(), // source from
              left_subtree.cend(),   // source till
              cond_tree.begin() + 1, // destination
              [] (L1TMuonEndcapForest::DTreeNode cond_node) {
                     // increment indecies only for existing children, left 0 for non-existing
                     if( cond_node.ileft ) cond_node.ileft  += 1;
                     if( cond_node.iright) cond_node.iright += 1;
                     return cond_node;
              }
    );
    unsigned int offset = left_subtree.size();
    local_root.iright = (offset+right_subtree.size() ? 1 + offset : 0); // right subtree is placed after the left one
    transform(right_subtree.cbegin(), // source from
              right_subtree.cend(),   // source till
              cond_tree.begin() + 1 + offset, // destination
              [offset] (L1TMuonEndcapForest::DTreeNode cond_node) {
                     // increment indecies only for existing children, left 0 for non-existing
                     if( cond_node.ileft ) cond_node.ileft  += 1 + offset;
                     if( cond_node.iright) cond_node.iright += 1 + offset;
                     return cond_node;
              }
    );
    return cond_tree;
}

L1TMuonEndcapForestESProducer::ReturnType
L1TMuonEndcapForestESProducer::produce(const L1TMuonEndcapForestRcd& iRecord)
{
  // piggyback on the PtAssignmentEngine class to read the XMLs in
  PtAssignmentEngine* pt_assign_engine_;
  std::unique_ptr<PtAssignmentEngine> pt_assign_engine_2016_;
  std::unique_ptr<PtAssignmentEngine> pt_assign_engine_2017_;
  
  pt_assign_engine_2016_.reset(new PtAssignmentEngine2016());
  pt_assign_engine_2017_.reset(new PtAssignmentEngine2017());
  
  if (ptLUTVersion <= 5) pt_assign_engine_ = pt_assign_engine_2016_.get();
  else                   pt_assign_engine_ = pt_assign_engine_2017_.get();

  pt_assign_engine_->configure( true, ptLUTVersion, false, false, false, false, false );
  pt_assign_engine_->read(bdtXMLDir);
  
  // get a hold on the forests; copy to non-const locals
  std::array<emtf::Forest, 16> forests = pt_assign_engine_->getForests();
  std::vector<int> allowedModes = pt_assign_engine_->getAllowedModes();
  // construct empty cond payload
  std::shared_ptr<L1TMuonEndcapForest> pEMTFForest(new L1TMuonEndcapForest());
  // pack the forests into the cond payload for each mode
  pEMTFForest->forest_coll_.resize(0);
  for (unsigned int i = 0; i < allowedModes.size(); i++) {
    int mode = allowedModes[i];
    pEMTFForest->forest_map_[mode] = i;
    // convert emtf::Forest into the L1TMuonEndcapForest::DForest
    emtf::Forest& forest = forests.at(mode);
    // Store boostWeight (initial pT value of tree 0) as an integer: boostWeight x 1 million
    pEMTFForest->forest_map_[mode+16] = forest.getTree(0)->getBoostWeight() * 1000000;
    L1TMuonEndcapForest::DForest cond_forest;
    for (unsigned int j = 0; j < forest.size(); j++)
      cond_forest.push_back( traverse( forest.getTree(j)->getRootNode() ) );
    // of course, move has no effect here, but I'll keep it in case move constructor will be provided some day
    pEMTFForest->forest_coll_.push_back( std::move( cond_forest ) );
  }
  
  return pEMTFForest;
}

// Define this as a plug-in
DEFINE_FWK_EVENTSETUP_MODULE(L1TMuonEndcapForestESProducer);

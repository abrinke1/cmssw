#ifndef dataevtsummaryhandler_h
#define dataevtsummaryhandler_h

#if !defined(__CINT__) || defined(__MAKECINT__)
 
#include <string.h>
#include <iomanip>
#include <iostream>
#include <fstream>
#include <set>
#include <cmath>

#include "Math/LorentzVector.h"
#include "TMath.h"
#include "TVector2.h"
#include "TTree.h"
#include "TLorentzVector.h"
#include "DataFormats/Math/interface/deltaR.h"

#endif

#define MAXEMTF 4
#define MAXTRK 4
#define MAXTRKLCTS 4
#define MAX_MUONS 100
#define MAX_CSC_RECHIT 48 // 4 stations x 6 layers + (overlap between chambers: added other 24 hits to be safe)
#define MAX_TRK_SEGS 100  // max # segments to a given tracker muon
#define MAX_LCTS_PER_TRK 4  // max # of LCTS which form a CSCTF track
#define MAX_SEGS_STD 16 // MAX number of segments which can be associated to StandAlone component of the GBL muon

struct DataEvtSummary_t {

  Int_t run,lumi,event;
    
  // ==================
  // Gen Muons
  // ==================
 
  Int_t numGenMuons;

  std::vector<float>* gen_eta;
  std::vector<float>* gen_pt;
  std::vector<float>* gen_phi;
  std::vector<int>*   gen_id;
  
  
  // ==================
  // RECO GLobal Muons
  // ==================
  int numGblRecoMuons;
  
  std::vector<float>* gmrPt;
  std::vector<float>* gmrSamPt;
  std::vector<float>* gmrEta;
  std::vector<float>* gmrPhi;
  std::vector<float>* gmrD0;
  std::vector<float>* gmrChi2Norm;
  std::vector<int>* gmrValHits;
  std::vector<int>* gmrCharge;

  // Muon Segments
  std::vector<int>* muonNsegs;

  // segment position information, global
  float muon_cscsegs_gbl_x[MAX_MUONS][MAX_SEGS_STD];
  float muon_cscsegs_gbl_y[MAX_MUONS][MAX_SEGS_STD];
  float muon_cscsegs_gbl_eta[MAX_MUONS][MAX_SEGS_STD];
  float muon_cscsegs_gbl_phi[MAX_MUONS][MAX_SEGS_STD];
  float muon_cscsegs_gbl_dir_eta[MAX_MUONS][MAX_SEGS_STD];
  float muon_cscsegs_gbl_dir_phi[MAX_MUONS][MAX_SEGS_STD];
  
  
  // general segment information
  int muon_cscsegs_endcap[MAX_MUONS][MAX_SEGS_STD];
  int muon_cscsegs_station[MAX_MUONS][MAX_SEGS_STD];
  int muon_cscsegs_ring[MAX_MUONS][MAX_SEGS_STD];
  int muon_cscsegs_chamber[MAX_MUONS][MAX_SEGS_STD];
  int muon_cscsegs_nhits[MAX_MUONS][MAX_SEGS_STD];
  int muon_cscsegs_sector[MAX_MUONS][MAX_SEGS_STD];
  int muon_cscsegs_islctable[MAX_MUONS][MAX_SEGS_STD];
  int muon_cscsegs_ismatched[MAX_MUONS][MAX_SEGS_STD];  // lctId is the position of the lct in the all LCT collection
  int muon_cscsegs_lctId[MAX_MUONS][MAX_SEGS_STD];
  
  
  // ==================
  // CSC LCTS
  // ==================
  
  Int_t numLCTs;
  std::vector<int>* lctEndcap;
  std::vector<int>* lctSector;
  std::vector<int>* lctSubSector;
  std::vector<int>* lctBx;
  std::vector<int>* lctBx0;
  std::vector<int>* lctStation;
  std::vector<int>* lctRing;
  std::vector<int>* lctChamber;
  std::vector<int>* lctTriggerCSCID;
  std::vector<float>* lctGlobalPhi;
  std::vector<float>* lctGlobalEta;
  std::vector<int>* lctLocPhi;
  std::vector<int>* lctLocEta;
  std::vector<int>* lctStrip;
  std::vector<int>* lctWire;
  
  
  // ====================
  // CSC Tracks and LCTs
  // ====================
  Int_t numTrks;
  std::vector<Int_t>* numTrkLCTs;
  std::vector<float>* trkPt;
  std::vector<float>* trkEta;
  std::vector<float>* trkPhi;
  std::vector<float>* trkGeomPhi;
  std::vector<Int_t>* trkMode;
  std::vector<Int_t>* trkBx;
  std::vector<Int_t>* trkBxBeg;
  std::vector<Int_t>* trkBxEnd;
  std::vector<Int_t>* trkRank;
  std::vector<Int_t>* trkStraight;

  // Track LCTs
  Int_t trkLctEndcap[MAXTRK][MAXTRKLCTS];
  Int_t trkLctStation[MAXTRK][MAXTRKLCTS];
  Int_t trkLctSector[MAXTRK][MAXTRKLCTS];
  Int_t trkLctRing[MAXTRK][MAXTRKLCTS];
  Int_t trkLctChamber[MAXTRK][MAXTRKLCTS];
  Int_t trkLctWire[MAXTRK][MAXTRKLCTS];
  Int_t trkLctStrip[MAXTRK][MAXTRKLCTS];
  Int_t trkLctCSCID[MAXTRK][MAXTRKLCTS];
  float trkLctGblPhi[MAXTRK][MAXTRKLCTS];
  float trkLctGeomPhi[MAXTRK][MAXTRKLCTS];
  float trkLctGblEta[MAXTRK][MAXTRKLCTS];
  Int_t trkLctLocPhi[MAXTRK][MAXTRKLCTS];
  Int_t trkLctLocTheta[MAXTRK][MAXTRKLCTS];
  Int_t trkLctBx[MAXTRK][MAXTRKLCTS];
  Int_t trkLctQual[MAXTRK][MAXTRKLCTS];
  Int_t trkLctPattern[MAXTRK][MAXTRKLCTS];
  
  
  // ====================
  // RPC Tracks and LCTs
  // ====================

  // RPC Tracks
  Int_t numTrks_rpc;
  Int_t numTrkLCTs_rpc;
  std::vector<float>* trkPt_rpc;
  std::vector<float>* trkEta_rpc;
  std::vector<float>* trkPhi_rpc;
  std::vector<Int_t>* trkMode_rpc;
  std::vector<Int_t>* isRPC_cand;

  //RPC LCTs
  Int_t numRPC_clusters;
  std::vector<int>* rpc_cluster_Endcap;
  std::vector<int>* rpc_cluster_Sector;
  std::vector<int>* rpc_cluster_SubSector;
  std::vector<int>* rpc_cluster_Station;
  std::vector<int>* rpc_cluster_Chamber;
  std::vector<int>* rpc_cluster_Wire;
  std::vector<int>* rpc_cluster_Strip;
  std::vector<int>* rpc_cluster_Ring;
  std::vector<int>* rpc_cluster_CSCId;
  std::vector<float>* rpc_cluster_globalPhi;
  std::vector<float>* rpc_cluster_globalEta;
  
  
  
  // ====================
  // Legacy CSC Tracks
  // ====================
  Int_t numLegTrks;

  std::vector<Int_t>* numLegTrkLCTs;
  std::vector<float>* leg_trkPt;
  std::vector<float>* leg_trkPtOld;
  std::vector<float>* leg_trkPtMatt;
  std::vector<float>* leg_trkPtGmt;
  std::vector<float>* leg_trkEta;
  std::vector<float>* leg_trkPhi;
  std::vector<Int_t>* leg_trkMode;
  std::vector<Int_t>* leg_trkModeA;
  std::vector<Int_t>* leg_trkModeB;
  std::vector<Int_t>* leg_trkQual;
  std::vector<Int_t>* leg_trkQualA;
  std::vector<Int_t>* leg_trkQualB;
  std::vector<Int_t>* leg_trkBx;
  std::vector<Int_t>* leg_trkBxBeg;
  std::vector<Int_t>* leg_trkBxEnd;

  // Track LCTs
  Int_t leg_trkLctEndcap[MAXTRK][MAXTRKLCTS];
  Int_t leg_trkLctStation[MAXTRK][MAXTRKLCTS];
  Int_t leg_trkLctSector[MAXTRK][MAXTRKLCTS];
  Int_t leg_trkLctRing[MAXTRK][MAXTRKLCTS];
  Int_t leg_trkLctChamber[MAXTRK][MAXTRKLCTS];
  Int_t leg_trkLctWire[MAXTRK][MAXTRKLCTS];
  Int_t leg_trkLctStrip[MAXTRK][MAXTRKLCTS];
  Int_t leg_trkLctCSCID[MAXTRK][MAXTRKLCTS];
  float leg_trkLctGblPhi[MAXTRK][MAXTRKLCTS];
  float leg_trkLctGblEta[MAXTRK][MAXTRKLCTS];
  Int_t leg_trkLctLocPhi[MAXTRK][MAXTRKLCTS];
  Int_t leg_trkLctLocEta[MAXTRK][MAXTRKLCTS];
  Int_t leg_trkLctBx[MAXTRK][MAXTRKLCTS];
  
  
  // ====================
  // Legacy CSCTF input-to-GMT Tracks
  // ====================
  Int_t numCscTrks;

  std::vector<float>* csc_trkPt;
  std::vector<float>* csc_trkEta;
  std::vector<float>* csc_trkPhi;
  std::vector<Int_t>* csc_trkQual;
  std::vector<Int_t>* csc_trkCharge;
  std::vector<Int_t>* csc_trkBx;

  // ====================
  // Legacy GMT Tracks
  // ====================

  // From any part of the detector
  Int_t numGtTrks;

  std::vector<float>* gt_trkEta;
  std::vector<float>* gt_trkPhi;
  std::vector<float>* gt_trkPt;
  std::vector<Int_t>* gt_trkQual;
  std::vector<Int_t>* gt_trkBx;
  std::vector<Int_t>* gt_trkDetector;

  // Only from endcaps
  Int_t numGmtTrks;

  std::vector<float>* gmt_trkPt;
  std::vector<float>* gmt_trkEta;
  std::vector<float>* gmt_trkPhi;
  std::vector<Int_t>* gmt_trkQual;
  std::vector<Int_t>* gmt_trkCharge;
  std::vector<Int_t>* gmt_trkBx;
  std::vector<Int_t>* gmt_trkDetector;

};


class DataEvtSummaryHandler {
public:
    //
  DataEvtSummaryHandler();
  ~DataEvtSummaryHandler();

    //current event
    DataEvtSummary_t evSummary_;
    
    
    DataEvtSummary_t &getEvent() {
        return evSummary_;
    }

    //write mode
    bool initTree(TTree *t);
    void fillTree();

    //read mode
    int getEntries() {
        return (t_ ? t_->GetEntriesFast() : 0);
    }
    void getEntry(int ientry) {
        resetStruct();
        if(t_) t_->GetEntry(ientry);
    }

    void initStruct();
    void resetStruct();
    


private:
    //the tree
    TTree *t_;
};

#endif

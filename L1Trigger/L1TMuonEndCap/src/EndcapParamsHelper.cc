#include "L1Trigger/L1TMuonEndCap/interface/EndcapParamsHelper.h"

#include <iostream>

using namespace l1t;
using namespace std;

const EndcapParamsHelper *  EndcapParamsHelper::readFromEventSetup(const L1TMuonEndcapParams * es){
  return new EndcapParamsHelper(es);
}

EndcapParamsHelper *  EndcapParamsHelper::readAndWriteFromEventSetup(const L1TMuonEndcapParams * es){
  EndcapParamsHelper * x = new EndcapParamsHelper(es);
  x->useCopy();
  return x;
}

EndcapParamsHelper::EndcapParamsHelper(L1TMuonEndcapParams * w) {
  write_ = w; 
  check_write(); 
  we_own_write_ = false;
  //write_->m_version = VERSION; 
  read_ = write_; 
}

EndcapParamsHelper::EndcapParamsHelper(const L1TMuonEndcapParams * es) {read_ = es; write_=NULL;}

void EndcapParamsHelper::useCopy(){
  write_ = new L1TMuonEndcapParams(*read_);
  we_own_write_ = true;
  read_  = write_;
}

EndcapParamsHelper::~EndcapParamsHelper() {
  if (we_own_write_ && write_) delete write_;
}


// print all the L1 GT stable parameters
void EndcapParamsHelper::print(std::ostream& myStr) const {
    myStr << "\nL1T EndCap  Parameters \n" << std::endl;
}

#include <iostream>
#include <memory>
#include <iostream>

#include "FWCore/Framework/interface/ModuleFactory.h"
#include "FWCore/Framework/interface/ESProducer.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Framework/interface/ESProducts.h"

#include "CondFormats/L1TObjects/interface/L1TMuonEndcapParams.h"
#include "CondFormats/DataRecord/interface/L1TMuonEndcapParamsRcd.h"
#include "L1Trigger/L1TMuonEndCap/interface/EndcapParamsHelper.h"

#include "FWCore/ParameterSet/interface/FileInPath.h"
#include "TXMLEngine.h"

using namespace std;

// Class declaration

class L1TMuonEndcapParamsESProducer : public edm::ESProducer {
public:
  L1TMuonEndcapParamsESProducer(const edm::ParameterSet&);
  ~L1TMuonEndcapParamsESProducer();
  
  typedef std::shared_ptr<L1TMuonEndcapParams> ReturnType;

  ReturnType produce(const L1TMuonEndcapParamsRcd&);

private:
  l1t::EndcapParamsHelper data_;
};

// Constructor

L1TMuonEndcapParamsESProducer::L1TMuonEndcapParamsESProducer(const edm::ParameterSet& iConfig) :
  data_(new L1TMuonEndcapParams())
{
  // The following line is needed to tell the framework what data is being produced
   setWhatProduced(this);

   data_.SetPtAssignVersion(iConfig.getParameter<int>("PtAssignVersion"));
   data_.SetFirmwareVersion(iConfig.getParameter<int>("FirmwareVersion"));
   data_.SetPrimConvVersion(iConfig.getParameter<int>("PrimConvVersion"));

}

// Destructor

L1TMuonEndcapParamsESProducer::~L1TMuonEndcapParamsESProducer()
{
}

// Member functions

// ------------ method called to produce the data  ------------
L1TMuonEndcapParamsESProducer::ReturnType
L1TMuonEndcapParamsESProducer::produce(const L1TMuonEndcapParamsRcd& iRecord)
{
   using namespace edm::es;
   auto pEMTFParams = std::make_shared<L1TMuonEndcapParams>(*data_.getWriteInstance());
   return pEMTFParams;
   
}

// Define this as a plug-in
DEFINE_FWK_EVENTSETUP_MODULE(L1TMuonEndcapParamsESProducer);

#include <iostream>
#include <fstream>

#include "FWCore/Framework/interface/ModuleFactory.h"
#include "FWCore/Framework/interface/ESProducer.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "CondFormats/L1TObjects/interface/L1TMuonEndcapForest.h"
#include "CondFormats/DataRecord/interface/L1TMuonEndcapForestRcd.h"
#include "CondFormats/DataRecord/interface/L1TMuonEndcapForestO2ORcd.h"

class L1TMuonEndcapForestOnlineProxy : public edm::ESProducer {
public:
    std::shared_ptr<L1TMuonEndcapForest> produce(const L1TMuonEndcapForestO2ORcd& record);

    L1TMuonEndcapForestOnlineProxy(const edm::ParameterSet&);
    ~L1TMuonEndcapForestOnlineProxy(void){}
};

L1TMuonEndcapForestOnlineProxy::L1TMuonEndcapForestOnlineProxy(const edm::ParameterSet& iConfig) : edm::ESProducer() {
    setWhatProduced(this);
}

std::shared_ptr<L1TMuonEndcapForest> L1TMuonEndcapForestOnlineProxy::produce(const L1TMuonEndcapForestO2ORcd& record) {

    const L1TMuonEndcapForestRcd& baseRcd = record.template getRecord< L1TMuonEndcapForestRcd >() ;
    edm::ESHandle< L1TMuonEndcapForest > baseSettings ;
    baseRcd.get( baseSettings ) ;

    std::shared_ptr< L1TMuonEndcapForest > retval = std::make_shared< L1TMuonEndcapForest >( *(baseSettings.product()) );

    return retval;
}

//define this as a plug-in
DEFINE_FWK_EVENTSETUP_MODULE(L1TMuonEndcapForestOnlineProxy);

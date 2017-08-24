#include <iostream>
#include <fstream>
#include <stdexcept>

#include "CondTools/L1TriggerExt/interface/L1ConfigOnlineProdBaseExt.h"
#include "CondFormats/L1TObjects/interface/L1TMuonEndcapForest.h"
#include "CondFormats/DataRecord/interface/L1TMuonEndcapForestRcd.h"
#include "CondFormats/DataRecord/interface/L1TMuonEndcapForestO2ORcd.h"

class L1TMuonEndcapForestOnlineProd : public L1ConfigOnlineProdBaseExt<L1TMuonEndcapForestO2ORcd,L1TMuonEndcapForest> {
private:
public:
    virtual std::shared_ptr<L1TMuonEndcapForest> newObject(const std::string& objectKey, const L1TMuonEndcapForestO2ORcd& record) override ;

    L1TMuonEndcapForestOnlineProd(const edm::ParameterSet&);
    ~L1TMuonEndcapForestOnlineProd(void){}
};

L1TMuonEndcapForestOnlineProd::L1TMuonEndcapForestOnlineProd(const edm::ParameterSet& iConfig) : L1ConfigOnlineProdBaseExt<L1TMuonEndcapForestO2ORcd,L1TMuonEndcapForest>(iConfig) {}

std::shared_ptr<L1TMuonEndcapForest> L1TMuonEndcapForestOnlineProd::newObject(const std::string& objectKey, const L1TMuonEndcapForestO2ORcd& record) {

    edm::LogError( "L1-O2O" ) << "L1TMuonEndcapForest object with key " << objectKey << " not in ORCON!" ;

    throw std::runtime_error("You are never supposed to get this code running!");

    std::shared_ptr< L1TMuonEndcapForest > retval = std::make_shared< L1TMuonEndcapForest >();
    return retval;
}

//define this as a plug-in
DEFINE_FWK_EVENTSETUP_MODULE(L1TMuonEndcapForestOnlineProd);

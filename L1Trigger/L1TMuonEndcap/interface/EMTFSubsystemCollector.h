#ifndef L1TMuonEndcap_EMTFSubsystemCollector_h
#define L1TMuonEndcap_EMTFSubsystemCollector_h

#include "L1Trigger/L1TMuonEndcap/interface/Common.h"


// Forward declarations
namespace edm {
  class Event;
  class EDGetToken;
}


// Class declaration
class EMTFSubsystemCollector {
public:
  template<typename T>
  void extractPrimitives(
    T tag,
    const edm::Event& iEvent,
    const edm::EDGetToken& token,
    TriggerPrimitiveCollection& out
  );

};

#endif

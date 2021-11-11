#ifndef L1Trigger_TrackFindingTracklet_ChannelAssignment_h
#define L1Trigger_TrackFindingTracklet_ChannelAssignment_h

#include "FWCore/Framework/interface/data_default_record_trait.h"
#include "L1Trigger/TrackFindingTracklet/interface/ChannelAssignmentRcd.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/L1TrackTrigger/interface/TTTypes.h"
#include "L1Trigger/TrackTrigger/interface/Setup.h"
#include "DataFormats/L1TrackTrigger/interface/TTTypes.h"

#include <vector>

namespace trklet {

  /*! \class  trklet::ChannelAssignment
   *  \brief  Class to assign tracklet tracks ans stubs to output channel
   *          based on their Pt or seed type as well as DTC stubs to input channel
   *  \author Thomas Schuh
   *  \date   2020, Nov; updated 2021 Oct
   */
  class ChannelAssignment {
  public:
    ChannelAssignment() {}
    ChannelAssignment(const edm::ParameterSet& iConfig, const tt::Setup* setup);
    ~ChannelAssignment() {}
    // sets channelId of given TTTrackRef, return false if track outside pt range
    bool channelId(const TTTrackRef& ttTrackRef, int& channelId) const;
    // number of used channels
    int numChannels() const { return numChannels_; }
    // sets layerId of given TTStubRef and seedType, returns false if seeed stub
    bool layerId(int seedType, const TTStubRef& ttStubRef, int& layerId) const;
    // return tracklet layerId (barrel: [0-5], endcap: [6-10]) for given TTStubRef
    int trackletLayerId(const TTStubRef& ttStubRef) const;
    // max number layers a sedd type may project to
    int maxNumProjectionLayers() const { return maxNumProjectionLayers_; }
    // map of used DTC tfp channels in InputRouter
    std::vector<int> channelEncoding() const { return channelEncoding_; }

  private:
    // checks is seedType is supported
    void checkSeedType(int seedType) const;

    // helper class to store configurations
    const tt::Setup* setup_;
    // use tracklet seed type as channel id if False, binned track pt used if True
    bool useDuplicateRemoval_;
    // pt Boundaries in GeV, last boundary is infinity
    std::vector<double> boundaries_;
    // seed type names
    std::vector<std::string> seedTypeNames_;
    // number of used seed types in tracklet algorithm
    int numSeedTypes_;
    // number of used channels
    int numChannels_;
    // max number layers a sedd type may project to
    int maxNumProjectionLayers_;
    // seeding layers of seed types using default layer id [barrel: 1-6, discs: 11-15]
    std::vector<std::vector<int>> seedTypesSeedLayers_;
    // layers a seed types can project to using default layer id [barrel: 1-6, discs: 11-15]
    std::vector<std::vector<int>> seedTypesProjectionLayers_;
    // map of used DTC tfp channels in InputRouter
    std::vector<int> channelEncoding_;
  };

}  // namespace trklet

EVENTSETUP_DATA_DEFAULT_RECORD(trklet::ChannelAssignment, trklet::ChannelAssignmentRcd);

#endif
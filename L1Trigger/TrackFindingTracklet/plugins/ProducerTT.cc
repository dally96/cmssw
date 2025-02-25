#include "FWCore/Framework/interface/stream/EDProducer.h"
#include "FWCore/Framework/interface/Run.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/Utilities/interface/EDGetToken.h"
#include "FWCore/Utilities/interface/EDPutToken.h"
#include "FWCore/Utilities/interface/ESGetToken.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/Common/interface/Handle.h"

#include "L1Trigger/TrackTrigger/interface/Setup.h"
#include "L1Trigger/TrackerTFP/interface/DataFormats.h"

#include <string>
#include <numeric>

using namespace std;
using namespace edm;
using namespace trackerTFP;
using namespace tt;

namespace trklet {

  /*! \class  trklet::ProducerTT
   *  \brief  Converts KF output into TTTracks
   *  \author Thomas Schuh
   *  \date   2021, Aug
   */
  class ProducerTT : public stream::EDProducer<> {
  public:
    explicit ProducerTT(const ParameterSet&);
    ~ProducerTT() override {}

  private:
    void beginRun(const Run&, const EventSetup&) override;
    void produce(Event&, const EventSetup&) override;
    void endJob() {}

    // ED input token of kf stubs
    EDGetTokenT<StreamsStub> edGetTokenStubs_;
    // ED input token of kf tracks
    EDGetTokenT<StreamsTrack> edGetTokenTracks_;
    // ED output token for TTTracks
    EDPutTokenT<TTTracks> edPutToken_;
    // Setup token
    ESGetToken<Setup, SetupRcd> esGetTokenSetup_;
    // DataFormats token
    ESGetToken<DataFormats, DataFormatsRcd> esGetTokenDataFormats_;
    // configuration
    ParameterSet iConfig_;
    // helper class to store configurations
    const Setup* setup_;
    // helper class to extract structured data from tt::Frames
    const DataFormats* dataFormats_;
  };

  ProducerTT::ProducerTT(const ParameterSet& iConfig) : iConfig_(iConfig) {
    const string& label = iConfig.getParameter<string>("LabelKF");
    const string& branchStubs = iConfig.getParameter<string>("BranchAcceptedStubs");
    const string& branchTracks = iConfig.getParameter<string>("BranchAcceptedTracks");
    // book in- and output ED products
    edGetTokenStubs_ = consumes<StreamsStub>(InputTag(label, branchStubs));
    edGetTokenTracks_ = consumes<StreamsTrack>(InputTag(label, branchTracks));
    edPutToken_ = produces<TTTracks>(branchTracks);
    // book ES products
    esGetTokenSetup_ = esConsumes<Setup, SetupRcd, Transition::BeginRun>();
    esGetTokenDataFormats_ = esConsumes<DataFormats, DataFormatsRcd, Transition::BeginRun>();
    // initial ES products
    setup_ = nullptr;
    dataFormats_ = nullptr;
  }

  void ProducerTT::beginRun(const Run& iRun, const EventSetup& iSetup) {
    // helper class to store configurations
    setup_ = &iSetup.getData(esGetTokenSetup_);
    if (!setup_->configurationSupported())
      return;
    // check process history if desired
    if (iConfig_.getParameter<bool>("CheckHistory"))
      setup_->checkHistory(iRun.processHistory());
    // helper class to extract structured data from tt::Frames
    dataFormats_ = &iSetup.getData(esGetTokenDataFormats_);
  }

  void ProducerTT::produce(Event& iEvent, const EventSetup& iSetup) {
    // empty KFout product
    TTTracks ttTracks;
    // read in KF Product and produce KFout product
    if (setup_->configurationSupported()) {
      Handle<StreamsStub> handleStubs;
      iEvent.getByToken<StreamsStub>(edGetTokenStubs_, handleStubs);
      const StreamsStub& streamsStubs = *handleStubs.product();
      Handle<StreamsTrack> handleTracks;
      iEvent.getByToken<StreamsTrack>(edGetTokenTracks_, handleTracks);
      const StreamsTrack& streamsTracks = *handleTracks.product();
      // count number of kf tracks
      int nTracks(0);
      for (const StreamTrack& stream : streamsTracks)
        nTracks += accumulate(stream.begin(), stream.end(), 0, [](int& sum, const FrameTrack& frame) {
          return sum += frame.first.isNonnull() ? 1 : 0;
        });
      ttTracks.reserve(nTracks);
      // convert kf track frames per channel and stub frames per channel and layer to TTTracks
      for (int channel = 0; channel < (int)streamsTracks.size(); channel++) {
        const int offset = channel * setup_->numLayers();
        int iTrk(0);
        for (const FrameTrack& frameTrack : streamsTracks[channel]) {
          if (frameTrack.first.isNull())
            continue;
          // convert stub frames to kf stubs
          vector<StubKF> stubs;
          stubs.reserve(setup_->numLayers());
          for (int layer = 0; layer < setup_->numLayers(); layer++) {
            const FrameStub& frameStub = streamsStubs[offset + layer][iTrk];
            if (frameStub.first.isNonnull())
              stubs.emplace_back(frameStub, dataFormats_, layer);
          }
          // convert track frame to kf track
          TrackKF track(frameTrack, dataFormats_);
          // convert kf track and kf stubs to TTTrack
          ttTracks.emplace_back(track.ttTrack(stubs));
          iTrk++;
        }
      }
    }
    // store products
    iEvent.emplace(edPutToken_, move(ttTracks));
  }

}  // namespace trklet

DEFINE_FWK_MODULE(trklet::ProducerTT);
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
#include "L1Trigger/TrackFindingTracklet/interface/TrackBuilderChannel.h"
#include "L1Trigger/TrackFindingTracklet/interface/Settings.h"

#include <string>
#include <vector>
#include <deque>
#include <iterator>
#include <cmath>
#include <numeric>

using namespace std;
using namespace edm;
using namespace trackerTFP;
using namespace tt;

namespace trklet {

  /*! \class  trklet::ProducerTBout
   *  \brief  Transforms TTTracks from Tracklet pattern reco. into f/w comparable format
   *  \author Thomas Schuh
   *  \date   2021, Oct
   */
  class ProducerTBout : public stream::EDProducer<> {
  public:
    explicit ProducerTBout(const ParameterSet&);
    ~ProducerTBout() override {}

  private:
    virtual void beginRun(const Run&, const EventSetup&) override;
    virtual void produce(Event&, const EventSetup&) override;
    virtual void endJob() {}

    // ED input token of TTTracks
    EDGetTokenT<TTTracks> edGetTokenTTTracks_;
    // ED input token of Tracklet tracks
    EDGetTokenT<Streams> edGetTokenTracks_;
    // ED input token of Tracklet Stubs
    EDGetTokenT<StreamsStub> edGetTokenStubs_;
    // ED output token for stubs
    EDPutTokenT<StreamsStub> edPutTokenAcceptedStubs_;
    EDPutTokenT<StreamsStub> edPutTokenLostStubs_;
    // ED output token for tracks
    EDPutTokenT<StreamsTrack> edPutTokenAcceptedTracks_;
    EDPutTokenT<StreamsTrack> edPutTokenLostTracks_;
    // Setup token
    ESGetToken<Setup, SetupRcd> esGetTokenSetup_;
    // DataFormats token
    ESGetToken<DataFormats, DataFormatsRcd> esGetTokenDataFormats_;
    // TrackBuilderChannel token
    ESGetToken<TrackBuilderChannel, TrackBuilderChannelRcd> esGetTokenTrackBuilderChannel_;
    // configuration
    ParameterSet iConfig_;
    // helper class to store configurations
    const Setup* setup_;
    // helper class to extract structured data from TTDTC::Frames
    const DataFormats* dataFormats_;
    // helper class to assign tracks to channel
    TrackBuilderChannel* trackBuilderChannel_;
    //
    bool enableTruncation_;
    //
    trklet::Settings settings_;
  };

  ProducerTBout::ProducerTBout(const ParameterSet& iConfig) : iConfig_(iConfig) {
    const InputTag& inputTag = iConfig.getParameter<InputTag>("InputTag");
    const string& branchAcceptedStubs = iConfig.getParameter<string>("BranchAcceptedStubs");
    const string& branchAcceptedTracks = iConfig.getParameter<string>("BranchAcceptedTracks");
    const string& branchLostStubs = iConfig.getParameter<string>("BranchLostStubs");
    const string& branchLostTracks = iConfig.getParameter<string>("BranchLostTracks");
    // book in- and output ED products
    edGetTokenTTTracks_ = consumes<TTTracks>(inputTag);
    edGetTokenTracks_ = consumes<Streams>(inputTag);
    edGetTokenStubs_ = consumes<StreamsStub>(inputTag);
    edPutTokenAcceptedStubs_ = produces<StreamsStub>(branchAcceptedStubs);
    edPutTokenAcceptedTracks_ = produces<StreamsTrack>(branchAcceptedTracks);
    edPutTokenLostStubs_ = produces<StreamsStub>(branchLostStubs);
    edPutTokenLostTracks_ = produces<StreamsTrack>(branchLostTracks);
    // book ES products
    esGetTokenSetup_ = esConsumes<Setup, SetupRcd, Transition::BeginRun>();
    esGetTokenDataFormats_ = esConsumes<DataFormats, DataFormatsRcd, Transition::BeginRun>();
    esGetTokenTrackBuilderChannel_ = esConsumes<TrackBuilderChannel, TrackBuilderChannelRcd, Transition::BeginRun>();
    // initial ES products
    setup_ = nullptr;
    dataFormats_ = nullptr;
    trackBuilderChannel_ = nullptr;
    //
    enableTruncation_ = iConfig.getParameter<bool>("EnableTruncation");
  }

  void ProducerTBout::beginRun(const Run& iRun, const EventSetup& iSetup) {
    // helper class to store configurations
    setup_ = &iSetup.getData(esGetTokenSetup_);
    if (!setup_->configurationSupported())
      return;
    // check process history if desired
    if (iConfig_.getParameter<bool>("CheckHistory"))
      setup_->checkHistory(iRun.processHistory());
    // helper class to extract structured data from TTDTC::Frames
    dataFormats_ = &iSetup.getData(esGetTokenDataFormats_);
    // helper class to assign tracks to channel
    trackBuilderChannel_ = const_cast<TrackBuilderChannel*>(&iSetup.getData(esGetTokenTrackBuilderChannel_));
  }

  void ProducerTBout::produce(Event& iEvent, const EventSetup& iSetup) {
    const int numStreamsTracks = setup_->numRegions() * trackBuilderChannel_->numChannels();
    const int numStreamsStubs = numStreamsTracks * trackBuilderChannel_->maxNumProjectionLayers();
    // empty KFin products
    StreamsStub streamAcceptedStubs(numStreamsStubs);
    StreamsTrack streamAcceptedTracks(numStreamsTracks);
    StreamsStub streamLostStubs(numStreamsStubs);
    StreamsTrack streamLostTracks(numStreamsTracks);
    // read in hybrid track finding product and produce KFin product
    if (setup_->configurationSupported()) {
      // create and structure TTrackRefs in h/w channel
      vector<deque<TTTrackRef>> ttTrackRefs(numStreamsTracks);
      Handle<TTTracks> handleTTTracks;
      iEvent.getByToken<TTTracks>(edGetTokenTTTracks_, handleTTTracks);
      int channelId(-1);
      for (int i = 0; i < (int)handleTTTracks->size(); i++) {
        const TTTrackRef ttTrackRef(handleTTTracks, i);
        if (trackBuilderChannel_->channelId(ttTrackRef, channelId))
          ttTrackRefs[channelId].push_back(ttTrackRef);
      }
      // get and trunacte tracks
      Handle<Streams> handleTracks;
      iEvent.getByToken<Streams>(edGetTokenTracks_, handleTracks);
      channelId = 0;
      for (const Stream& streamTrack : *handleTracks) {
        StreamTrack& accepted = streamAcceptedTracks[channelId];
        StreamTrack& lost = streamLostTracks[channelId];
        auto limit = streamTrack.end();
        if (enableTruncation_ && (int)streamTrack.size() > setup_->numFrames())
          limit = next(streamTrack.begin(), setup_->numFrames());
        accepted.reserve(distance(streamTrack.begin(), limit));
        lost.reserve(distance(limit, streamTrack.end()));
        int nFrame(0);
        const deque<TTTrackRef>& ttTracks = ttTrackRefs[channelId++];
        auto toFrameTrack = [&nFrame, &ttTracks](const Frame& frame) {
          if (frame.any())
            return FrameTrack(ttTracks[nFrame++], frame);
          return FrameTrack();
        };
        transform(streamTrack.begin(), limit, back_inserter(accepted), toFrameTrack);
        transform(limit, streamTrack.end(), back_inserter(lost), toFrameTrack);
      }
      // get and trunacte stubs
      Handle<StreamsStub> handleStubs;
      iEvent.getByToken<StreamsStub>(edGetTokenStubs_, handleStubs);
      const StreamsStub& streamsStub = *handleStubs;
      // reserve output ed products
      channelId = 0;
      for (const StreamStub& streamStub : streamsStub) {
        auto limit = streamStub.end();
        if (enableTruncation_ && (int)streamStub.size() > setup_->numFrames())
          limit = next(streamStub.begin(), setup_->numFrames());
        streamAcceptedStubs[channelId] = StreamStub(streamStub.begin(), limit);
        streamLostStubs[channelId++] = StreamStub(limit, streamStub.end());
      }
    }
    // store products
    iEvent.emplace(edPutTokenAcceptedStubs_, move(streamAcceptedStubs));
    iEvent.emplace(edPutTokenAcceptedTracks_, move(streamAcceptedTracks));
    iEvent.emplace(edPutTokenLostStubs_, move(streamLostStubs));
    iEvent.emplace(edPutTokenLostTracks_, move(streamLostTracks));
  }

}  // namespace trklet

DEFINE_FWK_MODULE(trklet::ProducerTBout);
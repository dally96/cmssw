import FWCore.ParameterSet.Config as cms

from L1Trigger.TrackTrigger.ProducerSetup_cff import TrackTriggerSetup
from L1Trigger.TrackerTFP.Producer_cfi import TrackerTFPProducer_params
from L1Trigger.TrackerTFP.ProducerES_cff import TrackTriggerDataFormats
from L1Trigger.TrackerTFP.ProducerLayerEncoding_cff import TrackTriggerLayerEncoding
from L1Trigger.TrackerTFP.KalmanFilterFormats_cff import TrackTriggerKalmanFilterFormats
from L1Trigger.TrackFindingTracklet.ProducerTrackBuilderChannel_cff import TrackBuilderChannel
from L1Trigger.TrackFindingTracklet.ProducerKF_cfi import TrackFindingTrackletProducerKF_params

TrackFindingTrackletProducerIRin = cms.EDProducer( 'trackFindingTracklet::ProducerIRin', TrackFindingTrackletProducerKF_params )
TrackFindingTrackletProducerTBout = cms.EDProducer( 'trackFindingTracklet::ProducerTBout', TrackFindingTrackletProducerKF_params )
TrackFindingTrackletProducerKFin = cms.EDProducer( 'trackFindingTracklet::ProducerKFin', TrackFindingTrackletProducerKF_params )
TrackFindingTrackletProducerKF = cms.EDProducer( 'trackerTFP::ProducerKF', TrackFindingTrackletProducerKF_params )
TrackFindingTrackletProducerTT = cms.EDProducer( 'trackFindingTracklet::ProducerTT', TrackFindingTrackletProducerKF_params )
TrackFindingTrackletProducerAS = cms.EDProducer( 'trackFindingTracklet::ProducerAS', TrackFindingTrackletProducerKF_params )
TrackFindingTrackletProducerKFout = cms.EDProducer( 'trackFindingTracklet::ProducerKFout', TrackFindingTrackletProducerKF_params )
import FWCore.ParameterSet.Config as cms
from L1Trigger.TrackTrigger.TrackQualityParams_cfi import *
from L1Trigger.TrackFindingTracklet.ChannelAssignment_cff import ChannelAssignment

TTTracksFromTrackletEmulation = cms.EDProducer("L1FPGATrackProducer",
                                               TTStubSource = cms.InputTag("TTStubsFromPhase2TrackerDigis","StubAccepted"),
                                               InputTagTTDTC = cms.InputTag("TrackerDTCProducer", "StubAccepted"),
                                               readMoreMcTruth = cms.bool(True),
                                               MCTruthClusterInputTag = cms.InputTag("TTClusterAssociatorFromPixelDigis", "ClusterAccepted"),
                                               MCTruthStubInputTag = cms.InputTag("TTStubAssociatorFromPixelDigis", "StubAccepted"),
                                               TrackingParticleInputTag = cms.InputTag("mix", "MergedTrackTruth"),
                                               BeamSpotSource = cms.InputTag("offlineBeamSpot"),
                                               asciiFileName = cms.untracked.string(""),
                                               Extended = cms.bool(False),
                                               Reduced = cms.bool(False),
                                               Hnpar = cms.uint32(4),
                                               # (if running on CRAB use "../../fitpattern.txt" etc instead)
                                               fitPatternFile = cms.FileInPath('L1Trigger/TrackFindingTracklet/data/fitpattern.txt'),
                                               memoryModulesFile = cms.FileInPath('L1Trigger/TrackFindingTracklet/data/memorymodules_hourglassExtended.dat'),
                                               processingModulesFile = cms.FileInPath('L1Trigger/TrackFindingTracklet/data/processingmodules_hourglassExtended.dat'),
                                               wiresFile = cms.FileInPath('L1Trigger/TrackFindingTracklet/data/wires_hourglassExtended.dat'),
                                               # Quality Flag and Quality params
                                               TrackQuality = cms.bool(True),
                                               TrackQualityPSet = cms.PSet(TrackQualityParams),
                                               Fakefit = cms.bool(False),
                                               EmulateTB = cms.bool(False)
    )

TTTracksFromExtendedTrackletEmulation = TTTracksFromTrackletEmulation.clone(
                                               Extended = cms.bool(True),
                                               Reduced = cms.bool(False),
                                               Hnpar = cms.uint32(5),
                                               # specifying where the TrackletEngineDisplaced(TED)/TripletEngine(TRE) tables are located
                                               tableTEDFile = cms.FileInPath('L1Trigger/TrackFindingTracklet/data/table_TED/table_TED_D1PHIA1_D2PHIA1.txt'),
                                               tableTREFile = cms.FileInPath('L1Trigger/TrackFindingTracklet/data/table_TRE/table_TRE_D1AD2A_1.txt'),
                                               # Quality Flag and Quality params
                                               TrackQuality = cms.bool(False),
                                               TrackQualityPSet = cms.PSet(TrackQualityParams)
    )
# The included files correspond to the reduced "Summer Chain" configuration
# These files can be modified to emulate any other reduced configuration
TTTracksFromReducedTrackletEmulation = TTTracksFromTrackletEmulation.clone(
                                               Reduced = cms.bool(True),
                                               # specifying where the reduced configuration files are
                                               memoryModulesFile = cms.FileInPath('L1Trigger/TrackFindingTracklet/data/reduced_memorymodules.dat'),
                                               processingModulesFile = cms.FileInPath('L1Trigger/TrackFindingTracklet/data/reduced_processingmodules.dat'),
                                               wiresFile = cms.FileInPath('L1Trigger/TrackFindingTracklet/data/reduced_wires.dat'),
    )

# this is to run Tracklet pattern reco with new KF
TrackletTracksFromTrackletEmulation = TTTracksFromTrackletEmulation.clone(
                                               Fakefit = cms.bool(True)
    )
import FWCore.ParameterSet.Config as cms

def summerChainConfig(process):
    process.TrackTriggerSetup.Firmware.FreqBE = 240
    process.TrackTriggerSetup.KalmanFilter.NumWorker = 1
    process.TrackBuilderChannel.SummerChain = True
    process.TrackBuilderChannel.MaxNumProjectionLayers = 4
    process.TrackFindingTrackletProducerIRin.SummerChain = True
    process.TTTracksFromTrackletEmulation.Fakefit = True
    process.TTTracksFromTrackletEmulation.RemovalType = ""
    process.TTTracksFromTrackletEmulation.DoMultipleMatches = False
    process.TTTracksFromTrackletEmulation.Reduced = True
    process.TTTracksFromTrackletEmulation.memoryModulesFile = 'L1Trigger/TrackFindingTracklet/data/reduced_memorymodules.dat'
    process.TTTracksFromTrackletEmulation.processingModulesFile = 'L1Trigger/TrackFindingTracklet/data/reduced_processingmodules.dat'
    process.TTTracksFromTrackletEmulation.wiresFile = 'L1Trigger/TrackFindingTracklet/data/reduced_wires.dat'
    return process

def newKFConfig(process):
    process.TTTracksFromTrackletEmulation.Fakefit = True
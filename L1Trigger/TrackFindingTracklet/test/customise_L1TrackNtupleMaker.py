############################################################
# define basic process
############################################################
import FWCore.ParameterSet.VarParsing as VarParsing
options = VarParsing.VarParsing ('analysis')

options.outputFile = 'outputHLT.root'
options.inputFiles = 'infile.root'
options.parseArguments()


from L1TrackNtupleMaker_cfg import *

process.TFileService = cms.Service("TFileService", fileName = cms.string(options.outputFile), closeFileFast = cms.untracked.bool(True))

process.maxEvents.input = cms.untracked.int32(-1)
process.source.fileNames = cms.untracked.vstring (options.inputFiles)

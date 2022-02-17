#!/bin/tcsh
source  /cvmfs/cms.cern.ch/cmsset_default.csh
pushd /afs/cern.ch/user/d/dally/CMSSW_12_0_0_pre4/src/L1Trigger/TrackFindingTracklet/test
eval `scram runtime -csh`

setenv X509_USER_PROXY $1
voms-proxy-info -all
voms-proxy-info -all -file $1

setenv ifile $2 

echo cmsRun /afs/cern.ch/user/d/dally/CMSSW_12_0_0_pre4/src/L1Trigger/TrackFindingTracklet/test/customise_L1TrackNtupleMaker.py inputFiles_clear inputFiles_load=/afs/cern.ch/user/d/dally/CMSSW_12_0_0_pre4/src/L1Trigger/TrackFindingTracklet/test/ntuples/No_DR_Test2/pFiles_$ifile.txt outputFile=outputL1Ntuple_$ifile.root print
cmsRun /afs/cern.ch/user/d/dally/CMSSW_12_0_0_pre4/src/L1Trigger/TrackFindingTracklet/test/customise_L1TrackNtupleMaker.py inputFiles_clear inputFiles_load=/afs/cern.ch/user/d/dally/CMSSW_12_0_0_pre4/src/L1Trigger/TrackFindingTracklet/test/ntuples/No_DR_Test2/pFiles_$ifile.txt outputFile=outputL1Ntuple_$ifile.root print
mv outputL1Ntuple_$ifile.root /afs/cern.ch/user/d/dally/CMSSW_12_0_0_pre4/src/L1Trigger/TrackFindingTracklet/test/ntuples/No_DR_Test2/ 

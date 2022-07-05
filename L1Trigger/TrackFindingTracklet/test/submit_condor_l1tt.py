#!/bin/env python

import os
import subprocess
import datetime
from argparse import ArgumentParser
import pdb
import math
# from samples import samples
from glob import glob
from pdb import set_trace

parser = ArgumentParser()
parser.add_argument("analyzer", help = "which analyser to run", default = 'L1TrackNtupleMaker_cfg.py' )
parser.add_argument("sample", help = "sample", default = 'ttbar_pu200_d76' )
parser.add_argument("-n"  , "--njobs"  , dest = "njobs"  ,  type = int, help = "tot number of input files to be read. All = -1" , default =  -1                            )
parser.add_argument("-d"  , "--outdir" , dest = "outdir" ,  help = "output dir"                                     , default = "ntuples" )
parser.add_argument("-a"  , "--addtag" , dest = "addtag" ,  help = "add tag to output dir"                          , default = "ntuples" )
parser.add_argument("-t"  , "--test"   , dest = "test"   ,  help = "do not submit to queue"                        , default = False, action='store_true')
args = parser.parse_args()


script_loc = os.path.realpath(args.analyzer)
print(script_loc)
base_out = '%s/%s' %(args.outdir, args.addtag)
filelist_loc = os.path.realpath(base_out) + '/'
os.makedirs('%s/scripts'%base_out)
os.makedirs('%s/outCondor'%base_out)

##  output folder for root files
full_eos_out = '{eos_out_folder}/{base_out}/'.format(eos_out_folder = os.getcwd(), base_out = base_out)
    
sample_dict = {
  'ttbar_pu200_d76'     : '/RelValTTbar_14TeV/CMSSW_11_3_0_pre6-PU_113X_mcRun4_realistic_v6_2026D76PU200-v1/GEN-SIM-DIGI-RAW', 
}

ds_name = sample_dict[args.sample]

# njobs = 0
filelistname = '%s_filelist.txt'%args.sample
if not os.path.isfile(filelistname):
    with open(filelistname, 'w') as f:
        process = subprocess.Popen(['dasgoclient', '--query=file dataset=%s'%ds_name, '--format=list'], stdout=f)
        process.wait()

# files = open(filelistname, 'r').readlines()
# with open(filelistname, 'r') as f:
# njobs = len(open(filelistname, 'r').readlines())
# njobs=len(open(filelistname, 'r').readlines())
# os.system('cp {fname} {base_out}'.format(fname=filelistname, base_out=base_out))


## get number of jobs
njobs = args.njobs
inlist = open(filelistname, 'r')
infiles = inlist.readlines()
if args.njobs == -1:         
    njobs = len(infiles)
inlist.close()    

## for each input file, create one single list
pfilenames = 'pFiles'
for i in range(njobs):
    ifile = infiles[i]
    ipfilenames   = pfilenames + '_%s.txt'%i
    ## create list of one miniaod
    with open(ipfilenames, 'w') as f:
        f.write(ifile)
    os.system('mv {fname} {base_out}'.format(fname=ipfilenames, base_out=base_out))
        


os.system('cp {fname} {base_out}'.format(fname=filelistname, base_out=base_out))
print 'n jobs to be submitted: ', njobs 

bname = os.path.realpath('%s/scripts/script_condor.sh'%base_out)
getcwd = os.getcwd()

command_string = "cmsRun {script_loc} inputFiles_clear inputFiles_load={pFiles}_$ifile.txt outputFile=outputL1Ntuple_$ifile.root print".format(\
        script_loc   = script_loc, 
        pFiles = filelist_loc+pfilenames
        )

with open(bname, 'w') as batch:
    batch.write('''#!/bin/tcsh
source  /cvmfs/cms.cern.ch/cmsset_default.csh
pushd {cwd}
eval `scram runtime -csh`

setenv X509_USER_PROXY $1
voms-proxy-info -all
voms-proxy-info -all -file $1

setenv ifile $2 
echo {the_command_string}
{the_command_string}
mv outputL1Ntuple_$ifile.root {full_eos_out} 
'''
.format(script_loc   = script_loc, 
        full_eos_out = full_eos_out,
        primaryFilesList = args.sample,
        pFiles = filelist_loc+pfilenames,
        cwd    = getcwd,
        the_command_string = command_string
#         thesample    = args.sample
        )
)
subprocess.call(['chmod', '+x', bname])
    

## write the cfg for condor submission condor_multiple_readnano.cfg
with open('%s/condor_sub.cfg'%base_out, 'w') as cfg:
    cfg.write('''Universe = vanilla
Executable = {bname}
use_x509userproxy = True 
Proxy_path = /afs/cern.ch/user/d/dally/private/x509up_u141138
transfer_input_files = {filelistname}
Should_Transfer_Files = YES
WhenToTransferOutput = ON_EXIT
getenv = False
requirements = (OpSysAndVer =?= "CentOS7")
Log    = {base_out}/outCondor/condor_job_$(Process).log
Output = {base_out}/outCondor/condor_job_$(Process).out
Error  = {base_out}/outCondor/condor_job_$(Process).err
Arguments = $(Proxy_path) $(Process) 
on_exit_remove = (ExitBySignal == False) && (ExitCode == 0)
max_retries = 3
requirements = Machine =!= LastRemoteHost
+JobFlavour = "longlunch"
Queue {njobs}'''.format( bname = bname, 
                    base_out = base_out, 
                    outdir = args.outdir, 
#                     sample = args.sample, 
                    filelistname = filelistname,
#                      era = args.era, 
                    njobs = njobs )
)    
    # submit to the queue
print('condor_submit {base_out}/condor_sub.cfg'.format(base_out=base_out))
if not args.test:
    os.system("condor_submit {base_out}/condor_sub.cfg".format(base_out=base_out))   


# +JobFlavour = "{flavour}"

# import numpy
from argparse import ArgumentParser
import math

parser = ArgumentParser()
parser.add_argument("-i"  , "--input"     , dest = "input"     ,  help = "input file"       , default = ''                        )
parser.add_argument("-d"  , "--diff"      , dest = "diff"      ,  help = "plot differences" , default = False, action='store_true')
parser.add_argument("-l"  , "--leg"       , dest = "leg"       ,  help = "legend labels"    , default = ''                        )
parser.add_argument("-o"  , "--outtag"    , dest = "ouffiletag",  help = "tag for out pdf file"    , default = 'default'                        )

options = parser.parse_args()
if not options.input:   
  parser.error('Input filename not given')

import ROOT
from   ROOT  import TFile, TLine, TTree, gDirectory, TH1F, TCanvas, TLegend, TEfficiency, gPad, gStyle, gROOT, TGaxis, TPad, TGraphErrors, TPaveText
from   array import array
from   math  import sqrt, isnan
from   copy  import deepcopy as dc

gStyle.SetOptStat('emr')
gStyle.SetTitleAlign(23)
gStyle.SetPadLeftMargin(0.16)
gStyle.SetPadBottomMargin(0.16)
TGaxis.SetMaxDigits(3)

gROOT.SetBatch(True)
import pdb; 

namefiles = options.input.split(',')
nfiles   = len(namefiles)
files    = []

print('number of input files is ' + str(nfiles))

for i in range(0, nfiles):
  print('opening file ' + str(i) + ': ' + namefiles[i])
  files.append(TFile.Open(namefiles[i]   , 'r') )


pt_bins  = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,20,25] 
pt_binsExtended  = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,20,25,40,70,100] 
eta_bins = [-2.4, -2.1, -1.6, -1.2, -0.9, -0.3, -0.2, 0.2, 0.3, 0.9, 1.2, 1.6, 2.1, 2.4]

colorlist = [ROOT.kBlack, ROOT.kRed, ROOT.kAzure+1, ROOT.kOrange, ROOT.kGreen+2, ROOT.kViolet, ROOT.kBlue, ROOT.kGray, ROOT.kMagenta+3, ROOT.kOrange+2, ROOT.kYellow]


def doHisto(file, var, thecolor, i, marker=8, toReplace=[]):
#   pdb.set_trace()
  if len(toReplace)==0:
    pEff = file.Get(var[0])
  else:    
    pEff = file.Get(var[0].replace(toReplace[0],toReplace[1]))
  pEff.SetLineColor(thecolor)
  pEff.SetMarkerColor(thecolor)
  pEff.SetMarkerStyle(marker  )
  pEff.SetMarkerSize(0.8)

  pEff.SetTitle(";" + var[1] + ";" + var[2])
  return pEff


ytitlez = 'z0 resolution'
ytitlep = 'pt resolution'
ytitlep2 = 'pt resolution/pt'
ytitlee = 'efficiency'
variables = [
#  numerator          # x axis title        # y title   # nbins    # x range      # y range      # pdf name                     # legend position         #y range ratio          
    #('notloose_pt' , 'Track p_{T}'                  , 'not loose fraction',   17   , pt_bins, (0.00 , 0.13), 'notloosefraction',   (0.2 , 0.35, 0.75, 0.88),  (0.501, 1.05 )), 
    #('combinatoric_pt' , 'Track p_{T}'                  , 'combinatoric fraction',   50   , (  0   , 100   ), (0.00 , 0.13), 'combinatoricfraction',   (0.2 , 0.35, 0.75, 0.88),  (0.501, 1.05 )), 
  #  ('eff_pt_L'            , 'p_{T}'               , ytitlee,    40   , (  0   , 8), (0   , 1.1),     'effVsPt_L',      (0.7 , 0.85, 0.25, 0.38),  (0.501, 1.05 )), 
    #('eff_eta'           , '#eta'              , ytitlee,   100   , ( -2.4  , 2.4    ), (0.8  , 1.0),    'effVsEta',      (0.7 , 0.85, 0.25, 0.38),  (0.5  , 1.05  )),
   # ('eff_eta_L1L2'           , '#eta'              , ytitlee,   100   , ( -2.4  , 2.4    ), (0  , 1.0),    'effVsEta_L1L2',      (0.7 , 0.85, 0.25, 0.38),  (0.5  , 1.05  )),
   # ('eff_eta_L2L3'           , '#eta'              , ytitlee,   100   , ( -2.4  , 2.4    ), (0  , 1.0),    'effVsEta_L2L3',      (0.7 , 0.85, 0.25, 0.38),  (0.5  , 1.05  )),
   # ('eff_eta_L3L4'           , '#eta'              , ytitlee,   100   , ( -2.4  , 2.4    ), (0  , 1.0),    'effVsEta_L3L4',      (0.7 , 0.85, 0.25, 0.38),  (0.5  , 1.05  )),
   # ('eff_eta_L5L6'           , '#eta'              , ytitlee,   100   , ( -2.4  , 2.4    ), (0  , 1.0),    'effVsEta_L5L6',      (0.7 , 0.85, 0.25, 0.38),  (0.5  , 1.05  )),
   # ('eff_eta_D1D2'           , '#eta'              , ytitlee,   100   , ( -2.4  , 2.4    ), (0  , 1.0),    'effVsEta_D1D2',      (0.7 , 0.85, 0.25, 0.38),  (0.5  , 1.05  )),
   # ('eff_eta_D3D4'           , '#eta'              , ytitlee,   100   , ( -2.4  , 2.4    ), (0  , 1.0),    'effVsEta_D3D4',      (0.7 , 0.85, 0.25, 0.38),  (0.5  , 1.05  )),
   # ('eff_eta_L1D1'           , '#eta'              , ytitlee,   100   , ( -2.4  , 2.4    ), (0  , 1.0),    'effVsEta_L1D1',      (0.7 , 0.85, 0.25, 0.38),  (0.5  , 1.05  )),
   # ('eff_eta_L2D1'           , '#eta'              , ytitlee,   100   , ( -2.4  , 2.4    ), (0  , 1.0),    'effVsEta_L2D1',      (0.7 , 0.85, 0.25, 0.38),  (0.5  , 1.05  )),
   # ('eff_eta_L2L3L4'           , '#eta'              , ytitlee,   100   , ( -2.4  , 2.4    ), (0  , 1.0),    'effVsEta_L2L3L4',      (0.7 , 0.85, 0.25, 0.38),  (0.5  , 1.05  )),
   # ('eff_eta_L4L5L6'           , '#eta'              , ytitlee,   100   , ( -2.4  , 2.4    ), (0  , 1.0),    'effVsEta_L4L5L6',      (0.7 , 0.85, 0.25, 0.38),  (0.5  , 1.05  )),
   # ('eff_eta_L2L3D1'           , '#eta'              , ytitlee,   100   , ( -2.4  , 2.4    ), (0  , 1.0),    'effVsEta_L2L3D1',      (0.7 , 0.85, 0.25, 0.38),  (0.5  , 1.05  )),
   # ('eff_eta_D1D2L2'           , '#eta'              , ytitlee,   100   , ( -2.4  , 2.4    ), (0  , 1.0),    'effVsEta_D1D2L2',      (0.7 , 0.85, 0.25, 0.38),  (0.5  , 1.05  )),
    #('eff_pt'            , 'p_{T}'               , ytitlee,    20   , pt_binsExtended, (0.85   , 1),     'effVsPt',      (0.6 , 0.75, 0.25, 0.38),  (0.501, 1.05 )), 
    #('eff_phi'           , '#phi'                , ytitlee,    35   , (-3.2, 3.2), (0.9, 1.0),            'effVsPhi',     (0.6 , 0.85, 0.25, 0.38),  (0.501, 1.05 )),
    #('eff_phi_disp'           , '#phi'                , '#phi efficiency (d_{0} > 0.01 cm)',    35   , (-3.2, 3.2), (0.7, 1.0),            'effVsPhiDisp',     (0.6 , 0.85, 0.25, 0.38),  (0.501, 1.05 )),
# # #  ('eff_d0'            , 'd0'                  , ytitlee,    50   , ( -10. ,  10. ), (0.   , 1.),    'effVsD0',       (0.2 , 0.5, 0.75, 0.88),  (0.5  , 1.05  )),
# # #  ('eff_z0'            , 'z0'                  , ytitlee,    50   , ( -10. ,  10. ), (0.   , 1.),    'effVsZ0',       (0.2 , 0.5, 0.75, 0.88),  (0.5  , 1.05  )),
  ('duplicatefrac_pt' , 'p_{T} [GeV]'          , 'duplicate fraction',    17   , pt_binsExtended, (0.   , .08),    'dupVsPt',       (0.2 , 0.4, 0.55, 0.68),  (0.5  , 1.05  )),
  #('duplicatefrac_phi' , '#phi [rad]'          , 'duplicate fraction',    64   , (-3.2, 3.2), (0.   , .035),    'dupVsPhi',       (0.25 , 0.45, 0.75, 0.88),  (0.5  , 1.05  )),
  #('matchtp_pt', 'p_{T} [GeV]', 'A.U.', 20, (0, 100), (0, 1), 'matchtp_pt',  (0.65, 0.85, 0.75, 0.88), (0.5, 1.05)),
  #('matchtp_eta', '#eta', 'A.U.', 50, (-2.5, 2.5), (0, 0.1), 'matchtp_eta', (0.25 , 0.45, 0.75, 0.88), (0.5, 1.05)),
  #('matchtp_pdgid', 'pdgId', 'A.U.', 2300, (0, 2300), (0, 1), 'matchtp_pdgId', (0.65, 0.85, 0.75, 0.88), (0.5, 1.05)),
  #('matchtrk_nmatch', 'nmatch', 'A.U.', 7, (0, 7), (0, 1), 'matchtp_nmatch', (0.65, 0.85, 0.75, 0.88), (0.5, 1.05)),
  #('matchtp_phi', '#phi', 'A.U.', 64, (-3.2, 3.2), (0, 0.2), 'matchtp_phi', (0.25 , 0.45, 0.75, 0.88), (0.5, 1.05)),
  #('matchtrk_pt', 'p_{T} [GeV]', 'A.U.', 20, (0, 100), (0, 1), 'matchtrk_pt',  (0.25 , 0.45, 0.75, 0.88), (0.5, 1.05)),
  #('matchtrk_eta', '#eta', 'A.U.', 50, (-2.5, 2.5), (0, 0.1), 'matchtrk_eta', (0.25 , 0.45, 0.75, 0.88), (0.5, 1.05)), 
  #('matchtrk_nstub', 'nstub', 'A.U.', 10, (0, 10), (0, 1), 'matchtrk_nstub', (0.25 , 0.45, 0.75, 0.88), (0.5, 1.05)),
  #('matchtrk_z0', 'z_{0} [cm]', 'A.U.', 100, (0, 10), (0, 0.1), 'matchtrk_z0', (0.25 , 0.45, 0.75, 0.88), (0.5, 1.05)),  
  #('duplicatefrac_rinv' , 'rInv [cm^{-1}]'          , 'duplicate fraction',    60   , (0, 6E-3), (0.   , .08),    'dupVsRInv',       (0.5 , 0.7, 0.65, 0.88),  (0.5  , 1.05  )),
  #('resVsRInv2_pt', 'rInv [cm^{-1}]'            , 'p_{T} resolution [GeV]',     20,     (0, 6E-3),    (0, 2E1),                 'resVsRInv_pt', (0.6 , 0.85, 0.25, 0.38), (0.5, 1.05 )),
  #('resVsRInv2_phi', 'rInv [cm^{-1}]'            , '#phi resolution [rad]',     20,     (0, 6E-3),    (0, 0.003),                 'resVsRInv_phi', (0.6 , 0.85, 0.25, 0.38), (0.5, 1.05 )),
  #('resVsRInv2_rInv', 'rInv [cm^{-1}]'            , 'rInv resolution [cm^{-1}]',     20,     (0, 6E-3),    (0, 0.12E-3),          'resVsRInv_phi', (0.6 , 0.85, 0.25, 0.38), (0.5, 1.05 )),
  #('resVsEta_rInv', "#eta", "rInv resolution [cm^{-1}]", 64, (-3.2, 3.2), (0.   , .08), "resVsEta_rInv", (0.6 , 0.85, 0.25, 0.38), (0.5, 1.05 )),
  #('resVsEta_phi', "#eta", "#phi resolution [rad]",  64, (-3.2, 3.2), (0.   , 3E-3), "resVsEta_phi", (0.6 , 0.85, 0.25, 0.38), (0.5, 1.05 )),
  #('resVsEta_pt', "#eta", "p_{T} resolution [GeV]",  64, (-3.2, 3.2), (0.   , 0.25), "resVsEta_pt", (0.6 , 0.85, 0.25, 0.38), (0.5, 1.05 )),
  #('notgenuine_pt_extended' , 'p_{T} [GeV]'          , 'not genuine fraction',    17   , pt_binsExtended, (0.   , 1),    'notgenfrac_pt',       (0.22, 0.42, 0.78, 0.91),  (0.5  , 1.05  )),
  #('notgenuine_phi' , '#phi [rad]'          , 'not genuine fraction',    35   , (-0.35, 0.35), (0.   , 0.5),    'notgenfrac_phi',       (0.2 , 0.5, 0.45, 0.58),  (0.5  , 1.05  )),
  #('genuine_pt_extended' , 'p_{T} [GeV]'          , 'genuine fraction',    17   , pt_binsExtended, (0.   , 1),    'genfrac_pt',       (0.22, 0.42, 0.68, 0.81),  (0.5  , 1.05  )),
  #('genuine_phi' , '#phi [rad]'          , 'genuine fraction',    35   , (-0.35, 0.35), (0.5   , 1),    'genfrac_phi',       (0.2 , 0.4, 0.67, 0.80),  (0.5  , 1.05  )),
  #('trk_chi2_dof',  'chi^{2}/ndof', 'A.U.', 100, (0, 10), (0, 0.2), 'chi2_dof', (0.5 , 0.9, 0.5, 0.65), (0.501, 1.05)),
  #("duplicate_pt",      'p_{T} [GeV]',          'A.U.',                   200,     (0, 100), (0, 10000), 'dup', (0.7 , 0.85, 0.5, 0.65), (0.5  , 1.05  )),
  #('trk_pt', 'p_{T} [GeV]',          'A.U.',                   200,     (0, 100), (0, 8E5), 'trk_pt', (0.7 , 0.85, 0.5, 0.65), (0.5  , 1.05  ))     
  #("res_eta", "eta residual (L1 - sim)", "A.U.", 300, (-0.3, 0.3), (0, 0.1), "resEta", (0.7 , 0.9, 0.5,  0.65), (0.501, 1.05)),
  #("res_phi", "phi residual (L1 - sim)", "A.U.", 300, (-0.3, 0.3), (0, 0.1), "resPhi", (0.7 , 0.9, 0.5,  0.65), (0.501, 1.05)),
  #("res_pt", "pt residual (L1 - sim)", "A.U.", 300, (-0.3, 0.3), (0, 0.1), "resPt", (0.7 , 0.9, 0.5,  0.65), (0.501, 1.05)),
  #('match_trk_seed',  'seed type',  'A.U.', 8, (-0.5, 7.5), (1E-4, 1), 'seedType',  ( 0.2 , 0.35, 0.25, 0.38 ), (0.5, 1.05)),
  #('match_trk_seedRank',  'seed rank',  'A.U.', 9, (-0.5, 7.5), (1E-9, 1), 'seedRank',  ( 0.6 , 0.75, 0.25, 0.38 ), (0.5, 1.05)),
  #('eff_pt_perseedL1L2', "p_{T}",  ytitlee, 19, pt_binsExtended, (0.7, 1.), "effVsPt_L1L2", (0.2 , 0.5, 0.75, 0.88), (0.501, 1.05 )),
  #('eff_pt_perseedL2L3', "p_{T}",  ytitlee, 19, pt_binsExtended, (0, 0.009), "effVsPt_L2L3", (0.2 , 0.5, 0.75, 0.88), (0.501, 1.05 )),
  #('eff_pt_perseedL3L4', "p_{T}",  ytitlee, 19, pt_binsExtended, (0, 0.08), "effVsPt_L3L4", (0.2 , 0.5, 0.75, 0.88), (0.501, 1.05 )),
  #('eff_pt_perseedL5L6', "p_{T}", ytitlee, 19, pt_binsExtended, (0, 0.006), "effVsPt_L5L6", (0.2 , 0.5, 0.75, 0.88), (0.501, 1.05 )),
  #('eff_pt_perseedL1D1', "p_{T}", ytitlee, 19, pt_binsExtended, (0, 0.006), "effVsPt_L1D1", (0.5 , 0.75, 0.75, 0.88), (0.501, 1.05 )),
  #('eff_pt_perseedL2D1', "p_{T}", ytitlee, 19, pt_binsExtended, (0,0.006), "effVsPt_L2D1", (0.2 , 0.5, 0.75, 0.88), (0.501, 1.05 )),
  #('eff_pt_perseedD1D2', "p_{T}", ytitlee, 19, pt_binsExtended, (0,0.14), "effVsPt_D1D2", (0.2 , 0.5, 0.75, 0.88), (0.501, 1.05 )),
  #('eff_pt_perseedD3D4', "p_{T}", ytitlee, 19, pt_binsExtended, (0, 0.1), "effVsPt_D3D4", (0.2 , 0.5, 0.75, 0.88), (0.501, 1.05 )),
] 

import pdb

for i in files:
  for var in variables:
    print(i)
    print(var[0])
    print(i.Get(var[0]))

c2 = TCanvas('c2', 'c2', 1000,1000)
c1 = TCanvas('c1', 'c1', 1000,1000)
if options.diff:
  stackPad = ROOT.TPad('stackPad', 'stackPad', 0.,  .25, 1., 1.  , 0, 0)  
  ratioPad = ROOT.TPad('ratioPad', 'ratioPad', 0., 0., 1.,  .3, 0, 0)  
else:
  stackPad = ROOT.TPad('stackPad', 'stackPad', 0,  .25 , 1., 1.  , 0, 0)  
  ratioPad = ROOT.TPad('ratioPad', 'ratioPad', 0., 0. , 1., .3  , 0, 0)  

## define baseline legend
leg_labels = []
if options.leg:
  for i in range(len(files)):
    leg_labels.append(options.leg.split(',')[i])

  for var in variables:
    c1.cd()
    stackPad.Draw()
    ratioPad.Draw()

    l = TLegend(var[7][0], var[7][2], var[7][1], var[7][3])
    l.SetBorderSize(1)
    l.SetTextSize(0.023)

    eff_list = [] 
    for i, ifile in enumerate(files):
      c2.cd() 
      eff_list.append(dc(doHisto(ifile , var, colorlist[i], i)))

      if '_68' in var[0]:
        if i==0:
          sec_leg = TLegend( .66, .75, .75, .88 )
#         sec_leg = TLegend( .8, .2, .9, .35 )
          sec_leg.SetBorderSize(1)
          sec_leg.SetTextSize(0.022)
          sec_leg.AddEntry(eff_list[-1], '68%', 'p')

        eff_list.append(dc(doHisto(ifile , var, colorlist[i], i, 26, ['68','90'])))
        eff_list[-1].SetLineStyle(2)
        eff_list[-1].SetLineWidth(1)
        if i==0:  sec_leg.AddEntry(eff_list[-1], '90%', 'p')

        eff_list.append(dc(doHisto(ifile , var, colorlist[i], i, 25, ['68','99'])))
        eff_list[-1].SetLineStyle(3)
        eff_list[-1].SetLineWidth(1)
        if i==0:  sec_leg.AddEntry(eff_list[-1], '99%', 'p')

    c1.cd()
    stackPad.cd()

    drawOption = 'PL'*('res' in var[0]) + 'E1P'*('res' not in var[0])
    for i,k in enumerate(eff_list):
      Mean = '%.3f'%(k.GetMean())
      RMS = '%.3f'%(k.GetRMS())
      if (i == 0):
        if (var[2] == "A.U."):
          k.Scale(1/k.GetEntries())  
        k.Draw(drawOption)
        #if ("rinv" in var[0]):
         # bin1 = ROOT.TLine(
        #c1.Update()
        #c1.Modified()

        k.SetMarkerSize(1)

        #k.GetXaxis().SetRangeUser(var[4][0],var[4][1])
        k.GetYaxis().SetRangeUser(var[5][0],var[5][1])             
        k.GetXaxis().SetLabelSize(0.04)
        k.GetYaxis().SetLabelSize(0.04)   
        k.GetXaxis().SetTitleSize(0.04)
        k.GetYaxis().SetTitleSize(0.04)
        k.GetYaxis().SetTitleOffset(1.5)
        k.GetXaxis().SetTitleOffset(1.2)
        
        #if 'eff_phi' in var[0]:
        #  lines = []
        #  for sec in range(8):
        #    lines.append(TLine((2 * sec - 7) * math.pi / 9, gPad.GetUymin(), (2 * sec - 7) * math.pi / 9, gPad.GetUymax()))
        #  for sec in range(8):
        #    lines[sec].Draw('SAME') 
        
      else:
        k.SetMarkerSize(1)
        if (var[2] == "A.U."):
          k.Scale(1/k.GetEntries())  
        k.Draw(drawOption + 'SAME')

      if options.leg and '68' not in var[0]:
          l.AddEntry(k , leg_labels[i], "pel")
      elif options.leg and i%3==0:
          l.AddEntry(k , leg_labels[i/3]  , "pel")

    if options.leg: l.Draw()
    if '_68' in var[0] :
      sec_leg.Draw()


    gPad.SetGridx(True)
    gPad.SetGridy(True)
    c1.SaveAs("" +  var[6] + "_D88_%s.pdf"%options.ouffiletag)

import math
import numpy as np
import awkward as ak
import scipy
import matplotlib as mpl
from matplotlib import pyplot as plt
import uproot 

ex_wb  = uproot.open("ExtendedTracking_withBins_seedRankBugFix.root")
ex_wob = uproot.open("ExtendedTracking_withoutBins_seedRankBugFix.root")
pr_wb  = uproot.open("RegularTracking_withBins_seedRankBugFix.root")
pr_wob = uproot.open("RegularTracking_withoutBins_seedRankBugFix.root")

events_ex_wb  = ex_wb["L1TrackNtuple/eventTree"]
events_ex_wob = ex_wob["L1TrackNtuple/eventTree"]
events_pr_wb  = pr_wb["L1TrackNtuple/eventTree"]
events_pr_wob = pr_wob["L1TrackNtuple/eventTree"]

ex_wob_pt = events_ex_wob["trk_pt"].array()
ex_wob_eta = events_ex_wob["trk_eta"].array()

ex_wb_pt = events_ex_wb["trk_pt"].array()
ex_wb_eta = events_ex_wb["trk_eta"].array()

pr_wob_pt = events_pr_wob["trk_pt"].array()
pr_wob_eta = events_pr_wob["trk_eta"].array()

pr_wb_pt = events_pr_wb["trk_pt"].array()
pr_wb_eta = events_pr_wb["trk_eta"].array()



#plt.hist(ak.flatten(wob_pt), bins = np.linspace(0,50,26), weights = [1/len(ak.flatten(wob_pt, axis = None)),] * len(ak.flatten(wob_pt, axis = None)), histtype = "step", color = "blue", label = "Prompt tracking w/ bins")
#plt.hist(ak.flatten(wb_pt), bins = np.linspace(0,50,26), weights = [1/len(ak.flatten(wb_pt, axis = None)),] * len(ak.flatten(wb_pt, axis = None)), histtype = "step", color = "red", label = "Extended tracking w/ bins")
#plt.xlabel("pt [GeV]")
#plt.ylabel("Fraction of tracks")
##plt.title("Both types tracking")
#plt.legend()
#plt.savefig("extended_trk_pt.pdf")

plt.cla()
plt.hist(ak.flatten(ex_wob_eta), bins = np.linspace(-2.4,2.4,25),  weights = [1/len(ak.flatten(ex_wob_eta, axis = None)),] * len(ak.flatten(ex_wob_eta, axis = None)), histtype = "step", color = "blue", label = "Extended no bins")
plt.hist(ak.flatten(ex_wb_eta), bins = np.linspace(-2.4,2.4,25), weights = [1/len(ak.flatten(ex_wb_eta, axis = None)),] * len(ak.flatten(ex_wb_eta, axis = None)), histtype = "step", color = "red", label = "Extended bins")
plt.hist(ak.flatten(pr_wob_eta), bins = np.linspace(-2.4,2.4,25),  weights = [1/len(ak.flatten(pr_wob_eta, axis = None)),] * len(ak.flatten(pr_wob_eta, axis = None)), histtype = "step", color = "green", label = "Prompt no bins")
plt.hist(ak.flatten(pr_wb_eta), bins = np.linspace(-2.4,2.4,25), weights = [1/len(ak.flatten(pr_wb_eta, axis = None)),] * len(ak.flatten(pr_wb_eta, axis = None)), histtype = "step", color = "black", label = "Prompt bins")
#plt.hist(ak.flatten(wob_eta), bins = np.linspace(-2.4,2.4,25), histtype = "step", color = "blue", label = "Prompt tracking w/ bins")
#plt.hist(ak.flatten(wb_eta), bins = np.linspace(-2.4,2.4,25), histtype = "step", color = "red", label = "Extended tracking w/ bins")
plt.xlabel("eta")
plt.ylabel("Fraction of tracks")
#plt.title("Extended tracking")
plt.legend()
plt.savefig("extended_trk_eta.pdf")




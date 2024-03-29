import math
import numpy as np
import awkward as ak
import scipy
import matplotlib as mpl
from matplotlib import pyplot as plt
import uproot 

wb = uproot.open("ExtendedTracking_withBins_seedRankBugFix.root")
wob = uproot.open("RegularTracking_withBins_seedRankBugFix.root")

events_wb = wb["L1TrackNtuple/eventTree"]
events_wob = wob["L1TrackNtuple/eventTree"]

wob_pt = events_wob["trk_pt"].array()
wob_eta = events_wob["trk_eta"].array()

wb_pt = events_wb["trk_pt"].array()
wb_eta = events_wb["trk_eta"].array()

plt.hist(ak.flatten(wob_pt), bins = np.linspace(0,50,26), weights = [1/len(ak.flatten(wob_pt, axis = None)),] * len(ak.flatten(wob_pt, axis = None)), histtype = "step", color = "blue", label = "Prompt tracking w/ bins")
plt.hist(ak.flatten(wb_pt), bins = np.linspace(0,50,26), weights = [1/len(ak.flatten(wb_pt, axis = None)),] * len(ak.flatten(wb_pt, axis = None)), histtype = "step", color = "red", label = "Extended tracking w/ bins")
plt.xlabel("pt [GeV]")
plt.ylabel("Fraction of tracks")
#plt.title("Both types tracking")
plt.legend()
plt.savefig("extended_trk_pt.pdf")

plt.cla()
plt.hist(ak.flatten(wob_eta), bins = np.linspace(-2.4,2.4,25),  weights = [1/len(ak.flatten(wob_eta, axis = None)),] * len(ak.flatten(wob_eta, axis = None)), histtype = "step", color = "blue", label = "Prompt tracking w/ bins")
plt.hist(ak.flatten(wb_eta), bins = np.linspace(-2.4,2.4,25), weights = [1/len(ak.flatten(wb_eta, axis = None)),] * len(ak.flatten(wb_eta, axis = None)), histtype = "step", color = "red", label = "Extended tracking w/ bins")
#plt.hist(ak.flatten(wob_eta), bins = np.linspace(-2.4,2.4,25), histtype = "step", color = "blue", label = "Prompt tracking w/ bins")
#plt.hist(ak.flatten(wb_eta), bins = np.linspace(-2.4,2.4,25), histtype = "step", color = "red", label = "Extended tracking w/ bins")
plt.xlabel("eta")
plt.ylabel("Fraction of tracks")
#plt.title("Extended tracking")
plt.legend()
plt.savefig("extended_trk_eta.pdf")




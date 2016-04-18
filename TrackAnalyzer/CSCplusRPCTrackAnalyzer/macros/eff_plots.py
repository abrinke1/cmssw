###########################################
# Plot Maker for quick plots
#
# by David Curry
#
# 7.22.1014
###########################################

import sys
import os
import re
from ROOT import *
from matplotlib import interactive
from ROOT import gROOT
from eff_modules import *

# Root file of Histograms
file = TFile('plots/eff.root')
#file = TFile('plots/eff_withMattPt.root')

title = 'test'

print '\n\n============ Making Efficiency Plots ============='


# ====== Track matching efficiency ======
pt  = file.Get('hpt')
eta = file.Get('heta')
phi = file.Get('hphi')

pt_tr  = file.Get('hpt_trigger')
eta_tr = file.Get('heta_trigger')
phi_tr = file.Get('hphi_trigger')

pt_tr_leg  = file.Get('hpt_trigger_leg')
eta_tr_leg = file.Get('heta_trigger_leg')
phi_tr_leg = file.Get('hphi_trigger_leg')

'''
pt_tr_gmt  = file.Get('h_pt_trigger_gmt')
eta_tr_gmt = file.Get('h_eta_trigger_gmt')
phi_tr_gmt = file.Get('h_phi_trigger_gmt')
'''

tg_pt   = TGraphAsymmErrors(pt_tr, pt, '')
tg_eta  = TGraphAsymmErrors(eta_tr, eta, '')
tg_phi  = TGraphAsymmErrors(phi_tr, phi, '')

tg_pt_leg   = TGraphAsymmErrors(pt_tr_leg, pt, '')
tg_eta_leg  = TGraphAsymmErrors(eta_tr_leg, eta, '')
tg_phi_leg  = TGraphAsymmErrors(phi_tr_leg, phi, '')

'''
tg_pt_gmt   = TGraphAsymmErrors(pt_tr_gmt, pt, '')
tg_eta_gmt  = TGraphAsymmErrors(eta_tr_gmt, eta, '')
tg_phi_gmt  = TGraphAsymmErrors(phi_tr_gmt, phi, '')
'''

cEta = TCanvas('cEta')
cPt  = TCanvas('cPt')
cPhi = TCanvas('cPhi')

cPt_leg  = TCanvas('cPt_leg')
cPhi_leg  = TCanvas('cPhi_leg')
cEta_leg  = TCanvas('cEta_leg')

# ====== Find the mode efficiencies =======

print '\n -----> Finding Mode Efficincies...'

# PT
# Get the modes
pt_tr_15_14_13_11 = file.Get('hpt_trigger_15_14_13_11')
pt_tr_15_14_13    = file.Get('hpt_trigger_15_14_13')
pt_tr_15_14       = file.Get('hpt_trigger_15_14')
pt_tr_15          = file.Get('hpt_trigger_15')

pt_tr_15_14_13_11_leg = file.Get('hpt_trigger_15_14_13_11_leg')
pt_tr_15_14_13_leg    = file.Get('hpt_trigger_15_14_13_leg')
pt_tr_15_14_leg       = file.Get('hpt_trigger_15_14_leg')
pt_tr_15_leg          = file.Get('hpt_trigger_15_leg')

pt_tr_gmt = file.Get('hpt_trigger_gmt')

# Eta
# Get the modes
eta_tr_15_14_13_11 = file.Get('heta_trigger_15_14_13_11')
eta_tr_15_14_13    = file.Get('heta_trigger_15_14_13')
eta_tr_15_14       = file.Get('heta_trigger_15_14')
eta_tr_15          = file.Get('heta_trigger_15')

eta_tr_15_14_13_11_leg = file.Get('heta_trigger_15_14_13_11_leg')
eta_tr_15_14_13_leg    = file.Get('heta_trigger_15_14_13_leg')
eta_tr_15_14_leg       = file.Get('heta_trigger_15_14_leg')
eta_tr_15_leg          = file.Get('heta_trigger_15_leg')

eta_tr_gmt = file.Get('heta_trigger_gmt')

# Phi
# Get the modes
phi_tr_15_14_13_11 = file.Get('hphi_trigger_15_14_13_11')
phi_tr_15_14_13    = file.Get('hphi_trigger_15_14_13')
phi_tr_15_14       = file.Get('hphi_trigger_15_14')
phi_tr_15          = file.Get('hphi_trigger_15')

phi_tr_15_14_13_11_leg = file.Get('hphi_trigger_15_14_13_11_leg')
phi_tr_15_14_13_leg    = file.Get('hphi_trigger_15_14_13_leg')
phi_tr_15_14_leg       = file.Get('hphi_trigger_15_14_leg')
phi_tr_15_leg          = file.Get('hphi_trigger_15_leg')

phi_tr_gmt = file.Get('hphi_trigger_gmt')

phi_tr_gmt_leg = file.Get('hphi_trigger_gmt_leg')
eta_tr_gmt_leg = file.Get('heta_trigger_gmt_leg')
pt_tr_gmt_leg = file.Get('hpt_trigger_gmt_leg')

# Making the Tgraph
tg_pt_15_14_13_11 = TGraphAsymmErrors(pt_tr_15_14_13_11, pt, '')
tg_pt_15_14_13 = TGraphAsymmErrors(pt_tr_15_14_13, pt, '')
tg_pt_15_14 = TGraphAsymmErrors(pt_tr_15_14, pt, '')
tg_pt_15 = TGraphAsymmErrors(pt_tr_15, pt, '')

# Now for legacy
tg_pt_15_14_13_11_leg = TGraphAsymmErrors(pt_tr_15_14_13_11_leg, pt, '')
tg_pt_15_14_13_leg = TGraphAsymmErrors(pt_tr_15_14_13_leg, pt, '')
tg_pt_15_14_leg = TGraphAsymmErrors(pt_tr_15_14_leg, pt, '')
tg_pt_15_leg = TGraphAsymmErrors(pt_tr_15_leg, pt, '')

tg_pt_gmt_leg = TGraphAsymmErrors(pt_tr_gmt_leg, pt, '')
tg_pt_gmt = TGraphAsymmErrors(pt_tr_gmt, pt, '')

tg_eta_15_14_13_11 = TGraphAsymmErrors(eta_tr_15_14_13_11, eta, '')
tg_eta_15_14_13 = TGraphAsymmErrors(eta_tr_15_14_13, eta, '')
tg_eta_15_14 = TGraphAsymmErrors(eta_tr_15_14, eta, '')
tg_eta_15 = TGraphAsymmErrors(eta_tr_15, eta, '')

tg_eta_15_14_13_11_leg = TGraphAsymmErrors(eta_tr_15_14_13_11_leg, eta, '')
tg_eta_15_14_13_leg = TGraphAsymmErrors(eta_tr_15_14_13_leg, eta, '')
tg_eta_15_14_leg = TGraphAsymmErrors(eta_tr_15_14_leg, eta, '')
tg_eta_15_leg = TGraphAsymmErrors(eta_tr_15_leg, eta, '')

tg_eta_gmt_leg = TGraphAsymmErrors(eta_tr_gmt_leg, eta, '')
tg_eta_gmt     = TGraphAsymmErrors(eta_tr_gmt, eta, '')

tg_phi_15_14_13_11 = TGraphAsymmErrors(phi_tr_15_14_13_11, phi, '')
tg_phi_15_14_13 = TGraphAsymmErrors(phi_tr_15_14_13, phi, '')
tg_phi_15_14 = TGraphAsymmErrors(phi_tr_15_14, phi, '')
tg_phi_15 = TGraphAsymmErrors(phi_tr_15, phi, '')

tg_phi_15_14_13_11_leg = TGraphAsymmErrors(phi_tr_gmt_leg, phi, '')
tg_phi_15_14_13_leg = TGraphAsymmErrors(phi_tr_15_14_13_leg, phi, '')
tg_phi_15_14_leg = TGraphAsymmErrors(phi_tr_15_14_leg, phi, '')
tg_phi_15_leg = TGraphAsymmErrors(phi_tr_15_leg, phi, '')


tg_phi_gmt_leg = TGraphAsymmErrors(phi_tr_gmt_leg, phi, '')
tg_phi_gmt     = TGraphAsymmErrors(phi_tr_gmt, phi, '')

# ============================================


# ETA ==============================================================================
cEta.cd()
tg_eta.SetLineColor(kBlue)
tg_eta.SetLineWidth(2)
tg_eta.SetMarkerStyle(23)
tg_eta.SetMarkerSize(0.8)
tg_eta.GetXaxis().SetTitle("|#eta(Reco #mu)|")
tg_eta.GetYaxis().SetTitle("EMTF Efficiency")
tg_eta.GetYaxis().SetTitleOffset(1.35)
tg_eta.GetXaxis().SetNdivisions(509)
tg_eta.GetYaxis().SetNdivisions(514)
cEta.SetGridx()
cEta.SetGridy()
tg_eta.SetMinimum(0.0)
tg_eta.SetMaximum(1.02)
tg_eta.Draw('AP')
cEta.Modified()
cEta.Update()

tg_eta_15_14_13_11.SetLineColor(kRed)
tg_eta_15_14_13_11.SetLineWidth(2)
tg_eta_15_14_13_11.SetMarkerStyle(23)
tg_eta_15_14_13_11.SetMarkerSize(0.8)
tg_eta_15_14_13.SetLineColor(kGreen)
tg_eta_15_14_13.SetLineWidth(2)
tg_eta_15_14_13.SetMarkerStyle(23)
tg_eta_15_14_13.SetMarkerSize(0.8)
tg_eta_15_14.SetLineColor(kBlack)
tg_eta_15_14.SetLineWidth(2)
tg_eta_15_14.SetMarkerStyle(23)
tg_eta_15_14.SetMarkerSize(0.8)
tg_eta_15.SetLineColor(kOrange)
tg_eta_15.SetLineWidth(2)
tg_eta_15.SetMarkerStyle(23)
tg_eta_15.SetMarkerSize(0.8)
tg_eta_gmt.SetLineColor(6)
tg_eta_gmt.SetLineWidth(2)
tg_eta_gmt.SetMarkerStyle(23)
tg_eta_gmt.SetMarkerSize(0.8)


tg_eta.Draw('AP')
tg_eta_15_14_13_11.Draw('sameP')
tg_eta_15_14_13.Draw('sameP')
tg_eta_15_14.Draw('sameP')
tg_eta_15.Draw('sameP')
tg_eta_gmt.Draw('sameP')

leta = TLegend(0.85,0.6,1,0.1);
leta.SetBorderSize(0)
leta.SetFillColor(0)

leta.AddEntry(tg_eta, "All Modes")
leta.AddEntry(tg_eta_gmt, "GMT Modes")
leta.AddEntry(tg_eta_15_14_13_11, "uGMT Modes")
leta.AddEntry(tg_eta_15_14_13, "15-14-13")
leta.AddEntry(tg_eta_15_14, "15-14")
leta.AddEntry(tg_eta_15, "15")

leta.Draw("same");

cEta.Modified()
cEta.Update()
cEta.SaveAs('plots/efficiency_alleta_'+title+'.pdf')

# FOR LEGACY Eta ==================================================================
cEta_leg.cd()
cEta_leg.SetGridx()
cEta_leg.SetGridy()
tg_eta_leg.SetLineColor(kBlue)
tg_eta_leg.SetLineWidth(2)
tg_eta_leg.SetMarkerStyle(23)
tg_eta_leg.SetMarkerSize(0.8)
tg_eta_leg.GetXaxis().SetTitle("|#eta(Reco #mu)|")
tg_eta_leg.GetYaxis().SetTitle("CSCTF Efficiency")
tg_eta_leg.GetYaxis().SetTitleOffset(1.35)
tg_eta_leg.GetXaxis().SetNdivisions(509)
tg_eta_leg.GetYaxis().SetNdivisions(514)
tg_eta_leg.SetMinimum(0.0)
tg_eta_leg.SetMaximum(1.02)

tg_eta_15_14_13_11_leg.SetLineColor(kRed)
tg_eta_15_14_13_11_leg.SetLineWidth(2)
tg_eta_15_14_13_11_leg.SetMarkerStyle(23)
tg_eta_15_14_13_11_leg.SetMarkerSize(0.8)
tg_eta_15_14_13_leg.SetLineColor(kGreen)
tg_eta_15_14_13_leg.SetLineWidth(2)
tg_eta_15_14_13_leg.SetMarkerStyle(23)
tg_eta_15_14_13_leg.SetMarkerSize(0.8)
tg_eta_15_14_leg.SetLineColor(kBlack)
tg_eta_15_14_leg.SetLineWidth(2)
tg_eta_15_14_leg.SetMarkerStyle(23)
tg_eta_15_14_leg.SetMarkerSize(0.8)
tg_eta_15_leg.SetLineColor(kOrange)
tg_eta_15_leg.SetLineWidth(2)
tg_eta_15_leg.SetMarkerStyle(23)
tg_eta_15_leg.SetMarkerSize(0.8)
tg_eta_gmt_leg.SetLineColor(6)
tg_eta_gmt_leg.SetLineWidth(2)
tg_eta_gmt_leg.SetMarkerStyle(23)
tg_eta_gmt_leg.SetMarkerSize(0.8)


tg_eta_leg.Draw('AP')
tg_eta_15_14_13_11_leg.Draw('sameP')
tg_eta_15_14_13_leg.Draw('sameP')
tg_eta_15_14_leg.Draw('sameP')
tg_eta_15_leg.Draw('sameP')
tg_eta_gmt_leg.Draw('sameP')

l2 = TLegend(0.85,0.6,1,0.1);
l2.SetBorderSize(0)
l2.SetFillColor(0)

l2.AddEntry(tg_eta_leg, "All Modes")
l2.AddEntry(tg_eta_gmt_leg, "GMT Modes")
l2.AddEntry(tg_eta_15_14_13_11_leg, "uGMT")
l2.AddEntry(tg_eta_15_14_13_leg, "15-14-13")
l2.AddEntry(tg_eta_15_14_leg, "15-14")
l2.AddEntry(tg_eta_15_leg, "15")

l2.Draw("same");

cEta_leg.Modified()
cEta_leg.Update()

cEta_leg.SaveAs('plots/efficiency_eta_leg_'+title+'.pdf')




# Phi ==============================================================================
cPhi.cd()
tg_phi.SetLineColor(kBlue)
tg_phi.SetLineWidth(2)
tg_phi.SetMarkerStyle(23)
tg_phi.SetMarkerSize(0.8)
tg_phi.GetXaxis().SetTitle("|#phi(GBL RECO #mu)|")
tg_phi.GetYaxis().SetTitle("EMTF Efficiency")
tg_phi.GetYaxis().SetTitleOffset(1.35)
tg_phi.GetXaxis().SetNdivisions(509)
tg_phi.GetYaxis().SetNdivisions(514)
cPhi.SetGridx()
cPhi.SetGridy()
tg_phi.SetMinimum(0.0)
tg_phi.SetMaximum(1.02)

tg_phi_15_14_13_11.SetLineColor(kRed)
tg_phi_15_14_13_11.SetLineWidth(2)
tg_phi_15_14_13_11.SetMarkerStyle(23)
tg_phi_15_14_13_11.SetMarkerSize(0.8)
tg_phi_15_14_13.SetLineColor(kGreen)
tg_phi_15_14_13.SetLineWidth(2)
tg_phi_15_14_13.SetMarkerStyle(23)
tg_phi_15_14_13.SetMarkerSize(0.8)
tg_phi_15_14.SetLineColor(kBlack)
tg_phi_15_14.SetLineWidth(2)
tg_phi_15_14.SetMarkerStyle(23)
tg_phi_15_14.SetMarkerSize(0.8)
tg_phi_15.SetLineColor(kOrange)
tg_phi_15.SetLineWidth(2)
tg_phi_15.SetMarkerStyle(23)
tg_phi_15.SetMarkerSize(0.8)
tg_phi_gmt.SetLineColor(6)
tg_phi_gmt.SetLineWidth(2)
tg_phi_gmt.SetMarkerStyle(23)
tg_phi_gmt.SetMarkerSize(0.8)

tg_phi.Draw('AP')
tg_phi_15_14_13_11.Draw('sameP')
tg_phi_15_14_13.Draw('sameP')
tg_phi_15_14.Draw('sameP')
tg_phi_15.Draw('sameP')
tg_phi_gmt.Draw('sameP')

lphi = TLegend(0.85,0.6,1,0.1);
lphi.SetBorderSize(0)
lphi.SetFillColor(0)

lphi.AddEntry(tg_phi, "All Modes")
lphi.AddEntry(tg_phi_gmt, "GMT Modes")
lphi.AddEntry(tg_phi_15_14_13_11, "uGMT Modes")
lphi.AddEntry(tg_phi_15_14_13, "15-14-13")
lphi.AddEntry(tg_phi_15_14, "15-14")
lphi.AddEntry(tg_phi_15, "15")

lphi.Draw("same");

cPhi.Modified()
cPhi.Update()

cPhi.SaveAs('plots/efficiency_phi_'+title+'.pdf')


# FOR LEGACY PHI ==================================================================
# Phi
cPhi_leg.cd()
cPhi_leg.SetGridx()
cPhi_leg.SetGridy()
tg_phi_leg.SetLineColor(kBlue)
tg_phi_leg.SetLineWidth(2)
tg_phi_leg.SetMarkerStyle(23)
tg_phi_leg.SetMarkerSize(0.8)
tg_phi_leg.GetXaxis().SetTitle("#phi(Reco #mu)")
tg_phi_leg.GetYaxis().SetTitle("CSCTF Efficiency")
tg_phi_leg.GetYaxis().SetTitleOffset(1.35)
tg_phi_leg.GetXaxis().SetNdivisions(509)
tg_phi_leg.GetYaxis().SetNdivisions(514)
tg_phi_leg.SetMinimum(0.0)
tg_phi_leg.SetMaximum(1.02)

tg_phi_15_14_13_11_leg.SetLineColor(kRed)
tg_phi_15_14_13_11_leg.SetLineWidth(2)
tg_phi_15_14_13_11_leg.SetMarkerStyle(23)
tg_phi_15_14_13_11_leg.SetMarkerSize(0.8)
tg_phi_15_14_13_leg.SetLineColor(kGreen)
tg_phi_15_14_13_leg.SetLineWidth(2)
tg_phi_15_14_13_leg.SetMarkerStyle(23)
tg_phi_15_14_13_leg.SetMarkerSize(0.8)
tg_phi_15_14_leg.SetLineColor(kBlack)
tg_phi_15_14_leg.SetLineWidth(2)
tg_phi_15_14_leg.SetMarkerStyle(23)
tg_phi_15_14_leg.SetMarkerSize(0.8)
tg_phi_15_leg.SetLineColor(kOrange)
tg_phi_15_leg.SetLineWidth(2)
tg_phi_15_leg.SetMarkerStyle(23)
tg_phi_15_leg.SetMarkerSize(0.8)
tg_phi_gmt_leg.SetLineColor(6)
tg_phi_gmt_leg.SetLineWidth(2)
tg_phi_gmt_leg.SetMarkerStyle(23)
tg_phi_gmt_leg.SetMarkerSize(0.8)


tg_phi_leg.Draw('AP')
tg_phi_15_14_13_11_leg.Draw('sameP')
tg_phi_15_14_13_leg.Draw('sameP')
tg_phi_15_14_leg.Draw('sameP')
tg_phi_15_leg.Draw('sameP')
tg_phi_gmt_leg.Draw('sameP')

lphil = TLegend(0.85,0.6,1,0.1);
lphil.SetBorderSize(0)
lphil.SetFillColor(0)

lphil.AddEntry(tg_phi_leg, "All Modes")
lphil.AddEntry(tg_phi_gmt_leg, "GMT Modes")
lphil.AddEntry(tg_phi_15_14_13_11_leg, "uGMT Modes")
lphil.AddEntry(tg_phi_15_14_13_leg, "15-14-13")
lphil.AddEntry(tg_phi_15_14_leg, "15-14")
lphil.AddEntry(tg_phi_15_leg, "15")

lphil.Draw("same");

cPhi_leg.Modified()
cPhi_leg.Update()

cPhi_leg.SaveAs('plots/efficiency_phi_leg_'+title+'.pdf')



# Pt ==================================================================
cPt.cd()
cPt.SetGridx()
cPt.SetGridy()
tg_pt.SetLineColor(kBlue)
tg_pt.SetLineWidth(2)
tg_pt.SetMarkerStyle(23)
tg_pt.SetMarkerSize(0.8)
tg_pt.GetXaxis().SetTitle("p_{T}(Reco #mu)")
tg_pt.GetYaxis().SetTitle("EMTF Efficiency")
tg_pt.GetYaxis().SetTitleOffset(1.35)
tg_pt.GetXaxis().SetNdivisions(509)
tg_pt.GetYaxis().SetNdivisions(514)
tg_pt.SetMinimum(0.0)
tg_pt.SetMaximum(1.02)

tg_pt_15_14_13_11.SetLineColor(kRed)
tg_pt_15_14_13_11.SetLineWidth(2)
tg_pt_15_14_13_11.SetMarkerStyle(23)
tg_pt_15_14_13_11.SetMarkerSize(0.8)
tg_pt_15_14_13.SetLineColor(kGreen)
tg_pt_15_14_13.SetLineWidth(2)
tg_pt_15_14_13.SetMarkerStyle(23)
tg_pt_15_14_13.SetMarkerSize(0.8)
tg_pt_15_14.SetLineColor(kBlack)
tg_pt_15_14.SetLineWidth(2)
tg_pt_15_14.SetMarkerStyle(23)
tg_pt_15_14.SetMarkerSize(0.8)
tg_pt_15.SetLineColor(kOrange)
tg_pt_15.SetLineWidth(2)
tg_pt_15.SetMarkerStyle(23)
tg_pt_15.SetMarkerSize(0.8)
tg_pt_gmt.SetLineColor(6)
tg_pt_gmt.SetLineWidth(2)
tg_pt_gmt.SetMarkerStyle(23)
tg_pt_gmt.SetMarkerSize(0.8)

tg_pt.Draw('AP')
tg_pt_15_14_13_11.Draw('sameP')
tg_pt_15_14_13.Draw('sameP')
tg_pt_15_14.Draw('sameP')
tg_pt_15.Draw('sameP')
tg_pt_gmt.Draw('sameP')

lpt = TLegend(0.85,0.6,1,0.1);
lpt.SetBorderSize(0)
lpt.SetFillColor(0)

lpt.AddEntry(tg_pt, "All Modes")
lpt.AddEntry(tg_pt_gmt, "GMT Modes")
lpt.AddEntry(tg_pt_15_14_13_11, "uGMT Modes")
lpt.AddEntry(tg_pt_15_14_13, "15-14-13")
lpt.AddEntry(tg_pt_15_14, "15-14")
lpt.AddEntry(tg_pt_15, "15")

lpt.Draw("same");

cPt.Modified()
cPt.Update()

cPt.SaveAs('plots/efficiency_pt_'+title+'.pdf')


# FOR LEGACY PT ==================================================================
# Pt
cPt_leg.cd()
cPt_leg.SetGridx()
cPt_leg.SetGridy()
tg_pt_leg.SetLineColor(kBlue)
tg_pt_leg.SetLineWidth(2)
tg_pt_leg.SetMarkerStyle(23)
tg_pt_leg.SetMarkerSize(0.8)
tg_pt_leg.GetXaxis().SetTitle("p_{T}(Reco #mu)")
tg_pt_leg.GetYaxis().SetTitle("CSCTF Efficiency")
tg_pt_leg.GetYaxis().SetTitleOffset(1.35)
tg_pt_leg.GetXaxis().SetNdivisions(509)
tg_pt_leg.GetYaxis().SetNdivisions(514)
tg_pt_leg.SetMinimum(0.0)
tg_pt_leg.SetMaximum(1.02)

tg_pt_15_14_13_11_leg.SetLineColor(kRed)
tg_pt_15_14_13_11_leg.SetLineWidth(2)
tg_pt_15_14_13_11_leg.SetMarkerStyle(23)
tg_pt_15_14_13_11_leg.SetMarkerSize(0.8)
tg_pt_15_14_13_leg.SetLineColor(kGreen)
tg_pt_15_14_13_leg.SetLineWidth(2)
tg_pt_15_14_13_leg.SetMarkerStyle(23)
tg_pt_15_14_13_leg.SetMarkerSize(0.8)
tg_pt_15_14_leg.SetLineColor(kBlack)
tg_pt_15_14_leg.SetLineWidth(2)
tg_pt_15_14_leg.SetMarkerStyle(23)
tg_pt_15_14_leg.SetMarkerSize(0.8)
tg_pt_15_leg.SetLineColor(kOrange)
tg_pt_15_leg.SetLineWidth(2)
tg_pt_15_leg.SetMarkerStyle(23)
tg_pt_15_leg.SetMarkerSize(0.8)
tg_pt_gmt_leg.SetLineColor(6)
tg_pt_gmt_leg.SetLineWidth(2)
tg_pt_gmt_leg.SetMarkerStyle(23)
tg_pt_gmt_leg.SetMarkerSize(0.8)

tg_pt_leg.Draw('AP')
tg_pt_15_14_13_11_leg.Draw('sameP')
tg_pt_15_14_13_leg.Draw('sameP')
tg_pt_15_14_leg.Draw('sameP')
tg_pt_15_leg.Draw('sameP')
tg_pt_gmt_leg.Draw('sameP')

lptl = TLegend(0.85,0.6,1,0.1);
lptl.SetBorderSize(0)
lptl.SetFillColor(0)

lptl.AddEntry(tg_pt_leg, "All Modes")
lptl.AddEntry(tg_pt_gmt_leg, "GMT Modes")
lptl.AddEntry(tg_pt_15_14_13_11_leg, "uGMT Modes")
lptl.AddEntry(tg_pt_15_14_13_leg, "15-14-13")
lptl.AddEntry(tg_pt_15_14_leg, "15-14")
lptl.AddEntry(tg_pt_15_leg, "15")

lptl.Draw("same");

cPt_leg.Modified()
cPt_leg.Update()

cPt_leg.SaveAs('plots/efficiency_pt_leg_'+title+'.pdf')


# ========= Ratio of Pt plots ============
cEff_divide = TCanvas('cEff_divide')
cEff_divide.cd()
cEff_divide.SetGridx()
cEff_divide.SetGridy()

copy_tg_pt_leg             = tg_pt_leg.Clone('copy_tg_pt_leg')
copy_tg_pt_15_14_13_11_leg = tg_pt_15_14_13_11_leg.Clone('copy_tg_pt_15_14_13_11_leg')
copy_tg_pt_15_14_13_leg    = tg_pt_15_14_13_leg.Clone('copy_tg_pt_15_14_13_leg')
copy_tg_pt_15_14_leg       = tg_pt_15_14_leg.Clone('copy_tg_pt_15_14_leg')
copy_tg_pt_15_leg          = tg_pt_15_leg.Clone('copy_tg_pt_15_leg')
copy_tg_pt_gmt_leg         = tg_pt_gmt_leg.Clone('copy_tg_pt_gmt_leg')

copy_tg_pt             = tg_pt.Clone('copy_tg_pt')
copy_tg_pt_15_14_13_11 = tg_pt_15_14_13_11.Clone('copy_tg_pt_15_14_13_11')
copy_tg_pt_15_14_13    = tg_pt_15_14_13.Clone('copy_tg_pt_15_14_13')
copy_tg_pt_15_14       = tg_pt_15_14.Clone('copy_tg_pt_15_14')
copy_tg_pt_15          = tg_pt_15.Clone('copy_tg_pt_15')
copy_tg_pt_gmt         = tg_pt_gmt.Clone('copy_tg_pt_gmt')

# ===== Loop over the tgraphs and get EMTF/CSCTF ratio by accessing bin contents =====

# tgraph bins
nbins = pt_tr.GetSize() - 2

effPt_divide             = TH1F('effPt_divide', '', len(scale_pt_temp)-1, scale_pt)
effPt_divide_15_14_13_11 = TH1F('effPt_divide_15_14_13_11', '', len(scale_pt_temp)-1, scale_pt)
effPt_divide_15_14_13    = TH1F('effPt_divide_15_14_13', '',len(scale_pt_temp)-1, scale_pt)
effPt_divide_15_14       = TH1F('effPt_divide_15_14', '',len(scale_pt_temp)-1, scale_pt)
effPt_divide_15          = TH1F('effPt_divide_15', '',len(scale_pt_temp)-1, scale_pt)
effPt_divide_gmt         = TH1F('effPt_divide_gmt', '',len(scale_pt_temp)-1, scale_pt)

for i, bin in enumerate(scale_pt_temp):

    y_value             = copy_tg_pt.Eval(bin)
    y_value_15_14_13_11 = copy_tg_pt_15_14_13_11.Eval(bin)
    y_value_15_14_13    = copy_tg_pt_15_14_13.Eval(bin)
    y_value_15_14       = copy_tg_pt_15_14.Eval(bin)
    y_value_15          = copy_tg_pt_15.Eval(bin)
    y_value_gmt         = copy_tg_pt_gmt.Eval(bin)

    y_value_leg             = copy_tg_pt_leg.Eval(bin)
    y_value_15_14_13_11_leg = copy_tg_pt_15_14_13_11_leg.Eval(bin)
    y_value_15_14_13_leg    = copy_tg_pt_15_14_13_leg.Eval(bin)
    y_value_15_14_leg       = copy_tg_pt_15_14_leg.Eval(bin)
    y_value_15_leg          = copy_tg_pt_15_leg.Eval(bin)
    y_value_gmt_leg         = copy_tg_pt_gmt_leg.Eval(bin)

    y_value_div             = y_value             / y_value_leg 
    y_value_15_14_13_11_div = y_value_15_14_13_11 /  y_value_15_14_13_11_leg
    y_value_15_14_13_div    = y_value_15_14_13    /  y_value_15_14_13_leg
    y_value_15_14_div       = y_value_15_14       /  y_value_15_14_leg
    y_value_15_div          = y_value_15          /  y_value_15_leg
    y_value_gmt_div         = y_value_gmt         /  y_value_gmt_leg


    # Set divide hitogram bin content
    effPt_divide.SetBinContent(i,  y_value_div)
    effPt_divide_15_14_13_11.SetBinContent(i,  y_value_15_14_13_11_div)
    effPt_divide_15_14_13.SetBinContent(i,  y_value_15_14_13_div)
    effPt_divide_15_14.SetBinContent(i,  y_value_15_14_div)
    effPt_divide_15.SetBinContent(i,  y_value_15_div)
    effPt_divide_gmt.SetBinContent(i,  y_value_gmt_div)

# ==================================

effPt_divide.SetLineColor(kBlue)
effPt_divide.SetLineWidth(2)

effPt_divide_15_14_13_11.SetLineColor(kRed)
effPt_divide_15_14_13_11.SetLineWidth(2)

effPt_divide_gmt.SetLineColor(6)
effPt_divide_gmt.SetLineWidth(2)

effPt_divide_15_14_13.SetLineColor(kGreen)
effPt_divide_15_14_13.SetLineWidth(2)

effPt_divide_15_14.SetLineColor(kBlack)
effPt_divide_15_14.SetLineWidth(2)

effPt_divide_15.SetLineColor(kOrange)
effPt_divide_15.SetLineWidth(2)

s1 = THStack('s1', '')

s1.Add( effPt_divide)
s1.Add( effPt_divide_15_14_13_11)
s1.Add( effPt_divide_15_14_13)
s1.Add( effPt_divide_15_14)
s1.Add( effPt_divide_15)
s1.Add( effPt_divide_gmt)

s1.Draw('nostack')
s1.GetXaxis().SetTitle("EMTF p_{T}[GeV]")
s1.GetYaxis().SetTitle("EMTF/CSCTF")
s1.GetYaxis().SetTitleOffset(1.35)
s1.GetXaxis().SetNdivisions(509)
s1.GetYaxis().SetNdivisions(514)

lptl.Draw('same')


cEff_divide.Modified()
cEff_divide.Update()
cEff_divide.SaveAs('plots/eff_pt_divide_'+title+'.pdf')



# ========================================================================

# Quick plotting
# List of variables to plot:  var name, # of bins, x-axis range, x axis
variable_list = [ 
    #['hdpt', 'Gen p_{T} - EMTF p_{T}', 50, -10, 10],
    #['hdpt_rpc', 'Gen p_{T} - EMTF+RPC p_{T}', 50, -10, 10],
    #['h_mode_trigger', 'tr EMTF Mode', 16, 0, 15],
    #['h_RPC_mode_trigger', 'tr EMTF Mode(+RPC)', 16, 0, 15],
    #['h_mode', 'EMTF Mode', 16, 0, 15],
    #['h_RPC_mode', 'EMTF Mode(+RPC)', 16, 0, 15],
    #['h_trkPt', 'CSCTF p_{T} [GeV]', 50, 0, 150],
    #['h_trkEta', 'CSCTF #eta', 50, 0, 2.4],
    #['h_trkPhi', 'CSCTF #phi', 50, -3.2, 3.2],
    #['h_trkPt_rpc', 'CSCTF+RPC p_{T} [GeV]', 50,0, 150],
    #['h_trkEta_rpc', 'CSCTF+RPC #eta', 50, 0, 2.4],
    #['h_trkPhi_rpc', 'CSCTF+RPC #phi', 50, -3.2, 3.2],
    #['h_GenPt', 'Gen p_{T} [GeV]', 50,0, 150],
    #['h_GenEta', 'Gen #eta', 50, 0, 2.4],
    #['h_GenPhi', 'Gen #phi', 50, -3.2, 3.2]
    #['hdEta', 'Delta #eta (RPC Cluster-CSC)', 50, -0.2, 0.2],
    #['hdPhi', 'Delta #phi (RPC Cluster-CSC)', 50, -0.1, 0.1],
    #['hdEta1', 'Delta #eta (RPC Cluster1-CSC1)', 50, -0.2, 0.2],
    #['hdPhi1', 'Delta #phi (RPC Cluster1-CSC1)', 50, -0.1, 0.1],
    #['hdEta2', 'Delta #eta (RPC Cluster2-CSC2)', 50, -0.2, 0.2],
    #['hdPhi2', 'Delta #phi (RPC Cluster2-CSC2)', 50, -0.1, 0.1],
    #['hdEta3', 'Delta #eta (RPC Cluster3-CSC3)', 50, -0.2, 0.2],
    #['hdPhi3', 'Delta #phi (RPC Cluster3-CSC3)', 50, -0.1, 0.1],
    #['hdEta4', 'Delta #eta (RPC Cluster4-CSC4)', 50, -0.2, 0.2],
    #['hdPhi4', 'Delta #phi (RPC Cluster4-CSC4)', 50, -0.3, 0.3]
    ]




def doPlot(variable, xaxis, nbins, bin_low, bin_high):

    canvas = TCanvas('canvas')
    hist = file.Get(variable) 
    hist.GetXaxis().SetLimits(bin_low, bin_high)
    hist.GetXaxis().SetTitle(xaxis)
    #if variable == 'hdPhi' or variable== 'hdEta':

    hist.SetFillColor(kYellow)
    hist.SetStats(0)
    hist.Draw()

    #raw_input('Press return to continue...')
    
    canvas.SaveAs('plots/'+variable+'_'+title+'.pdf')

    canvas.IsA().Destructor(canvas)
    hist.IsA().Destructor(hist)


# end do plot

for variable in variable_list:

    doPlot(variable[0], variable[1], variable[2], variable[3], variable[4])

raw_input('Press return to continue...')

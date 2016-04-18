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

file = TFile('trig_eff_plots_noB_minusEta.root')
#file = TFile('trig_eff_plots_noB_plusEta.root')
header = 'Single Muon 2015B,  All Q,  GBl Muon P_{t} > 3 '
title = 'noB_minusEta'
#title = 'noB_plusEta'


# === Basic Vars ====

hgbl_pt = file.Get('hgbl_pt')
hcsctf_pt = file.Get('hcsctf_pt')

cgbl_pt   = TCanvas('cgbl_pt')
ccsctf_pt = TCanvas('ccsctf_pt')

cgbl_pt.cd()
hgbl_pt.SetStats(0)
hgbl_pt.GetXaxis().SetTitle('Global #mu P_{t} [GeV]')
hgbl_pt.GetXaxis().SetTitleOffset(1.4)
hgbl_pt.SetFillColor(kYellow)
hgbl_pt.Draw()

cgbl_pt.SaveAs('plots/gbl_reco_pt_'+title+'.pdf')

ccsctf_pt.cd()
hcsctf_pt.SetStats(0)
hcsctf_pt.GetXaxis().SetTitle('CSCTF P_{t} [GeV]')
hcsctf_pt.GetXaxis().SetTitleOffset(1.4)
hcsctf_pt.SetFillColor(kYellow)
hcsctf_pt.Draw()

ccsctf_pt.SaveAs('plots/csctf_pt_'+title+'.pdf')


# ===== efficiency =======
pt_all = file.Get('csctfPt_all')
pt_all_eta1 = file.Get('csctfPt_all_eta1')
pt_all_eta2 = file.Get('csctfPt_all_eta2')
pt_all_eta3 = file.Get('csctfPt_all_eta3')
pt_all_eta4 = file.Get('csctfPt_all_eta4')

hpt7 = file.Get('csctfPt_7.0')
hpt12 = file.Get('csctfPt_12.0')
hpt16 = file.Get('csctfPt_16.0')

hpt7_eta1 = file.Get('csctfPt_eta1_7.0')
hpt7_eta2 = file.Get('csctfPt_eta2_7.0')
hpt7_eta3 = file.Get('csctfPt_eta3_7.0')
hpt7_eta4 = file.Get('csctfPt_eta4_7.0')

hpt16_eta1 = file.Get('csctfPt_eta1_16.0')
hpt16_eta2 = file.Get('csctfPt_eta2_16.0')
hpt16_eta3 = file.Get('csctfPt_eta3_16.0')
hpt16_eta4 = file.Get('csctfPt_eta4_16.0')

tg7 = TGraphAsymmErrors(hpt7, pt_all, '')
tg12 = TGraphAsymmErrors(hpt12, pt_all, '')
tg16 = TGraphAsymmErrors(hpt16, pt_all, '')

tg7_eta1  = TGraphAsymmErrors(hpt7_eta1, pt_all_eta1, '')
tg16_eta1 = TGraphAsymmErrors(hpt16_eta1, pt_all_eta1, '')

tg7_eta2  = TGraphAsymmErrors(hpt7_eta2, pt_all_eta2, '')
tg16_eta2 = TGraphAsymmErrors(hpt16_eta2, pt_all_eta2, '')

tg7_eta3  = TGraphAsymmErrors(hpt7_eta3, pt_all_eta3, '')
tg16_eta3 = TGraphAsymmErrors(hpt16_eta3, pt_all_eta3, '')

tg7_eta4  = TGraphAsymmErrors(hpt7_eta4, pt_all_eta4, '')
tg16_eta4 = TGraphAsymmErrors(hpt16_eta4, pt_all_eta4, '')

c7 = TCanvas('c7')

ceta1 = TCanvas('ceta1')
ceta2 = TCanvas('ceta2')
ceta3 = TCanvas('ceta3')
ceta4 = TCanvas('ceta4')

ceta1.SetLogx(1)
ceta2.SetLogx(1)
ceta3.SetLogx(1)
ceta4.SetLogx(1)

c7.SetLogx(1)


fit7 = TF1('fit7',  '[0]* (1 + TMath::Erf( (x - [1])*[2] ))/2.0', 0, 100);
fit7.SetParameter(0,1.0);
fit7.SetParameter(1,5.0);
fit7.SetParameter(2,0.5);
fit7.SetParLimits(0,1,10);
fit7.SetParLimits(1,1,10);
fit7.SetParLimits(2,0,10);


c7.cd()
#tg7.SetTitle('Turn On Efficiency: 7 GeV')
tg7.GetXaxis().SetTitle('Global #mu P_{t} [GeV]')
tg7.GetXaxis().SetTitleOffset(1.4)
tg7.GetYaxis().SetRangeUser(0,1.05)
tg7.Draw('APE')
#tg16.Draw('sameAPE')

#tg7.Fit('fit7')

line_7 = TLine(7, 0, 7, 1.05)
line_7.SetLineWidth(2)
line_7.SetLineStyle(kDashed)
line_7.SetLineColor(kRed)
line_7.Draw('same')

l_1 = TLatex()
l_1.SetNDC()
l_1.SetTextSize(0.03)
l_1.DrawLatex(0.1, 0.93, header+', All eta,  Turn On: 7 GeV')
#l_1.Draw('same')

c7.SaveAs('plots/efficiency_7GeV_'+title+'.pdf')


ceta1.cd()
#tg7.SetTitle('Turn On Efficiency: 7 GeV')
tg7_eta1.GetXaxis().SetTitle('Global #mu P_{t} [GeV]')
tg7_eta1.GetXaxis().SetTitleOffset(1.4)
tg7_eta1.GetYaxis().SetRangeUser(0,1.05)
tg7_eta1.Draw('APE')
#tg16.Draw('sameAPE')

#tg7.Fit('fit7')

line_7 = TLine(7, 0, 7, 1.05)
line_7.SetLineWidth(2)
line_7.SetLineStyle(kDashed)
line_7.SetLineColor(kRed)
line_7.Draw('same')

l_1 = TLatex()
l_1.SetNDC()
l_1.SetTextSize(0.03)
l_1.DrawLatex(0.1, 0.93, header+', 0.9 < |eta| < 1.3,  Turn On: 7 GeV')

ceta1.SaveAs('plots/efficiency_7GeV_eta1_'+title+'.pdf')

ceta2.cd()
#tg7.SetTitle('Turn On Efficiency: 7 GeV')
tg7_eta2.GetXaxis().SetTitle('Global #mu P_{t} [GeV]')
tg7_eta2.GetXaxis().SetTitleOffset(1.4)
tg7_eta2.GetYaxis().SetRangeUser(0,1.05)
tg7_eta2.Draw('APE')
#tg16.Draw('sameAPE')

#tg7.Fit('fit7')

line_7 = TLine(7, 0, 7, 1.05)
line_7.SetLineWidth(2)
line_7.SetLineStyle(kDashed)
line_7.SetLineColor(kRed)
line_7.Draw('same')

l_1 = TLatex()
l_1.SetNDC()
l_1.SetTextSize(0.03)
l_1.DrawLatex(0.1, 0.93, header+', 1.3 < |eta| < 1.7,  Turn On: 7 GeV')

ceta2.SaveAs('plots/efficiency_7GeV_eta2_'+title+'.pdf')

ceta3.cd()
#tg7.SetTitle('Turn On Efficiency: 7 GeV')
tg7_eta3.GetXaxis().SetTitle('Global #mu P_{t} [GeV]')
tg7_eta3.GetXaxis().SetTitleOffset(1.4)
tg7_eta3.GetYaxis().SetRangeUser(0,1.05)
tg7_eta3.Draw('APE')
#tg16.Draw('sameAPE')

#tg7.Fit('fit7')

line_7 = TLine(7, 0, 7, 1.05)
line_7.SetLineWidth(2)
line_7.SetLineStyle(kDashed)
line_7.SetLineColor(kRed)
line_7.Draw('same')

l_1 = TLatex()
l_1.SetNDC()
l_1.SetTextSize(0.03)
l_1.DrawLatex(0.1, 0.93, header+', 1.7 < |eta| < 2.1,  Turn On: 7 GeV')

ceta3.SaveAs('plots/efficiency_7GeV_eta3_'+title+'.pdf')

ceta4.cd()
#tg7.SetTitle('Turn On Efficiency: 7 GeV')
tg7_eta4.GetXaxis().SetTitle('Global #mu P_{t} [GeV]')
tg7_eta4.GetXaxis().SetTitleOffset(1.4)
tg7_eta4.GetYaxis().SetRangeUser(0,1.05)
tg7_eta4.Draw('APE')
#tg16.Draw('sameAPE')

#tg7.Fit('fit7')

line_7 = TLine(7, 0, 7, 1.05)
line_7.SetLineWidth(2)
line_7.SetLineStyle(kDashed)
line_7.SetLineColor(kRed)
line_7.Draw('same')

l_1 = TLatex()
l_1.SetNDC()
l_1.SetTextSize(0.03)
l_1.DrawLatex(0.1, 0.93, header+', 2.1 < |eta| < 2.4,  Turn On: 7 GeV')

ceta4.SaveAs('plots/efficiency_7GeV_eta4_'+title+'.pdf')





# ========================

# end efficiency


raw_input('Press return to continue...')



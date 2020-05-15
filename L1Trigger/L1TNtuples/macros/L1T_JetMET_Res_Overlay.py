#! /usr/bin/env python

## ************************************************** ##
##  Overlay output histograms from L1T_JetMET_Res.py  ##
## ************************************************** ##

import os
from shutil import copyfile

import ROOT as R
R.gROOT.SetBatch(True)  ## Don't print histograms to screen while processing
R.gStyle.SetOptStat(0)  ## Don't draw stats boxes

USER = 'abrinke1'
# USER = 'ssawant'

## List of sample numbers to plot, with their proper label
SAMPS = {}
SAMPS['0'] = ["PFA2",  R.kBlue]
SAMPS['3'] = ["PFA1p", R.kRed]


def main():

    print '\nInside L1T_JetMET_Res_Overlay.py\n'

    ## Set input and output files and directories
    in_dir = 'plots/'

    # in_file_name = 'L1T_JetMET_Res_nVtxMax_20_2018D_6p6k.root'
    in_file_name = 'L1T_JetMET_Res_nVtxMin_45_2018AB_13p6k.root'


    top_dir = '/afs/cern.ch/work/a/abrinke1/public/L1T/CaloTP/2018/HCAL_OOT_PUS/plots/'
    out_dir = top_dir+'Overlay_'
    out_dir += in_file_name.replace('.root','')
    for i in SAMPS.keys():
        out_dir += '_%s' % SAMPS[i][0]
    out_dir += '/'
    if not os.path.exists(out_dir):
        print 'Creating new directory %s' % out_dir
        os.makedirs(out_dir)

    out_file_str = 'Overlay.root'
    out_file = R.TFile(out_dir+out_file_str,'recreate')
    print '\nWill write to output file %s' % out_dir+out_file_str


    ## Copy plots to webpage: https://abrinke1.web.cern.ch/abrinke1/
    web_dir = 'NONE'
    if USER == 'abrinke1':
        web_dir = '/afs/cern.ch/user/%s/%s/www/L1T/CaloTP/HCAL_OOT_PUS/' % (USER[0], USER)
        if not os.path.exists(web_dir):
            print '\nCreating new web directory: %s' % web_dir
            os.makedirs(web_dir)
        web_dir += out_dir.replace(top_dir,'')

        ## Link webpage directory to local plots rather than copying over
        if os.path.exists(web_dir):
            os.unlink(web_dir[:-1])
        os.symlink(out_dir, web_dir[:-1])
        copyfile('/afs/cern.ch/user/%s/%s/www/index.php' % (USER[0], USER), web_dir+'index.php')

    
    ## Open input file
    print '\nOpening input file %s' % in_dir+in_file_name
    in_file = R.TFile.Open(in_dir+in_file_name, 'READ')

    
    ## List of histograms with sample number and 'emu' stripped out
    h_list = []
    for hist in R.gDirectory.GetListOfKeys():
        h_str = ''
        for i in SAMPS.keys():
            if '_%s_emu' % i in hist.GetName():
                h_str = hist.GetName().replace('_%s_emu' % i, '')
        if len(h_str) > 0 and not h_str in h_list:
            h_list.append(h_str)

    print '\n\nFound the following list of histograms:'
    print h_list

    ## Move to output file
    out_file.cd()

    ## Loop over all histograms and draw
    for h_name in h_list:

        print '\n  * Drawing histogram %s' % h_name
        can = R.TCanvas('can_'+h_name, 'can_'+h_name, 1)
        can.Clear()
        can.cd()

        ## Draw style for histograms and TEfficiency plots
        style = 'hist'
        ssame = 'histsame'
        if '_eff_' in h_name:
            style = 'AP'
            ssame = 'Psame'

        h_first = True
        for i in SAMPS.keys():
            if h_first:
                hist = in_file.Get(h_name+'_%s_unp' % i)
                hist.SetTitle('Unpacked')
                hist.SetLineColor(R.kBlack)
                hist.Draw(style)
                h_first = False
            else:
                hist = in_file.Get(h_name+'_%s_emu' % i)
                hist.SetTitle('Emu %s' % SAMPS[i][0])
                hist.SetLineColor(SAMPS[i][1])
                hist.Draw(ssame)

        can.SaveAs(out_dir+'/'+h_name+'.png')
        can.SaveAs(out_dir+'/'+h_name+'.pdf')
        
    out_file.Close()

    in_file.Close()
    
    print '\n\nWrote out file: '+out_dir+out_file_str
    if USER == 'abrinke1':
        print '\nOuput web directory: '+web_dir
        print '\nOutput webpage: https://abrinke1.web.cern.ch/abrinke1/'+web_dir.replace('/afs/cern.ch/user/%s/%s/www/' % (USER[0], USER),'')


if __name__ == '__main__':
    main()

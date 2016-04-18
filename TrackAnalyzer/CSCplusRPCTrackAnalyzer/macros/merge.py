# Python script to merge root files together

import sys
import os
from ROOT import *

# ==== Choose a task ====
clean = False
#clean = True

merge = False
merge = True

# ======================


if merge:

    # input files come from creating a single line of file names, seperated by a space.
    # using awk we put file names in hadd.  Only user input is path of directory after cmsLs and target file

    target_file = 'root://eoscms//eos/cms/store/user/dcurry/trig/9_5_zeroBias/zeroBias_merge_20.root'

    os.system('rm hadd')
 
    print '----> Printing file names/paths to hadd...'
    
    #os.system("cmsLs /store/user/dcurry/trig/8_15_ZeroBias/ZeroBias/crab_20150814_153930/150814_133951/0000/ | grep root | awk '{print ""$5""}' >> hadd")
    #os.system("cmsLs /store/user/dcurry/trig/8_15_MinBias/MinimumBias/crab_20150815_142328/150815_122408/0001/ | grep root | awk '{print ""$5""}' >> hadd")
    os.system("cmsLs /store/user/dcurry/trig/9_5_zeroBias/ZeroBias/crab_20150909_130623/150909_110657/0000/ | grep root | awk '{print ""$5""}' >> hadd")


    input_file = ''
    with open('hadd') as file:
    
        for i, line in enumerate(file):
            
            if i is 20: break
            
            line = 'root://eoscms//eos/cms' + line 
            
            x = line.replace('\n', ' ')
            
            input_file += x

    merge = "hadd -f %s %s" % (target_file, input_file) 
    
    print '----> Merging Files into', target_file,'.  This may take a while....'

    os.system(merge)



# ====== For cleaning EOS ========
if clean: 

    print '----> Cleaning EOS Files...'
    
    os.system('rm clean')

    # make a list of files to be removed
    os.system("cmsLs /store/user/dcurry/rpc/2012D_MinBias_Raw_Reco_1_11_15/MinimumBias/crab_20150113_223829/150113_213900/0000/ | grep root | awk '{print ""$5""}' >> clean")
    
    with open('clean') as file:

        for i, line in enumerate(file):
            
            temp = 'cmsRm %s' % (line)
            
            print temp
            os.system(temp)


    print '----> Cleaning Finished.'

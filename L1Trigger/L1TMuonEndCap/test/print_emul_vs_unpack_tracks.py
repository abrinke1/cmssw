#! /usr/bin/env python

## Compare tracks coming out of unpacker and emulator

from ROOT import *
gROOT.SetBatch(False)

def main():

    print 'Inside emul_vs_unpack_tracks'

    file_name_1 = '/afs/cern.ch/work/d/dcurry/private/rpc_mtf8/CMSSW_8_0_2/src/L1Trigger/L1TMuonEndCap/test/l1temtf_superprimitives1.root'
    file_name_2 = '/afs/cern.ch/work/d/dcurry/private/rpc_mtf8/CMSSW_8_0_2/src/L1Trigger/L1TNtuples/test/l1Ntuple_RAW2DIGI.root'
    
    # out_file = TFile('plots/emul_vs_unpack_tracks.root','recreate')

    tree_name_1 = 'Events'
    tree_name_2 = 'Events'

    file_1 = TFile.Open(file_name_1)
    file_2 = TFile.Open(file_name_2)

    tree_1 = file_1.Get(tree_name_1)
    tree_2 = file_2.Get(tree_name_2)

    print 'Tree 1:', tree_1 
    

    #################
    ### Book counters
    #################

    numHits = {}
    numHitsUnm = {}
    numHitsUnmExist = {}
    numTrks = {}
    numTrksUnm = {}
    numTrksUnmExist = {}

    numHits[0] = 0
    numHitsUnm[0] = 0
    numHitsUnmExist[0] = 0
    numTrks[0] = 0
    numTrksUnm[0] = 0
    numTrksUnmExist[0] = 0

    numHits[1] = 0
    numHitsUnm[1] = 0
    numHitsUnmExist[1] = 0
    numTrks[1] = 0
    numTrksUnm[1] = 0
    numTrksUnmExist[1] = 0

    ## Main event loop    
    for iEvt in range(tree_1.GetEntries()):
        
        ## if (iEvt > 93346): continue
        if (iEvt > 1000): continue
        if iEvt % 100 is 0: print 'Event #', iEvt

        tree_1.GetEntry(iEvt)
        tree_2.GetEntry(iEvt)

        ## Get branches from the trees
        Event = tree_1.EventAuxiliary
        #Output_1_tmp = tree_1.l1tEMTFOutputs_unpack__EMTF
        #Hits_1 = []
        #Trks_1 = []
        
        # for emu vs emu comparisons
        Hits_1 = tree_1.l1tEMTFHits_simEmtfDigis_EMTF_L1TMuonEmulation
        Trks_1 = tree_1.l1tEMTFTracks_simEmtfDigis_EMTF_L1TMuonEmulation
        
        Hits_2 = tree_2.l1tEMTFHits_simEmtfDigis_EMTF_RAW2DIGI
        Trks_2 = tree_2.l1tEMTFTracks_simEmtfDigis_EMTF_RAW2DIGI
        
        if Event.event() != tree_2.EventAuxiliary.event():
            print 'In iEvt %d, tree 1 event = %d, tree 2 event = %d' % ( iEvt, Event.event(), tree_2.EventAuxiliary.event() )

        ## Fill hits and tracks from unpacker output
        #for iOut in range( Output_1_tmp.size() ):
        #    for iHit in range( Output_1_tmp.at(iOut).PtrMECollection().size() ):
        #        Hits_1.append( Output_1_tmp.at(iOut).PtrMECollection().at(iHit) )
        #    for iTrk in range( Output_1_tmp.at(iOut).PtrSPCollection().size() ):
        #        Trks_1.append( Output_1_tmp.at(iOut).PtrSPCollection().at(iTrk) )


        #nHits1 = len(Hits_1)
        #nTrks1 = len(Trks_1)
        
        nHits1 = Hits_1.size()
        nTrks1 = Trks_1.size()
    
        nHits2 = Hits_2.size()
        nTrks2 = Trks_2.size()

        nHits_min = min(nHits1, nHits2)
        nHits_max = max(nHits1, nHits2)
        nTrks_min = min(nTrks1, nTrks2)
        nTrks_max = max(nTrks1, nTrks2)

        if (nHits1 == 0 and nHits2 == 0): continue

        # ######################################
        # ### Print out every hit in every event
        # ######################################

        print 'L1T Emulator: %d hits in event %d' % ( nHits1, Event.event() )
        for iHit1 in range(nHits1):
            Hit1 = Hits_1.at(iHit1)
            print 'BX = %d, station = %d, sector = %d, ' % ( Hit1.BX() - 6, Hit1.Station(), Hit1.Sector() ), \
                 'CSC ID = %d, strip = %d, wire = %d, neighbor = %d' % ( Hit1.CSC_ID(), Hit1.Strip(), Hit1.Wire(), nTrks1)
            
        print 'EMTF Emulator: %d hits and %d tracks in event %d' % ( nHits2, nTrks2, Event.event() )
        for iHit2 in range(nHits2):
            Hit2 = Hits_2.at(iHit2)
            if (nTrks2 > 0 or nHits1 > 0):
                print 'BX = %d, station = %d, sector = %d, ' % ( Hit2.BX() - 6, Hit2.Station(), Hit2.Sector() ), \
                    'CSC ID = %d, strip = %d, wire = %d, nTrks = %d' % ( Hit2.CSC_ID(), Hit2.Strip(), Hit2.Wire(), nTrks2 )
                

        #####################################################################################
        ### Compare hits in emulator and unpacker
        ###   * Emulator outputs all hits it received, whether or not a track was formed
        ###   * Unpacker outputs hits only in sectors with tracks (zero-suppression)
        ###   * Unpacker ouputs neighbor hits twice, and may build duplicate tracks with them
        #####################################################################################
        print 
        
        ## Check that unpacker hits have match in emulator
        unmatched_hit_exists = False
        for iHit1 in range(nHits1):
            Hit1 = Hits_1.at(iHit1)
            #if Hit1.Neighbor() == 1:  ## Remove neighbor hits (which should appear twice)
            #    continue
            
            numHits[0] += 1
            unp_hit_matched = False
            for iHit2 in range(nHits2):
                Hit2 = Hits_2.at(iHit2)
                if Hit1.BX() == Hit2.BX() and Hit1.Station() == Hit2.Station() and Hit1.Sector() == Hit2.Sector():
                    if Hit1.CSC_ID() == Hit2.CSC_ID() and Hit1.Strip() == Hit2.Strip() and Hit1.Wire() == Hit2.Wire():
                        unp_hit_matched = True
            
            if not unp_hit_matched:
                unmatched_hit_exists = True
                numHitsUnm[0] += 1
                if nHits2 > 0:
                    numHitsUnmExist[0] += 1
                print 'Unpacker: unmatched hit in event %d' % Event.event()
                print 'BX = %d, station = %d, sector = %d, ' % ( Hit1.Tbin_num() - 2, Hit1.Station(), Hit1.Sector() ), \
                    'CSC ID = %d, strip = %d, wire = %d, neighbor = %d' % ( Hit1.CSC_ID(), Hit1.Strip(), Hit1.Wire(), Hit1.Neighbor() )
        
        ## Check that emulator hits have match in unpacker
        for iHit2 in range(nHits2):
            Hit2 = Hits_2.at(iHit2)
 
            numHits[1] += 1
            emu_hit_matched = False
            for iHit1 in range(nHits1):
                Hit1 = Hits_1.at(iHit1)
                #if Hit1.Neighbor() == 1:
                #    continue
                if Hit1.BX() == Hit2.BX() and Hit1.Station() == Hit2.Station() and Hit1.Sector() == Hit2.Sector():
                    if Hit1.CSC_ID() == Hit2.CSC_ID() and Hit1.Strip() == Hit2.Strip() and Hit1.Wire() == Hit2.Wire():
                        emu_hit_matched = True

            if not emu_hit_matched:
                unmatched_hit_exists = True
                numHitsUnm[1] += 1
                if nHits1 > 0:
                    numHitsUnmExist[1] += 1
                print 'Emulator: unmatched hit in event %d' % Event.event()
                print 'BX = %d, station = %d, sector = %d, ' % ( Hit2.BX() - 6, Hit2.Station(), Hit2.Sector() ), \
                    'CSC ID = %d, strip = %d, wire = %d, nTrks = %d' % ( Hit2.CSC_ID(), Hit2.Strip(), Hit2.Wire(), nTrks2 )


        # ########################################
        # ### Print out every track in every event
        # ########################################

        # print 'Unpacker: %d tracks in event %d' % ( nTrks1, Event.event() )
        # for iTrk1 in range(nTrks1):
        #     Trk1 = Trks_1[iTrk1]
        #     tmp_sector = -99
        #     has_neighbor = 0
        #     all_neighbor = 0
        #     ## Assign track sector based on hit sectors
        #     if (tmp_sector < 0 and Trk1.ME1_sector() > 0 and Trk1.ME1_neighbor() != 1): tmp_sector = Trk1.ME1_sector()
        #     if (tmp_sector < 0 and Trk1.ME2_sector() > 0 and Trk1.ME2_neighbor() != 1): tmp_sector = Trk1.ME2_sector()
        #     if (tmp_sector < 0 and Trk1.ME3_sector() > 0 and Trk1.ME3_neighbor() != 1): tmp_sector = Trk1.ME3_sector()
        #     if (tmp_sector < 0 and Trk1.ME4_sector() > 0 and Trk1.ME4_neighbor() != 1): tmp_sector = Trk1.ME4_sector()
        #     ## Check if some (or all) of the hits in the track are from a neighboring sector
        #     if ( Trk1.ME1_neighbor() == 1 or Trk1.ME2_neighbor() == 1 or Trk1.ME3_neighbor() == 1 or Trk1.ME4_neighbor() == 1 ): has_neighbor = 1
        #     if ( Trk1.ME1_neighbor() != 0 and Trk1.ME2_neighbor() != 0 and Trk1.ME3_neighbor() != 0 and Trk1.ME4_neighbor() != 0 ): all_neighbor = 1
        #     ## if ( all_neighbor == 1 ): continue  
        #     print 'BX = %d, sector = %d, mode = %d, eta = %d, ' % ( Trk1.TBIN_num() - 3, tmp_sector, Trk1.Mode(), Trk1.Eta_GMT_int() ), \
        #         'phi = %d, pT = %d, has some (all) neighbor hits = %d (%d)' % ( Trk1.Phi_GMT_int(), Trk1.Pt_int(), has_neighbor, all_neighbor )

        # print 'Emulator: %d tracks in event %d' % ( nTrks2, Event.event() )
        # for iTrk2 in range(nTrks2):
        #     Trk2 = Trks_2.at(iTrk2)
        #     print 'BX = %d, sector = %d, mode = %d, eta = %d, ' % ( Trk2.First_BX() - 6, Trk2.Sector(), Trk2.Mode(), Trk2.Eta_GMT() ), \
        #         'phi = %d, pT = %d' % ( Trk2.Phi_GMT(), Trk2.Pt_GMT() )


        #####################################################################################
        ### Compare tracks in emulator and unpacker
        ###   * Only compare if emulator and unpacker hits are identical
        #####################################################################################

        if unmatched_hit_exists:
            continue
        if ( nTrks1 == 0 and nTrks2 == 0 ):
            continue

        ## Check that unpacker tracks have match in emulator
        for iTrk1 in range(nTrks1):
            Trk1 = Trks_1.at(iTrk1)
            tmp_sector = -99
            has_neighbor = 0
            all_neighbor = 0
            ## Assign track sector based on hit sectors
            #if (tmp_sector < 0 and Trk1.ME1_sector() > 0 and Trk1.ME1_neighbor() != 1): tmp_sector = Trk1.ME1_sector()
            #if (tmp_sector < 0 and Trk1.ME2_sector() > 0 and Trk1.ME2_neighbor() != 1): tmp_sector = Trk1.ME2_sector()
            #if (tmp_sector < 0 and Trk1.ME3_sector() > 0 and Trk1.ME3_neighbor() != 1): tmp_sector = Trk1.ME3_sector()
            #if (tmp_sector < 0 and Trk1.ME4_sector() > 0 and Trk1.ME4_neighbor() != 1): tmp_sector = Trk1.ME4_sector()
            ## Check if some (or all) of the hits in the track are from a neighboring sector
            #if ( Trk1.ME1_neighbor() == 1 or Trk1.ME2_neighbor() == 1 or Trk1.ME3_neighbor() == 1 or Trk1.ME4_neighbor() == 1 ): has_neighbor = 1
            #if ( Trk1.ME1_neighbor() != 0 and Trk1.ME2_neighbor() != 0 and Trk1.ME3_neighbor() != 0 and Trk1.ME4_neighbor() != 0 ): all_neighbor = 1
            #if ( all_neighbor == 1 ): continue

            numTrks[0] += 1
            unp_trk_matched = False
            for iTrk2 in range(nTrks2):
                Trk2 = Trks_2.at(iTrk2)
                if ( abs(Trk1.Eta_GMT() - Trk2.Eta_GMT()) < 3 and abs(Trk1.Phi_GMT() - Trk2.Phi_GMT()) < 6 ): 
                    unp_trk_matched = True

            if not unp_trk_matched:
                numTrksUnm[0] += 1
                if (nTrks2 > 0):
                    numTrksUnmExist[0] += 1
                print 'Unpacker: unmatched track in event %d' % Event.event()
                print 'BX = %d, sector = %d, mode = %d, eta = %d, ' % ( Trk1.TBIN_num() - 3, tmp_sector, Trk1.Mode(), Trk1.Eta_GMT_int() ), \
                    'phi = %d, pT = %d, has neighbor hits = %d' % ( Trk1.Phi_GMT_int(), Trk1.Pt_int(), has_neighbor )


        ## Check that emulator tracks have match in unpacker
        for iTrk2 in range(nTrks2):
            Trk2 = Trks_2.at(iTrk2)

            numTrks[1] += 1
            emu_trk_matched = False
            for iTrk1 in range(nTrks1):
                Trk1 = Trks_1.at(iTrk1)
                tmp_sector = -99
                has_neighbor = 0
                all_neighbor = 0
                #if (tmp_sector < 0 and Trk1.ME1_sector() > 0 and Trk1.ME1_neighbor() != 1): tmp_sector = Trk1.ME1_sector()
                #if (tmp_sector < 0 and Trk1.ME2_sector() > 0 and Trk1.ME2_neighbor() != 1): tmp_sector = Trk1.ME2_sector()
                #if (tmp_sector < 0 and Trk1.ME3_sector() > 0 and Trk1.ME3_neighbor() != 1): tmp_sector = Trk1.ME3_sector()
                #if (tmp_sector < 0 and Trk1.ME4_sector() > 0 and Trk1.ME4_neighbor() != 1): tmp_sector = Trk1.ME4_sector()
                #if ( Trk1.ME1_neighbor() == 1 or Trk1.ME2_neighbor() == 1 or Trk1.ME3_neighbor() == 1 or Trk1.ME4_neighbor() == 1 ): has_neighbor = 1
                #if ( Trk1.ME1_neighbor() != 0 and Trk1.ME2_neighbor() != 0 and Trk1.ME3_neighbor() != 0 and Trk1.ME4_neighbor() != 0 ): all_neighbor = 1
                #if ( all_neighbor == 1 ): continue

                if ( abs(Trk1.Eta_GMT() - Trk2.Eta_GMT()) < 3 and abs(Trk1.Phi_GMT() - Trk2.Phi_GMT()) < 6 ):
                    emu_trk_matched = True

            if not emu_trk_matched:
                numTrksUnm[1] += 1
                if (nTrks1 > 0):
                    numTrksUnmExist[1] += 1
                print 'Emulator: unmatched track in event %d' % Event.event()
                print 'BX = %d, sector = %d, mode = %d, eta = %d, ' % ( Trk2.First_BX() - 6, Trk2.Sector(), Trk2.Mode(), Trk2.Eta_GMT() ), \
                    'phi = %d, pT = %d' % ( Trk2.Phi_GMT(), Trk2.Pt_GMT() )



    print '*************************************************'
    print '*******         The BIG picture           *******'
    print '*************************************************'
    print '                 L1T Emulator  -  EMTF Emulator'
    print 'numHits:          %6d %11d' % (numHits[0], numHits[1]) 
    print 'numHitsUnm:       %6d %11d' % (numHitsUnm[0], numHitsUnm[1]) 
    print 'numHitsUnmExist:  %6d %11d' % (numHitsUnmExist[0], numHitsUnmExist[1]) 
    print 'numTrks:          %6d %11d' % (numTrks[0], numTrks[1]) 
    print 'numTrksUnm:       %6d %11d' % (numTrksUnm[0], numTrksUnm[1]) 
    print 'numTrksUnmExist:  %6d %11d' % (numTrksUnmExist[0], numTrksUnmExist[1]) 

    ## out_file.cd()

    del tree_1
    del tree_2

    file_1.Close()
    file_2.Close()

if __name__ == '__main__':
    main()

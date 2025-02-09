from __future__ import print_function
__author__ = 'Leanne Whitmore and Lucy Chian'
__email__ = 'lwhitmo@sandia.gov'
__description__ = 'Compare flux balance analysis results from wildtype \
                   to results with added reactions '

class Compare(object):
    """
    Compares flux values between simulation without added reactions and compounds and simulation
    with the reactions and compounds
    """
    def __init__(self, target_compound_ID, wtresults, exresults, ex_paths, DB, fold_threshold=1.5):
        '''Initialize class'''
        self.target = target_compound_ID
        self.wtresults = wtresults
        self.exresults = exresults
        self.ex_paths = ex_paths
        self.DB = DB
        self.fold_threshold = fold_threshold+1
        self.fluxchange = {}
        self.externalrxnfluxes = {}
        self.get_flux_differences()
        self.external_pathanalyze_fluxes()

    def analyze_fluxes(self, rxn):
        '''
        Determines if flux differences between simulations is greater than 2.5 fold
        '''
        name = self.DB.get_reaction_name(rxn)
        if rxn in self.wtresults.fluxes:
            if self.wtresults.fluxes[rxn] != 0 and self.exresults.fluxes[rxn] != 0:
                upperfold = self.wtresults.fluxes[rxn] * self.fold_threshold
                changefold = abs(upperfold - self.wtresults.fluxes[rxn])
                if self.wtresults.fluxes[rxn] < 0:
                    lowerfold = self.wtresults.fluxes[rxn] + changefold
                elif self.wtresults.fluxes[rxn] > 0:
                    lowerfold = self.wtresults.fluxes[rxn] - changefold
                if upperfold < 0:
                    if (self.exresults.fluxes[rxn] <= upperfold
                            or self.exresults.fluxes[rxn] >= lowerfold):
                        self.fluxchange[rxn] = '\t'.join([name, str(self.wtresults.fluxes[rxn]),
                                                          str(self.exresults.fluxes[rxn])])
                    if (self.exresults.fluxes[rxn] <= lowerfold or
                            self.exresults.fluxes[rxn] >= upperfold):
                        self.fluxchange[rxn] = '\t'.join([name, str(self.wtresults.fluxes[rxn]),
                                                          str(self.exresults.fluxes[rxn])])
            elif self.wtresults.fluxes[rxn] == 0 and self.exresults.fluxes[rxn] != 0:
                if self.exresults.fluxes[rxn] <= -1 or self.exresults.fluxes[rxn] >= 1:
                    self.fluxchange[rxn] = '\t'.join([str(self.wtresults.fluxes[rxn]),
                                                      str(self.exresults.fluxes[rxn])])
        elif rxn not in self.wtresults.fluxes:
            self.externalrxnfluxes[rxn] = name+'\t'+str(self.exresults.fluxes[rxn])

    def get_flux_differences(self):
        '''
        Gets reactions for the flux difference is greater than 2.5 fold
        '''
        for rxn in self.exresults.fluxes.index:
            self.analyze_fluxes(rxn)

    def external_pathanalyze_fluxes(self):
        '''
        Extracts the external (added reactions) path carrying the most flux
        '''
        pathwayflux = {}
        if len(self.ex_paths) != 0:
            for key, path in self.ex_paths.iteritems():
                flux = 0
                for r in path:
                    if r not in self.externalrxnfluxes.keys():
                        # print ('WARNING: {} reaction is internal to target organism'.format(r))
                        pass
                    elif r in self.externalrxnfluxes and len(self.externalrxnfluxes) != 0:
                        values = self.externalrxnfluxes[r].split('\t')
                        flux += abs(float(values[1]))
                pathwayflux[key] = flux
            self.maxflux = max(pathwayflux.values())
            self.maxpath = pathwayflux.keys()[pathwayflux.values().index(self.maxflux)]
        else:
            self.maxpath = 'No added path'
            self.maxflux = self.exresults.fluxes['Sink_'+self.target]

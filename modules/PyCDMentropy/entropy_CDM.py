from oct2py import octave,Struct
from hdnet.spikes import Spikes
class CDMentropy:
    def __init__(self, isDBer=True, verbose=False, nMC=999):
        octave.addpath(octave.genpath('CDMentropy'))
        self.opts=octave.struct('isDBer',isDBer,'verbose',verbose,'nMC',nMC)

    def entropy_CDM(self,spikes,trial):
        nn,ocnts=octave.words2nnOcnts(spikes._spikes[trial],nout=2)
        m = octave.size(spikes._spikes[trial], 2)
        H, Hvar, CIhandle, internal, Hsamples, opts = octave.computeH_CDM(
            nn, ocnts, m, self.opts,nouts=6)
        return H,Hvar
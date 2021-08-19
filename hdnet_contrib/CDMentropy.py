from oct2py import octave
import numpy as np
import os

class CDMentropy:
    """
    Calculates entropy and corresponding mutual information for spiketrain data appended with stimulus
    """
    def __init__(self, spikes, source=None, isDBer=True, verbose=False, nMC=999):
        """
        Initialises oct2py interface for CDMentropy MATLAB code
        Parameters
        ----------
        source : string
            path to CDMentropy MATLAB codebase
        spikes : HDNet Spikes object
        isDBer : bool
        verbose : bool
        nMC : int
        """
        if source is None:
            source = os.path.join(os.path.dirname(__file__),"PyCDMentropy/CDMentropy")
        octave.addpath(octave.genpath(source))
        octave.addpath(octave.genpath(source+'/lib/PYMentropy'))
        self.opts=octave.struct('isDBer',isDBer,'verbose',verbose,'nMC',nMC)
        self.spikes=spikes

    def _entropyCDM(self,matrix_spikes):
        """
        Parameters
        ----------
        matrix_spikes : 2d array
            M*N array of spiketrain
        Returns
        -------
        """
        nn,ocnts=octave.words2nnOcnts(matrix_spikes,nout=2)
        m = np.shape(matrix_spikes)[0]
        return octave.computeH_CDM(nn, ocnts, m, self.opts) 

    def entropyCDM(self, trial, time_start, neuron_start, time_end=None,neuron_end=None):
        """
        Returns entropy calculated upon spiketrain, specifying time bins to consider and neurons to include in calculation
        Parameters
        ----------
        trial : int
            trial number to calculate on from spikes
        time_start : int
            start of range of timebins included in calculation (included in range)
        time_end : int
            end of range of timebins included in calculation (excluded in range)
        neuron_start : int
            start of range of neurons included in calculation (included in range)
        neuron_end : int
            end of range of neurons included in calculation (excluded in range)
        Returns
        -------
        """
        if time_end is None:
            time_end=time_start+1
        if neuron_end is None:
            neuron_end=neuron_start+1
        return self._entropyCDM(self.spikes._spikes[trial][neuron_start:neuron_end,time_start:time_end].T)

    def mutualInformationWindowed(self, trial, time_start, neuron_start, stimulus_start, tau, time_end=None, 
    neuron_end=None, stimulus_end=None):
        """
        WIP
        Returns mutualInformation between neuron responses and stimulus appended to spikes for timebins in a range using CDM Entropy
        Parameters
        ----------
        trial : int
            trial number to calculate on from spikes
        time_start : int
            start of range of timebins included in calculation (included in range)
        time_end : int
            end of range of timebins included in calculation (excluded in range)
        neuron_start : int
            start of range of neurons included in calculation (included in range)
        neuron_end : int
            end of range of neurons included in calculation (excluded in range)
        stimulus_start : int
            start of range of neurons in spikes denoting binary stimulus (included in range)
        stimulus_end : int
            end of range of neurons in spikes denoting binary stimulus (excluded in range)
        tau : int
            shift in time from which stimulus considered
        Returns
        -------
        """
        if stimulus_end is None:
            stimulus_end = np.shape(self.spikes._spikes[trial])[0]

        HR = self._entropyCDM(self.spikes._spikes[trial][neuron_start:neuron_end,time_start:time_end].T)
        HX = self._entropyCDM(self.spikes._spikes[trial][stimulus_start:stimulus_end,time_start+tau:time_end+tau].T)
        temp_concat_spikes = np.zeros((time_end-time_start,neuron_end-neuron_start+stimulus_end-stimulus_start))
        for t in range(time_start, time_end):
            temp_concat_spikes[t,:] = np.append(self.spikes._spikes[trial][neuron_start:neuron_end,t],self.spikes._spikes[trial][stimulus_start:stimulus_end,t+tau]).T
        HRX = self._entropyCDM(temp_concat_spikes)
        return HR+HX-HRX

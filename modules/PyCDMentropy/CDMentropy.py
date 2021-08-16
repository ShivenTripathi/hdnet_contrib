from oct2py import octave
import numpy as np

class CDMentropy:
    """
    Calculates entropy and corresponding mutual information for spiketrain data appended with stimulus
    """
    def __init__(self, source, spikes, isDBer=True, verbose=False, nMC=999):
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

    def mutualInformation(self, trial, neuron_start, neuron_end, stimulus_start, stimulus_end, time, tau):
        """
        Parameters
        ----------
        trial : int
            trial number to calculate on from spikes
        neuron_start : int
            start of range of neurons included in calculation (included in range)
        neuron_end : int
            end of range of neurons included in calculation (excluded in range)
        stimulus_start : int
            start of range of neurons in spikes denoting binary stimulus (included in range)
        stimulus_end : int
            end of range of neurons in spikes denoting binary stimulus (excluded in range)
        time : int
            timestep for which neuron spikes considered
        tau : int
            shift in time from which stimulus considered

        Returns
        -------
        """
        HX_t = self._entropyCDM(self.spikes._spikes[trial][neuron_start:neuron_end, time:time+1])
        HR_t_tau = self._entropyCDM(self.spikes._spikes[trial][stimulus_start:stimulus_end, time+tau:time+tau+1])
        H_R_t_tau_X_t = self._entropyCDM(np.atleast_2d(np.append(self.spikes._spikes[trial][neuron_start:neuron_end, time:time+1], 
        self.spikes._spikes[trial][stimulus_start:stimulus_end, time+tau:time+tau+1])).T)
        return HX_t+HR_t_tau-H_R_t_tau_X_t 

    def mutualInformationWindowed(self, trial, neuron_time_start, neuron_start, stimulus_start, stimulus_time_start, neuron_time_end=None, 
    neuron_end=None, stimulus_end=None, stimulus_time_end=None):
        """
        WIP

        Returns mutualInformation between neuron responses and stimulus appended to spikes for timebins in a range using CDM Entropy

        Parameters
        ----------
        trial : int
            trial number to calculate on from spikes
        neuron_time_start : int
            start of range of timebins included in calculation (included in range)
        neuron_time_end : int
            end of range of timebins included in calculation (excluded in range)
        neuron_start : int
            start of range of neurons included in calculation (included in range)
        neuron_end : int
            end of range of neurons included in calculation (excluded in range)
        stimulus_start : int
            start of range of neurons in spikes denoting binary stimulus (included in range)
        stimulus_end : int
            end of range of neurons in spikes denoting binary stimulus (excluded in range)
        stimulus_time_start : int
        stimulus_time_end : int

        Returns
        -------
        """
        if stimulus_end is None:
            stimulus_end = np.shape(self.spikes._spikes[trial])[0]
        HR = self._entropyCDM(self.spikes._spikes[trial][neuron_start:neuron_end,neuron_time_start:neuron_time_end])
        HX = self._entropyCDM(self.spikes._spikes[trial][stimulus_start:stimulus_end,stimulus_time_start:stimulus_time_end])
        temp_concat_spikes = np.atleast_2d(np.append(self.spikes._spikes[trial][neuron_start:neuron_end, neuron_time_start:neuron_time_end], 
        self.spikes._spikes[trial][stimulus_start:stimulus_end, stimulus_time_start:stimulus_time_end])).T
        HRX = self._entropyCDM(temp_concat_spikes)
        return HR+HX-HRX
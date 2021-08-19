function [nn,ocnts] = words2nnOcnts(words, BINARIZE)
% [nn ocnts] = words2nnOcnts(words, BINARIZE)
%
% Returns the histogram & spike counts of the matrix words, where 
% words is a [time x ncells] matrix. 
%
% Unlike regular entropy estimators, the CDM estimator requires the knowledge
% of the # of 1's in each binary vector to assign them to appropriate partitions
% 
% Input:
%       words - [time x ncells] matrix
%    BINARIZE - (optional) If false, permit non-binary spike counts.
%               (default: true)
% Output:
%          nn - histogram of words
%       ocnts - number of spikes in each word
%
% See also: makeMex

if nargin < 2
    BINARIZE = true;
end
   
if BINARIZE
    nAlphabet = 2;
else
    nAlphabet = max(words(:)) + 1;
end

warning('words2nnOcnts:slow', 'Using words2multiplicities (slower). Consider compiling discreteTimeSeries2Words for faster processing.\n')
[~,~,nn,bin] = words2multiplicities(words, nAlphabet);     


% find the number of spikes in each unique word
[~, IA] = unique(bin);
ocnts = full(sum(words(IA,:), 2));
end

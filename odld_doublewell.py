from westpa.core.propagators import WESTPropagator
from westpa.core.systems import WESTSystem
#from westpa.binning import RectilinearBinMapper
from westpa.core.binning import VectorizingFuncBinMapper

import numpy as np
from numpy.random import uniform
from numpy import random
import pickle
from numpy import linspace, int32, float32, array, empty, zeros, int_, any
from numpy.random import Generator, PCG64
from numpy import sqrt as np_sqrt


pcoord_len = 2	# Number of timesteps to be saved
pcoord_dtype = float32

x_to_x_h = np.loadtxt("../x_to_xh.txt")
x_to_x_h = x_to_x_h.astype(int)
boundary = np.loadtxt("../bin_s.txt")
boundary = boundary.astype(int)
allocation = np.loadtxt("../bin_s_alloc_w.txt")
nbins = 5+1
total_walker = 30

class ODLDPropagator(WESTPropagator):
    def __init__(self, rc=None):
        super(ODLDPropagator, self).__init__(rc)

        self.coord_len = pcoord_len
		#self.coord_len = how many timesteps to take (which is set to be same as pcoord_len)
        self.coord_dtype = pcoord_dtype
        self.coord_ndim = 1

        # Initialize at state 0 
        self.initial_pcoord = array([0.0], dtype=self.coord_dtype)

        self.rng = Generator(PCG64())

        data = np.load('./T_mtx_cumulative.npz')
        self.cumulative_transition_matrix = data["t_mtx_cumulative"]
	# The matrix in this file does NOT have BC
	# Will have BC in init.sh file 

    def get_pcoord(self, state):
        """Get the progress coordinate of the given basis or initial state."""
        state.pcoord = self.initial_pcoord.copy()

    def gen_istate(self, basis_state, initial_state):
        initial_state.pcoord = self.initial_pcoord.copy()
        initial_state.istate_status = initial_state.ISTATE_STATUS_PREPARED
        return initial_state

    def propagate(self, segments):

        n_segs = len(segments)

        coords = empty(
            (n_segs, self.coord_len, self.coord_ndim), dtype=self.coord_dtype
        )

        # Set the zeroth index to the starting positions
        for iseg, segment in enumerate(segments):
            coords[iseg, 0] = segment.pcoord[0]

        coord_len = self.coord_len
        #all_displacements = zeros(
        #    (n_segs, self.coord_len, self.coord_ndim), dtype=self.coord_dtype
        #)

        RNDMnumber = random.rand(n_segs)
	# Generate random number for each segment (trajectory) 
	# Apparently it's faster than generating one random number n_segs times

        for istep in range(1, coord_len):
            for k in range(n_segs):
                old_x = coords[k, istep-1, 0]

                if RNDMnumber[k] <= self.cumulative_transition_matrix[int(old_x)][0]:
                    coords[k, istep, 0] = 0.0
                for j in range(len(self.cumulative_transition_matrix)-1):
                    if self.cumulative_transition_matrix[int(old_x)][j] < RNDMnumber[k] and RNDMnumber[k] <= self.cumulative_transition_matrix[int(old_x)][j+1]:
                        coords[k, istep, 0] = float(j+1)
 
        for iseg, segment in enumerate(segments):
            segment.pcoord[...] = coords[iseg, :]
            segment.status = segment.SEG_STATUS_COMPLETE

        return segments

def func(coord):
    #print("x: ",int(coord[0]))
    if int(coord[0]) == 2019:
        #print("bin: ",nbins)
        return nbins - 1
    else:
        coord_in_xh = x_to_x_h[int(coord[0])][1]
            # The coord in x_h
    #print("x_h: ",coord_in_xh)
        if coord_in_xh <= boundary[0]:
        #print("bin: ",1)
            return 0
        for i in range(nbins - 1):
            if boundary[i] < coord_in_xh and coord_in_xh <= boundary[i+1]:
            #print("bin: ",i+2)
                return i+1

class ODLDSystem(WESTSystem):

    def initialize(self):
        self.pcoord_ndim = 1
        self.pcoord_dtype = pcoord_dtype
        self.pcoord_len = pcoord_len

        # Be careful about dealing with the target state / bin 
        # Read in x_to_x_h
        #self.x_to_x_h = np.loadtxt("./x_to_xh.txt")
        # Read in bin_boundaries_in_x_h
        #self.boundary = np.loadtxt("./boundary_S.txt")
        # Read in allocation for each bin (normalized so that the sum of allocation for all bin is 1) 
        self.allocation = allocation
        self.normalization = 0.0
        for j in range(len(self.allocation)):
            self.normalization += self.allocation[j]
        for j in range(len(self.allocation)):
            self.allocation[j] *= 1/self.normalization
	    
        self.nbins = nbins;
	    # Last bin only contains the tstate
        self.total_walker = total_walker;
	    # Total number of trajectories you want to maintain during WE

        #self.bin_mapper = RectilinearBinMapper([[-float('inf'), 500.0, 1000.0, 1500.0, 2018.5, float('inf')]])

        self.bin_mapper = VectorizingFuncBinMapper(func, self.nbins)

        self.bin_target_counts = empty((self.nbins,), int_)
        #self.bin_target_counts[...] = 2
#        print("AAA")
#        print(self.bin_target_counts)

        bin_random = random.rand(self.nbins)

        for i in range(self.nbins-1):
	# Note that last bin is just allocated 1 trajectory
            self.avg_alloc = self.allocation[i] * self.total_walker
            if bin_random[i] < (1 - (self.avg_alloc - np.floor(self.avg_alloc))):
                self.bin_target_counts[i] = np.floor(self.avg_alloc)
            else:
                self.bin_target_counts[i] = np.floor(self.avg_alloc) + 1
        self.bin_target_counts[self.nbins-1] = 1

#        print(self.bin_target_counts)
        #self.bin_target_counts[...] = 3
	    # Number of trajectories per bin 

import h5py
import pandas
import numpy as np

directory='/Users/WHR/Desktop/work_while_in_cali/mod_WE/runs/strategies/bin_s_alloc_w/flux_analysis/'

f = h5py.File(directory+'flux_1.h5', 'r')
uhh = f['target_flux/target_0/flux']
np.savetxt(directory+'flux_1.txt',uhh,delimiter=' ')

f = h5py.File(directory+'flux_2.h5', 'r')
uhh = f['target_flux/target_0/flux']
np.savetxt(directory+'flux_2.txt',uhh,delimiter=' ')

f = h5py.File(directory+'flux_3.h5', 'r')
uhh = f['target_flux/target_0/flux']
np.savetxt(directory+'flux_3.txt',uhh,delimiter=' ')

f = h5py.File(directory+'flux_4.h5', 'r')
uhh = f['target_flux/target_0/flux']
np.savetxt(directory+'flux_4.txt',uhh,delimiter=' ')

f = h5py.File(directory+'flux_5.h5', 'r')
uhh = f['target_flux/target_0/flux']
np.savetxt(directory+'flux_5.txt',uhh,delimiter=' ')

f = h5py.File(directory+'flux_6.h5', 'r')
uhh = f['target_flux/target_0/flux']
np.savetxt(directory+'flux_6.txt',uhh,delimiter=' ')

f = h5py.File(directory+'flux_7.h5', 'r')
uhh = f['target_flux/target_0/flux']
np.savetxt(directory+'flux_7.txt',uhh,delimiter=' ')

f = h5py.File(directory+'flux_8.h5', 'r')
uhh = f['target_flux/target_0/flux']
np.savetxt(directory+'flux_8.txt',uhh,delimiter=' ')

f = h5py.File(directory+'flux_9.h5', 'r')
uhh = f['target_flux/target_0/flux']
np.savetxt(directory+'flux_9.txt',uhh,delimiter=' ')

f = h5py.File(directory+'flux_10.h5', 'r')
uhh = f['target_flux/target_0/flux']
np.savetxt(directory+'flux_10.txt',uhh,delimiter=' ')

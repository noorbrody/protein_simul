import time
import cryo as cr
from pathos.multiprocessing import Pool
from scipy.stats import special_ortho_group as og
import numpy as np
import mrcfile
from itertools import repeat

# number of images
k = 100

# load data
mol = mrcfile.open("zika_153.mrc").data

t0 = time.time()
# random rotation matrices
with Pool() as p:
    orientations = list(map(og.rvs, repeat(3,k)))
    images = p.map((lambda R: cr.project_fst(mol, R)), orientations)
    b = cr.reconstruct(images, orientations)
with mrcfile.new('zika_reconstruction_1.mrc', overwrite=True) as mrc:
    mrc.set_data(b)
 
print("Completed", k, "in", time.time()-t0)

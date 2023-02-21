import os

def run():
    fnames=  np.load('fnames.npy')
    for fname in fnames:
        os.system(f'sacct --format=JobID,Elapsed,State --job {fname}')



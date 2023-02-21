import os
import numpy as np

def run():
    fnames = np.load('fnames.npy')
    for fname in fnames:
        os.system(f'sacct --format=JobID,Elapsed,State --job {fname}')


if __name__ == '__main__':
    run()
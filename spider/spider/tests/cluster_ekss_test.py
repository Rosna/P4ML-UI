'''
    spider.tests: cluster_ekss_test.py

    @mingyuaz

    Unit tests for the spider.cluster.ekss module
'''

import unittest
import tempfile
import os.path
import shutil

import numpy as np
from scipy.linalg import orth
from sklearn.preprocessing import normalize

from spider.cluster.ekss import EKSS


class testEKSS(unittest.TestCase):


    def test_ekss(self):
        """ Test runnability and verify shapes of estimated_labels

        """

        # parameters
        D = 100  # dimension of ambient space
        K = 5  # number of subspaces
        Nk = 100  # points per subspace
        d = 1  # dimension of subspace
        varn = 0.01   # noise variance
        B = 10 # number of base clusterings
        q = 10 # threshold parameter
        N = K * Nk

        # generate data
        X = np.zeros((D, N))
        true_labels = np.zeros(N)
        true_U = np.zeros((K, D, d))
        for kk in range(K):
            true_U[kk] = orth(np.random.randn(D, d))
            x = np.dot(true_U[kk], np.random.randn(d, Nk))
            X[:,range(Nk*kk, Nk*(kk+1))] = x
            true_labels[range(Nk*kk, Nk*(kk+1))] = kk * np.ones(Nk)

        noise = np.sqrt(varn) * np.random.randn(D, N)
        X = X + noise
        X = normalize(X, norm='l2', axis=0)

        # run EKSS
        eksub = EKSS(n_clusters=5, dim_subspaces=d, n_base=B, thresh=q)
        estimated_labels = eksub.produce(X.T)

        self.assertEqual(len(estimated_labels), N)

if __name__ == '__main__':
    unittest.main()

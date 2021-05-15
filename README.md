# inhibitory-connectivity

This repository contains the code for reproduction of results obtained in the report submitted for the Practical Biomedical Module,
as part of our completion of the Master of Science in Computational Neuroscience, Cognition and Artificial Intelligence of the University of Nottingham.

There are four different notebooks for reproducing figures 1, 2, 5 and 7 of the paper Inhibitory Connections Define the Realm for Excitatory Plasticity. The network in simulated using Brian2 package.


To open the notebook in Google Colab to reproduce figure 1:

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/albertalbesa/inhibitory-connectivity/blob/main/Notebooks/Figure1.ipynb)

To open the notebook in Google Colab to reproduce figure 2:

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/albertalbesa/inhibitory-connectivity/blob/main/Notebooks/Figure2.ipynb)

To open the notebook in Google Colab to reproduce figure 5:

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/albertalbesa/inhibitory-connectivity/blob/main/Notebooks/Figure5.ipynb)

To open the notebook in Google Colab to reproduce figure 7:

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/albertalbesa/inhibitory-connectivity/blob/main/Notebooks/Figure7.ipynb)


Reproduction of all figures requires initializing the network voltage with initial_voltage.npy file, which can be found in the Data folder.

Reproduction of figures 2 and 5 requires to generate the connectivity matrices. This can be done by executing the following:

figure 2 -> execute process_dataset.py and then random_network.jl (Random Network folder)

figure 5 -> execute structured_network.jl and then csv_to_sparse.py (Structured Network folder)


In the Report folder you can also take a look at the original report submitted!

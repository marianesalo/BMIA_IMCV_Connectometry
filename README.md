# ICMV - BMIA: Connectometry Using HCP-YA and DSI Studio

## Overview

This repository represents the work of the students from BMIA course to reproduce the connectometry pipeline proposed by the paper:

Yeh, F.-C., Badre, D., & Verstynen, T. (2016). Connectometry: A statistical approach harnessing the analytical potential of the local connectome. NeuroImage, 125, 162–171. https://doi.org/10.1016/j.neuroimage.2015.10.053

In order to reproduce the local connectome analysis the following was used:

* Human Connectome Project Young Adult (HCP-YA) diffusion MRI data
* [DSI Studio](https://dsi-studio.labsolver.org/?utm_source=chatgpt.com)
* QSDR-reconstructed diffusion data (.qsdr.fz)
* Correlational tractography / connectometry

## Repo structure

```
BMIA_IMCV_Connoctometry/
│
├── data/
│   ├── *.qsdr.fz
│   ├── *.gqi.fz
│   ├── *.sz
│   └── ...
│
├── scripts/
│   ├── generate_fake_demographics.py
│   └── ...
│
├── results/
│   └── ...
│
├── docs/
│   └── ...specific documentation...
│
├── README.md
│
└── requirements.txt
```
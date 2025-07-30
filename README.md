# HmtG-PacBio Pipeline

> Comprehensive pipeline for processing Haemosporidian mitochondrial genome data from PacBio sequencing.

![Python](https://img.shields.io/badge/python-3.9%2B-blue)  
![MAFFT](https://img.shields.io/badge/mafft-7.520-green)  
![BLAST](https://img.shields.io/badge/blast-2.6.0-orange)  
![License](https://img.shields.io/badge/license-MIT-lightgrey)

---

## Table of Contents

- [Features](#features)  
- [Requirements](#requirements)  
- [Installation](#installation)  
- [Usage](#usage)  
  - [Arguments](#arguments)  
  - [Examples](#examples)  
- [Output](#output)  
- [Citation](#citation)  
- [License](#license)  
- [Contributing](#contributing)  

---

## Features

- 🔍 **Primer detection**  
- 🔗 **Sequence alignment** (MAFFT)  
- 💾 **DNA → binary** conversion  
- 🧠 **Variational Autoencoder (VAE)** modeling  
- 📦 **DBSCAN** clustering  
- 🛠 **Sequence correction**  
- 🔬 **Local BLAST** analysis  

---

## Requirements

- **Python 3.9+**  
- **MAFFT v7.520**  
- **BLAST+ 2.6.0**  
- Python libraries:  
  - TensorFlow 2.14.0  
  - Keras 2.14.0  
  - BioPython  
  - numpy, pandas, scipy, …  

---

## Installation

```bash
# 1. Clone this repository
git clone https://github.com/asgiraldoc/HmtG-PacBio-Pipeline.git
cd HmtG-PacBio-Pipeline

# 2. Create & activate conda environment
conda create -n HmtG-PacBio python=3.9 -y
conda activate HmtG-PacBio

# 3. Install system dependencies
conda install -c bioconda mafft blast -y

# 4. Install Python packages
pip install -r requirements.txt
```

---

## Usage

```bash
python HmtG-PacBio-Pipeline.py   -rR /path/to/raw_reads.fastq   [ -pF FORWARD_PRIMER ]   [ -pR REVERSE_PRIMER ]   [ -eps EPS_VALUE ]   [ --remove-temp yes|no ]   [ --blastn yes|no ]
```

### Arguments

| Flag                   | Description                                           | Default                                              |
| ---------------------- | ----------------------------------------------------- | ---------------------------------------------------- |
| `-rR`, `--rawReads`    | Raw PacBio reads (FASTQ/FASTA) **(required)**         | —                                                    |
| `-pF`, `--primerF`     | Forward primer sequence                              | `GATTCTCTCCACACTTCAATTCGTACTTC`                     |
| `-pR`, `--primerR`     | Reverse primer sequence                              | `GAAGTACGAATTGAAGTGTGGAGAGAATC`                     |
| `-eps`, `--epsDBScan`  | Epsilon parameter for DBSCAN clustering               | `1.0`                                                |
| `--remove-temp`        | Remove intermediate files after completion            | `yes`                                                |
| `--blastn`             | Run local BLASTn                                      | `yes`                                                |

### Examples

```bash
# Basic run with defaults
python HmtG-PacBio-Pipeline.py -rR data/sample_reads.fastq

# Custom primers, disable BLAST
python HmtG-PacBio-Pipeline.py   -rR data/sample_reads.fastq   -pF ACTGACTGACTG   -pR CAGTCAGTCAGT   --blastn no
```

---

## Output

Upon successful execution, you will find:

```
aligned/         # MAFFT .aln and .fasta files
binary/          # Binary-encoded sequences
clusters/        # DBSCAN cluster assignments
vae_model.png    # VAE training & loss curve
clusters.png     # Cluster visualization
distances.tsv    # Pairwise genetic distances
blast_results/   # Local BLASTn outputs
```

---

## Citation

If you use this pipeline in your research, please cite:

> Pacheco, M.A., Cepeda, A.S., Miller, E.A. *et al.*  
> **A new long-read mitochondrial-genome protocol (PacBio HiFi) for haemosporidian parasites: a tool for population and biodiversity studies.**  
> *Malaria Journal*, 23:134 (2024).  
> https://doi.org/10.1186/s12936-024-04961-8

---

## License

Distributed under the **MIT License**. See [LICENSE](LICENSE) for details.

---

## Contributing

Contributions, issues and feature requests are welcome!  
Feel free to check [issues page](https://github.com/username/HmtG-PacBio-Pipeline/issues).

1. Fork the project  
2. Create your feature branch (`git checkout -b feature/YourFeature`)  
3. Commit your changes (`git commit -m 'Add some feature'`)  
4. Push to the branch (`git push origin feature/YourFeature`)  
5. Open a Pull Request  

---

*Happy genotyping!*

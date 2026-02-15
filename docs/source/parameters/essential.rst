Essential parameters
====================

These are the parameters most users will care about.

Input
-----

- ``input_fastq``: input FASTQ file (``.fastq/.fq``, optionally gzipped)

Output naming
-------------

- ``--outdir``: output directory (default: current directory)
- ``-o / --outprefix``: output prefix / sample name (default: input basename)

Read filtering / subsampling
----------------------------

- ``--min-meanq``: minimum mean Q-score per read (default: 30)
- ``--sample``: number of reads to subsample after filtering (default: 5000)
- ``--seed``: random seed (default: 420)

Alignment (MAFFT)
-----------------

- ``--mafft``: path to MAFFT executable (default: ``mafft``)
- ``--threads``: MAFFT thread count (default: 30)

Reproducibility
---------------

- ``--force``: ignore existing intermediate files and recompute (default: off)


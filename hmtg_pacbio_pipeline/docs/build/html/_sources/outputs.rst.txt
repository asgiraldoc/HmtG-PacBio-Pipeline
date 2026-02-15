Outputs
=======

The pipeline writes files using a common prefix (sample name). The prefix is either:

- ``-o/--outprefix`` (if provided), or
- derived from the input filename (basename without extensions)

Main report artifacts
---------------------

- ``<prefix>_report.pdf``
- ``<prefix>_report.json``

Haplotype FASTA outputs
-----------------------

Common FASTA outputs include:

- ``<prefix>_cluster.fasta`` — high-frequency haplotypes
- ``<prefix>_lowFreqHap.fasta`` — low-frequency haplotypes
- ``<prefix>_chimeraHap.fasta`` — suspected chimeras

BLAST output (optional)
-----------------------

If BLAST is available:

- ``<prefix>_blast.tsv``

Distances
---------

- ``<prefix>_hapDistances.tsv`` — all-vs-all haplotype distance matrix

Intermediate files
------------------

These are useful for debugging and reproducibility:

- ``<prefix>_subsample.fastq``
- ``<prefix>_subsample.fasta``
- ``<prefix>_mafftRaw.fasta``
- ``<prefix>_mafft.log``


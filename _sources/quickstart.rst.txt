Quick Start
===========

This is the minimal end-to-end run.

1) Make sure MAFFT works
------------------------

From a terminal:

.. code-block:: bash

   mafft --help

If MAFFT is not on your PATH, note the full path to the executable (or to ``mafft.bat`` on Windows).

2) Run the pipeline (CLI)
-------------------------

From the pipeline folder:

.. code-block:: bash

   python HmtG-PacBio.py your_reads.fastq.gz

To control output location + prefix:

.. code-block:: bash

   python HmtG-PacBio.py your_reads.fastq.gz --outdir results -o SampleA

3) Inspect outputs
------------------

In ``results/`` you should see:

- ``SampleA_report.pdf`` and ``SampleA_report.json``
- intermediate files (subsampled FASTQ/FASTA, MAFFT MSA)
- haplotype FASTA files and distance tables

See :doc:`outputs` for a detailed description.

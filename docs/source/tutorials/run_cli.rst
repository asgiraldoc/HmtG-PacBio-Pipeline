Run from the CLI
================

Basic run
---------

.. code-block:: bash

   python HmtG-PacBio.py reads.fastq.gz

Choose output folder + sample name
----------------------------------

.. code-block:: bash

   python HmtG-PacBio.py reads.fastq.gz --outdir results -o Sample01

Quality filter + subsampling
----------------------------

The first stage filters reads by **mean Q-score** and then randomly subsamples.

Common knobs:

- ``--min-meanq`` (default: 30)
- ``--sample`` (default: 5000)
- ``--seed`` (default: 420)

Example:

.. code-block:: bash

   python HmtG-PacBio.py reads.fastq.gz --min-meanq 30 --sample 8000 --seed 123 -o Sample01 --outdir results

MAFFT settings
--------------

The pipeline runs MAFFT with orientation adjustment enabled.

- ``--threads`` (default: 30)
- ``--mafft`` (default: ``mafft``)

Example (explicit MAFFT path):

.. code-block:: bash

   python HmtG-PacBio.py reads.fastq.gz --mafft /usr/local/bin/mafft --threads 8 -o Sample01 --outdir results

Re-running / overwriting
------------------------

By default, intermediate files are re-used if present.

To force regeneration:

.. code-block:: bash

   python HmtG-PacBio.py reads.fastq.gz --force -o Sample01 --outdir results


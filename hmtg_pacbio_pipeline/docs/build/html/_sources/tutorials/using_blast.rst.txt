Using local BLAST
=================

What BLAST is used for (in this workflow)
-----------------------------------------

BLAST is optional and is used as an *exploration tool*:

- For each inferred haplotype, the pipeline can query a **local** nucleotide BLAST database.
- Results are summarized in ``<prefix>_blast.tsv`` and optionally included in the PDF report.

.. warning::

   BLAST hits are **not** treated as an automatic species identification criterion.
   They are intended to help you compare haplotypes to your own curated reference set.

Install BLAST+
--------------

You need the BLAST+ executables, typically:

- ``blastn``
- ``makeblastdb`` (only required if you need to build a DB from FASTA)

Prepare a database
------------------

If you already have a formatted BLAST DB, place it in:

.. code-block:: text

   blast/HmtG_database_PacBio.*

If you want to build a DB from a FASTA file:

.. code-block:: bash

   makeblastdb -in HmtG_database_PacBio.fasta -dbtype nucl -out blast/HmtG_database_PacBio

Run and verify
--------------

After a run, look for:

- ``<prefix>_blast.tsv``

If the file is missing, check :doc:`../faq` (common causes: BLAST not found, DB prefix incorrect).

Introduction
============

What is this pipeline?
----------------------

The **Haemo Mito Pipeline** is a small, practical workflow developed by the
**Escalante–Pacheco Lab (Temple University)** to turn **long-read amplicon data**
(targeting a ~6 kb haemosporidian mitochondrial genome region) into:

- A curated set of mitochondrial **haplotypes** (FASTA)
- Summary tables (TSV)
- A human-readable **PDF report**
- A machine-readable **JSON report**

The workflow follows the general strategy described in our published PacBio HiFi protocol
and its companion HmtG-PacBio-style analysis approach.

What it is *not*
----------------

- It is **not** a diagnostic assay.
- It is **not** a full metagenomic assembler.
- It does not attempt to delimit species automatically based on BLAST hits.

Instead, the idea is to provide a reproducible way to explore mixed infections / co-infections
and to compare recovered haplotypes to a user-managed reference set.

Inputs and outputs at a glance
------------------------------

**Input**

- FASTQ (optionally gzipped)

**Outputs (prefix-based)**

- ``<prefix>_report.pdf`` and ``<prefix>_report.json``
- Haplotype FASTA outputs (high-frequency, low-frequency, chimeras)
- Optional ``<prefix>_blast.tsv`` if BLAST is available
- ``<prefix>_hapDistances.tsv`` all-vs-all distances

See :doc:`outputs` for details.

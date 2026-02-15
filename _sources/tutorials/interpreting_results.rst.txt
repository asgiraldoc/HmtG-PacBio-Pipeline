Interpreting results
====================

The PDF report
--------------

The report is intended to be read quickly:

- A summary of read filtering / subsampling
- A view of haplotype clustering / OTUs
- Optional BLAST tables (if enabled and available)
- A haplotype distance matrix summary

If a figure is missing in the PDF, see :doc:`../faq` (common causes: missing matplotlib/Pillow,
or a plotting backend issue on headless systems).

FASTA outputs
-------------

Typical FASTA outputs include:

- high-frequency haplotypes
- low-frequency haplotypes
- suspected chimeras

The exact filenames are documented in :doc:`../outputs`.

JSON report
-----------

The JSON report mirrors the PDF in machine-readable form:

- run configuration (parameters)
- read statistics
- haplotype/cluster summaries
- file paths for generated artifacts

This is useful if you want to post-process results in R/Python.


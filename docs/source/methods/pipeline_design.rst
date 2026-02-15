Pipeline design
===============

This page describes the computational logic at a conceptual level.

Key components
--------------

The published HmtG-PacBio pipeline concept combines:

- Multiple sequence alignment (MSA) to place reads into a comparable coordinate system
- A machine-learning representation step (modified variational autoencoders)
- Density-based clustering (DBSCAN) to group reads into OTUs / haplotypes

The implementation in this repository follows that spirit, with a pragmatic script-first structure.

Step-by-step (conceptual)
-------------------------

1. **Read QC + subsampling**
   - Filter reads by mean Q score
   - Randomly subsample a fixed number of reads (to keep runtimes predictable)

2. **MSA**
   - Convert subsampled reads to FASTA
   - Run MAFFT with nucleotide orientation adjustment enabled
   - Save the raw MSA for auditability

3. **Haplotype inference**
   - Transform aligned reads into a feature representation
   - Cluster reads into OTUs/haplotypes
   - Summarize each haplotype and write FASTA outputs

4. **Optional: local BLAST**
   - If BLAST+ + database are present, search haplotypes against the local reference set
   - Include results in the PDF/JSON report

5. **Distance matrix**
   - Compute all-vs-all distances between inferred haplotypes
   - Write a TSV table (and summarize in the PDF)

Why the pipeline is structured this way
---------------------------------------

- Long reads that span the full amplicon reduce the need for assembly and help avoid chimeric consensus artifacts.
- Subsampling makes it feasible to run many samples and still get informative haplotype sets.
- A local reference DB keeps control in the researcher's hands (you can include unpublished or curated sequences).


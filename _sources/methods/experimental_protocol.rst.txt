Experimental protocol context
=============================

This documentation summarizes (at a high level) the experimental workflow described in our protocol paper:

- Pacheco *et al.* (2024), *Malaria Journal* — PacBio HiFi long-amplicon mt-genome protocol for haemosporidian parasites.

For full wet-lab details, always refer to the published protocol.

Target region
-------------

The protocol targets a long amplicon (~6 kb), covering close to the full length
of the haemosporidian mitochondrial genome.

Primer design and multiplexing strategy
---------------------------------------

The protocol builds on previously reported primers (AE170 / AE171) and extends them with
sample barcoding so many specimens can be multiplexed in one sequencing run.

Target-specific primer sequences (as reported):

- Forward (AE170-derived): ``GAT TCT CTC CAC ACT TCA ATT CGT ACT TC``
- Reverse (AE171-derived): ``GAA AAT WAT AGA CCG AAC CTT GGA CTC`` (W = A/T)

Barcoding scheme (summary):

- Each oligo includes a short 5′ buffer sequence, a 16 bp barcode, and the target-specific primer sequence.
- The paper describes 8 forward and 24 reverse barcoded oligos (32 total),
  enabling up to 192 asymmetric barcode pairs (8×24).

Practical primer notes from the protocol:

- Oligos were ordered with 5′ phosphates and HPLC purification.
- In our tests, the primer set amplified diverse haemosporidian taxa (e.g., *Plasmodium*,
  *Haemoproteus*, *Leucocytozoon*) and did not show obvious genus-specific amplification bias.

PCR overview (summary)
----------------------

The protocol describes long-amplicon PCR with a long extension time to capture the ~6 kb product.
A typical cycling scheme in the paper includes:

- Initial denaturation (~94°C)
- ~30 cycles with a short denaturation and long extension (~7 minutes)
- Final extension (~72°C)

Amplicons are visualized on agarose gels, and gel purification is described as optional but recommended
for cleaner library preparation.

Sequencing
----------

Amplicons are prepared for PacBio HiFi sequencing (SMRTbell library prep) and sequenced to yield
high-accuracy reads whose length distribution matches the expected amplicon size.

Recommended coverage (rule of thumb)
------------------------------------

The protocol reports low per-read error rates and recommends ~30× coverage per haplotype as a minimum,
consistent with the observed error rates in our study.

How this relates to the software
--------------------------------

The software pipeline is designed to:

- Filter reads (quality thresholding)
- Align reads to a common coordinate system (MSA)
- Infer haplotypes / OTUs from the aligned reads
- Optionally compare haplotypes to a curated local reference set (BLAST)

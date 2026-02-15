Optional parameters
===================

BLAST integration (optional)
----------------------------

If BLAST+ and a local database are available, the pipeline can include BLAST hit tables
in the report and write a ``*_blast.tsv`` file.

See :doc:`../tutorials/using_blast`.

Primer trimming/orientation
---------------------------

The current workflow relies on MAFFT's orientation adjustment. Primer trimming and
explicit orientation checks may exist as CLI/GUI arguments for future work, but are not
required for the current default path.

Advanced GUI-only toggles
-------------------------

Depending on the desktop wrapper you use, you may also see options like:

- "Create timestamped run folder"
- "Save intermediate files"
- "Force rerun"

These do not change the underlying scientific pipeline logic; they control file management
and reproducibility behavior.


FAQ / Troubleshooting
=====================

MAFFT failed (return code 1) on Windows
---------------------------------------

Most often this happens when:

- You copied only ``mafft.bat`` but not the full MAFFT distribution folder, or
- The GUI/runner is pointing to the wrong file.

Fix:

1. Use the full MAFFT Windows distribution folder.
2. Point the pipeline to the launcher (often ``mafft.bat``) in the GUI Advanced panel or via ``--mafft``.

BLAST table is missing
----------------------

The pipeline will only write ``*_blast.tsv`` if:

- ``blastn`` is discoverable, and
- the database prefix points to a formatted nucleotide database

Double-check:

- ``blast/HmtG_database_PacBio.nsq`` (and siblings) exist
- You are using the *prefix* (no file extension)

The PDF report is missing a figure
----------------------------------

Common causes:

- ``matplotlib`` or ``Pillow`` is missing
- Matplotlib backend issues on some systems (e.g., headless runs)

Fix:

- Ensure dependencies are installed (``pip install matplotlib pillow``)
- Try setting a headless-safe backend before running:

  - Linux/macOS:

    .. code-block:: bash

       export MPLBACKEND=Agg

  - Windows (CMD):

    .. code-block:: bat

       set MPLBACKEND=Agg

Where are my intermediate files?
--------------------------------

By design, the pipeline writes intermediate files alongside final outputs using the same prefix.
These include the subsample FASTQ/FASTA and the raw MAFFT alignment.

If you are using a GUI wrapper that creates timestamped run folders, check inside the run folder.

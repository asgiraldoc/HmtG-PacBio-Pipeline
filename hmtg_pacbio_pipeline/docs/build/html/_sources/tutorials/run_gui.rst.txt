Run from the GUI
================

Download the latest desktop GUI build (Windows or macOS) from :doc:`../downloads`.

A lightweight desktop GUI wraps the same pipeline logic with a simple form.

Basic panel
-----------

- **Input FASTQ**: your reads file (gzipped is OK)
- **Output folder**: where a run folder will be created
- **Output prefix**: sample name (defaults to input basename)
- **MAFFT threads**: how many CPU threads MAFFT can use

Advanced panel (collapsible)
----------------------------

The advanced panel exposes options that are useful for power users, but not required
for most runs:

- Subsample size
- Minimum mean Q
- Random seed
- Override MAFFT executable (useful on Windows when MAFFT is a ``.bat``)
- Toggle BLAST integration (if BLAST+ + DB are available)
- Force re-run / ignore existing intermediates

Recommended folder layout (project-local tools)
-----------------------------------

Place third-party tools under a project-local ``bin/`` folder:

.. code-block:: text

   bin/
     # Windows
     mafft-win/mafft.bat
     blastn.exe
     makeblastdb.exe

     # macOS (either system-installed tools OR local binaries)
     mafft-mac/mafft.bat
     blastn
     makeblastdb

And your reference DB under:

.. code-block:: text

   blast/
     HmtG_database_PacBio.*

The GUI can auto-detect these paths if you keep this layout.

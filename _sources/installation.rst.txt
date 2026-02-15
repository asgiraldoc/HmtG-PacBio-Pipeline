Installation
============

Requirements
------------

- Python 3.9+ (3.10/3.11 recommended)
- MAFFT (multiple sequence alignment)
- Optional: BLAST+ (``blastn`` and a nucleotide database)

Python dependencies (core)
--------------------------

The haplotyping/report stage uses common scientific Python packages, e.g.:

- biopython
- numpy
- scikit-learn
- reportlab
- matplotlib (for plots inside the PDF report)

If you are running from the "script-first" pipeline, install dependencies using:

.. code-block:: bash

   pip install -r requirements.txt

MAFFT
-----

MAFFT must be available as an executable. The pipeline calls it via ``subprocess``.

MAFFT provides pre-compiled packages for macOS and Windows, including a signed macOS installer (pkg) and a portable macOS package.

- On Linux/macOS, MAFFT is usually installed via the system package manager or conda.
- On Windows, the MAFFT distribution commonly provides a ``mafft.bat`` launcher.

If MAFFT is not on your PATH, point the pipeline to it using the ``--mafft`` argument
(or select it in the GUI's Advanced section).

BLAST (optional)
----------------

If BLAST+ is installed and a local nucleotide database is available, the report can include BLAST tables
for inferred haplotypes.

Recommended structure (relative to the project root):

.. code-block:: text

   blast/
     HmtG_database_PacBio.nsq
     HmtG_database_PacBio.nin
     HmtG_database_PacBio.nhr
     ...

The pipeline expects the database *prefix*:

.. code-block:: text

   blast/HmtG_database_PacBio

Build the docs locally (this website)
-------------------------------------

To preview this documentation site locally:

.. code-block:: bash

   python -m venv .venv
   # Windows (PowerShell): .venv\Scripts\Activate.ps1
   # Git Bash: source .venv/Scripts/activate

   python -m pip install -r docs/requirements.txt
   python -m sphinx -b html docs/source docs/build/html

Then open ``docs/build/html/index.html``.

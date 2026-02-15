Downloads
=========

The Haemo Mito Pipeline can be used in two ways:

1. **Windows Desktop GUI** (recommended for day-to-day use)
2. **Command-line workflow** (recommended for automation and reproducibility)

Windows Desktop GUI
-------------------

We distribute the Windows GUI as a bundled application so users do **not** need to install Python.

**Recommended distribution method:** publish the build as a **GitHub Release asset**.

.. raw:: html

   <div class="lab-cta">
     <a class="primary" href="https://github.com/<GITHUB_ORG_OR_USER>/<REPO_NAME>/releases/latest" target="_blank" rel="noopener">Go to latest release</a>
     <a class="ghost" href="https://github.com/<GITHUB_ORG_OR_USER>/<REPO_NAME>/releases" target="_blank" rel="noopener">All releases</a>
   </div>

When you create a release, we recommend attaching a single ZIP named like:

- ``HaemoMitoPipeline_Windows.zip``

That ZIP should contain the full ``dist/HaemoMitoPipeline/`` folder produced by PyInstaller
(not just the ``.exe``).


macOS Desktop GUI
----------------

We also support a macOS desktop GUI build (a standard ``.app`` bundle).

**Recommended distribution method:** publish the build as a **GitHub Release asset**,
similar to the Windows build.

.. raw:: html

   <div class="lab-cta">
     <a class="primary" href="https://github.com/<GITHUB_ORG_OR_USER>/<REPO_NAME>/releases/latest" target="_blank" rel="noopener">Go to latest release</a>
     <a class="ghost" href="https://github.com/<GITHUB_ORG_OR_USER>/<REPO_NAME>/releases" target="_blank" rel="noopener">All releases</a>
   </div>

When you create a release, we recommend attaching a single ZIP named like:

- ``HaemoMitoPipeline_macOS.zip``

That ZIP should contain the full ``dist/HaemoMitoPipeline/HaemoMitoPipeline.app`` bundle
produced by PyInstaller.

.. note::

   macOS may block unsigned apps. Users can usually run the app by
   right-clicking the ``.app`` → **Open** (Gatekeeper prompt).

CLI workflow
------------

For CLI usage (or to build your own GUI executable), clone the repository and install dependencies.
The CLI is also ideal for running on HPC/servers.

See:

- :doc:`installation`
- :doc:`tutorials/run_cli`

Data + database downloads
-------------------------

If you distribute a curated BLAST database (``blast/HmtG_database_PacBio``), we strongly recommend
shipping it as a separate release asset:

- it can be updated independently of the GUI
- it can be large

Tip: the pipeline expects a **database prefix** (no extension), e.g. ``blast/HmtG_database_PacBio``.

Update these placeholders
------------------------

This documentation template ships with placeholder URLs:

- ``https://github.com/<GITHUB_ORG_OR_USER>/<REPO_NAME>``

After you publish the repo, replace those placeholders with your real GitHub organization/user and repo name.

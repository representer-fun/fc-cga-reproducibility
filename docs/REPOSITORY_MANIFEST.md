# Repository Manifest

This repository is organized as a research artifact for writing a CIKM full
paper, not as a raw-data archive.

## Tracked In Git

- Experiment source code and run scripts.
- Progress/status scripts.
- Compact CSV and Markdown result summaries.
- Paper-facing tables, figures, and writing notes.
- The curated `final_paper_package/` folder.

## Intentionally Not Tracked

- Raw datasets under `data/raw/`.
- Processed feature caches under `data/processed/`.
- Downloaded external repositories under `external/`.
- Large run logs, prediction archives, and model outputs under `runs/`.
- Binary model/cache artifacts such as `*.npz`, `*.parquet`, `*.joblib`, and
  `*.pkl`.

## Why

The completed workspace is several gigabytes. The GitHub repository should stay
usable as a paper and code artifact. Reproduction instructions in
`final_paper_package/REPRODUCIBILITY_AND_COMMANDS.md` describe how the final
suite was run on the 16 vCPU, 120 GB RAM machine.

Large generated artifacts that are useful for reproduction are stored as GitHub
Release assets instead of normal git files:

- <https://github.com/representer-fun/fc-cga-reproducibility>

The release includes processed feature caches and split run-artifact zip parts,
but not raw datasets or trained model objects.

## Start Here

1. Read `jumpoff.md`.
2. Read `final_paper_package/README.md`.
3. Write from `final_paper_package/PAPER_OUTLINE.md`.
4. Use `final_paper_package/RESULTS_AT_A_GLANCE.md` for the abstract and main
   result narrative.
5. Use `final_paper_package/TABLE_CAPTIONS.md` when converting Markdown tables
   into LaTeX.

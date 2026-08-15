# Changelog

All notable changes to this repository are recorded here, using the vocabulary
this repo already uses for OpenSpec deltas: `ADDED`, `MODIFIED`, and `REMOVED`.
Breaking `MODIFIED` entries are marked **BREAKING**.

The repo carries a single, unified version for both `frontend` and `backend`,
tracked in the root `VERSION` file. See `AGENTS.md` for the classification and
exemption rules, and `openspec/changes/add-changelog-semver-versioning/` for
the design behind this process.

## Unreleased

### ADDED

- Published documentation site (mkdocs + Material for MkDocs), deployed to GitHub Pages on
  every push to `main`, covering getting started, project structure, adding features, testing,
  tech stack, configuration, deployment, API client codegen, and troubleshooting.

### MODIFIED

- **BREAKING**: `README.md` is trimmed to the project pitch, prerequisites, "Use this template"
  steps, and a quickstart, linking out to the documentation site for everything else. Anyone
  deep-linking to a specific README section/anchor that moved should update the link to the
  corresponding docs site page.

### REMOVED

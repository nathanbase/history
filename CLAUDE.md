# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

A novelty repo that generates 3,745 backdated git commits (2013–2026) with satirical commit messages to paint a GitHub contribution heatmap. The commit messages chronicle tech industry trends across eras (jQuery, Angular, React, Microservices, COVID, AI Hype, Vibe Coding). None of the generated source files contain real code — they're stubs with era-appropriate comments.

## The Only Real Code

`generate_history.py` is the entire project. It:
- Defines 7 tech eras with era-specific commit message templates
- Uses a probabilistic model for realistic activity patterns (weekday bias, vacation gaps, sprint bursts, burnout dips)
- Manages a simulated file system where files appear in era-appropriate years (e.g., `ai.js` in 2022, `vibes.js` in 2024)
- Creates backdated commits using `GIT_AUTHOR_DATE` / `GIT_COMMITTER_DATE` env vars

Run it with: `python generate_history.py` (uses SEED=42, outputs to local git repo)

## Pushing to GitHub

GitHub's contribution indexer can't process thousands of backdated commits in a single force push. Push incrementally by year with ~10s delays between pushes. See git log for year-end commit SHAs.

## Branch Convention

Default branch is `master` (not `main`).

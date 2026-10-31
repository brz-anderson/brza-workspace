---
name: shared-spec-files-do-not-run
description: "In brza-studio, src/shared/**/*.spec.ts are neither run by vitest nor typechecked; put new tests in .test.ts"
metadata:
  node_type: memory
  type: project
  originSessionId: 7f713049-9bdf-4161-8e35-632159d1ce0b
  modified: 2026-10-30T23:11:52.527Z
---

In `brza-studio`, `src/shared/**/*.spec.ts` files are dead: vitest's `UNIT_INCLUDE` (`config/scripts/ci-unit-files.mjs`) only matches `*.test.ts(x)`, and `config/tsconfig.tc.*.json` excludes them.

**Why:** found on 2026-10-29 in PLN-001/P66 (X45): a failing test added to `native-chat-reasoning-row.spec.ts` never ran.

**How to apply:** add new tests to a sibling `*.test.ts`, even when a `.spec.ts` for the module exists. Related: [[worktree-node-modules-no-symlink]].

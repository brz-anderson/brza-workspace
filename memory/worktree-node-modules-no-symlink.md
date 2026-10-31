---
name: worktree-node-modules-no-symlink
description: "In brza-studio worktrees, never symlink node_modules to the root's; run pnpm install --offline in the worktree instead"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 238492bc-7887-4523-9e28-a65d27ad654f
  modified: 2026-10-28T02:10:23.390Z
---

In a `brza-studio` worktree (`.worktrees/<name>`), never make `node_modules` a symlink to the root checkout's.

**Why:** on 2026-10-27 a `pnpm` script run in a worktree whose `node_modules` was a symlink triggered pnpm's pre-script install (`verifyDepsBeforeRun`). That install wrote relative links computed from the worktree, which is two levels deeper, into the root `node_modules`. The root then pointed at `/Library/pnpm` instead of `~/Library/pnpm`, which broke the `brza-studio-rebrand` session's checkout until it reinstalled. The symlink also makes Vite deny the `onig.wasm` load ("Denied ID") and stops typecheck from finding `tsrs`/`typescript`.

**How to apply:** in a new worktree, run `pnpm install --offline --frozen-lockfile` there; the global virtual store makes it take under a second. `pnpm` lives at `~/.npm/_npx/aa4546e781591cea/node_modules/.bin`.

# Version Control Workflow

## Branching Model
- `main` — stable, always-deployable code
- `develop` — integration branch for completed features
- `feature/*` — one branch per feature, created off `develop`

## Commit Message Convention
| Prefix | Meaning |
|---|---|
| feat: | new functionality |
| fix: | bug correction |
| docs: | documentation changes |
| chore: | tooling/config changes |
| refactor: | code change, no behavior change |

## Conflict Resolution Steps
1. Identify conflicting files after `git merge`
2. Open file, locate `<<<<<<<`, `=======`, `>>>>>>>` markers
3. Manually combine or choose the correct version
4. Remove all conflict markers
5. `git add <file>`
6. `git commit` to finalize the merge
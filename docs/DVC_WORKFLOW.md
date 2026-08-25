# DVC Workflow — mlops-iris-classifier

## Remote Configuration
- Remote name: `myremote`
- Type: local folder (simulates cloud storage for this lab)
- Location: `~/dvc-remote-storage`
- Configured as default remote (`-d` flag)

## Standard Workflow for Every Data Change
1. `dvc add <file>` — track/update the dataset, generates a `.dvc` pointer file
2. `git add <file>.dvc` — stage the pointer file (not the data itself)
3. `git commit -m "..."` — commit the pointer, creating a new dataset version in Git history
4. `dvc push` — upload the actual data object to the remote

## Comparing & Restoring Versions
- `git log --oneline -- <file>.dvc` — view all versions of a dataset
- `dvc diff <commit>` — compare current data against a past commit
- `git show <commit>:<file>.dvc` — inspect the hash/size recorded at a specific commit
- To restore an old version:
  1. `git checkout <commit> -- <file>.dvc` (restores the pointer only)
  2. `dvc checkout <file>.dvc` (restores the actual data to match)

## Versions Tracked in This Experiment
| Version | Commit | Rows | MD5 Hash |
|---|---|---|---|
| v1 | f19aec6 | 150 | 21d441a2... |
| v2 | 68bf305 | 170 | 674c8c36... |
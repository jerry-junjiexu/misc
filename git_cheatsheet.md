# Personal git cheat sheet

## g4 patch
- create new branch
  ```
  git checkout -b dest_branch
  git push
  ```
- find merge base
  ```
  git merge-base master source_branch
  ```
- finding commit hashes
  ```
  git log --oneline merge_base..source_branch
  ```
- patch into new branch
  ```
  git cherry-pick commit_hash
  ```
  

from git import Repo

repo_url = 'https://github.com/bhargavvermareddy/temp1.git'
repo_dir = 'gitclones/temp1'

Repo.clone_from(repo_url, repo_dir)


repo = Repo('gitclones/temp1')
print(repo.active_branch.name)

remote = repo.remote(name='origin')
remote.fetch()

# local
# local_branches = sorted(repo.branches, key=lambda b: b.commit.committed_datetime)

# remote
remote_branches = sorted(
    remote.refs, key=lambda b: b.commit.committed_datetime)
# print(remote_branches)
latest_branch = remote_branches[-1]

branch_name = latest_branch.name
final_branch_name = branch_name.replace('origin/', '')

repo.git.checkout(final_branch_name)
# print(repo.active_branch.name)

# branch = repo.heads[repo.active_branch.name]
new_branch = repo.create_head(
    'feature/XY-adding-helm-charts')
new_branch.checkout()

print(repo.active_branch.name)

import os
import json
import shutil
from git import Repo

path = 'clonedrepos'
jenkins_directory = 'jenkins'
docker_filename = 'Dockerfile'
entrypoint_file = 'entrypoint.sh'
httpdconf_file = 'httpd.conf'

npm_source = 'dockfile/npm'
npm_dockerfile = 'dockfile/npm/Dockerfile'
npm_entrypoint = 'dockfile/npm/entrypoint.sh'
npm_httpdconf = 'dockfile/npm/httpd.conf'
npm_helm = 'helmchart/npm-helm'

spring_source = 'dockfile/spring'
spring_dockerfile = 'dockfile/spring/Dockerfile'
spring_entrypoint = 'dockfile/spring/entrypoint.sh'
spring_helm = 'helmchart/spring-helm'

configs_dir = 'configs'


def get_release_branches():
    repo = Repo(repo_dir)
    remote = repo.remote(name='origin')
    remote.fetch()
    branches = [x for x in remote.refs if 'release/v' in x.name]
    return branches


def get_latest_commit(branch):
    repo = Repo(repo_dir)
    commit = repo.commit(branch)
    return commit.committed_date


def sort_branches():
    branches = get_release_branches()
    sorted_branches = sorted(branches, key=get_latest_commit, reverse=True)
    return sorted_branches


# get the latest release branch name
latest_rel_branch = sort_branches()[0].name.replace('origin/', '')
# latest_rel_branch = rel_branch.replace()

# clone the repos
with open('repolist.txt', 'r') as f:
    data = f.read()
    for each_repo in data:
        # repo_url = 'https://github.com/bhargavvermareddy/temp1.git'
        repo_dir = f'gitclones/{each_repo}'
        Repo.clone_from(each_repo, repo_dir)
        repo = Repo(f'gitclones/{each_repo}')
        print(
            f'Current Active Branch in {each_repo} is: {repo.active_branch.name}')
        remote = repo.remote(name='origin')
        remote.fetch()
        # check out the latest release branch
        repo.git.checkout(latest_rel_branch)
        new_feature_branch = repo.create_head('feature/adding-helm-charts')
        new_feature_branch.checkout()
        print(
            f'Current Active Branch post checkout in {each_repo} is: {repo.active_branch.name}')

# print(repo.active_branch.name)

directories = [d for d in os.listdir(
    path) if os.path.isdir(os.path.join(path, d))]

print(directories)

for each in directories:
    # checking whether jenkins folder exists in each directory
    repo_path = f"{path}/{each}"
    print(f"Target repo path: {repo_path}")
    if os.path.isdir(os.path.join(f"{repo_path}", jenkins_directory)):
        print(f'{jenkins_directory} exists in {repo_path}')
        with open(f"{repo_path}/jenkins/pipeline_config.json", 'r') as file:
            data = json.load(file)
            # print(data)
            print(data["appType"])
            # checking the service type (spring or npm)
            if(data["appType"] == "spring"):
                print("spring app")
                # copying spring helmchart
                print("copying spring_helm")
                shutil.copytree(
                    spring_helm, f"{repo_path}/helm", dirs_exist_ok=True)
                # checking whether Dockerfile exists or not
                if os.path.isfile(os.path.join(repo_path, docker_filename)):
                    print(f'{docker_filename} exists in {repo_path}')
                    shutil.copy(spring_entrypoint, repo_path)
                else:
                    print(f'{docker_filename} does not exist in {repo_path}')
                    shutil.copy(spring_dockerfile, repo_path)
                # checking whether etnrypoint.sh exists or not
                if os.path.isfile(os.path.join(repo_path, entrypoint_file)):
                    print(f'{entrypoint_file} exists in {repo_path}')
                else:
                    print(f'{entrypoint_file} does not exist in {repo_path}')
                    shutil.copy(spring_entrypoint, repo_path)
                # copying env config yaml files to resources directory
                # this is only applicable for spring apps
                shutil.copytree(f"{configs_dir}/{each}/",
                                f"{repo_path}/src/main/resources/", dirs_exist_ok=True)
            elif(data["appType"] == "npm"):
                print("npm app")
                # copying spring helmchart
                print("copying npm_helm")
                shutil.copytree(
                    npm_helm, f"{repo_path}/helm", dirs_exist_ok=True)
                # checking whether Dockerfile exists or not
                if os.path.isfile(os.path.join(repo_path, docker_filename)):
                    print(f'{docker_filename} exists in {repo_path}')
                else:
                    print(f'{docker_filename} does not exist in {repo_path}')
                    shutil.copy(npm_dockerfile, repo_path)
                # checking whether entrypoint.sh exists or not
                if os.path.isfile(os.path.join(repo_path, entrypoint_file)):
                    print(f'{entrypoint_file} exists in {repo_path}')
                else:
                    print(f'{entrypoint_file} does not exist in {repo_path}')
                    shutil.copy(npm_entrypoint, repo_path)
                # checking whether httpd.conf exists or not
                if os.path.isfile(os.path.join(repo_path, httpdconf_file)):
                    print(f'{httpdconf_file} exists in {repo_path}')
                else:
                    print(f'{httpdconf_file} does not exist in {repo_path}')
                    shutil.copy(npm_httpdconf, repo_path)
            else:
                pass
    else:
        print(f'{jenkins_directory} does not exist in {repo_path}')

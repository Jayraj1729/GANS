import subprocess
import os

def scan_repository(access_token, repo_url):
    repo_name = repo_url.split('/')[-1]
    repo_dir = 'repos/' + repo_name.split('.')[0]
    if not os.path.exists(repo_dir):
        subprocess.run(['git', 'clone', '--quiet', '--depth=1', '--branch=master', f'{repo_url}.git', repo_dir], check=True, env={'GIT_TERMINAL_PROMPT': '0', 'GITHUB_TOKEN': access_token})
    else:
        subprocess.run(['git', '-C', repo_dir, 'pull', '--quiet'], check=True, env={'GIT_TERMINAL_PROMPT': '0', 'GITHUB_TOKEN': access_token})
    scan_results = {}
    subprocess.run(['npm', 'install', '-g', 'snyk'])
    snyk_result = subprocess.run(['snyk', 'test', '--json', '--file=' + repo_dir + '/package.json'], capture_output=True, text=True)
    scan_results['snyk'] = snyk_result.stdout
    subprocess.run(['npm', 'uninstall', '-g', 'snyk'])
    return scan_results

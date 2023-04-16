import subprocess
import os

def scan_repository(repo_url):
    repo_dir = 'repos/' + repo_url.split('/')[-1].split('.')[0]
    if not os.path.exists(repo_dir):
        os.makedirs(repo_dir)
        subprocess.run(['git', 'clone', repo_url, repo_dir])
    else:
        subprocess.run(['git', '-C', repo_dir, 'pull'])
    scan_results = {}
    subprocess.run(['npm', 'install', '-g', 'snyk'])
    snyk_result = subprocess.run(['snyk', 'test', '--json', '--file=' + repo_dir + '/package.json'], capture_output=True, text=True)
    scan_results['snyk'] = snyk_result.stdout
    subprocess.run(['npm', 'uninstall', '-g', 'snyk'])
    return scan_results

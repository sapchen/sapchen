#!/usr/bin/env python3
import requests
import sys

def get_total_stars(username):
    total_stars = 0
    page = 1
    
    while True:
        url = f'https://api.github.com/users/{username}/repos?page={page}&per_page=100'
        response = requests.get(url)
        
        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            sys.exit(1)
        
        repos = response.json()
        if not repos:
            break
            
        for repo in repos:
            total_stars += repo.get('stargazers_count', 0)
        
        page += 1
        if len(repos) < 100:  # 没有更多仓库了
            break
    
    return total_stars

if __name__ == "__main__":
    if len(sys.argv) > 1:
        username = sys.argv[1]
    else:
        # 如果没有提供用户名，可以从git配置中获取
        import subprocess
        result = subprocess.run(['git', 'config', 'user.name'], capture_output=True, text=True)
        username = result.stdout.strip()
    
    stars = get_total_stars(username)
    print(f"GitHub用户 {username} 的所有仓库共有 {stars} 个Star！")
    
    # 输出到文件，方便README引用
    with open('total_stars.txt', 'w') as f:
        f.write(str(stars))
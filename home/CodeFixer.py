import g4f
import subprocess
import os 
from datetime import datetime 
import shutil

class CodeFixer:
    def __init__(self):
        pass

    def clone_repo(self, github_repo):
        if os.path.exists("media"):
            prefix_path = "media/"
        elif os.path.exists("../media"):
            prefix_path = "../media/"

        if not os.path.exists(prefix_path+"GitHubRepos"):
            os.makedirs(prefix_path+"GitHubRepos")

        self.destination_dir = prefix_path + "GitHubRepos/" + github_repo.split("/")[-1]
        if not os.path.exists(self.destination_dir):
            try:
                subprocess.run(['git', 'clone', github_repo, self.destination_dir], check=True)
                print("Repository cloned successfully.")
            except subprocess.CalledProcessError as e:
                print(f"Error cloning repository: {e}")
        else:
            print("[*] Deleting old repo ...")
            shutil.rmtree(self.destination_dir)
            self.clone_repo(github_repo)

    def find_code_path(self):
        if os.path.exists(self.destination_dir + "/app.py"):
            return self.destination_dir + "/app.py"
        else:
            return ""
        
    def find_code(self, filepath):
        print("[*] Finding Vulnerable Code ...")
        with open(filepath) as f:
            code = f.read() 

        print("[+] Done")

        return code 

    def generate_response(self, code, vulnerability_name):
        print("[*] Generating Code ...")
        prompt = f"Fix this {vulnerability_name} vulnerability in this code & only write complete code without any explanation: ```{code}```"
        response = g4f.ChatCompletion.create(model="airoboros-70b", messages=[{"role": "user", "content": prompt}])
        print(response)
        response = "from flask" + response.split("from flask")[1].split("app.run(debug=True)")[0] + "app.run(debug=True)"
        print("[+] Fixed Code")
        return response
    
    def fix_code(self, filepath, fixed_code):
        print("[*] Fixing code ...")
        with open(filepath, "w") as f:
            f.write(fixed_code)
        print("[+] Done")

    def create_pull_request(self):
        try:
            os.chdir(self.destination_dir)
            
            # Generate a dynamic branch name based on current date/time
            branch_name = f"feature-branch-{datetime.now().strftime('%Y%m%d%H%M%S')}"
            
            # Check for unstaged changes
            status = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True)
            if status.stdout:
                print("Unstaged changes detected. Committing changes before creating pull request.")
                subprocess.run(['git', 'add', '.'])
                subprocess.run(['git', 'commit', '-m', 'Committing changes before creating pull request'])

            subprocess.run(['git', 'checkout', '-b', branch_name])
            subprocess.run(['git', 'push', 'origin', branch_name])
            
            # Create the pull request
            pull_request_command = [
                'git', 'pull-request', '--target-branch', 'main', '--title', 'Fix Vulnerable Code', '-R',
                '--message', 'Fix Vulnerable Code',
            ]
            subprocess.run(pull_request_command, check=True)
            print("[+] Pull request created successfully.")
            return True
        except subprocess.CalledProcessError as e:
            print(f"[-] Error creating pull request: {e}")
            return False

    def start(self, github_repo):
        self.clone_repo(github_repo)
        filepath = self.find_code_path()
        code = self.find_code(filepath)
        fixed_code = self.generate_response(code, "SQL Injection")
        self.fix_code(filepath, fixed_code)
        self.create_pull_request()

        # print("="*100)
        # print("Fixed Code")
        # print("="*100)
        # print(fixed_code)

if __name__ == "__main__":
    test = CodeFixer()
    test.start("https://github.com/PriyadarshiIndia/TestingWebsite") 
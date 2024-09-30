import random
import string 
import subprocess
import os, sys 
from urllib.parse import urlparse

class Recon:
    def get_domain_name(self, url):
        parsed_url = urlparse(url)
        domain = parsed_url.netloc
        if domain.startswith('www.'):
            domain = domain[4:]
        return domain

    def url_recon(self, domain):
        random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))

        if os.path.exists("media"):
            prefix_path = "media"
        elif os.path.exists("../media"):
            prefix_path = "../media"

        final_domain = self.get_domain_name(domain)

        # File paths
        urls_path = f"{prefix_path}/urls_{random_suffix}.txt"
        dynamic_path = f"{prefix_path}/dynamic_{random_suffix}.txt"
        get_params_path = f"{prefix_path}/get_params_{random_suffix}.txt"
        post_params_path = f"{prefix_path}/post_params_{random_suffix}.txt"

        try:
            # Command 1: Fetching all URLs of the target domain
            subprocess.run("echo '"+final_domain+"' | httpx -silent -nc | katana -u {} -silent -nc -o '"+urls_path+"' -c 100", shell=True, check=True)

            # Command 2: Removing static URLs
            subprocess.run(f"cat {urls_path} | uro -f keepcontent > {dynamic_path}", shell=True, check=True)

            # Command 3: Segregate GET Parameters URLs
            subprocess.run(f"grep '?' {dynamic_path} > {get_params_path}", shell=True, check=True)

            # Command 4: Segregate POST Parameters URLs
            subprocess.run(f"grep -v '?' {dynamic_path} > {post_params_path}", shell=True, check=True)
        except: pass 

        os.remove(urls_path)
        os.remove(dynamic_path)

        return get_params_path, post_params_path, random_suffix

# Example usage:
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: python {sys.argv[0]} http://testphp.vulnweb.com")
        sys.exit(1)

    url = sys.argv[1]
    recon = Recon()
    get_params_file, post_params_file, random_suffix = recon.url_recon(url)
    print("GET Parameters file path:", get_params_file)
    print("POST Parameters file path:", post_params_file)


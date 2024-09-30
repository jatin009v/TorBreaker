import os
import requests
import zipfile
from tqdm import tqdm
import csv
import json

class WhiteBox:
    def download_file(self, url, save_as):
        response = requests.get(url, stream=True)
        total_size = int(response.headers.get('content-length', 0))
        block_size = 1024
        progress_bar = tqdm(total=total_size, unit='B', unit_scale=True)
        with open(save_as, 'wb') as f:
            for data in response.iter_content(block_size):
                progress_bar.update(len(data))
                f.write(data)
        progress_bar.close()

    def extract_zip(self, zip_file, extract_to):
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            files = zip_ref.namelist()
            progress_bar = tqdm(total=len(files), desc="Extracting", unit='file')
            for file in files:
                zip_ref.extract(file, extract_to)
                progress_bar.update(1)
            progress_bar.close()

    def set_permissions(self, directory):
        for root, dirs, files in os.walk(directory):
            for d in dirs:
                os.chmod(os.path.join(root, d), 0o777)
            for f in files:
                os.chmod(os.path.join(root, f), 0o777)

    def setup_language_database(self):
        list_db = ['codeql/cpp-queries', 'codeql/csharp-queries', 'codeql/go-queries', 'codeql/java-queries', 'codeql/javascript-queries', 'codeql/python-queries', 'codeql/ruby-queries', 'codeql/swift-queries']
        for db in list_db:
            os.system(f"{codebase_path}/.model/codeql/codeql pack download {db}")
            print(f"Downloaded {db} database.")

    def setup_whitebox_model(self, codebase_path):
        # model_folder = os.path.join(os.path.dirname(codebase_path), '.model')
        model_folder = os.path.join(codebase_path, '.model')
        if not os.path.exists(model_folder):
            os.makedirs(model_folder)
            print("Created folder:", model_folder)
            zip_url = 'https://github.com/github/codeql-cli-binaries/releases/download/v2.17.2/codeql-linux64.zip'
            zip_file = os.path.join(model_folder, 'codeql-linux64.zip')
            self.download_file(zip_url, zip_file)
            print("Downloaded zip file.")
            self.extract_zip(zip_file, model_folder)
            print("Extracted zip file.")
            self.set_permissions(model_folder)
            print("Set permissions for all files in the folder.")
            self.setup_language_database()
            print("Downloaded language databases.")
        else:
            print("Folder", model_folder, "already exists. Doing nothing.")

    def create_codebase_database(self, language, codebase_path):
        os.system(f"{codebase_path}/.model/codeql/codeql database create {codebase_path}/.model/whitebox --language={language} --source-root={codebase_path}")
        print(f"Created database for {codebase_path} codebase.")

    def analyze_codebase(self, codebase_path):
        os.system(f"{codebase_path}/.model/codeql/codeql database analyze {codebase_path}/.model/whitebox/ --format=csv --output={codebase_path}/scanned_results.csv")
        print(f"Analyzed {codebase_path} codebase.")

    def convert_csv_to_json(self, csv_file):
        vulnerabilities = []

        with open(csv_file, 'r') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                vulnerability = {
                    "Vulnerability Name": row[0],
                    "Vulnerability Description": row[1],
                    "Severity": row[2],
                    "Message": row[3],
                    "Vulnerable File Path": row[4],
                    "Start Line": row[5],
                    "End Line": row[7]
                }
                vulnerabilities.append(vulnerability)

        return vulnerabilities

    def whitebox_analysis_output(self, codebase_path):
        csv_file = f"{codebase_path}/scanned_results.csv"
        vulnerabilities = self.convert_csv_to_json(csv_file)
        json_output = json.dumps(vulnerabilities, indent=4)
        print(json_output)

    def start(self, codebase_path, language):
        self.setup_whitebox_model(codebase_path)

        # Running the analysis
        self.create_codebase_database(language, codebase_path)
        self.analyze_codebase(codebase_path)
        self.whitebox_analysis_output(codebase_path)

if __name__ == "__main__":
    # Initial Setup
    codebase_path = "../media/TestingWebsite"
    language = "python"
    test = WhiteBox()
    test.start(codebase_path, language)
    
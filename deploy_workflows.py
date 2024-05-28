import os
import requests
import json
import argparse

def deploy_job(workspace_url,api_token,job_config):
    response = requests.post(f"{workspace_url}/api/2.1/jobs/create", 
                            headers={'Authorization': f'Bearer {api_token}'}, 
                                     json=job_config)
    if response.status_code == 200:
        print(f"Job deployed successfully: {job_config['name']}")
    else:
        print(f"Failed to deploy job: {job_config['name']}. Status code: {response.status_code}, Response: {response.text}")

def main():
    
    parser = argparse.ArgumentParser(description='Export Databricks jobs')
    parser.add_argument('--workspace-url', required=True, help='Databricks workspace URL')
    parser.add_argument('--api-token', required=True, help='Databricks API token')
    args = parser.parse_args()

    workspace_url = args.workspace_url
    api_token = args.api_token
    
    for filename in os.listdir("jobs_config"):
        if filename.endswith(".json"):
            with open(os.path.join("jobs_config", filename), "r") as file:
                job_config = json.load(file)
                deploy_job(workspace_url,api_token,job_config)

if __name__ == "__main__":
    main()

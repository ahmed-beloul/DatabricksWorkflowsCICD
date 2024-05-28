import requests
import json
import argparse


def list_jobs(workspace_url,api_token):
    response = requests.get(
        f'{workspace_url}/api/2.0/jobs/list',
        headers={'Authorization': f'Bearer {api_token}'},
        json={})
    if response.status_code == 200:
        return response.json()["jobs"]
    else:
        print(f"Failed to list jobs. Status code: {response.status_code}")
        return []

def export_job_config(workspace_url,api_token,job_id):
    response = requests.get(f"{workspace_url}/api/2.0/jobs/get?job_id={job_id}", 
                            headers={'Authorization': f'Bearer {api_token}'})
    if response.status_code == 200:
        return response.json()["settings"]
    else:
        print(f"Failed to export job config for job ID {job_id}. Status code: {response.status_code}")
        return None

def main():
    
    parser = argparse.ArgumentParser(description='Export Databricks jobs')
    parser.add_argument('--workspace-url', required=True, help='Databricks workspace URL')
    parser.add_argument('--api-token', required=True, help='Databricks API token')
    args = parser.parse_args()

    workspace_url = args.workspace_url
    api_token = args.api_token
    
    jobs = list_jobs(workspace_url,api_token)
    if jobs:
        for job in jobs:
            job_id = job["job_id"]
            if job['settings'].get('tags',{}).get('deploy',False):
                job_config = export_job_config(workspace_url,api_token,job_id)
                if job_config:
                    with open(f"jobs_config/job_{job_id}_config.json", "w") as outfile:
                        json.dump(job_config, outfile, indent=4)
                        print(f"Exported job configuration for job ID {job_id} to job_{job_id}_config.json")
    else:
        print("No jobs found in the workspace.")

if __name__ == "__main__":
    main()

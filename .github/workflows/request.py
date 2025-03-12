#comunication with sqaas.py

print('preimports')
import requests
import json
print('1st')
import sys
import time
import argparse
print('all')

def get_input_args():
    parser = argparse.ArgumentParser(description=("Find Ophidia workflows"))
    parser.add_argument(
        "--repo", metavar="REPO", type=str, help="name of the local repo", default='.'
    )
    
    return parser.parse_args()
    
payload={
    "repo_code": {
        "repo": "https://github.com/OphidiaBigData/ophidia-workflow-catalogue",
        "branch": "master"
    },}
'''
    "criteria_workflow": [
        {
            "id": "QC.Sty",
            "tools": [
                {
                    "docs": "https://pyophidia.readthedocs.io/en/latest",
                    "docker": {
                        "dockerfile": "QC.Sty/pyophidia/Dockerfile"
                    },
                    "args": [
                        {
                            "type": "optional", "description": "Path to the folder where the workflows are located", "value": ".", "option": "--path", "selectable": True, "explicit_paths": True
                        },{"type": "optional", "description": "args for validation", "value": "[arg]", "option": "--paath", "selectable": True, "explicit_paths": True},
                        
                    ],
                    "reporting": {
                        "validator": "pyophidia",
                        "subcriterion": "QC.Sty",
                        "requirement_level": "RECOMMENDED",
                        "lang_name":"python",
                        "tool_name":"pyophidia",
                    },
                    "name": "find_oph_workflows.py",
                    "lang": "python"
                }
            ]
        }
    ]
}
'''
args= get_input_args()

payload['repo_code']['repo'] ='https://github.com/'+args.repo
#print(payload)
#create the pipeline
#crea=requests.post('https://api-staging.sqaaas.eosc-synergy.eu/v1/pipeline/assessment?run_criteria_workflow_only=True',json=payload)
crea=requests.post('https://api-staging.sqaaas.eosc-synergy.eu/v1/pipeline/assessment?run_criteria_workflow_only=True',json=payload)
#print (crea,crea.json())
#look at the json
ide=crea.json()['id']
'''
with open('creation_'+ide+'.json','w') as creation_file:
   json.dump(crea.json(), creation_file)
'''

#run the pipeline

run=requests.post('https://api-staging.sqaaas.eosc-synergy.eu/v1/pipeline/'+ide+'/run')
#check if it generates next job, check the jsons with the identifier
#print (run,run.text)
#time.sleep(10)
#get the output
for i in range(100):
    time.sleep(5)
    #print(i)  
    status=requests.get('https://api-staging.sqaaas.eosc-synergy.eu/v1/pipeline/'+ide+'/status')

    #print (status,status.json())
    if status.json()['build_status']=='SUCCESS':
        output=requests.get('https://api-staging.sqaaas.eosc-synergy.eu/v1/pipeline/'+ide+'/output')
        break
print(str(output.json))

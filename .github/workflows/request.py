#comunication with sqaas.py


import requests
import json
import sys
import time


payload={
    "repo_code": {
        "repo": "https://github.com/OphidiaBigData/ophidia-workflow-catalogue",
        "branch": "devel"
    },
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
                        },{"type": "optional", "description": "Path to the folder where the workflows are located", "value": "[pata]", "option": "--paath", "selectable": True, "explicit_paths": True},
                        
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


#create the pipeline
#crea=requests.post('https://api-staging.sqaaas.eosc-synergy.eu/v1/pipeline/assessment?run_criteria_workflow_only=True',json=payload)
crea=requests.post('https://api-staging.sqaaas.eosc-synergy.eu/v1/pipeline/assessment?run_criteria_workflow_only=True',json=payload)
print (crea,crea.json())
#look at the json
ide=crea.json()['id']
'''
with open('creation_'+ide+'.json','w') as creation_file:
   json.dump(crea.json(), creation_file)
'''

#run the pipeline

run=requests.post('https://api-staging.sqaaas.eosc-synergy.eu/v1/pipeline/'+ide+'/run')
#check if it generates next job, check the jsons with the identifier
print (run,run.text)
#time.sleep(10)
#get the output
for i in range(100):
    time.sleep(5)
    print(i)  
    status=requests.get('https://api-staging.sqaaas.eosc-synergy.eu/v1/pipeline/'+ide+'/status')

    #print (status,status.json())
    if status.json()['build_status']=='SUCCESS':
        output=requests.get('https://api-staging.sqaaas.eosc-synergy.eu/v1/pipeline/'+ide+'/output')
        break


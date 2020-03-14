########################
### Install Packages ###
########################

import argparse
import sodapy
import json
import pprint
import pandas
import os
from sodapy import Socrata
from requests import get, HTTPError
from elasticsearch import Elasticsearch
from datetime import datetime


########################
#### Elastic Search ####
########################

def create_and_update_index(index_name, doc_type):
    es = Elasticsearch()
    try:
        es.indices.create(index=index_name)
        es.indices.put_mapping(index=index_name, doc_type=doc_type)
    except:
        pass
    return es

########################
###### API Inputs ######
########################

API_BASE = 'data.cityofnewyork.us'
DATASET = 'nc67-uf89'

########################
##### NYC API Pull #####
########################

#### NYC_PARKING Funtion ####

def nyc_parking(APP_KEY, page_size, elastics, output) -> dict:

    try:
        API_KEY = os.environ.get(APP_KEY)
        client = Socrata(API_BASE,API_KEY)
        citations = client.get(DATASET,limit=page_size)
        for citation in citations:
            citation['issue_date'] = datetime.strptime(citation['issue_date'],'%m/%d/%Y')
            if elastics:
                pprint.pprint(citation)
                es = create_and_update_index('bigdata1_index', 'bigdata1')
                res = es.index(index='bigdata1_index', doc_type='bigdata1', body=citation)
                print(res)
            if output:
                pprint.pprint(citation)
                dfoutput = pandas.DataFrame(citations)
                dfoutput.to_csv('main_output.csv', index=False)
            else:
                pprint.pprint(citation)

    except HTTPError as e:
        print(f"Failed to make API call: {e}")

    except KeyError as e:
        print(f"Failed to get rates from response: {e}")
        raise
        
    except Exception as e:
        print(f"Something went wrong: {e}")
        raise

###### Argparse ########

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Return NYC Parking Violations')
    parser.add_argument('--APP_KEY', type=str, required=True,help="NYC Open Data Unique Token")
    parser.add_argument('--page_size', type=int, required=True, help="Number of Violation Entries to Return")
    parser.add_argument("--elastics", default=None, help="Push to ElasticSearch")
    parser.add_argument("--output", default=None, help="Send CSV File to Local Directory")
    args = parser.parse_args()
    nyc_parking(args.APP_KEY,args.page_size,args.elastics,args.output)
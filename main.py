### 9708 HW Part 1

### Using OS Environs Secret Key Call ODNYC API To Retrieve Parking Violations Data
### JSON and optional CSV Output to Local pwd based on arguments specified in Funtion 

import argparse
import sodapy
import json
import pandas
import os
from sodapy import Socrata
from requests import get, HTTPError

API_BASE = 'data.cityofnewyork.us'
DATASET = 'nc67-uf89'


parser = argparse.ArgumentParser(description='Return NYC Parking Violations')
parser.add_argument('--APP_KEY', type=str, required=True,help="NYC Open Data Unique Token")
parser.add_argument('--page_size', type=int, required=True, help="Number of Violation Entries to Return")
parser.add_argument('--output', type=int, help="Number of Violation Entries to Return")

args = parser.parse_args()

def nyc_parking(APP_KEY,page_size, outputcsv = 1) -> dict:

    try:
        if outputcsv == 1:
            API_KEY = os.environ.get(APP_KEY)
            client = Socrata(API_BASE,API_KEY)
            r = client.get(DATASET,limit=page_size)
            dfoutput = pandas.DataFrame(r)
            dfoutput.to_csv('main_output.csv', index=False)
            r = json.dumps(r)
            print(r)

        else: 
            API_KEY = os.environ.get(APP_KEY)
            client = Socrata(API_BASE,API_KEY)
            r = client.get(DATASET,limit=page_size)
            r = json.dumps(r)
            print(r)

    except HTTPError as e:
        print(f"Failed to make API call: {e}")

    except KeyError as e:
        print(f"Failed to get rates from response: {e}")
        raise
        
    except Exception as e:
        print(f"Something went wrong: {e}")
        raise
        
if __name__ == "__main__":
    print(nyc_parking(args.APP_KEY,args.page_size,args.output))
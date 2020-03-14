# ParkingViolations9760

The following project provides a workflow to connect to the OpenData NYC API to analyze parking violations in the city of
New York since 2016. 

The scope of the project will expand beyond basic Python Scripting to include ElasticSearch, Kibana, and EC2 functionality.

## Resources
[STA 9760 - Analyzing Millions of NYC Parking Violations](https://docs.google.com/document/d/1jjArRAV462E6N6IcSBxPAtGBoIy3Iqn0KDEgRgaxC8A/edit#)  
[Data Set - Open Parking and Camera Violations](https://dev.socrata.com/foundry/data.cityofnewyork.us/nc67-uf89)  
[Connecting to API - Create ODNYC Login and Request API Token](https://data.cityofnewyork.us/login)  
[Docker Documentation](https://docs.docker.com/)  
[sodapy/Socrata Documentation](https://dev.socrata.com/)  

# Part I: Python Scripting

## Using API Token Seceretly
To ensure that your ODNYC API Token remains private and does not get posted online, please declare and 'APP_KEY'  
environmental variable that will be called in the primary script instead of posting hardcoded values or manually entering a long hashed string:

os.environ['APP_KEY'] = 'YOUR UNIQUE API TOKEN'

The entry for the APP_KEY argument in the nyc_parking function within the main.py script should therefore be 'APP_KEY'

### Output 
Based on running the main.py script in Docker or locally, the script will return the page size of json entries specified in the function and a csv output to the pwd if specified 1 or not entered when run using volume in Docker

## Docker Image Build 
### Build:
 ```console
docker build -t bigdata1:1.0 .
 ```
 
### Initial Dockerfile
```py
FROM python:3.7  
RUN pip install requests  
ENV HELLO = 1  
WORKDIR /app  
COPY main.py /app  
```

### Get Requirements.txt Contents from Terminal Mode
 ```console
docker run -it bigdata1:1.0 /bin/bash  
pip freeze
 ```

### Update Dockerfile
```py
FROM python:3.7  
WORKDIR /app  
COPY main.py /app  
COPY requirements.txt /app  
RUN pip install -r requirements.txt  
```

docker build -t bigdata1:1.0 .

### To Test:
 ```console
docker run -v $(pwd):/app -it bigdata1:1.0 python3 main.py --APP_KEY 'APP_KEY' --page_size {'Enter Int'} --output OUTPUT
 ```

### Login to Dockerhub
docker login --username=username

### Update Dockerfile
```py
FROM python:3.7  
WORKDIR /app  
COPY main.py /app
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt 
```

### Deploy via Dockerhub
 ```console
docker images | grep bigdata1
 ```
 COPY THE TAG 
```console 
docker tag 819a6dd0320e pparham/bigdata1:1.0
docker push pparham/bigdata1
 ```

## Launching from EC2
#### (Instructions Example for Ubuntu)
sudo apt install docker.io  
sudo docker login --username  
sudo docker pull username/project name  
sudo docker run -v $(pwd):/app -it bigdata1:1.0 python3 main.py --APP_KEY 'APP_KEY' --page_size {'Enter Int'} --output {'1 for csv to pwd, 0 for no csv, 1 by default'}

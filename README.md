# ParkingViolations9760
*** ReadMe Updated to Include Parts II & III

The following project provides a workflow to connect to the OpenData NYC API to analyze parking violations in the city of
New York since 2016. The primary script ('main.py') includes functionality to allow users to export to csv and analyze the specific API call with ElasticSearch/Kibana.

## Resources
[STA 9760 - Analyzing Millions of NYC Parking Violations](https://docs.google.com/document/d/1jjArRAV462E6N6IcSBxPAtGBoIy3Iqn0KDEgRgaxC8A/edit#)  
[Data Set - Open Parking and Camera Violations](https://dev.socrata.com/foundry/data.cityofnewyork.us/nc67-uf89)  
[Connecting to API - Create ODNYC Login and Request API Token](https://data.cityofnewyork.us/login)  
[Docker Documentation](https://docs.docker.com/)  
[sodapy/Socrata Documentation](https://dev.socrata.com/)  


## Using API Token Seceretly
To ensure that your ODNYC API Token remains private and does not get posted online, please declare and 'APP_KEY'  
environmental variable that will be called in the primary script instead of posting hardcoded values or manually entering a long hashed string:

os.environ['APP_KEY'] = 'YOUR UNIQUE API TOKEN'

The entry for the APP_KEY argument in the nyc_parking function within the main.py script should therefore be 'APP_KEY'

### Output 
Based on running the main.py script in Docker or locally, the script will return the page size of json entries specified in the function and a csv output to the pwd if included. 

The --elastics argument should not be included at this time as ElasticSearch has not yet been stood up in the workflow.


# Docker Image Build and Initial Script 
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

 ```console
docker build -t bigdata1:1.0 .
 ```

### To Test:
 ```console
docker run -v $(pwd):/app -it bigdata1:1.0 python3 main.py --APP_KEY 'APP_KEY' --page_size {'Enter Int'} --output OUTPUT
 ```

### Login to Dockerhub
 ```console
docker login --username=username
 ```
 
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
docker tag {'COPY THE TAG'} pparham/bigdata1:1.0
docker push pparham/bigdata1
 ```

## Launching from EC2
#### (Instructions Example for Ubuntu)
sudo apt install docker.io  
sudo docker login --username  
sudo docker pull username/project name  
sudo docker run -v $(pwd):/app -it bigdata1:1.0 python3 main.py --APP_KEY 'APP_KEY' --page_size {'Enter Int'} --output {'1 for csv to pwd, 0 for no csv, 1 by default'}


# Launching ElasticSearch and Kibana
### Creating docker-compose.yml:
 ```py
version: '3'
services:
  pyth:
    network_mode: host
    container_name: pyth
    build:
      context: .
    volumes:
      - .:/app:rw
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:6.3.2
    environment:
      - cluster.name=docker-cluster
      - bootstrap.memory_lock=true
      - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
    ulimits:
      memlock:
        soft: -1
        hard: -1
    ports:
      - "9200:9200"
  kibana:
    image: docker.elastic.co/kibana/kibana:6.3.2
    ports:
      - "5601:5601"
 ```
 
### Build ElasticSearch and Kibana:
```console
docker-compose build pyth
```

### Initiate ElasticSearch and Kibana:
```console
docker-compose up -d
```

### Push to ElasticSearch:
In order to push to ElasticSearch, the --elastics argument is now required. The --output argument that allows users to receive a csv version of the data in their working directory remains optional.
```console
docker-compose run -v ${PWD}:/app/out pyth /bin/bash
python3 main.py --APP_KEY 'APP_KEY' --page_size 10  --elastics ELASTICS --output OUTPUT
```

### Lanuch Kibana in Browser:
[http://localhost:5601/app/kibana](http://localhost:5601/app/kibana)

### Configure Index Based on Date Data Type:

# Examples of Kibana Visualizations

# Cloud Infrastructure for Mining Challenge Analytics

### To Load the dump in Neo4J.
Download the dataset dump file from: https://zenodo.org/records/13683940/files/ with_metrics_goblin_maven_30_08_24.dump and then add it to a cloud Bucket to perform the Load in the Neo4J container.

On Dockerfile:
```bash
RUN curl -Lv -o /data/graph.dump <YOUR LINK DO SEU BUCKET Object Storage HERE> && \
    neo4j-admin load --from=/data/graph.dump --database=neo4j --force && \
    rm -fv /data/graph.dump
```

# Container Stack
The instance was configured to support a stack of Docker containers, consisting of the following services:
1. Neo4j Community Edition  
◦ Database management system specialized in graphs.  
◦ Used for storing, querying and analyzing data.  

2. Weaver REST API  
◦ Responsible for programmatic interactions with the Neo4j database.  
◦ Allows queries and enrichment of the dataset.  

3. JupyterLab  
◦ Development environment with support for notebooks in Python, R and Java.  

# Minimum requirements:  
Instance configuration in IaaS (Infrastructure as a Service)  
• Instance type: VM.Standard2.4  
• Processor: Intel Xeon Platinum 8167M (Skylake), 2.0 GHz  
• Physical cores (OCPU): 4  
• RAM: 60 GB  
• Network: 4.1 Gbps bandwidth  
• Block storage: 199 GB  

## To use services
### Neo4jWeaver
```bash
docker compose -f docker-compose.metrics.yml -p metrics up -d
docker compose -f docker-compose.metrics.yml -p metrics down
```
#### Logs
```sh
docker compose -f docker-compose.metrics.yml -p metrics logs -f
```
### JupyterLabAnalyticsGrafo
```bash
docker compose up -d
docker compose down
```
#### Logs
```sh
docker compose logs -f
```

## Web Browser Access (localhost or cloud)
neo4j://localhost:7688 (for external access, jupyter, neo4j, other tools)   
http://localhost:8081/swagger-ui/index.html  
http://localhost:7475/browser   
http://localhost:8889  

### References
D. Jaime, "Goblin: Neo4J Maven Central dependency graph (2024-08-30 & metrics), **Dataset, presented at the 21st International Conference on Mining Software Repositories (MSR)**, Lisbon, 2024. Available: https://doi.org/10.5281/zenodo.13734581  

D. Jaime, J. El Haddad, and P. Poizat, **Navigating and Exploring Software Dependency Graphs using Goblin**, in Proceedings of the International Conference on Mining Software Repositories (MSR), 2025.  

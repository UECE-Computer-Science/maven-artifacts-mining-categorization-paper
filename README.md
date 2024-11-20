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

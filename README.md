# Cloud Infrastructure for Mining Challenge Analytics

### To Load the dump in Neo4J.
Download the dataset dump file from: https://zenodo.org/records/13683940/files/ with_metrics_goblin_maven_30_08_24.dump and then add it to a cloud Bucket to perform the Load in the Neo4J container.

On Dockerfile:
```bash
RUN curl -Lv -o /data/graph.dump <YOUR LINK DO SEU BUCKET Object Storage HERE> && \
    neo4j-admin load --from=/data/graph.dump --database=neo4j --force && \
    rm -fv /data/graph.dump
```

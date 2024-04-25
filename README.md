# LmRaC - Language Model Research Assistant & Collaborator

## Prerequisites
### Docker
x
### OpenAI
x
### Pinecone
x

---
## Quick Start
Pull the desired tagged image from Docker Hub.
```
docker pull dbcraig/lmrac:0.1.0
```
Run LmRaC using Docker. Pass API keys for OpenAI and Pinecone and mount the local directory (e.g., $PWD) to the LmRaC /app/user directory. All logs and output will be written to this path.
```
docker run -m1024m -it -e OPENAI_API_KEY=${OPENAI_API_KEY} -e PINECONE_API_KEY=${PINECONE_API_KEY} -v $(PWD)/work:/app/user lmracv:0.1.0
```


---
## Configuration
If not user configuration is supplied, LmRaC will use the following default:
```
Session Logs Directory  : /app/user/sessions/
Final Answers Directory : /app/user/sessions/finalAnswers/
Experiments Directory   : /app/user/experiments/
Vocabularies Directory  : /app/user/vocab/

```

---
## Q & A 
xxx

---
## Experiments
xxx

---
## Troubleshooting
### Memory
Because LmRaC uses multiprocessing extensively, complex questions can require significant memory resources while documents are being processed. We recommend a minimum of 1GB for the Docker container, though 2GB may be necessary for large multi-part questions. The error **A process in the process pool was terminated abruptly while the future was running or pending** is usually an indication that LmRaC ran out of memory.

---
## Citation
xxx


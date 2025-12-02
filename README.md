# Predicting-Diabetes
Reprodução e avaliação do artigo  
**“Comparative Effectiveness of Classification Algorithms in Predicting Diabetes”**  
(IEEE, 2024)

Projeto da disciplina **Aprendizado de Máquina – CESAR School (2025.2)**.  

---

# 1. Estrutura Geral do Projeto

```
Predicting-Diabetes/
├── docker-compose.yml
├── fastapi/
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── routes/upload.py
│   │   └── services/minio_service.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── minio/
│   └── data/
├── postgres/
│   └── data/
├── mlflow/
├── jupyterlab/
├── notebooks/
├── trendz/
└── reports/
```

---

## FastAPI – Camada de Ingestão 
Responsável por receber arquivos `.csv` ou `.json` e enviá-los diretamente ao bucket S3 da Amazon `diabetes-raw`.

Endpoints disponíveis:
- **GET /** → Healthcheck  
- **POST /api/upload** → Upload e envio ao bucket S3

Tecnologias usadas:
- FastAPI  
- Bucket S3 Amazon  
- Pydantic Settings  
- Uvicorn  

## Bucket S3 Amazon
Serviço de armazenamento.  
A FastAPI cria automaticamente o bucket `diabetes-raw` caso ele ainda não exista.

## Ambiente Docker
Todos os serviços principais sobem via `docker-compose`:
- FastAPI
- S3 Amazon
- PostgreSQL
- JupyterLab
- MLflow
- Trendz 

---

# Configuração do Ambiente 
Criar um arquivo .env na raiz.

```
#AWS
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_DEFAULT_REGION=
S3_BUCKET_NAME=

#Snowflake
SNOWFLAKE_USER=
SNOWFLAKE_PASSWORD=
SNOWFLAKE_ACCOUNT=
SNOWFLAKE_WAREHOUSE=
SNOWFLAKE_DATABASE=
SNOWFLAKE_SCHEMA=
SNOWFLAKE_TABLE=
```

---

# Como executar o projeto

### Passo 1 — Subir toda a stack
```bash
docker compose up -d
```

### Passo 2 — Verificar serviços

| Serviço      | URL                        | Credenciais |
|--------------|----------------------------|-------------|
| FastAPI      | http://localhost:8000       | — |
| Swagger UI   | http://localhost:8000/docs  | — |
| S3 Amazon    | http://localhost:9001       | - |
| JupyterLab   | http://localhost:8888       | - |
| MLflow       | http://localhost:5500       | — |
| PostgreSQL   | localhost:5432              | admin / admin |

---

# 4. Como testar a ingestão (FastAPI)

### Via CURL
```bash
curl -X POST "http://localhost:8000/api/upload"  \  -F "file=\data\raw\Dataset_of_Diabetes.csv" 
```

### Via Navegador (Swagger)
1. Abrir: http://localhost:8000/docs  
2. Abrir o endpoint POST `/api/upload`  
3. Clicar em “Try it out”  
4. Selecionar o arquivo `.csv` ou `.json`  
5. Executar  

### Resultado esperado
```json
{
  "message": "File uploaded successfully",
  "object_name": "20251125-213950_Dataset_of_Diabetes.csv"
}
```

O arquivo aparecerá no S3 em:
```
http://localhost:9001/browser/diabetes-raw
```
--- 

Grupo:
- Eduardo Lins
- Gabriel Belliato
- Gabriel Bezerra
- Letícia Gomes da Silva
- Vinicius Petribu 

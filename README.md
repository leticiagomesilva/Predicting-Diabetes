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
│   │   └── services/s3_service.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── postgres/
│   └── data/
├── mlflow/
│   ├── Dockerfile
│   └── ...
├── jupyter-lab/
│   ├── Dockerfile
│   └── ...
├── notebooks/
├── trendz/
└── reports/
```

---

# 2. FastAPI – Camada de Ingestão

Responsável por receber arquivos `.csv` ou `.json` e enviá-los para o bucket S3 definido na variável `S3_BUCKET_NAME`.

Endpoints:

| Método | Rota             | Descrição |
|--------|------------------|-----------|
| GET    | `/`              | Healthcheck |
| POST   | `/api/upload`    | Upload e envio para S3 |

Tecnologias:
- FastAPI  
- Amazon S3  
- Boto3  
- Pydantic Settings  
- Uvicorn  

---

# 3. Bucket S3 Amazon

- Utilizado para armazenar os arquivos enviados pela FastAPI.  
- O bucket principal é definido em `.env` via `S3_BUCKET_NAME`.  
- O MLflow salva artefatos dentro de um **subdiretório interno**, por exemplo:

```
s3://diabetes-ml2025/mlflow/
```

---

# 4. Ambiente Docker

Todos os serviços sobem via `docker-compose`:

| Serviço | Descrição |
|---------|-----------|
| FastAPI | Ingestão + Upload para S3 |
| PostgreSQL | Banco para MLflow |
| JupyterLab | Execução dos notebooks |
| MLflow | Tracking de modelos e experimentos |
| Trendz | Visualização/monitoramento |
| S3 Amazon | Armazenamento de arquivos |

---

# 5. Configuração – Criar o arquivo `.env`

```
# AWS
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_DEFAULT_REGION=
S3_BUCKET_NAME=diabetes-ml2025

# Snowflake
SNOWFLAKE_USER=
SNOWFLAKE_PASSWORD=
SNOWFLAKE_ACCOUNT=
SNOWFLAKE_WAREHOUSE=
SNOWFLAKE_DATABASE=
SNOWFLAKE_SCHEMA=
SNOWFLAKE_TABLE=
```

---

# 6. Como executar o projeto

### 1 — Subir toda a stack
```bash
docker compose up -d
```

### 2 — Acessar serviços

| Serviço    | URL                                                      |
| ---------- | -------------------------------------------------------- |
| FastAPI    | http://localhost:8000           |
| Swagger    | http://localhost:8000/docs |
| JupyterLab | http://localhost:8888           |
| MLflow     | http://localhost:5500           |
| PostgreSQL | localhost:5432                                           |

---

# 7. Testar Ingestão via FastAPI

### Via CURL

```bash
curl -X POST "http://localhost:8000/api/upload"      -F "file=@Dataset_of_Diabetes.csv"
```

### Via Swagger

1. Abrir `http://localhost:8000/docs`
2. POST `/api/upload`
3. Selecionar arquivo
4. Enviar

### Resposta esperada

```json
{
  "message": "File uploaded successfully",
  "object_name": "20251125-213950_Dataset_of_Diabetes.csv"
}
```

O arquivo estará em:

```
s3://diabetes-raw/
```

---

# 8. Logging de Modelos no MLflow

O projeto registra automaticamente:

* parâmetros
* métricas
* assinatura do modelo
* input_example
* versão final do modelo

Configuração:

```python
mlflow.set_tracking_uri("http://mlflow:5000")
mlflow.set_experiment("predicting-diabetes")
```

---

# 9. Como resetar o MLflow e o PostgreSQL

Caso o MLflow falhe por causa de runs antigos, corrupção de volume ou banco ausente:

### 1 — Apagar dados do Postgres
```bash
rm -rf ./postgres/data
```

### 2 — Derrubar containers
```bash
docker compose down -v
```

### 3 — Subir tudo de novo
```bash
docker compose up -d --build
```

### 4 — Criar o banco do MLflow
```bash
docker exec -it postgres psql -U admin -d postgres -c "CREATE DATABASE mlflowdb;"
```

### 5 — Reiniciar somente o MLflow
```bash
docker restart mlflow
```

---

# 10. Grupo

* Eduardo Lins  
* Gabriel Belliato  
* Gabriel Bezerra  
* Letícia Gomes da Silva  
* Vinicius Petribu

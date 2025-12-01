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

# 2. Componentes já funcionais neste commit

## ✔ FastAPI – Camada de Ingestão (sua parte)
Responsável por receber arquivos `.csv` ou `.json` e enviá-los diretamente ao bucket MinIO `diabetes-raw`.

Endpoints disponíveis:
- **GET /** → Healthcheck  
- **POST /api/upload** → Upload e envio ao MinIO

Tecnologias usadas:
- FastAPI  
- MinIO SDK v7  
- Pydantic Settings  
- Uvicorn  

## ✔ MinIO
Serviço de armazenamento S3-like.  
A FastAPI cria automaticamente o bucket `diabetes-raw` caso ele ainda não exista.

## ✔ Ambiente Docker
Todos os serviços principais sobem via `docker-compose`:
- FastAPI
- MinIO
- PostgreSQL
- JupyterLab
- MLflow
- Trendz (estrutura inicial)

---

# Como executar o projeto

### Passo 1 — Subir toda a stack
```bash
docker compose up -d
```

### ▶ Passo 2 — Verificar serviços

| Serviço      | URL                        | Credenciais |
|--------------|----------------------------|-------------|
| FastAPI      | http://localhost:8000       | — |
| Swagger UI   | http://localhost:8000/docs  | — |
| MinIO        | http://localhost:9001       | minioadmin / minioadmin |
| JupyterLab   | http://localhost:8888       | Token nos logs |
| MLflow       | http://localhost:5500       | — |
| PostgreSQL   | localhost:5432              | admin / admin |

---

# 4. Como testar a ingestão (FastAPI)

### Via CURL
```bash
curl -X POST "http://localhost:8000/api/upload"      -F "file=@Dataset_of_Diabetes.csv"
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

O arquivo aparecerá no MinIO em:
```
http://localhost:9001/browser/diabetes-raw
```

---

# 5. Próximas etapas do projeto

1. Pipeline Snowflake/Postgres → ingestão do dataset bruto  
2. Notebook de pré-processamento e limpeza  
3. Notebook de modelagem e comparação de algoritmos  
4. Registro de experimentos no MLflow  
5. Exportação do modelo final para o S3  
6. Criação de dashboards no ThingsBoard/Trendz  
7. Relatório final em `.docx`  

--- 

Grupo:
- Letícia Gomes da Silva
- Gabriel Belliato
- Gabriel Bezerra 
- Eduardo Lins
- Vinicius Petribu 

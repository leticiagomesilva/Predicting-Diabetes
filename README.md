# Predicting-Diabetes
Reprodução e avaliação do artigo  
**“Comparative Effectiveness of Classification Algorithms in Predicting Diabetes”**  
(IEEE, 2024)

Projeto da disciplina **Aprendizado de Máquina – CESAR School (2025.2)**.

* Eduardo Lins (@eduardoalins)
* Gabriel Belliato (@belli5)
* Gabriel Bezerra (@GabrielBza)
* Letícia Gomes da Silva (@leticiagomesilva)
* Vinicius Petribu (@vinipetribu)

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
| POST | `/send-to-thingsboard` | Envia o dataset para um device no ThingsBoard |

Tecnologias: FastAPI, S3, Boto3, Uvicorn, Pandas. 

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
| FastAPI | Ingestão + envio para S3 + envio para ThingsBoard |
| PostgreSQL | Banco para MLflow |
| JupyterLab | Execução dos notebooks |
| MLflow | Tracking de modelos e experimentos |
| ThingsBoard | Dashboard IoT |
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

TB_TOKEN=
```

---

# 6. Como executar o projeto

### 1 — Subir toda a stack
```bash
docker compose up -d --build
```

### 2 — Acessar serviços

| Serviço    | URL                                                      |
| ---------- | -------------------------------------------------------- |
| FastAPI    | http://localhost:8000           |
| Swagger    | http://localhost:8000/docs |
| JupyterLab | http://localhost:8888           |
| MLflow     | http://localhost:5500           |
| ThingsBoard | http://localhost:9090 |

```
user: tenant@thingsboard.org
pass: tenant
```

---

# 7. Testar Ingestão via FastAPI

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

# 8. Criar Device no ThingsBoard + Enviar Dados (Ingestão IoT)

## 8.1 Criar o Device

1. Acesse: http://localhost:9090  
2. Menu lateral → **Entidades**  → **Dispositivos** 
3. **Adicionar novo dispositivo (+)**  
4. Nome: `diabetes-device`  
5. **Next: Credenciais**
6. Copiar Token de acesso (ex: `rR9MfH2gFxP2nNhjC9Jp`) 

Antes de enviar as métricas ou contagens pelo JupyterLab, é necessário informar o token do dispositivo criado no ThingsBoard.
- Colar Token no .env (`TB_TOKEN=`) e no notebook na sessão:
```
import requests

DEVICE_TOKEN = "SEU_TOKEN_AQUI"   # copie do ThingsBoard
TB_URL = f"http://thingsboard:9090/api/v1/{DEVICE_TOKEN}/telemetry"
```
- Rodar comando 
```
docker compose down
docker compose up -d
```
## 8.2 Importar o Dashboard do ThingsBoard

Após criar o device, é necessário importar o dashboard utilizado no projeto. O dashboard fornecido pelo grupo contém o deviceId fixo do device original.
É necessário substituir para usar com o seu device.

Passo a passo:
1. No arquivo `dashboard_de_diabetes.json` substitua o ID do seu dispositivo em todos os campos `"deviceId": "seu-device-Id-aqui"`
2. Acesse o ThingsBoard:
http://localhost:9090
3. Menu lateral → Dashboards → Adicionar dashboard (+)
4. Selecione o arquivo `dashboard_de_diabetes.json`


---

# 9. Enviar o Dataset para o ThingsBoard

A FastAPI já possui o endpoint:

```
POST http://localhost:8000/send-to-thingsboard
```

Ele envia **todas as linhas** do `Dataset_of_Diabetes.csv` para o ThingsBoard.

### Estrutura no `main.py`:

* CSV dentro do container: `/app/Dataset_of_Diabetes.csv`
* Cada linha é enviada como JSON:

```json
{
  "Gender": "M",
  "AGE": 57,
  "Urea": 5.3,
  "Cr": 66,
  "HbA1c": 7.9,
  "Chol": 3.7,
  "TG": 2.9,
  "HDL": 1.1,
  "LDL": 3.0,
  "VLDL": 0.9,
  "BMI": 28.5,
  "CLASS": "Y"
}
```

### Testar via CURL:

```bash
curl -X POST http://localhost:8000/send-to-thingsboard
```

### Resposta esperada:

```json
{"status":"ok","rows_sent":1000}
```

---

# 10. Logging de Modelos no MLflow

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

# 11. Como resetar o MLflow e o PostgreSQL

Caso o MLflow falhe por causa de runs antigos, corrupção de volume ou banco ausente:
### 1 — Derrubar containers e apagar volumes
```bash
docker compose down -v
```
### 2 — Apagar dados do Postgres
```bash
rm -rf ./postgres/data
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
### 6 — Recriar o dispositivo no ThingsBoard
1. Acesse http://localhost:9090
2. Entidades → Dispositivos
3. Criar novo device
4. Copiar TOKEN NOVO
5. Atualizar:
- .env → TB_TOKEN=
- notebook:
```
DEVICE_TOKEN = "NOVO_TOKEN"
TB_URL = f"http://thingsboard:9090/api/v1/{DEVICE_TOKEN}/telemetry"
```
6. Subir novamente a stack para carregar o novo token::
```
docker compose up -d
```

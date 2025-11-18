# Predicting-Diabetes
Comparative Effectiveness of Classification Algorithms in Predicting Diabetes 

---

# Predicting Diabetes — Projeto AM (Commit Inicial)

Este repositório contém a **estrutura inicial** e o **ambiente Docker básico** para o projeto da disciplina de Aprendizagem de Máquina (AM).  
Neste primeiro commit, foi implementada apenas a **infraestrutura**, conforme orientações do professor.

---

## ✔ Estrutura inicial do projeto

```
Predicting-Diabetes/
├── docker-compose.yml
├── minio/
│ └── data/
├── postgres/
│ └── data/
├── mlflow/
├── jupyterlab/
├── notebooks/
├── trendz/
└── reports/
```

Todas as pastas estão vazias (exceto pelas áreas de dados após o Docker iniciar), pois este commit representa somente a base do ambiente.

---

## ✔ Serviços já disponíveis via Docker

O arquivo `docker-compose.yml` desta etapa inicial sobe os seguintes serviços:

- **MinIO** — Armazenamento de objetos (S3-like)
- **PostgreSQL** — Banco de dados relacional
- **MLflow** — Servidor para rastreamento de experimentos (será configurado posteriormente)
- **JupyterLab** — Ambiente para notebooks e desenvolvimento

Nenhum código de modelagem, ingestão ou API foi adicionado ainda.

---

## ▶ Como executar o ambiente

Antes de rodar pela primeira vez, garanta que os diretórios de dados estão vazios:
```
rm -rf minio/data
rm -rf postgres/data
```

Em seguida, execute:
```
docker compose up
```

---

## 🌐 Endpoints dos serviços

Após iniciar:

### • JupyterLab  
http://localhost:8888  
(O token aparece nos logs)

### • MinIO  
http://localhost:9001  
Usuário: `minioadmin`  
Senha: `minioadmin`

### • PostgreSQL  
Host: `localhost`  
Porta: `5432`  
Usuário: `admin`  
Senha: `admin`  
Banco: `diabetesdb`

### • MLflow  
http://localhost:5500  
(Ainda sem experimentos — será configurado em commits posteriores)

---

## 📌 Próximas etapas (próximos commits)

1. Criar o serviço FastAPI para ingestão de dados  
2. Implementar notebook de pré-processamento  
3. Implementar notebook de modelagem e comparação dos algoritmos  
4. Registrar experimentos com MLflow  
5. Criar dashboard de visualização com Trendz/ThingsBoard  
6. Elaborar relatório final

---

## 📄 Status Atual

**Commit inicial concluído:**  
✔ Estrutura criada  
✔ Docker funcionando  
✔ Ambiente pronto para desenvolvimento nas próximas etapas

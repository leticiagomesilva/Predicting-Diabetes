FROM python:3.10-slim

WORKDIR /mlflow

# Dependências opcionais mas recomendadas
RUN pip install --no-cache-dir \
    mlflow \
    boto3 \
    psycopg2-binary

# Porta padrão do MLflow
EXPOSE 5000

CMD ["mlflow", "server", "--backend-store-uri", "postgresql://admin:admin@postgres:5432/mlflowdb", "--default-artifact-root", "s3://mlflow-artifacts", "--host", "0.0.0.0", "--port", "5000"]
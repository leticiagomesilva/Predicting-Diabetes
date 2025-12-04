from fastapi import FastAPI
from app.routes.upload import router as upload_router
import requests
import os
import pandas as pd

app = FastAPI(title="Diabetes Ingestion API")

@app.get("/")
def root():
    return {"status": "running"}

app.include_router(upload_router, prefix="/api")

TB_TOKEN = os.getenv("TB_TOKEN")
TB_URL = f"http://thingsboard:9090/api/v1/{TB_TOKEN}/telemetry"

def send_row_to_thingsboard(row):
    payload = {
        "Gender": str(row["Gender"]).strip().upper(),
        "AGE": float(row["AGE"]),
        "Urea": float(row["Urea"]),
        "Cr": float(row["Cr"]),
        "HbA1c": float(row["HbA1c"]),
        "Chol": float(row["Chol"]),
        "TG": float(row["TG"]),
        "HDL": float(row["HDL"]),
        "LDL": float(row["LDL"]),
        "VLDL": float(row["VLDL"]),
        "BMI": float(row["BMI"]),
        "CLASS": str(row["CLASS"]).strip().upper()
    }


    requests.post(TB_URL, json=payload)


@app.post("/send-to-thingsboard")
def send_dataset_to_tb():
    csv_path = "/app/Dataset_of_Diabetes.csv"
    
    df = pd.read_csv(csv_path)

    df["CLASS"] = df["CLASS"].astype(str).str.strip().str.upper()
    df["Gender"] = df["Gender"].astype(str).str.strip().str.upper()

    for _, row in df.iterrows():
        send_row_to_thingsboard(row)

    return {"status": "ok", "rows_sent": len(df)}

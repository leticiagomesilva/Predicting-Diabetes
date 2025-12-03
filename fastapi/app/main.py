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
        "gender": str(row["Gender"]).strip().upper(),
        "age": float(row["AGE"]),
        "urea": float(row["Urea"]),
        "cr": float(row["Cr"]),
        "hba1c": float(row["HbA1c"]),
        "chol": float(row["Chol"]),
        "tg": float(row["TG"]),
        "hdl": float(row["HDL"]),
        "ldl": float(row["LDL"]),
        "vldl": float(row["VLDL"]),
        "bmi": float(row["BMI"]),
        "class": str(row["CLASS"]).strip().upper()
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

# export.py
import pandas as pd

def save_to_excel(df: pd.DataFrame, path: str):
    # salva Excel
    df.to_excel(path, index=False)
    print(f"✅ Exportado para Excel: {path}")
    # salva CSV paralelo, com mesmo nome (troca .xlsx por .csv)
    csv_path = path.rsplit('.', 1)[0] + '.csv'
    df.to_csv(csv_path, index=False)
    print(f"✅ Exportado para CSV: {csv_path}")
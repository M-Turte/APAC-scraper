# export.py
import pandas as pd

def save_to_excel(df: pd.DataFrame, path: str):
    df.to_excel(path, index=False)
    print(f"✅ Exportado para {path}")

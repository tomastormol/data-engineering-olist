import pandas as pd
from pathlib import Path

# Esto calcula la ruta raíz del proyecto automáticamente
# sin importar desde dónde ejecutes el script
ROOT = Path(__file__).parent.parent
DATA_PATH = ROOT / "data" / "raw"

orders = pd.read_csv(DATA_PATH / "olist_orders_dataset.csv")
print(orders.head(5))
print("\n")
print(orders.dtypes)
print("\n")
print(orders.isnull().sum())
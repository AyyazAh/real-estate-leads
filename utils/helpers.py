import os
import pandas as pd
from pandas.errors import EmptyDataError

def safe_read_csv(filepath):
    if not os.path.exists(filepath) or os.path.getsize(filepath) == 0:
        return None
    try:
        df = pd.read_csv(filepath)
        return df if not df.empty else None
    except EmptyDataError:
        return None
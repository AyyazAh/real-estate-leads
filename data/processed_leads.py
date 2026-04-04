# Run this once to create the file
import pandas as pd
pd.DataFrame({"Link": []}).to_csv("data/processed_leads.csv", index=False)
from pathlib import Path
import pandas as pd


def fields_to_csv(extracted_fields: pd.DataFrame, save_path: Path = Path("/Users/lucazosso/Desktop/IE_Course/Hackathon/Looping_Legends/csv_results/predictions.csv")) -> None:
    extracted_fields.to_csv(save_path)

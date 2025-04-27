# create excel file

# services/excel_writer.py

def save_to_excel(df, filepath):
    df.to_excel(filepath, index=False)
    print(f"Excel file saved at {filepath}")


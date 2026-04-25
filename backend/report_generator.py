import pandas as pd

def generate_report(file_path):

    # 🔥 Step 1: Read file without assuming header
    df_raw = pd.read_excel(file_path, header=None)
    print(df_raw.columns.tolist())
    header_row = None

    # 🔍 Step 2: Find actual header row
    for i in range(len(df_raw)):
        row = df_raw.iloc[i].astype(str).str.strip().tolist()
        
        if 'DPSU' in row and 'Equipment_Name' in row:
            header_row = i
            break

    if header_row is None:
        raise Exception("Header row not found. Check Excel format.")

    # 🔥 Step 3: Read again with correct header
    df = pd.read_excel(file_path, header=header_row)

    # Clean column names
    df.columns = df.columns.str.strip()

    print("Detected Columns:", df.columns.tolist())  # debug

    # 🔥 Step 4: Grouping
    grouped = df.groupby(['DPSU', 'Equipment_Name'])

    report_data = {}

    for (dpsu, equipment), group in grouped:
        total_codified = group['Received_Date'].notna().sum()
        fwd_dca = group['Forward_Date'].notna().sum()
        nsn_allotted = group['NSN'].notna().sum()
        returned = group['Return_Date'].notna().sum()

        if dpsu not in report_data:
            report_data[dpsu] = []

        report_data[dpsu].append({
            'Equipment': equipment,
            'Total_Codified': total_codified,
            'Fwd_DCA': fwd_dca,
            'NSN': nsn_allotted,
            'Returned': returned
        })

    return report_data
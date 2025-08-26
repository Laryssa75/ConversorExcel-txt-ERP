import pandas as pd


#Layout: nome da coluna no Excel + largura + alinhamento + preenchimento
layout = [
    {"col": "EMPRESA", "length": 4, "align": "right", "fill": " "},
    {"col": "CODIGO BEM", "length": 20, "align": "left", "fill": " "},
    {"col": "DATA LOCALIZACAO", "length": 14, "align": "left", "fill": " "},
    {"col": "SEQUENCIA",  "length": 5, "align": "left", "fill": " "}, 
    {"col": "CODIGO LOCAL REAL",  "length": 9, "align": "left", "fill": " "},
]

#lista de colunas que devem ser formatadas como data
date_columns = ["DATA LOCALIZACAO"]

def format_field(value, length, align, fill, col_name=None):
    if pd.isna(value):
        value = ""
    else:
        # Se for a coluna de data -> força formato DD/MM/YYYY
        if col_name in date_columns:
            try:
                value = pd.to_datetime(value).strftime("%d/%m/%Y")
            except Exception:
                value = str(value)  # fallback se não converter
    
        else:
            value = str(value)
     
    #Normaliza quebras de linhas e espaços extras
    value = value.replace("\r\n", " ").replace("\n", " ").replace("\r", " ")
    value = " ".join(value.split())
    
    #corta se passar do limite
    if len(value) > length:
        value = value[:length]  # corta se passar
        
    return value.ljust(length, fill) if align == "left" else value.rjust(length, fill)

def export_fixed_width(df, layout, output_file):
    df.columns = df. columns.str.strip()
    with open(output_file, "w", encoding="utf-8") as f:
        for _, row in df.iterrows():
            line = "".join(
                format_field(row[l["col"]], l["length"], l["align"], l["fill"], col_name=l["col"]) 
                for l in layout)
            f.write(line + "\n")

# Exemplo: lendo do Excel
df = pd.read_excel("E670LOCteste.xlsx")

# Gera TXT novo no formato fixo
export_fixed_width(df, layout, "testeE670LOC.txt")
print("txt gerado com sucesso!")

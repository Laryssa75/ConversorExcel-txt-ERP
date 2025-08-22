import pandas as pd


#Layout: nome da coluna no Excel + largura + alinhamento + preenchimento
layout = [
    {"col": "EMPRESA", "length": 4, "align": "right", "fill": " "},
    {"col": "COD LOCAL", "length": 9, "align": "left", "fill": " "},
    {"col": "NOME DO LOCAL", "length": 25, "align": "left", "fill": " "},
    {"col": "RESPONSAVEL",  "length": 10, "align": "right", "fill": " "},
    {"col": "DESCRICAO DO LOCAL",  "length": 80, "align": "left", "fill": " "},
    {"col": "PERMITE EMPRESTIMO",  "length": 5, "align": "left", "fill": " "},
    {"col": "FILIAL",  "length": 1, "align": "left", "fill": " "},
    {"col": "APLICACAO",  "length": 1, "align": "right", "fill": " "},
    {"col": "SITUACAO",  "length": 1, "align": "right", "fill": " "},
]

def format_field(value, length, align, fill):
    value = str(value) if pd.notna(value) else ""
    value = value.replace("\r\n", " ").replace("\n", " ").replace("\r", " ")
    value = " ".join(value.split())
    
    if len(value) > length:
        value = value[:length]  # corta se passar
        
    return value.ljust(length, fill) if align == "left" else value.rjust(length, fill)

def export_fixed_width(df, layout, output_file):
    df.columns = df. columns.str.strip()
    with open(output_file, "w", encoding="utf-8") as f:
        for _, row in df.iterrows():
            line = "".join(
                format_field(row[l["col"]], l["length"], l["align"], l["fill"]) 
                for l in layout)
            f.write(line + "\n")

# Exemplo: lendo do Excel
df = pd.read_excel("testelaryssa.xlsx")

# Gera TXT novo no formato fixo
export_fixed_width(df, layout, "teste1.txt")
print("txt gerado com sucesso!")

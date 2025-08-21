import pandas as pd

# Layout: nome da coluna no Excel + largura + alinhamento + preenchimento
layout = [
    {"col": "codigo", "length": 5, "align": "left", "fill": " "},
    {"col": "nome",   "length": 20, "align": "left", "fill": " "},
    {"col": "valor",  "length": 10, "align": "right", "fill": "0"},
]

def format_field(value, length, align, fill):
    value = str(value) if pd.notna(value) else ""
    if len(value) > length:
        value = value[:length]  # corta se passar
    if align == "left":
        return value.ljust(length, fill)
    else:
        return value.rjust(length, fill)

def export_fixed_width(df, layout, output_file):
    with open(output_file, "w", encoding="utf-8") as f:
        for _, row in df.iterrows():
            line = "".join(format_field(row[l["col"]], l["length"], l["align"], l["fill"]) for l in layout)
            f.write(line + "\n")

# Exemplo: lendo do Excel
df = pd.read_excel("dados.xlsx")

# Gera TXT no formato fixo
export_fixed_width(df, layout, "saida.txt")

import pandas as pd

# Layout usado também na leitura
layout = [
    {"col": "COD LOCAL", "length": 8},
    {"col": "NOME DO LOCAL", "length": 31},
    {"col": "RESPONSAVEL", "length": 1},
    {"col": "DESCRICAO DO LOCAL", "length": 80},
    {"col": "PERMITE EMPRESTIMO", "length": 2},
    {"col": "FILIAL", "length": 4},
    {"col": "APLICACAO", "length": 1},
    {"col": "SITUACAO", "length": 1},
]

def import_fixed_width(input_file, layout):
    col_names = [l["col"] for l in layout]
    col_widths = [l["length"] for l in layout]

    data = []
    with open(input_file, "r", encoding="utf-8") as f:
        for line in f:
            pos = 0
            row = {}
            for name, width in zip(col_names, col_widths):
                raw_value = line[pos:pos+width]
                row[name] = raw_value.strip()  # remove espaços extras
                pos += width
            data.append(row)
    
    return pd.DataFrame(data, columns=col_names)

# Ler do TXT
df = import_fixed_width("conferenciaLocais.txt", layout)

# Exportar para Excel
df.to_excel("testeExcel.xlsx", index=False)

print("Excel gerado com sucesso!")

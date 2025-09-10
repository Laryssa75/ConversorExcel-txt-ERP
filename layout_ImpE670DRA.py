import pandas as pd
import locale

#Define o padrão brasileiro
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')


#Layout: nome da coluna no Excel + largura + alinhamento + preenchimento
layout = [
    {"col": "EMPRESA", "length": 4, "align": "right", "fill": " "},
    {"col": "CODIGO BEM", "length": 20, "align": "left", "fill": " "},
    {"col": "DATA LOC", "length": 10, "align": "left", "fill": " "},
    {"col": "SEQ LOCALIZACAO",  "length": 5, "align": "right", "fill": " "},
    {"col": "COD C CUSTO",  "length": 9, "align": "left", "fill": " "}, 
    {"col": "PERC RATEIO",  "length": 9, "align": "left", "fill": " "}, 
]

#lista de colunas que devem ser formatadas como data
date_columns = ["DATA LOC"]

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
                
        elif col_name == "PERC RATEIO":
            try:
                num = float(value)
                
                #outra forma de converter para o padrão de numero brasileiro (testar depois)
                # value = locale.format_string("%.2f", num, grouping=True)
                
                #formata com 4 casas decimais fixas
                formatted = f"{abs(num):.4f}" #sempre positivo nesse passo
                
                #separa parte inteira e decimal
                inteiro, decimal = formatted.split(".")
                
                #garante 3 digitos na parte inteira (preenchendo com zeros à esquerda)
                inteiro = inteiro.zfill(3)
                
                #remonta no formato brasileiro
                value = f"{'-' if num < 0 else '' }{inteiro},{decimal}"
                
            except Exception:
                value = str(value)
    
    
    value = str(value).strip()
             
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
df = pd.read_excel("E670DRAteste.xlsx")

# Gera TXT novo no formato fixo
export_fixed_width(df, layout, "testeE670LOC.txt")
print("txt gerado com sucesso!")

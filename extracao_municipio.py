import pandas as pd

FI_ANO = 2021

print("Extraindo")

# Caminho do arquivo CSV original
input_file = f'Dados/{FI_ANO}/microdados_ed_basica_{FI_ANO}.csv'

# Código IBGE de Maracanaú
codigo_municipio = 2307650

# Ler o arquivo
df = pd.read_csv(input_file, sep=';', encoding='latin-1', engine='python', on_bad_lines='skip')

# Filtrar pelo código do município
filtered_df = df[df['CO_MUNICIPIO'] == codigo_municipio]


# Salvar apenas os dados filtrados em CSV
output_file = f'Dados/{FI_ANO}/ESCOLAS_MARACANAU.CSV'
filtered_df.to_csv(output_file, index=False, sep=',', encoding='latin-1')

print("Concluído")


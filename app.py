import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Função para carregar dados de um ano específico
@st.cache_data
def get_data(FI_ANO, CO_MUNICIPIO, TP_DEPENDENCIA, TP_SITUACAO):
    ds = pd.read_csv(f'Dados/{FI_ANO}/ESCOLAS_MARACANAU.CSV', sep=',', encoding='latin1')
    df = ds[(ds['CO_MUNICIPIO'] == CO_MUNICIPIO) &
            (ds['TP_DEPENDENCIA'] == TP_DEPENDENCIA) &
            (ds['TP_SITUACAO_FUNCIONAMENTO'] == TP_SITUACAO)]

    # Substituições
    df['TP_DEPENDENCIA'] = df['TP_DEPENDENCIA'].replace(3, 'MUNICIPAL')
    df['TP_SITUACAO_FUNCIONAMENTO'] = df['TP_SITUACAO_FUNCIONAMENTO'].replace(1, 'EM ATIVIDADE')
    df['TP_LOCALIZACAO'] = df['TP_LOCALIZACAO'].replace({1: 'URBANA', 2: 'RURAL'})
    df['TP_OCUPACAO_PREDIO_ESCOLAR'] = df['TP_OCUPACAO_PREDIO_ESCOLAR'].replace({1: 'PROPRIO', 2: 'ALUGADO', 3: 'CEDIDO'})

    return ds, df

# Função para relatório com gráfico
def relatorio(df, variavel, nome):
    df_rel = df[df[variavel].fillna(0) != 1][['NU_ANO_CENSO', 'CO_MUNICIPIO', 'NO_ENTIDADE', 'TP_LOCALIZACAO', 'TP_OCUPACAO_PREDIO_ESCOLAR']]
    st.table(df_rel)
    total = df['NO_ENTIDADE'].count()
    qtd = df_rel['NO_ENTIDADE'].count()
    perc = round((qtd / total) * 100, 2) if total > 0 else 0
    st.write(f"**Total**: {qtd} de {total} ({perc}%)")

    # Gráfico de barras
    fig, ax = plt.subplots()
    ax.bar(['Com', 'Sem'], [total - qtd, qtd], color=['green', 'red'])
    ax.set_title(nome)
    ax.set_ylabel('Número de escolas')
    st.pyplot(fig)

    # Download CSV
    st.download_button(
        label="Exportar CSV",
        data=df_rel.to_csv(index=False),
        file_name=f"{nome}.csv",
        mime="text/csv"
    )

# Função para gráfico de evolução temporal
def grafico_evolucao(variavel, nome, CO_MUNICIPIO, TP_DEPENDENCIA, TP_SITUACAO):
    anos = [str(ano) for ano in range(2015, 2025)]
    proporcoes = []

    for ano in anos:
        ds_ano = pd.read_csv(f'Dados/{ano}/ESCOLAS_MARACANAU.CSV', sep=',', encoding='latin1')
        df_ano = ds_ano[(ds_ano['CO_MUNICIPIO'] == CO_MUNICIPIO) &
                        (ds_ano['TP_DEPENDENCIA'] == TP_DEPENDENCIA) &
                        (ds_ano['TP_SITUACAO_FUNCIONAMENTO'] == TP_SITUACAO)]
        total = df_ano['NO_ENTIDADE'].count()
        sem_recurso = df_ano[df_ano[variavel].fillna(0) != 1]['NO_ENTIDADE'].count()
        proporcao = round((sem_recurso / total) * 100, 2) if total > 0 else 0
        proporcoes.append(proporcao)

    # Gráfico de linha
    fig, ax = plt.subplots()
    ax.plot(anos, proporcoes, marker='o', color='blue')
    ax.set_title(f"Evolução: {nome} (2015-2024)")
    ax.set_xlabel("Ano")
    ax.set_ylabel("% de escolas sem recurso")
    ax.grid(True)
    st.pyplot(fig)

# Sidebar
st.sidebar.subheader("Filtros")
NM_MUNICIPIO = st.sidebar.selectbox("MUNICÍPIO:", ["MARACANAÚ"])

if NM_MUNICIPIO == "MARACANAÚ":
    CO_MUNICIPIO = 2307650
    TP_DEPENDENCIA = 3  # Municipal
    TP_SITUACAO = 1     # Em atividade

    FI_BASE = st.sidebar.selectbox("BASE:", ['CENSO ESCOLAR', 'IDEB', 'ANA', 'SPAECE'])

    if FI_BASE == 'CENSO ESCOLAR':
        FI_DIMENSAO = st.sidebar.selectbox("DIMENSÃO:", ['INFRAESTRUTURA', 'RAÇA', 'NÍVEL SÓCIO-ECONÔMICO', 'COMPLEXIDADE DA GESTÃO'])

        if FI_DIMENSAO == 'INFRAESTRUTURA':
            FI_ANO = st.sidebar.selectbox("ANO:", [str(ano) for ano in range(2024, 2014, -1)])

            # Carregar dados
            ds, df = get_data(FI_ANO, CO_MUNICIPIO, TP_DEPENDENCIA, TP_SITUACAO)

            # Lista de análises
            analise = [
                ['IN_AGUA_REDE_PUBLICA', 'ESCOLAS SEM ÁGUA REDE PÚBLICA'],
                ['IN_ESGOTO_REDE_PUBLICA', 'ESCOLAS SEM ESGOTO REDE PÚBLICA'],
                ['IN_ESGOTO_FOSSA', 'ESCOLAS COM ESGOTO FOSSA'],
                ['IN_LABORATORIO_CIENCIAS', 'ESCOLAS SEM LABORATÓRIO DE CIÊNCIAS'],
                ['IN_LABORATORIO_INFORMATICA', 'ESCOLAS SEM LABORATÓRIO DE INFORMÁTICA'],
                ['IN_AUDITORIO', 'ESCOLAS SEM AUDITÓRIO'],
                ['IN_ALMOXARIFADO', 'ESCOLAS SEM ALMOXARIFADO'],
                ['IN_BANHEIRO_PNE', 'ESCOLAS SEM BANHEIRO PNE']
            ]

            fonte = "INEP"

# Interface principal
st.title("Análise Exploratória de Dados Educacionais")
st.markdown(f'Fonte: {fonte}')

# Criando lista de opções
op = [item[1] for item in analise]

# Selectbox para análise
tp_analise = st.selectbox("Selecione a análise:", op)

# Executando análise escolhida
for i in range(len(analise)):
    if tp_analise == analise[i][1]:
        relatorio(df, analise[i][0], analise[i][1])
        st.subheader("Evolução no período 2015-2024")
        grafico_evolucao(analise[i][0], analise[i][1], CO_MUNICIPIO, TP_DEPENDENCIA, TP_SITUACAO)

# Rodapé
st.sidebar.markdown('---')
st.sidebar.markdown('Autores')
st.sidebar.markdown('**Lívia Julyana G. V. Lira, Dra.**')
st.sidebar.markdown('Doutora em Educação')
st.sidebar.markdown('**Daniel Gleison M. Lira, Me.**')
st.sidebar.markdown('Mestre em Ciência da Computação')















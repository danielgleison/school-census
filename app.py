import pandas as pd
import streamlit as st

# Função para carregar o dataset
@st.cache_data
def get_data(FI_ANO):
    CO_MUNICIPIO = 2307650
    TP_DEPENDENCIA = 3  # Municipal
    TP_SITUACAO = 1     # Em atividade

    ds = pd.read_csv(f'Dados/{FI_ANO}/ESCOLAS_MARACANAU.CSV', sep=',', encoding='latin1')
    df = ds[(ds['CO_MUNICIPIO'] == CO_MUNICIPIO) & (ds['TP_DEPENDENCIA'] == TP_DEPENDENCIA) & (ds['TP_SITUACAO_FUNCIONAMENTO'] == TP_SITUACAO)]

    # Substituições
    df['TP_DEPENDENCIA'].replace(3, 'MUNICIPAL', inplace=True)
    df['TP_SITUACAO_FUNCIONAMENTO'].replace(1, 'EM ATIVIDADE', inplace=True)
    df['TP_LOCALIZACAO'].replace({1: 'URBANA', 2: 'RURAL'}, inplace=True)
    df['TP_OCUPACAO_PREDIO_ESCOLAR'].replace({1: 'PROPRIO', 2: 'ALUGADO', 3: 'CEDIDO'}, inplace=True)
    df['IN_COMUM_FUND_AF'].replace({0: 'NAO', 1: 'SIM'}, inplace=True)

    return ds, df

# Sidebar
st.sidebar.subheader("Filtros")
analise = []
fonte = ''
NM_MUNICIPIO = st.sidebar.selectbox("MUNICÍPIO:", ["MARACANAU"])

if NM_MUNICIPIO == "MARACANAU": 
    
    FI_BASE = st.sidebar.selectbox("BASE:", ['CENSO ESCOLAR','IDEB','ANA','SPAECE'])

    if FI_BASE == 'CENSO ESCOLAR':
    
        #FI_DIMENSAO = st.sidebar.selectbox("DIMENSÃO:", ['INFRAESTRUTURA','RAÇA','NÍVEL SÓCIO-ECONÔMICO','COMPLEXIDADE DA GESTÃO','DISTORÇAO SÉRIE-IDADE','APROVAÇÃO','REPROVAÇÃO','TAXA DE PARTICIPAÇÃO'])
        FI_DIMENSAO = st.sidebar.selectbox("DIMENSÃO:", ['INFRAESTRUTURA','RAÇA','NÍVEL SÓCIO-ECONÔMICO','COMPLEXIDADE DA GESTÃO'])
    
        if FI_DIMENSAO == 'INFRAESTRUTURA':
        
            FI_ANO = st.sidebar.selectbox("ANO:", ['2020','2019','2018','2017','2016','2015'])
            
        
            # Carregar dados
            ds, df = get_data(FI_ANO)
            
            # Função para relatório
            def relatorio(ano, variavel, nome, botao):
                df_rel = df[df[variavel] != 1][['NU_ANO_CENSO','CO_MUNICIPIO','NO_ENTIDADE','TP_LOCALIZACAO','TP_OCUPACAO_PREDIO_ESCOLAR']]
                st.table(df_rel)
                st.write(f"**Total**: {df_rel['NO_ENTIDADE'].count()} de {df['NO_ENTIDADE'].count()} ({round(df_rel['NO_ENTIDADE'].count()/df['NO_ENTIDADE'].count()*100,2)}%)")
            
                # Download seguro com Streamlit
                st.download_button(
                    label="Exportar CSV",
                    data=df_rel.to_csv(index=False),
                    file_name=f"{nome}.csv",
                    mime="text/csv"
                )
            
            # Lista de análises
            analise = [
                ['IN_AGUA_REDE_PUBLICA','ESCOLAS SEM AGUA REDE PUBLICA'],
                ['IN_ESGOTO_REDE_PUBLICA','ESCOLAS SEM ESGOTO REDE PUBLICA'],
                ['IN_ESGOTO_FOSSA','ESCOLAS COM ESGOTO FOSSA'],
                ['IN_LABORATORIO_CIENCIAS','ESCOLAS COM LABORATÓRIO DE CIÊNCIAS'],
                ['IN_LABORATORIO_INFORMATICA','ESCOLAS SEM LABORATÓRIO DE CIÊNCIAS'],
                ['IN_AUDITORIO','ESCOLAS COM AUDITORIO'],
                ['IN_ALMOXARIFADO','ESCOLAS SEM ALMOXARIFADO'],
                ['IN_BANHEIRO_PNE','ESCOLAS SEM BANHEIRO PNE']
            ]
        
            fonte = "INEP"

# Interface principal
st.title("Análise Exploratória de Dados Educacionais")
st.markdown(f'Fonte: {fonte}')

# Criando lista de opções
op = []
for i in range(len(analise)):
    op.append(analise[i][1])

# Selectbox
tp_analise = st.selectbox("Selecione a análise:", op)

# Executando análise escolhida
for i in range(len(analise)):
    if tp_analise == analise[i][1]:
        relatorio(FI_ANO, analise[i][0], analise[i][1], i + 1)

# Rodapé
st.sidebar.markdown('---')
st.sidebar.markdown('**Lívia Julyana G. V. Lira, Dra.**')
st.sidebar.markdown('Doutora em Educação')
st.sidebar.markdown('**Daniel Gleison M. Lira, Me.**')
st.sidebar.markdown('Mestre em Ciência da Computação')











































import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import time
import base64

# função para carregar o dataset
@st.cache(allow_output_mutation=True)
def get_data(FI_ANO):

    CO_MUNICIPIO = 2307650
    TP_DEPENDENCIA = 3 # Municipal
    TP_SITUACAO = 1 #Em atividade

    ds = pd.read_csv(f'http://dgautomacao.com.br/app/censo/dados/{FI_ANO}/ESCOLAS.CSV', 
                    sep = '|', 
                    encoding = 'latin1', 
                    decimal = ",")
                    
    df = ds[(ds['CO_MUNICIPIO'] == CO_MUNICIPIO) & (ds['TP_DEPENDENCIA'] == TP_DEPENDENCIA) & (ds['TP_SITUACAO_FUNCIONAMENTO'] == TP_SITUACAO)]
    
    df['TP_DEPENDENCIA'].replace(3, 'MUNICIPAL',inplace=True)
    df['TP_SITUACAO_FUNCIONAMENTO'].replace(1, 'EM ATIVIDADE',inplace=True)

    df['TP_LOCALIZACAO'].replace(1, 'URBANA',inplace=True)
    df['TP_LOCALIZACAO'].replace(2, 'RURAL',inplace=True)
    df['TP_OCUPACAO_PREDIO_ESCOLAR'].replace(1, 'PROPRIO',inplace=True)
    df['TP_OCUPACAO_PREDIO_ESCOLAR'].replace(2, 'ALUGADO',inplace=True)
    df['TP_OCUPACAO_PREDIO_ESCOLAR'].replace(3, 'CEDIDO',inplace=True)
    df['IN_COMUM_FUND_AF'].replace(0, 'NAO',inplace=True)
    df['IN_COMUM_FUND_AF'].replace(1, 'SIM',inplace=True)

    return ds, df



st.sidebar.subheader("Filtros")

# mapeando dados do usuário para cada atributo
FI_ANO =  st.sidebar.selectbox("ANO:", ['2020','2019'])
In2 =  st.sidebar.selectbox("UF:",["CE"])
In3 =  st.sidebar.selectbox("MUNICÍPIO:",["MARACANAU"])
In4 =  st.sidebar.selectbox("DEPENDÊNCIA:",["MUNICIPAL"])
In5 =  st.sidebar.selectbox("SITUAÇÃO:",["EM ATIVIDADE"])

# criando um dataframe
ds, df = get_data(FI_ANO)

def get_download(df, arq):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode() 
    href = f'<a href="data:file/csv;base64,{b64}" download="'+arq+'.csv">Download</a>'
    return href

# título
st.title("Análise Exploratória do Censo Escolar")
#######df['nova_descricao'] = df['descricao'].copy()

def relatorio(ano,variavel, nome, botao):
    st.write(nome)
    df_rel = df[(df[variavel] != 1)][['NU_ANO_CENSO','NO_ENTIDADE','TP_LOCALIZACAO','TP_OCUPACAO_PREDIO_ESCOLAR']]
    st.table(df_rel)
    st.write('**Total**:',df_rel['NO_ENTIDADE'].count(),'(',round(df_rel['NO_ENTIDADE'].count()/df['NO_ENTIDADE'].count()*100,2),'%)')       
    
    if st.button("Exportar CSV",botao):
        st.markdown(get_download(df_rel, nome), unsafe_allow_html=True)   

relatorio(FI_ANO,'IN_AGUA_REDE_PUBLICA','**ESCOLAS SEM AGUA REDE PUBLICA**',1)
relatorio(FI_ANO,'IN_ESGOTO_REDE_PUBLICA','**ESCOLAS SEM ESGOTO REDE PUBLICA**',2)
relatorio(FI_ANO,'IN_ESGOTO_FOSSA','**ESCOLAS COM ESGOTO FOSSA**',3)
relatorio(FI_ANO,'IN_LABORATORIO_CIENCIAS','**ESCOLAS COM LABORATÓRIO DE CIÊNCIAS**',4)
relatorio(FI_ANO,'IN_LABORATORIO_INFORMATICA','**ESCOLAS SEM LABORATÓRIO DE CIÊNCIAS**',5)
relatorio(FI_ANO,'IN_AUDITORIO','**ESCOLAS COM AUDITORIO**',6)
relatorio(FI_ANO,'IN_ALMOXARIFADO','**ESCOLAS SEM ALMOXARIFADO**',7)
relatorio(FI_ANO,'IN_BANHEIRO_PNE','**ESCOLAS SEM BANHEIRO PNE**',8)

st.sidebar.markdown('---')
st.sidebar.markdown('**Daniel Gleison M. Lira**')
st.sidebar.markdown('Mestrado em Ciências da Computação')
st.sidebar.markdown('Universidade Estadual do Ceará')
st.sidebar.markdown('mailto:daniel.gleison@aluno.uece.br')
st.sidebar.markdown('**Lívia Julyana Lira **')
st.sidebar.markdown('Doutorado em Educação')
st.sidebar.markdown('Universidade Estadual do Ceará')
st.sidebar.markdown('mailto:livia.liran@aluno.uece.br')




# -*- coding: utf-8 -*-
# %%
# Instalando e carregando bibliotecas necessárias

# !pip install psycopg2-binary sqlalchemy

import pandas as pd
from sqlalchemy import create_engine
from urllib.parse import quote_plus # Necessário para codificar a senha de forma segura

# %%
# -----------------------------------------------------------
# FASE 1: CARREGAMENTO INICIAL DOS DADOS
# -----------------------------------------------------------

# Carregamento dos dados a partir do arquivo CSV
df = pd.read_csv("customer_shopping_behavior.csv")
# Visualização das primeiras linhas do DataFrame para inspeção inicial
df.head()

# %%
# -----------------------------------------------------------
# FASE 2: ANÁLISE DE DADOS E TRATAMENTO DE VALORES AUSENTES
# -----------------------------------------------------------

# Estatísticas resumidas (forçando a inclusão de colunas categóricas)
# Isso ajuda a identificar a contagem, valores únicos, e o valor mais frequente (top)
# para colunas do tipo 'object' e 'category', além das estatísticas para numéricas
df.describe(include='all')

# %%

# Verificar colunas com valores missing (nulos)
# .isnull() retorna um booleano (True para nulo), e .sum() soma esses True (que valem 1)
df.isnull().sum()

# %%

# Corrigindo e preparando 'Review Rating' para imputação
# 1. Convertendo a coluna para tipo numérico. O parâmetro 'errors = coerce'
# força valores não-numéricos (que parecem ser espaços em branco ou texto) a se tornarem NaN (Not a Number),
# o que permite o cálculo correto de mediana/média
df['Review Rating'] = pd.to_numeric(df['Review Rating'], errors='coerce')

# Calculando a mediana e a média para referência, antes da imputação.
df['Review Rating'].agg(['median', 'mean'])

# %%

# 2. Imputando valores nulos em 'Review Rating' pela mediana, agrupada por 'Category'
# Essa é uma estratégia de imputação mais robusta, pois assume que o rating
# depende do tipo de produto (Category), usando a mediana específica daquele grupo
df['Review Rating'] = df.groupby('Category')['Review Rating'].transform(lambda x: x.fillna(x.median()))

# Visualiza as colunas 'Category' e 'Review Rating' (com valores imputados)
df[['Category', 'Review Rating']].head(10)

# %%
# -----------------------------------------------------------
# FASE 3: PADRONIZAÇÃO E CRIAÇÃO DE NOVAS FEATURES
# -----------------------------------------------------------

# Padronização os nomes das colunas para snake_case (minúsculas e separadas por underscore)
df.columns = df.columns.str.lower()
df.columns = df.columns.str.replace(' ', '_')

# Renomeia a coluna específica com caracteres especiais
df = df.rename(columns={'purchase_amount_(usd)': 'purchase_amount'})

# Exibe os novos nomes das colunas para verificação
pd.Series(df.columns)

# %%

# Criação da coluna de faixa etária ('age_group') usando quantis (quartis)
# pd.qcut divide a coluna 'age' em 4 grupos com o mesmo número de observações (quartis)
labels = ['young_adult', 'adult', 'middle-aged', 'senior'] # Labels em snake_case para padronização
df['age_group'] = pd.qcut(df['age'], q=4, labels=labels, precision=0) # precision=0 evita nomes de bin com muitas casas decimais

# Visualiza a comparação entre 'age' e 'age_group'
df[['age', 'age_group']]

# %%

# Criação da coluna de frequência de compras em dias ('purchase_frequency_days')
# Mapeia as categorias de frequência para valores numéricos em dias
frequency_mapping = {
    'fortnightly': 14,
    'weekly': 7,
    'monthly': 30,
    'quarterly': 90,
    'bi-weekly': 14,
    'annually': 365,
    'every 3 months': 90,
}

# A coluna de frequência é convertida para minúsculas antes do mapeamento para garantir consistência
df['purchase_frequency_days'] = df['frequency_of_purchases'].str.lower().str.strip().map(frequency_mapping).astype(int)

# Visualiza a comparação entre 'frequency_of_purchases' e 'purchase_frequency_days'
df[['frequency_of_purchases', 'purchase_frequency_days']]

# %%

# Análise de equivalência e remoção de redundância
# Verifica se a aplicação de desconto e o uso de código promocional são 100% equivalentes
print(f"Colunas são 100% equivalentes: {(df['discount_applied'] == df['promo_code_used']).all()}")

# Se forem equivalentes (True), remove-se uma para evitar redundância (multicolinearidade)
df = df.drop('promo_code_used', axis=1).copy()

# %%

# Agrupando 'location' (estados dos EUA) por região ('region')
# Cria um dicionário de mapeamento de estado para região
region_mapping = {
    'alabama': 'south', 'alaska': 'west', 'arizona': 'west', 'arkansas': 'south',
    'california': 'west', 'colorado': 'west', 'connecticut': 'northeast', 'delaware': 'south',
    'florida': 'south', 'georgia': 'south', 'hawaii': 'west', 'idaho': 'west',
    'illinois': 'midwest', 'indiana': 'midwest', 'iowa': 'midwest', 'kansas': 'midwest',
    'kentucky': 'south', 'louisiana': 'south', 'maine': 'northeast', 'maryland': 'south',
    'massachusetts': 'northeast', 'michigan': 'midwest', 'minnesota': 'midwest', 'mississippi': 'south',
    'missouri': 'midwest', 'montana': 'west', 'nebraska': 'midwest', 'nevada': 'west',
    'new hampshire': 'northeast', 'new jersey': 'northeast', 'new mexico': 'west', 'new york': 'northeast',
    'north carolina': 'south', 'north dakota': 'midwest', 'ohio': 'midwest', 'oklahoma': 'south',
    'oregon': 'west', 'pennsylvania': 'northeast', 'rhode island': 'northeast', 'south carolina': 'south',
    'south dakota': 'midwest', 'tennessee': 'south', 'texas': 'south', 'utah': 'west',
    'vermont': 'northeast', 'virginia': 'south', 'washington': 'west', 'west virginia': 'south',
    'wisconsin': 'midwest', 'wyoming': 'west'
}

# Mapeia a coluna 'location' (que já foi padronizada para minúsculas e sem espaços) para a nova coluna 'region'
df['region'] = df['location'].map(region_mapping)

# %%
# -----------------------------------------------------------
# FASE 4: OTIMIZAÇÃO E PREPARAÇÃO FINAL PARA SQL
# -----------------------------------------------------------

# Otimização para SQL

# 1. Padronização final das colunas de texto (limpa espaços e converte para minúsculas)
# Esta etapa é crucial para garantir que GROUP BYs em SQL não falhem devido a diferenças de case ou espaços
text_cols = df.select_dtypes(include='object').columns

for col in text_cols:
    df[col] = df[col].str.strip().str.lower()

# 2. Otimização colunas categóricas para tipo 'category' do Pandas
# Isso reduz o uso de memória e é eficiente para o carregamento em bancos de dados
category_cols = [
    'gender', 'item_purchased', 'category', 'location', 'size', 'color',
    'season', 'subscription_status', 'shipping_type', 'discount_applied',
    'payment_method', 'frequency_of_purchases', 'region', 'age_group'
]
df[category_cols] = df[category_cols].astype('category')

# %%
# -----------------------------------------------------------
# FASE 5: CONEXÃO E CARREGAMENTO NO POSTGRESQL
# -----------------------------------------------------------

# Conexão com o PostGreeSQL

# É necessário que o database ('customer_behavior') já tenha sido criado no seu servidor PostgreSQL

# Configuração das credenciais do banco de dados
username = "your_username" # Substitua pelo seu nome de usuário do PostgreSQL
password_raw = "your_password" # Substitua pela sua senha
host = "localhost" # Endereço do servidor (pode ser '127.0.0.1' ou o nome do host)
port = "5432" # Porta padrão do PostgreSQL
database = "customer_behavior" # Nome do banco de dados

# Codifica a senha para lidar com caracteres especiais (como #, $, % ou @)
password_encoded = quote_plus(password_raw)

# A string de conexão usa a senha codificada e o driver psycopg2
engine = create_engine(f"postgresql+psycopg2://{username}:{password_encoded}@{host}:{port}/{database}")

# Carregar o DataFrame 'df' (já limpo e transformado) no PostgreSQL
table_name = "customer"

try:
    # Usa o método to_sql do Pandas para carregar os dados
    # if_exists='replace': Se a tabela existir, ela será deletada e recriada
    # index=False: Não salva o índice do DataFrame como uma coluna no banco de dados
    df.to_sql(table_name, engine, if_exists='replace', index=False)
    print(f"Carregamento de dados na tabela feito com sucesso: '{table_name}' in '{database}'.")
except Exception as e:
    print(f"Erro ao carregar dados: {e}")

# O objeto 'engine' será automaticamente fechado quando sair do escopo ou pela finalização do script/notebook
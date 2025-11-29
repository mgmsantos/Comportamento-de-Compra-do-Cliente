# %%
# !pip install psycopg2-binary sqlalchemy
import pandas as pd
from sqlalchemy import create_engine

# %%

# Carregamento dos dados
df = pd.read_csv("customer_shopping_behavior.csv")
df.head()

# %%

# Estatísticas resumidas (forçando as categoricas)
df.describe(include = 'all')

# %%

# Verificar colunas com valores missing
df.isnull().sum()

# %%

# Corrigindo e preparando 'Review Rating' para imputação.
# 1. Convertendo a coluna para tipo numérico, forçando erros para NaN, o que permite o cálculo de mediana/média.
df['Review Rating'] = pd.to_numeric(df['Review Rating'], errors = 'coerce')

df['Review Rating'].agg(['median', 'mean'])

# %%

# 2. Imputando valores nulos em 'Review Rating' pela mediana, agrupada por 'Category'.
df['Review Rating'] = df.groupby('Category')['Review Rating'].transform(lambda x: x.fillna(x.median()))
df[['Category', 'Review Rating']].head(10)

# %%

# Padronizando os nomes das colunas para snake_case.
df.columns = df.columns.str.lower()
df.columns = df.columns.str.replace(' ', '_')
df = df.rename(columns = {'purchase_amount_(usd)':'purchase_amount'})
pd.Series(df.columns)

# %%

# Criando coluna de faixa etária ('age_group') usando quantis (quartis).
labels = ['Young Adult', 'Adult', 'Middle-aged', 'Senior']
df['age_group'] = pd.qcut(df['age'], q = 4, labels = labels)
df[['age', 'age_group']]

# %%

# Criação da coluna de frequência de compras em dias ('purchase_frequency_days').
# para garantir que todos os valores sejam mapeados corretamente, permitindo o .astype(int)
frequency_mapping = {
    'Fortnightly': 14,
    'Weekly': 7,
    'Monthly': 30,
    'Quarterly': 90,
    'Bi-Weekly': 14,
    'Annually': 365,
    'Every 3 Months': 90, # Mapeamento original (se houver)
}

df['purchase_frequency_days'] = df['frequency_of_purchases'].map(frequency_mapping).astype(int)
df[['frequency_of_purchases', 'purchase_frequency_days']]

# %%

# Análise de equivalência entre 'discount_applied' e 'promo_code_used'.
df[['discount_applied', 'promo_code_used']]

# Verificar se as duas colunas são 100% equivalentes (all)
print(f"Colunas são 100% equivalentes: {(df['discount_applied'] == df['promo_code_used']).all()}")

# remover uma das colunas: promo_code_used
df = df.drop('promo_code_used', axis = 1).copy()

# %%

# Agrupando 'location' (estados) por região dos EUA ('region').
region_mapping = {
    'Alabama': 'South', 'Alaska': 'West', 'Arizona': 'West', 'Arkansas': 'South',
    'California': 'West', 'Colorado': 'West', 'Connecticut': 'Northeast', 'Delaware': 'South',
    'Florida': 'South', 'Georgia': 'South', 'Hawaii': 'West', 'Idaho': 'West',
    'Illinois': 'Midwest', 'Indiana': 'Midwest', 'Iowa': 'Midwest', 'Kansas': 'Midwest',
    'Kentucky': 'South', 'Louisiana': 'South', 'Maine': 'Northeast', 'Maryland': 'South',
    'Massachusetts': 'Northeast', 'Michigan': 'Midwest', 'Minnesota': 'Midwest', 'Mississippi': 'South',
    'Missouri': 'Midwest', 'Montana': 'West', 'Nebraska': 'Midwest', 'Nevada': 'West',
    'New Hampshire': 'Northeast', 'New Jersey': 'Northeast', 'New Mexico': 'West', 'New York': 'Northeast',
    'North Carolina': 'South', 'North Dakota': 'Midwest', 'Ohio': 'Midwest', 'Oklahoma': 'South',
    'Oregon': 'West', 'Pennsylvania': 'Northeast', 'Rhode Island': 'Northeast', 'South Carolina': 'South',
    'South Dakota': 'Midwest', 'Tennessee': 'South', 'Texas': 'South', 'Utah': 'West',
    'Vermont': 'Northeast', 'Virginia': 'South', 'Washington': 'West', 'West Virginia': 'South',
    'Wisconsin': 'Midwest', 'Wyoming': 'West'
}

df['region'] = df['location'].map(region_mapping)

# %%

# OTIMIZAÇÃO FINAL PARA SQL: PADRONIZAÇÃO DE TEXTO E OTIMIZAÇÃO DE TIPOS

# 1. Padroniza colunas de texto (limpa espaços e converte para minúsculas)
# Isso garante que consultas GROUP BY em SQL não falhem por diferenças de case.
text_cols = df.select_dtypes(include = 'object').columns

for col in text_cols:
    df[col] = df[col].str.strip().str.lower()

# 2. Otimiza colunas categóricas para tipo 'category' (eficiência de memória e SQL)
category_cols = [
    'gender', 'item_purchased', 'category', 'location', 'size', 'color', 
    'season', 'subscription_status', 'shipping_type', 'discount_applied', 
    'payment_method', 'frequency_of_purchases', 'region', 'age_group'
]
df[category_cols] = df[category_cols].astype('category')

# %%

# %%

# CONEXÃO COM POSTGRESQL (CÓDIGO CORRIGIDO)

# É necessário importar create_engine do SQLAlchemy e a função quote_plus
# para codificar caracteres especiais na senha.
from sqlalchemy import create_engine
from urllib.parse import quote_plus

username = "your_username"
password_raw = "your_password"

# A senha é codificada para que o '@' não seja interpretado como separador de host
password_encoded = quote_plus(password_raw)

host = "localhost" ## verificar
port = "5432" # verificar
database = "customer_behavior"

# A string de conexão usa a senha codificada
engine = create_engine(f"postgresql+psycopg2://{username}:{password_encoded}@{host}:{port}/{database}")

# carregar o df no postgresql

table_name = "customer"
# NOTA: O DataFrame 'df' deve estar carregado na sua sessão antes de executar esta célula.
# Assume-se que 'df' é o DataFrame final limpo.
try:
    df.to_sql(table_name, engine, if_exists = 'replace', index = False)
    print(f"Carregamento de dados na tabela feito com sucesso: '{table_name}' in '{database}'.")
except Exception as e:
    print(f"Erro ao carregar dados: {e}")
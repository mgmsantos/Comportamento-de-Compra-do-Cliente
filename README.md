# Comportamento de compra do cliente

## Visão Geral do Projeto
Esse projeto representa um fluxo de trabalho completo de análise de dados, desenvolvido para simular responsabilidades reais de analistas em ambientes corporativos. O projeto passa por todas as etapas em análise de dados: preparação dos dados, criação de features, conexão entre plataformas e geração de insights por meio de consultas, visualização e relatórios.

---

## Sobre o dataset
O conjunto possui dados sobre hábitos de consumo de clientes em um comérico varejista do setor de moda: roupas e acessórios. O conjunto foi projetado visando realizar análises que possibilitem visualizar como diversos fatores influenciam decisões de compra, permitindo modelar o comportamento dos clientes e guiar decisões de negócio de forma estratégica e orientada por dados.
O dataset possui 3.900 linhas e 18 colunas, apresentando features, como:
- **Customer demographics:** `age`, `gender`, `location`, etc;
- **Purchase details:** `item purchased`, `category`, `purchase amount`, `season`, etc;
- **Shopping behavior:** `discout applied`, `promo code used`, `previous purchased`, `review rating`, etc.

Observação: há dados faltantes na coluna "Review Rating".

---

## Stack Técnico
- **Sistem Operacional:** Windows 10
- **Software:** VS Code | PostgreSQL | Power BI
- **Linguagem:** Python | SQL
- **Bibliotecas:** `pandas`

---

## Tratamento e Análise Exploratória dos Dados com Python

- **Padronização de colunas:** renomeção de colunas para **snake case** ("por_exemplo") para melhor legibilidade e execução das consultas;

- **Tratamento de dados faltantes:** checagem de valores faltantes e imputaçao de dados na coluna ``Review Rating`` usando a mediana das avaliações de acordo com a categoria dos protudos;

- **Criação de novas features:** agrupamento das idades dos clientes (age_group) e criação da coluna "purchase_frequency_days" a partir da frequência de compras;

- **Integração com PostgreSQL:** conexão Python-PostgreSQL com a função ``create_engine`` da biblioteca ``SQLAlchemy``.
---

## Análises de Dados com SQL (Business Intelligence)

### Resumo Executivo: Principais Insights

- **Público Principal:** os grupos Young Adult (26.7%) e Middle-aged (25.4%) possuem particição de 52.1% na receita total;

- **Satisfação do cliente:** o produto ``gloves`` possui a melhor avaliação geral, indicando maior satisfação do cliente;

- **Lealdade do cliente:** a base de clientes é predominantemente fiel, com 79.9% dos clientes com mais de 10 compras anteriores

- **Frete e Valor:** a modalidade ``2-day-shipping`` e ``express`` atraem compras com ticket médio superior às outras formas de envio

### I. Impacto Financeiro e Clientes de Alto Valor

**Objetivo:** analisar a distribuição de receita e o perfil dos clientes mais valiosos.

- **Dominância Etária:** a maior parte da receita (52.1%) é impulsionada pelos grupos ``Young Adult`` e ``Middle-aged``. Campanhas de marketing de alto valor devem ser direcionadas a esse segmento;

- **Eficiência do desconto:**

- **Eficiência da inscrição:** clientes inscritos e não inscritos possuem ticket médio de compra similar, contudo os não inscritos representam 73.1% da receita total e 92.7% dos clientes. É preciso investigar o motivo dos clientes não adquirirem a inscrição.


### II. Performance dos Produtos e Tendências Sazonais

**Objetivo:** focalizar quais produtos devem ser priorizados visando realizar o planejamento do estoque, assim como *merchandising*.

- **Qualidade e satisfação:** os produtos lideres em satisfação pelo cliente são ``gloves``, ``sandals`` e ``boots``, contudo se encontram com pontução menor que 4;

- **Visão sazonal:** os itens e cores ``hat peach``, ```shorts yellow``, ``scarf violet`` e ``sunglasses olive`` são os produtos mais adquiridos no outro, primavera, verão e inverno, respectivamente.

- **Efeito do desconto:** os produtos que mais dependem de desconto para fechar as vendas são: ``hat``, ``sneakers``, ``coat``, ``sweater`` e ``pants``, indicando que a margem pode ser mais apertada para esses itens.

### III. Fidelidade e Eficiência

**Objetivo:** analisar a saúde da base de clientes e a otimização de serviços de entrega e pagamento.

- **Segmentação de lealdade:** a base de clientes é majoritariamente classificada como ``Loyal``, com uma participação de 79.9%, validando as estratégias de retenção.

- **Métodos de pagamento:** o método de pagamento preferido corresponde a: ``Adult``: ``venmo``; ``Middle-aged``: ``paypal``; ``Senior``: ``credit card`` e ``Young Adult``: ``cash``.

- **Distribuição de receita:** o hotspot de receita para cada região está em: ``Illinois``, ``Nova York``, ``Alabama`` e ``Montana`` para Midweast, Northeast, South e West respectivamnete.

---

## Dashboard em Power BI
Na figura abaixo é possível visualizar o dashboard interativo confeccionado no Power BI, visando apresentar insights de forma visual:

<img title="dashboard_png" alt="Alt text" src="/dashboard_pbi_png.png">

---

## Conclusão e Recomendações

A análise dos dados demonstrou que a empresa possui uma **sólida base de clientes fiéis e recorrentes**, contudo enfrenta desafios em duas questões: **monetização de lealdade** e **otimização operacional**.

## Conclusão e Recomendações

O projeto demonstrou que a empresa possui uma **sólida base de clientes fiéis (79.9%)**, mas enfrenta desafios em duas frentes: **monetização da lealdade** e **otimização operacional**.

### Estratégias Recomendadas:

#### 1. Foco em Monetização e LTV (Valor de Vida do Cliente)

* **Programa de Assinaturas:** Apesar da alta fidelidade (79.9%), a baixa adesão à assinatura é uma oportunidade perdida. **Recomendação:** Criar ofertas exclusivas para a classe de clientes ``Loyal``, vinculando benefícios de frete (ex: Frete Expresso Gratuito) à adesão, convertendo fidelidade em receita recorrente.

* **Segmentação de Ticket:** Direcionar a introdução de produtos de alto valor aos grupos **Young Adult** e **Middle-aged**, que demonstram ser o *hotspot* de faturamento (52.1% da receita).

#### 2. Otimização da Margem e Qualidade de Produto

* **Análise de Desconto:** Redefinir as campanhas de desconto para itens de alta dependência (``hat``, ``sneakers``, ``coat``). **Recomendação:** Migrar descontos diretos para ofertas de pacote de produtos ou brindes, protegendo a margem de itens essenciais.

* **Capitalizar a Satisfação:** Utilizar os produtos de alta avaliação (``gloves``, ``sandals``, ``boots``) em promoções de aquisição de novos clientes ou para venda de produto superior, alavancando a confiança inicial.

#### 3. Excelência Operacional e Logística

* **Investimento em Frete e Satisfação do Cliente:** A modalidade ``2-day-shipping`` e ``Express`` atrai compras de maior valor. **Recomendação:** Auditar a performance dos parceiros de frete para essas modalidades nas regiões de maior receita (``Illinois``, ``Montana``), garantindo que o serviço de alta qualidade justifique o gasto superior do cliente.

---

## Conecte-se Comigo

*Siga os links abaixo para saber mais sobre minha trajetória profissional e me contatar:*

<div> 
  <a href="mailto:miguel.gms31@gmail.com"><img src="https://img.shields.io/badge/-Gmail-%23333?style=for-the-badge&logo=gmail&logoColor=white" target="_blank"></a>
  <a href="https://www.linkedin.com/in/miguelgms31/" target="_blank"><img src="https://img.shields.io/badge/-LinkedIn-%230077B5?style=for-the-badge&logo=linkedin&logoColor=white" target="_blank"></a>
  <a href="http://lattes.cnpq.br/2943203054995050" target="_blank"><img src="https://img.shields.io/badge/-Lattes-%230077B5?style=for-the-badge&logo=google-scholar&logoColor=white" target="_blank"></a>
</div>

Sinta-se à vontade para *favoritar* esse repositório com uma estrela e promor melhorias, abrir *issues* ou enviar *pull requests*!

---
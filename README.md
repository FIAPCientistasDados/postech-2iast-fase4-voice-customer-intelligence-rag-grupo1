# Postech Tech Challenge Fase 4 | Voice of Customer Intelligence com RAG: 

**Integrantes do Grupo (2IAST - Grupo1):**

✅ Célia Maria Tomitsuka - RM374490

✅ Nelson da Silva Paz - RM374983

✅ Nelson Toshikazu Yamamoto - RM374494

---

## 📋 Sumário

- [1. Introdução](#1-introdução)
- [2. Visão Geral da Solução](#2-visão-geral-da-solução)
- [3. Base de Dados](#3-base-de-dados)
- [4. Arquitetura da Solução](#4-arquitetura-da-solução)
- [5. Pipeline RAG](#5-pipeline-rag)
- [6. Tecnologias Utilizadas](#6-tecnologias-utilizadas)
- [7. Implementação](#7-implementação)
- [8. Respostas Baseadas em Evidências](#8-respostas-baseadas-em-evidências)
- [9. Tratamento de Alucinações](#9-tratamento-de-alucinações)
- [10. Resultados](#10-resultados)
- [11. Como Executar o Projeto](#11-como-executar-o-projeto)
- [12. Estrutura do Projeto](#12-estrutura-do-projeto)
- [13. Limitações e Trabalhos Futuros](#13-limitações-e-trabalhos-futuros)
- [14. Referências](#14-referências)
- [15. Entrega do projeto](#16-entrega-do-projeto)

---

# 1. Introdução

## Contextualização

Empresas de e-commerce recebem milhares de avaliações contendo informações valiosas sobre a experiência dos clientes. Apesar das notas ajudarem a medir satisfação, os principais insights estão nos comentários textuais.

Analisar manualmente milhares de avaliações é inviável. Dessa forma, técnicas de Inteligência Artificial Generativa e Retrieval-Augmented Generation (RAG) podem ser utilizadas para transformar esses comentários em uma base de conhecimento explorável.

## Objetivo

Desenvolver uma solução de Voice of Customer Intelligence capaz de:

- Recuperar avaliações relevantes;
- Responder perguntas em linguagem natural;
- Apresentar evidências que sustentem os insights;
- Evitar respostas sem suporte nos dados.

---

# 2. Visão Geral da Solução

A solução utiliza uma arquitetura baseada em RAG (Retrieval-Augmented Generation).

Fluxo geral:

```text
Pergunta
↓
Embedding da Pergunta
↓
Busca Semântica
↓
Recuperação das Avaliações
↓
Construção do Contexto
↓
LLM
↓
Resposta + Evidências
```

O sistema permite explorar a voz do cliente de forma rápida, escalável e fundamentada em evidências.

---

# 3. Base de Dados

## Download da Base

### Dataset

Brazilian E-Commerce Public Dataset by Olist

Acesse:

https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce

Baixe os arquivos e extraia para:

data/raw/


## Tabelas Utilizadas

| Tabela | Finalidade |
|----------|----------|
| olist_order_reviews_dataset | Comentários dos clientes |
| olist_orders_dataset | Informações dos pedidos |
| olist_products_dataset | Dados dos produtos |
| product_category_name_translation | Tradução das categorias |

## Critérios de Seleção

Foram utilizadas apenas avaliações contendo comentários textuais válidos.

Também foram considerados metadados relevantes como:

- Nota da avaliação;
- Categoria do produto;
- Data do pedido;
- Informações de entrega.

---

# 4. Arquitetura da Solução

## Arquitetura Geral

```text
Dataset Olist
       │
       ▼
Preparação dos Dados
       │
       ▼
Embeddings
       │
       ▼
ChromaDB
       │
       ▼
Retriever
       │
       ▼
LLM
       │
       ▼
Resposta + Evidências
```

## Componentes

### Camada de Dados

Responsável pela preparação e transformação das avaliações.

### Camada Vetorial

Responsável pelo armazenamento semântico dos documentos.

### Camada de Recuperação

Responsável pela busca das avaliações mais relevantes.

### Camada Generativa

Responsável pela geração da resposta fundamentada.

---

# 5. Pipeline RAG

## 1. Geração de Embeddings

Cada avaliação é convertida para representação vetorial.

## 2. Indexação Vetorial

Os vetores são armazenados no ChromaDB.

## 3. Recuperação Semântica

A pergunta do usuário é convertida em embedding.

São recuperadas as avaliações mais similares.

## 4. Construção do Contexto

As avaliações recuperadas são utilizadas como contexto para o modelo.

## 5. Geração da Resposta

O modelo gera a resposta utilizando exclusivamente o contexto recuperado.

---

# 6. Tecnologias Utilizadas

| Categoria | Tecnologia | Finalidade |
|------------|------------|------------|
| Linguagem | Python 3.12 | Desenvolvimento |
| Manipulação de Dados | Pandas | ETL e análise |
| Embeddings | Sentence Transformers | Vetorização |
| Modelo Embedding | BAAI/bge-m3 | Busca semântica |
| Banco Vetorial | ChromaDB | Armazenamento vetorial |
| Framework IA | LangChain | Pipeline RAG |
| LLM | GPT-4o-mini / Llama 3.1 | Geração das respostas |
| Frontend | Streamlit | Interface Web |
| Controle de Ambiente | Python Virtual Environment | Dependências |
| Versionamento | Git / GitHub | Controle do código |

---

# 7. Implementação

## Preparação da Base

Etapas realizadas:

- Remoção de valores nulos;
- Padronização dos textos;
- Criação dos documentos;
- Inclusão de metadados.

Exemplo de documento:

```text
Nota: 1

Categoria: Informática

Comentário:
Produto chegou atrasado e danificado.
```

## Armazenamento Vetorial

Cada documento recebe um embedding e é indexado no banco vetorial.

---

# 8. Respostas Baseadas em Evidências

Uma das premissas da solução é apresentar as evidências utilizadas na construção da resposta.

Exemplo:

### Resposta

Os principais problemas identificados estão relacionados a atrasos na entrega e produtos danificados.

### Evidências

- "produto chegou após o prazo informado"
- "caixa veio danificada"
- "entrega demorou mais de 20 dias"

---

# 9. Tratamento de Alucinações

Para evitar respostas incorretas:

- É utilizado limite mínimo de similaridade;
- Perguntas fora do contexto são rejeitadas;
- O sistema informa quando não existem com nota baixa?

## Benefícios Obtidos

- Recuperação semântica eficiente;
- Respostas contextualizadas;
- Evidências rastreáveis;
- Redução de alucinações.

---

# 11. Como Executar o Projeto

## Clonar Repositório

```bash
git clone <repositorio>
```

## Criar Ambiente Virtual

```bash
python -m venv .venv
```

## Ativar Ambiente

Windows:

```bash
.venv\Scripts\activate
```

Linux:

```bash
source .venv/bin/activate
```

## Instalar Dependências

```bash
pip install -r requirements.txt
```

## Executar Aplicação

```bash
streamlit run src/app/app.py
```

---

# 12. Estrutura do Projeto

```text
postech-2iast-fase4-voice-customer-intelligence-rag-grupo1/
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── vector_db/
│
├── docs/
│   ├── imagens/
│   └── [IAST] - Tech Challenge - Fase 4.pdf
│
├── notebooks/
│
├── reports/
│   ├── Dicionario_Dados.md
│
├── src/
│   ├── app/
│   ├── config/
│   ├── embeddings/
│   ├── preprocessing/
│   ├── rag/
│   ├── retrieval/
│   ├── vectorstore/
│   └── __init__.py
│
├── tests/
│
├── .env.EXAMPLE
│
├── environment.yml
│
├── Makefile
│
├── README.md
│
└── requirements.txt
```

---

# 13. Limitações e Trabalhos Futuros

## Limitações

- Dependência da qualidade das avaliações.
- Limitação do modelo de embeddings.
- Possibilidade de recuperar documentos parcialmente relevantes.

## Trabalhos Futuros

- Busca híbrida (BM25 + Vetorial);
- Re-ranking dos documentos;
- Dashboard analítico;
- Deploy em Azure;
- Avaliação automática das respostas.

---

# 14. Referências

- Kaggle - Brazilian E-Commerce Public Dataset by Olist
- LangChain Documentation
- ChromaDB Documentation
- Sentence Transformers Documentation
- OpenAI Documentation
- Streamlit Documentation

# 15. Entrega do projeto

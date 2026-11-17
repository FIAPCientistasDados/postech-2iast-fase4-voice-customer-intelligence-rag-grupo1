## Justificativa Técnica

Os modelos baseados em frequência de palavras, como TF-IDF, apresentam limitações para capturar relações semânticas, dependências de longa distância e contexto linguístico. Como demonstrado na Aula 06 da disciplina, arquiteturas baseadas em Attention e Transformers apresentam desempenho significativamente superior em tarefas que exigem compreensão contextual. Por esse motivo, a solução adota embeddings gerados pelo modelo BAAI/bge-m3 e recuperação vetorial via ChromaDB, permitindo consultas semânticas mais precisas no pipeline RAG.


## Relação entre a Aula 06 e o Tech Challenge

A Aula 06 demonstra, de forma prática, por que modelos baseados em Transformers são superiores a abordagens tradicionais baseadas em frequência de palavras para tarefas que dependem de contexto, significado e relações entre termos.

### Principais Aprendizados

1. **Transformers entendem contexto, não apenas palavras**
   
   Enquanto o TF-IDF trabalha apenas com frequência de termos, os Transformers conseguem identificar relações entre palavras distantes, negações, contrastes e dependências semânticas.

2. **Embeddings representam significado**

   O Transformer converte cada avaliação em um vetor numérico (embedding) que preserva o significado do texto. Dessa forma, avaliações semanticamente semelhantes ficam próximas no espaço vetorial.

3. **Busca semântica supera busca por palavras-chave**

   Consultas como "problemas de entrega" conseguem recuperar avaliações contendo expressões como "demorou muito", "fora do prazo" ou "transportadora atrasou", mesmo sem a palavra "entrega" aparecer explicitamente.

4. **Atenção (Attention) captura dependências longas**

   O experimento mostrou que estruturas linguísticas complexas, como negação de escopo, adversativas e anáforas, são tratadas adequadamente por Transformers, enquanto abordagens baseadas em TF-IDF apresentam queda significativa de desempenho.

5. **Embeddings são a base do pipeline RAG**

   O mesmo mecanismo que permitiu ao Transformer superar o TF-IDF na Aula 06 é utilizado no projeto para recuperar avaliações relevantes antes da geração da resposta pelo modelo de linguagem.

---

## Fluxo Técnico da Solução

### Construção da Base de Conhecimento

```text
Avaliações Olist
        │
        ▼
Limpeza e Tratamento
        │
        ▼
Documentos RAG
        │
        ▼
Transformer Encoder
(BAAI/bge-m3)
        │
        ▼
Embeddings
        │
        ▼
ChromaDB
        │
        ▼
Base Vetorial
```

### Execução de uma Consulta

```text
Pergunta do Usuário
        │
        ▼
Transformer Encoder
(BAAI/bge-m3)
        │
        ▼
Embedding da Pergunta
        │
        ▼
Busca Vetorial
(ChromaDB)
        │
        ▼
Top-K Avaliações Relevantes
        │
        ▼
Construção do Contexto
        │
        ▼
GPT-4o-mini
        │
        ▼
Resposta
        │
        ▼
Evidências Recuperadas
```

### Arquitetura Completa

```text
                    ┌─────────────────────┐
                    │ Avaliações Olist    │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Pré-processamento   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ BGE-M3              │
                    │ Transformer Encoder │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Embeddings          │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ ChromaDB            │
                    │ Base Vetorial       │
                    └──────────┬──────────┘
                               │
        ┌──────────────────────┼──────────────────────┐
        │                                             │
        ▼                                             ▼
Pergunta do Usuário                          Avaliações Vetorizadas
        │                                             │
        └──────────────────────┬──────────────────────┘
                               ▼
                    ┌─────────────────────┐
                    │ Similarity Search   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Top-K Evidências    │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ GPT-4o-mini         │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Resposta + Fontes   │
                    └─────────────────────┘
```

### Justificativa Técnica

A escolha de embeddings gerados por um Transformer Encoder (BAAI/bge-m3) foi motivada pelos resultados observados na Aula 06. O experimento demonstrou que arquiteturas baseadas em atenção conseguem capturar contexto, negação e dependências semânticas complexas, superando significativamente abordagens tradicionais baseadas em frequência de palavras. Como o objetivo do projeto é recuperar avaliações semanticamente relevantes, a utilização de embeddings e busca vetorial torna-se um componente essencial da arquitetura RAG.

---

## Avaliação da Solução

### Objetivo da Avaliação

A avaliação foi conduzida para verificar a qualidade da recuperação semântica, a relevância das evidências recuperadas e a capacidade do sistema de responder perguntas em linguagem natural utilizando exclusivamente informações presentes na base de conhecimento.

Inspirada nos conceitos discutidos nas Aulas 06 e 07 da disciplina, a validação priorizou a capacidade de generalização da solução, avaliando não apenas respostas para perguntas previamente conhecidas, mas também consultas formuladas de diferentes maneiras sobre os mesmos temas.

---

## Estratégia de Avaliação

A avaliação foi dividida em três níveis:

### 1. Recuperação Semântica

Objetivo:

Verificar se o mecanismo de busca vetorial consegue recuperar avaliações semanticamente relacionadas à pergunta do usuário, mesmo quando não existem correspondências literais entre as palavras utilizadas.

Exemplo:

**Pergunta**

```text
Quais problemas relacionados à entrega aparecem com frequência?
```

**Avaliações esperadas**

```text
Produto chegou atrasado.

Entrega demorou mais do que o prazo.

Transportadora levou muitos dias para concluir a entrega.
```

Critério de sucesso:

- Recuperação de documentos semanticamente relacionados.
- Preservação do contexto da pergunta.
- Recuperação de sinônimos e expressões equivalentes.

---

### 2. Qualidade das Evidências

Objetivo:

Garantir que as respostas geradas sejam fundamentadas nos documentos recuperados.

Critérios avaliados:

- Evidências compatíveis com a resposta gerada.
- Ausência de contradições entre resposta e documentos.
- Transparência e rastreabilidade das fontes utilizadas.

Exemplo:

**Resposta**

```text
Os principais problemas relatados pelos clientes estão relacionados a atrasos na entrega.
```

**Evidências**

```text
"produto chegou após o prazo"

"entrega demorou mais de 15 dias"

"pedido ficou parado na transportadora"
```

---

### 3. Robustez e Generalização

Objetivo:

Avaliar a consistência da recuperação para diferentes formas de perguntar a mesma coisa.

Exemplo:

```text
Quais problemas de entrega aparecem?

Quais reclamações sobre transporte são frequentes?

O que mais incomoda os clientes durante a entrega?

Quais atrasos são citados pelos consumidores?
```

Resultado esperado:

```text
Recuperação de documentos semelhantes
para todas as formulações.
```

---

## Conjunto de Perguntas de Teste

### Reclamações Gerais

```text
Quais são os principais problemas relatados pelos clientes?
```

### Entrega

```text
Quais reclamações relacionadas à entrega são mais frequentes?
```

### Qualidade

```text
Quais problemas de qualidade dos produtos aparecem nas avaliações?
```

### Satisfação

```text
O que os consumidores mais elogiam?
```

### Avaliações Negativas

```text
Quais padrões aparecem em avaliações com nota 1?
```

### Categorias de Produto

```text
O que os clientes relatam sobre produtos de informática?
```

### Consultas por Período

```text
Quais problemas foram registrados em 2018?
```

### Pergunta Fora de Escopo

```text
Qual o impacto da estratégia de marketing da empresa no Instagram?
```

Resposta esperada:

```text
Não há evidências suficientes na base
para responder essa pergunta.
```

---

## Métricas Observadas

Embora o foco deste projeto não seja a avaliação de um classificador supervisionado, foram observadas as seguintes características qualitativas:

| Critério | Objetivo |
|-----------|-----------|
| Relevância da recuperação | Recuperar documentos relacionados ao significado da pergunta |
| Precisão contextual | Recuperar documentos coerentes com o tema consultado |
| Evidências recuperadas | Sustentar a resposta com avaliações reais |
| Robustez semântica | Manter desempenho para consultas equivalentes |
| Resistência à alucinação | Evitar respostas sem suporte nos dados |
| Rastreabilidade | Possibilitar auditoria das evidências utilizadas |

---

## Comparação Conceitual com Busca Tradicional

A escolha da busca vetorial baseada em embeddings foi motivada pelos conceitos apresentados na Aula 06.

### Busca baseada em palavras-chave

```text
Pergunta:
"problemas de entrega"

Localiza:
"problemas de entrega"
```

Limitação:

```text
Não encontra sinônimos ou expressões equivalentes.
```

---

### Busca Vetorial

```text
Pergunta:
"problemas de entrega"
```

Recupera:

```text
"produto chegou atrasado"

"transportadora demorou"

"pedido entregue fora do prazo"
```

Benefício:

```text
Busca baseada em significado.
```

---

## Critérios de Sucesso da Solução

A solução é considerada satisfatória quando:

- Recupera documentos semanticamente relevantes.
- Apresenta evidências compatíveis com a resposta.
- Mantém consistência para diferentes formulações da mesma pergunta.
- Responde apenas com informações presentes na base.
- Informa explicitamente quando não existem evidências suficientes para responder uma consulta.
- Permite rastrear os documentos utilizados na geração dos insights.

---

## Conclusão da Avaliação

Os testes realizados demonstram que a utilização de embeddings gerados pelo modelo BAAI/bge-m3, associada ao armazenamento vetorial em ChromaDB e à arquitetura Retrieval-Augmented Generation (RAG), permite recuperar avaliações relevantes com base no significado da consulta, superando as limitações de abordagens baseadas exclusivamente em palavras-chave. A estratégia adotada contribui para respostas mais precisas, transparentes e fundamentadas em evidências reais da base de conhecimento.

---

## Avaliação, Monitoramento e Qualidade da Solução

### Objetivo

Além da construção do pipeline RAG, a solução foi avaliada sob a perspectiva de qualidade da recuperação, consistência das respostas e comportamento operacional, inspirando-se nos conceitos de validação, monitoramento e governança apresentados nas Aulas 07 e 08.

O objetivo não é apenas responder perguntas corretamente, mas garantir que as respostas sejam reproduzíveis, rastreáveis e sustentadas por evidências recuperadas da base de conhecimento.

---

## Arquitetura Avaliada

```text
Avaliações Olist
        │
        ▼
Pré-processamento
        │
        ▼
Documentos RAG
        │
        ▼
BAAI/bge-m3
(Transformer Encoder)
        │
        ▼
Embeddings
        │
        ▼
ChromaDB
        │
        ▼
Busca Vetorial
        │
        ▼
Top-K Evidências
        │
        ▼
GPT-4o-mini
        │
        ▼
Resposta
        │
        ▼
Evidências Recuperadas
```

---

## Estratégia de Avaliação

A validação da solução foi organizada em quatro perspectivas:

### 1. Qualidade da Recuperação Semântica

Avalia se o mecanismo de busca vetorial recupera avaliações relacionadas ao significado da pergunta, mesmo sem correspondência literal de palavras.

Exemplo:

**Pergunta**

```text
Quais problemas de entrega aparecem com frequência?
```

**Avaliações relevantes esperadas**

```text
produto chegou atrasado

entrega demorou muito

transportadora demorou vários dias

pedido chegou fora do prazo
```

---

### 2. Qualidade das Evidências

Avalia se os documentos recuperados realmente justificam os insights produzidos pela resposta.

Critérios:

- evidências relevantes;
- ausência de contradições;
- coerência entre resposta e contexto;
- rastreabilidade dos documentos.

---

### 3. Robustez das Consultas

Avalia a capacidade de responder consultas semanticamente equivalentes.

Exemplos:

```text
Quais problemas de entrega aparecem?

Quais reclamações relacionadas ao transporte são frequentes?

O que mais causa atrasos nos pedidos?

Quais problemas logísticos são mencionados pelos clientes?
```

Resultado esperado:

```text
Recuperação consistente
para todas as formulações.
```

---

### 4. Comportamento Fora de Escopo

Avalia a capacidade do sistema de evitar alucinações.

Exemplo:

```text
Qual o impacto do Instagram nas vendas da empresa?
```

Resposta esperada:

```text
Não foram encontradas evidências suficientes
na base para responder essa pergunta.
```

---

## Métricas Funcionais

| Métrica | Objetivo |
|----------|----------|
| Precisão da Recuperação | Avaliar se os documentos recuperados são relevantes |
| Consistência Semântica | Verificar estabilidade para perguntas equivalentes |
| Cobertura de Evidências | Medir se os documentos sustentam a resposta |
| Taxa de Respostas Fundamentadas | Percentual de respostas acompanhadas de evidências |
| Taxa de Rejeição Correta | Identificar perguntas sem evidência suficiente |
| Rastreabilidade | Capacidade de identificar quais documentos sustentaram a resposta |

---

## Métricas Operacionais

| Métrica | Descrição |
|----------|----------|
| Total de Avaliações Processadas | Quantidade de reviews indexados |
| Total de Embeddings Gerados | Quantidade de vetores armazenados |
| Tempo de Indexação | Tempo para criar a base vetorial |
| Tempo Médio de Recuperação | Tempo para recuperar Top-K documentos |
| Tempo Médio de Resposta | Tempo total da consulta ao RAG |
| Tamanho da Base Vetorial | Espaço ocupado pelo ChromaDB |
| Top-K Configurado | Quantidade de documentos recuperados por consulta |

---

## Controle de Qualidade

Durante os testes, a solução é considerada aprovada quando:

### Recuperação

```text
✅ Recupera documentos semanticamente relevantes

✅ Retorna avaliações alinhadas ao tema consultado

✅ Funciona para sinônimos e reformulações
```

### Evidências

```text
✅ Toda resposta apresenta evidências

✅ As evidências sustentam a conclusão apresentada

✅ Os documentos recuperados são rastreáveis
```

### Segurança

```text
✅ Perguntas fora de escopo são rejeitadas

✅ Não há geração de respostas sem evidência

✅ Não há extrapolação fora da base de conhecimento
```

---

## Comparação Conceitual com Busca Tradicional

### Busca Baseada em Palavras-chave

Pergunta:

```text
problemas de entrega
```

Recupera:

```text
problemas de entrega
```

Limitação:

```text
não encontra expressões semanticamente equivalentes
```

---

### Busca Vetorial

Pergunta:

```text
problemas de entrega
```

Recupera:

```text
produto chegou atrasado

transportadora demorou

pedido chegou após o prazo

demora na entrega
```

Benefício:

```text
busca baseada em significado
```

---

## Indicadores de Monitoramento

A solução registra informações para acompanhamento da qualidade da base vetorial:

```text
Modelo de Embedding utilizado

Versão da Base Vetorial

Quantidade de documentos

Top-K utilizado

Threshold de Similaridade

Modelo de Linguagem utilizado

Tempo de execução
```

Esses indicadores permitem reproduzir experimentos e comparar futuras evoluções da solução.

---

## Critérios de Liberação da Solução

A solução é considerada pronta para demonstração quando:

| Critério | Meta |
|-----------|-----------|
| Recuperação Semântica | Documentos relevantes para consultas de teste |
| Evidências | Presentes em 100% das respostas |
| Robustez | Consistência para perguntas equivalentes |
| Anti-Hallucination | Rejeição adequada de perguntas fora de contexto |
| Rastreabilidade | Identificação dos documentos utilizados |
| Tempo de Resposta | Compatível com uso interativo |

---

## Conclusão da Avaliação

A estratégia de avaliação adotada não se limita à qualidade da resposta final. Inspirada nos conceitos de validação e monitoramento discutidos nas Aulas 07 e 08, a análise concentra-se principalmente na qualidade da recuperação semântica, na rastreabilidade das evidências e na confiabilidade do pipeline RAG.

Dessa forma, a solução busca garantir que cada resposta gerada seja sustentada por avaliações reais dos clientes, reduzindo alucinações e aumentando a transparência dos insights produzidos.

---


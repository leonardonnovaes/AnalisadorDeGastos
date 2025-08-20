# Testado com:
-Extrato itau

# Analisador de Extrato Bancário em PDF

Este projeto é uma ferramenta em Python para extrair, analisar e visualizar seus gastos a partir de um extrato bancário em formato PDF. Ele utiliza bibliotecas populares como `pdfplumber`, `pandas` e `matplotlib` para automatizar a leitura do PDF, o processamento dos dados e a geração de um gráfico.

-----

### Funcionalidades

  - **Extração de Dados**: Lê um arquivo PDF e extrai as transações (data, descrição e valor).
  - **Limpeza de Dados**: Remove informações irrelevantes, como datas no final das descrições, para agrupar transações recorrentes de forma mais eficiente.
  - **Análise com Pandas**: Utiliza o poder do **pandas** para filtrar apenas os gastos, agrupar o valor total gasto por cada categoria e ordenar os resultados do maior para o menor gasto.
  - **Geração de CSV**: Salva o relatório de gastos em um arquivo CSV (`gastos_por_descricao.csv`), facilitando a visualização e o uso em outras planilhas.
  - **Visualização de Dados**: Gera um gráfico de barras com os seus **10 maiores gastos**, proporcionando uma visão rápida e clara de onde seu dinheiro está indo.

-----

### Como Usar

1.  **Instale as dependências**: Certifique-se de ter todas as bibliotecas necessárias instaladas.

    ```bash
    pip install pdfplumber pandas matplotlib
    ```

2.  **Configure o caminho do PDF**: Abra o arquivo `main.py` e insira o caminho completo do seu extrato bancário na variável `EXTRATO_PDF`.

    ```python
    EXTRATO_PDF = "caminho/para/o/seu/extrato.pdf"
    ```

3.  **Execute o script**: Execute o arquivo Python a partir do seu terminal.

    ```bash
    python seu_script.py
    ```

Após a execução, dois resultados serão gerados:

  - Um arquivo chamado **`gastos_por_descricao.csv`** será criado no mesmo diretório, contendo a lista completa de todos os seus gastos, agrupados por categoria.
  - Uma janela pop-up será exibida com um **gráfico de barras** mostrando o seu Top 10 de gastos.

-----

### Estrutura do Código

  - `extrair_transacoes(pdf_path)`: Responsável por ler o PDF, buscar o padrão de transação e extrair os dados brutos.
  - `limpar_descricao(desc)`: Função auxiliar que remove datas ou códigos do final das descrições.
  - `criar_data_frame(transacoes)`: Converte a lista de transações em um DataFrame, filtra gastos e agrupa os valores.
  - `top_10(df_gastos)`: Cria e exibe o gráfico de barras com os 10 maiores gastos.
  - `main()`: Orquestra o fluxo de execução do programa.

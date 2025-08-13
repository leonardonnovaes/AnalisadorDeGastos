import pdfplumber
import re
import pandas as pd
import matplotlib.pyplot as plt

# Caminho do PDF a ser processado.
# IMPORTANTE: Substitua "" pelo caminho real do seu arquivo, por exemplo: "caminho/do/seu/extrato.pdf"
EXTRATO_PDF = ""

# --- Funções de processamento de dados ---

# Função para limpar datas no final da descrição.
# Isso ajuda a agrupar transações recorrentes, como "Uber 07/01" e "Uber 08/01",
# em uma única categoria "Uber".
def limpar_descricao(desc):
    # Expressão regular para remover padrões de data ou números no final da string.
    # Ex: " 07/01", " 0712", " 19Jan", " 01Fev", " 3101"
    desc_limpo = re.sub(r"\s?(\d{2}/\d{2}|\d{4}|\d{2}[A-Za-z]{3}|\d{2}[A-Za-z]{2})$", "", desc)
    return desc_limpo.strip()

# Extrai transações do PDF.
def extrair_transacoes(pdf_path):
    transacoes = []
    
    # Abre o arquivo PDF com a biblioteca pdfplumber.
    with pdfplumber.open(pdf_path) as pdf:
        # Itera sobre cada página do documento.
        for page in pdf.pages:
            # Extrai o texto da página.
            text = page.extract_text()
            if text:
                # Divide o texto em linhas para processamento individual.
                linhas = text.split("\n")
                for linha in linhas:
                    # Busca por um padrão de linha que contenha data, descrição e valor.
                    # Exemplo: "01/01/2023 Descricao da Transacao -12,34"
                    match = re.search(r"(\d{2}/\d{2}/\d{4}) (.*?) (-?\d+,\d{2})", linha)
                    if match:
                        data, descricao, valor = match.groups()

                        # Limpa a descrição para remoção de datas no final.
                        descricao = limpar_descricao(descricao)
                        
                        # Converte o valor de string para float, trocando a vírgula por ponto.
                        valor = float(valor.replace(",", "."))
                        
                        # Adiciona a transação a uma lista de dicionários.
                        transacoes.append({
                            "data": data,
                            "descricao": descricao ,
                            "valor": valor
                        })
    return transacoes

# Cria um DataFrame do pandas e agrupa as transações.
def criar_data_frame(transacoes):
    # Cria o DataFrame a partir da lista de transações.
    df = pd.DataFrame(transacoes)

    # Remove linhas onde a descrição é "SALDO DO DIA", pois não é uma transação de gasto.
    df = df[df["descricao"] != "SALDO DO DIA"]

    # Filtra o DataFrame para incluir apenas os gastos (valores negativos).
    df = df[df["valor"] < 0]

    # Agrupa as transações pela descrição limpa e soma os valores.
    # Isso totaliza o gasto por categoria (ex: "Spotify", "Uber").
    df_agrupado = df.groupby("descricao", as_index=False)["valor"].sum()

    # Ordena os gastos do maior para o menor (em valor negativo, o que significa maior gasto).
    df_agrupado = df_agrupado.sort_values(by="valor")

    # Salva o resultado em um arquivo CSV.
    df_agrupado.to_csv("gastos_por_descricao.csv", index=False, encoding="utf-8")

    return df_agrupado

# Gera e exibe um gráfico de barras dos 10 maiores gastos.
def top_10(df_gastos):
    # Pega as 10 primeiras linhas do DataFrame (os 10 maiores gastos).
    top_10 = df_gastos.head(10)
    
    # Extrai as descrições (categorias) para o eixo X do gráfico.
    categorias = [desc for desc in top_10["descricao"]]
    
    # Extrai os valores, convertendo para positivo para o gráfico ficar mais claro.
    valores = [abs(valor) for valor in top_10["valor"]]
    
    # Configura o tamanho da figura do gráfico.
    plt.figure(figsize=(10,5))
    
    # Cria o gráfico de barras.
    plt.bar(categorias, valores, color="skyblue")
    
    # Rotação e alinhamento dos nomes no eixo X para evitar sobreposição.
    plt.xticks(rotation=45, ha="right")
    
    # Define os rótulos do eixo Y e o título do gráfico.
    plt.ylabel("Gasto (R$)")
    plt.title("Top 10 Gastos por Descrição")
    
    # Ajusta o layout para evitar que os rótulos sejam cortados.
    plt.tight_layout()
    
    # Exibe o gráfico.
    plt.show()

# --- Fluxo principal do programa ---

# A função `main` orquestra a execução das outras funções.
def main():
    # 1. Extrai as transações do PDF.
    transacoes = extrair_transacoes(EXTRATO_PDF)
    
    # 2. Cria um DataFrame e agrupa os gastos.
    df_gastos = criar_data_frame(transacoes)
    
    # 3. Gera o gráfico dos 10 maiores gastos.
    top_10(df_gastos)
    
# O bloco `if __name__ == "__main__":` garante que o código dentro dele
# só será executado quando o script for rodado diretamente.
if __name__ == "__main__":
    main()
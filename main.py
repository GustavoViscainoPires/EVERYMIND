import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text

#python -m streamlit run main.py

# Configuração da página
st.set_page_config(layout="wide")

# Criação do motor de conexão
username = 'root'
password = 'root'
host = 'localhost' 
database = 'DB_EVERYMIND'
engine = create_engine(f'mysql+mysqlconnector://{username}:{password}@{host}/{database}')

# Adiciona uma barra lateral com um botão de navegação
st.sidebar.title("Navegação")
page = st.sidebar.radio("Selecione uma página", ["Dashboard", "Novo Produto", "Editar Produto", "Deletar Produto"])

if page == "Dashboard":
    st.write("""
    # Produtos
    Aqui você encontra informações sobre todos os produtos da Nunes Sports:
    """)

    # Execução da query
    df = pd.read_sql('SELECT * FROM Produtos', con=engine)

    # Exibe o DataFrame na página principal
    st.dataframe(df)

elif page == "Novo Produto":
    st.write("## Adicionar Novo Produto")

    # Campos para inserir dados do novo produto
    nome = st.text_input("Nome")
    codigo = st.number_input("Código", min_value=0, step=1)
    descricao = st.text_area("Descrição")
    preco = st.number_input("Preço", min_value=0.0, step=0.01)

    # Botão para adicionar o produto
    if st.button("Adicionar Produto"):
        if nome and codigo and descricao and preco:
            try:
                # Cria a conexão e executa a query de inserção
                with engine.connect() as conn:
                    query = text("""
                    INSERT INTO Produtos (NOME, CODIGO, DESCRICAO, PRECO)
                    VALUES (:nome, :codigo, :descricao, :preco)
                    """)
                    conn.execute(query, {"nome": nome, "codigo": codigo, "descricao": descricao, "preco": preco})
                    conn.connection.commit()
                st.success("Produto adicionado com sucesso!")
            except Exception as e:
                st.error(f"Erro ao adicionar o produto: {e}")
        else:
            st.error("Por favor, preencha todos os campos.")

elif page == "Editar Produto":
    st.write("## Editar Produto")

    # Carregar a lista de produtos para seleção
    df_produtos = pd.read_sql('SELECT * FROM Produtos', con=engine)
    produtos = df_produtos['NOME'].tolist()
    
    produto_selecionado = st.selectbox("Escolha um produto para editar", produtos)
    
    if produto_selecionado:
        # Obter os detalhes do produto selecionado
        produto = df_produtos[df_produtos['NOME'] == produto_selecionado].iloc[0]
        
        nome = st.text_input("Nome", value=produto['NOME'])
        codigo = st.number_input("Código", min_value=0, step=1, value=produto['CODIGO'])
        descricao = st.text_area("Descrição", value=produto['DESCRICAO'])
        preco = st.number_input("Preço", min_value=0.0, step=0.01, value=produto['PRECO'])
        
        # Botão para atualizar o produto
        if st.button("Atualizar Produto"):
            if nome and codigo and descricao and preco:
                try:
                    # Cria a conexão e executa a query de atualização
                    with engine.connect() as conn:
                        query = text("""
                        UPDATE Produtos
                        SET NOME = :nome, DESCRICAO = :descricao, PRECO = :preco
                        WHERE CODIGO = :codigo
                        """)
                        conn.execute(query, {"nome": nome, "codigo": codigo, "descricao": descricao, "preco": preco})
                        conn.connection.commit()
                    st.success("Produto atualizado com sucesso!")
                except Exception as e:
                    st.error(f"Erro ao atualizar o produto: {e}")
            else:
                st.error("Por favor, preencha todos os campos.")


elif page == "Deletar Produto":
    st.write("## Deletar Produto")

    # Carregar a lista de produtos para seleção
    df_produtos = pd.read_sql('SELECT * FROM Produtos', con=engine)
    produtos = df_produtos['NOME'].tolist()

    produto_selecionado = st.selectbox("Escolha um produto para deletar", produtos)

    if produto_selecionado:
        if st.button("Deletar Produto"):
            try:
                # Obtém o código do produto selecionado e converte para int
                codigo = int(df_produtos[df_produtos['NOME'] == produto_selecionado]['CODIGO'].values[0])

                # Cria a conexão e executa a query de exclusão
                with engine.connect() as conn:
                    query = text("""
                    DELETE FROM Produtos
                    WHERE CODIGO = :codigo
                    """)
                    conn.execute(query, {"codigo": codigo})
                    conn.connection.commit()

                st.success(f"Produto '{produto_selecionado}' deletado com sucesso!")
            except Exception as e:
                st.error(f"Erro ao deletar o produto: {e}")



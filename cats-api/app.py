from flask import Flask, jsonify, render_template, request, url_for, redirect
import requests 

import oracledb

# ----Funções para manipulação do banco de dados Oracle----

def getConnection():
    '''
    Desc: Conecta ao banco de dados Oracle
    Return: conn (objeto de conexão)
    '''
    try:
        conn = oracledb.connect(user="rm98373", password="120503", host="oracle.fiap.com.br", port=1521, service_name="ORCL")
    except Exception as e:
        print(f'Erro ao obter conexão com banco de dados: {e}')        
    return conn

def insert(nome, id, url):
    try:
        conn = getConnection()
        cursor = conn.cursor()
        sql_insert = f"INSERT INTO MEUS_GATOS VALUES ('{nome}', '{id}', '{url}')"
        cursor.execute(sql_insert)
        conn.commit()
        print('\nDados inseridos com sucesso!\n')
    except Exception as e:
        print(f'Erro ao executar insert: {e}')

def select():
    '''
    Desc: Executa um select na tabela MEUS_GATOS
    Return: dic_linhas (dicionario com todos os registros da tabela)
    '''
    try:
        conn = getConnection()
        cursor = conn.cursor()
        sql_select = 'SELECT * FROM MEUS_GATOS'
        cursor.execute(sql_select)
        # percorrer as linhas da tabela
        i = 1  
        dic_linhas = {}
        for result in cursor: 
            # print(f'\nlinha {i}: {result}')
            # converter resultado para json
            dic_linhas[i] = {'nome': result[0], 'id': result[1], 'url': result[2]}
            i += 1
        return dic_linhas
    except Exception as e:
        print(f'Erro ao executar select: {e}')

def closeConnection(conn):
    '''
    Desc: Fecha a conexão com o banco de dados
    Return: None
    '''
    try:
        conn.close()
        print('\nConexão fechada com sucesso!')
    except Exception as e:
        print(f'Erro ao fechar conexão: {e}')

# Funções para manipulação de API
app = Flask(__name__) 

gatos = [] # lista de gatos

@app.route('/') # rota principal
def index(): 
    '''
     Função que retorna a página index.html com a lista de gatos e o formulário para adicionar novos gatos.
    '''
    return render_template('index.html',gatos=gatos)


@app.route('/adicionar_gato',methods=['POST']) 
def adicionar_gato():
    '''
    Função que adiciona uma novo gato na lista de gatos e redireciona para a página index.html
    '''
    novo_gato = request.form.get('gato') # pegando o valor do input com name="gato"
    url,id = get_cat_image()  # Chama a função para obter a URL da imagem do gato
    gato = {'nome': novo_gato, 'id': id,'url': url}  # Cria um dicionário com o nome e a URL da imagem
    gatos.append(gato) 
    registrar_gatos(gatos) 
    return redirect(url_for('index')) 

@app.route('/adicionar_gato',methods=['POST'])
def get_cat_image():
    '''
    Função que acessa a API TheCatAPI e retorna o Json da imagem(url) e url da imagem do gato
    '''
    url = 'https://api.thecatapi.com/v1/images/search'
    response = requests.get(url)
    
    if response.status_code == 200:
        json_data = response.json()
        url = json_data[0]['url']
        id = json_data[0]['id']
        return url,id
    else:
        return 'Erro ao acessar a API'
        
def registrar_gatos(matriz_gatos):
    '''
    Função que passa os dados dos gatos para a tabela MEUS_GATOS 
    param: matriz_gatos (lista de dicionários)
    '''
    conn = getConnection() 
    print('\n\n--Mostrando gatos--\n')
    for chave in range(len(matriz_gatos)):
        nome = matriz_gatos[chave]['nome']
        id = matriz_gatos[chave]['id']
        url = matriz_gatos[chave]['url']
        insert(nome, id, url)
    closeConnection(conn) 

@app.route('/buscar_no_banco',methods=['POST'])
def buscar_no_banco():
    '''
    Função que busca os gatos no banco de dados e retorna uma lista de gatos
    '''
    conn = getConnection() 
    lista_gatos = select() 

    print('\n\n--Mostrando gatos--\n')
    gatos_result = []
    for chave in range(len(lista_gatos)):
        nome = lista_gatos[chave + 1]['nome']
        id = lista_gatos[chave + 1]['id']
        url = lista_gatos[chave + 1]['url']
        print(lista_gatos[chave + 1])
        gatos_result.append({'nome': nome, 'url': url})
    closeConnection(conn) 
    return render_template('index.html', gatos=gatos_result)

# principal
# roda o servidor flask em modo debug na porta 5000 
if __name__ == '__main__':
    app.run(debug=True) 
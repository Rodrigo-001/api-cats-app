from flask import Flask, jsonify, render_template, request, url_for, redirect
import requests

app = Flask(__name__) # instanciando a classe Flask

gatos = [] # lista de gatos

@app.route('/')
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
    novo_gato = request.form.get('gato') 
    url,id = get_cat_image()  # Chama a função para obter a URL da imagem do gato
    gato = {'nome': novo_gato, 'url': url}  # Cria um dicionário com o nome e a URL da imagem
    gatos.append(gato)
    return redirect(url_for('index'))

@app.route('/')
def get_cat_image():

    url = 'https://api.thecatapi.com/v1/images/search'
    response = requests.get(url)
    
    if response.status_code == 200:
        json_data = response.json()
        # print(json_data)  # Imprime o JSON no console
        url = json_data[0]['url']
        id = json_data[0]['id']
        # print(f'\nUrl: {url} | ID: {id}\n')        
        return url,id
    else:
        return 'Erro ao acessar a API'


# principal
if __name__ == '__main__':
    '''
    Função principal que roda o servidor flask em modo debug na porta 5000 
    '''
    app.run(debug=True) 
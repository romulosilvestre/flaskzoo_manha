# pip install flask (no terminal)
# importando modulos
from flask import Flask,render_template,request,redirect,url_for
import urllib.parse
# realizar o mapeamento objeto relacional -DB First
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.automap import automap_base
from animal import Animal
from avaliacao import Avaliacao
from sqlalchemy.orm import sessionmaker
from googletrans import Translator
from textblob import TextBlob

# definindo objeto flask
app = Flask(__name__)

app.secret_key = "df6e83eb7983f75b2561c875cbebc40ab9900624b22c6040f5831ecd6faaea429f043b35bd5a6fae4692fa6c80fdcf060f61207f53eb744ba684f84517fc9881sua chave secreta"
# ==========================================
# senha : @
# tratar o arroba de uma senha
# importe urlib.parse
# =========================================
#              info do bd
user = 'root'
password = urllib.parse.quote_plus('senai@123')
host = 'localhost'
database = 'zooflask'
# ==========================================
#           connection string
connection_string = f'mysql+pymysql://{user}:{password}@{host}/{database}'
# ==========================================
# ==========sqlalchemy-orm-db first=========
# 1. instalar o SQLAlchemy
# 2. crie o motor 

"""
A função create_engine cria uma interface 
que permite a comunicação entre o aplicativo web
e o banco de dados

"""
engine = create_engine(connection_string)

#  Refletindo o Banco de Dados
metadata = MetaData()
metadata.reflect(engine)

"""
-- Cria uma classe base que vai mapear Automaticamente as tabelas do banco de dados 
-- Que estão descritas no objeto metadata.

"""
Base = automap_base(metadata=metadata) # definindo a classe

"""
 
--Gera uma classe para cada tabela 

"""
Base.prepare() # mapeando


# Ligando com a classe
Animal =  Base.classes.animal
Avaliacao = Base.classes.avaliacao
# Criar a sessão do SQLAlchemy
Session = sessionmaker(bind=engine)

# criando uma rota para renderizar a pagina
@app.route("/",methods=['GET'])
def pagina_inicial():
    return render_template("index.html")

@app.route('/novoanimal', methods=['POST','GET'])
def inserir_animal():
    
    session_db = Session()  # Criar uma nova sessão
    nome_popular = request.form['nome_popular']
    nome_cientifico = request.form['nome_cientifico']
    habitos_noturnos = request.form['habitos_noturnos']
    # erro
    animal = Animal(nome_popular=nome_popular,
                    nome_cientifico=nome_cientifico,
                    habitos_noturnos=habitos_noturnos) 
    try:
        session_db.add(animal)
        session_db.commit()
    except:
        session_db.rollback()
    finally:
        session_db.close()

    return redirect(url_for('pagina_inicial'))

@app.route('/cadastraravaliacao',methods=['POST','GET'])
def cadastrar_avaliacao():
    # verificar inserção no banco 
    sessao_db_cl = Session()
     # passo 1 - pegar do HTML
    texto = request.form['texto']
    # passo 2 - pegar a polaridade

    # tradução português para inglês
    blob_pt = TextBlob(texto)
    texto_traduzido = blob_pt.translate(from_lang='pt',to='en')
    # passando texto traduzido
    blob_en = TextBlob(str(texto_traduzido))
    polaridade = blob_en.sentiment.polarity
    avaliacao = Avaliacao(avaliacao=texto_traduzido,polaridade=polaridade)
    try:
       
        sessao_db_cl.add(avaliacao)
        sessao_db_cl.commit()
    except:
        sessao_db_cl.rollback()
    finally:
        sessao_db_cl.close()
    return redirect(url_for('mostrar_avaliacao'))

@app.route("/avaliacao")
def mostrar_avaliacao():
    return render_template('avaliacao.html')


@app.route("/listaravaliacao")
def listar_avaliacao():
    return render_template("listaravaliacao.html")

# definindo com o programa principal 
if __name__ == "__main__":
    app.run(debug=True)




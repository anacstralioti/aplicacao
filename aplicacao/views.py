from django.shortcuts import render, redirect, get_object_or_404
from django.http.response import HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from .models import ItemVenda, Produto, Cliente, Perfil, Venda, Avaliacao
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Produto
import io
import urllib, base64
import pandas as pd
import matplotlib.pyplot as plt

def index(request):
    context = {
        "texto": "Olá mundo!",
    }
    return render(request, 'index.html', context)

@login_required
def produtos(request):
    produtos = Produto.objects.all()
    context = {
        'produtos': produtos,
    }
    return render(request, 'entrar.html', context)

def cad_produto(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            return render(request, 'cad_produto.html')
        elif request.method == "POST":
            nome = request.POST.get('nome')
            preco = request.POST.get('preco').replace(',', '.')
            qtde = request.POST.get('qtde')

            produto = Produto(
                nome = nome,
                preco = preco,
                qtde = qtde
            )
            produto.save()
            return redirect('url_produtos')
    else:
        return redirect('url_entrar')

def atualizar_produto(request, id):
    prod = get_object_or_404(Produto, id=id)
    if request.method == "GET":
        context = {
            'prod': prod,
        }
        return render(request, 'atualizar_produto.html', context)
    elif request.method == "POST":
        nome = request.POST.get('nome')
        preco = request.POST.get('preco').replace(',', '.')
        qtde = request.POST.get('qtde')

        prod.nome = nome
        prod.preco = preco
        prod.qtde = qtde
        prod.save()
    return redirect('url_produtos')

def apagar_produto(request, id):
    prod = get_object_or_404(Produto, id=id)
    prod.delete()
    return redirect('url_produtos')

def entrar(request):
    if request.method == "GET":
        return render (request, "entrar.html")
    else:
        username = request.POST.get('nome')
        password = request.POST.get('senha')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('url_produtos')
        else:
            return HttpResponse("PANE NO SISTEMA ALGUÉM ME DESCONFIGUROU")

def cad_user(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        senha = request.POST.get('senha')
        email = request.POST.get('email')

        user = User.objects.filter(username=nome).first()

        if user:
            return HttpResponse("Usuário já existe")

        user = User.objects.create_user(username=nome,email=email,password=senha)
        user.save()
        messages.successs(request, "Usuário cadastrado")
    else: 
        return render(request, "cad_user.html")

def sair(request):
    logout(request)
    return redirect('url_entrar')

def cad_cliente(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')

        cliente = Cliente.objects.filter(nome=nome).first()

        if cliente:
            return HttpResponse("Usuário já existe")

        cliente = Cliente.objects.create(nome=nome,email=email)
        cliente.save()
        messages.successs(request, "Usuário cadastrado")
    else: 
        return render(request, "cad_cliente.html")
    
def cad_perfil(request):
    if request.method == 'GET':
        clientes_sem_perfil = Cliente.objects.filter(perfil__isnull=True)
        
        context = {
            'clientes': clientes_sem_perfil
        }
        return render(request, "cad_perfil.html", context)

    elif request.method == 'POST':
        cliente_id = request.POST.get('cliente_id')
        rua = request.POST.get('rua')
        numero = request.POST.get('numero')
        cep = request.POST.get('cep')
        bairro = request.POST.get('bairro')
        cidade = request.POST.get('cidade')
        complemento = request.POST.get('complemento')
        telefone = request.POST.get('telefone')

        if not cliente_id:
            messages.error(request, "Você precisa selecionar um cliente.")
            return redirect('url_cad_perfil')

        cliente_obj = get_object_or_404(Cliente, id=cliente_id)

        perfil = Perfil.objects.create(
            cliente=cliente_obj,
            rua=rua,
            numero=numero,
            cep=cep,
            bairro=bairro,
            cidade=cidade,
            complemento=complemento,
            telefone=telefone
        )

        messages.success(request, f"Perfil para {cliente_obj.nome} cadastrado com sucesso!")
        return redirect('cad_perfil.html')

def cad_venda(request):
    if request.method == "GET":
        clientes = Cliente.objects.all()
        context = {
            "clientes": clientes,
        }
        return render(request, "cad_venda.html", context)

    elif request.method == "POST":
        cliente_id = request.POST.get("cliente_id")

        if not cliente_id:
            messages.error(request, "Você precisa selecionar um cliente.")
            return redirect("url_cad_venda")

        cliente = get_object_or_404(Cliente, id=cliente_id)

        venda = Venda.objects.create(cliente=cliente)

        messages.success(request, f"Venda criada para {cliente.nome}. Agora adicione os itens.")
        return redirect("url_cad_venda")
    
def cad_itemvenda(request):
    if request.method == "GET":
        vendas = Venda.objects.all()
        produtos = Produto.objects.all()
        context = {
            "vendas": vendas,
            "produtos": produtos,
        }
        return render(request, "cad_itemvenda.html", context)

    elif request.method == "POST":
        venda_id = request.POST.get("venda_id")
        produto_id = request.POST.get("produto_id")
        qtde = request.POST.get("qtde")

        if not all([venda_id, produto_id, qtde]):
            messages.error(request, "Todos os campos são obrigatórios.")
            return redirect("url_cad_itemvenda")
        
        try:
            qtde = int(qtde)
            if qtde <= 0:
                raise ValueError()
        except ValueError:
            messages.error(request, "A quantidade deve ser um número inteiro positivo.")
            return redirect("url_cad_itemvenda")

        venda = get_object_or_404(Venda, id=venda_id)
        produto = get_object_or_404(Produto, id=produto_id)

        if produto.qtde < qtde:
            messages.error(request, f"Estoque insuficiente para '{produto.nome}'. Disponível: {produto.qtde}.")
            return redirect("url_cad_itemvenda")

        ItemVenda.objects.create(
            venda=venda,
            produto=produto,
            qtde=qtde
        )

        produto.qtde -= qtde
        produto.save()

        messages.success(request, f"Item '{produto.nome}' adicionado à venda de {venda.cliente.nome}.")
        return redirect("url_cad_itemvenda")

def get_dataframe():
    # Busca todos os dados do banco e retorna um DataFrame do Pandas
    avaliacoes = Avaliacao.objects.all().values()
    df = pd.DataFrame(list(avaliacoes))
    return df

def plot_to_base64(fig):
    # Converte uma figura Matplotlib para uma string base64 para ser usada no HTML
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    return urllib.parse.quote(string)

def distribuicao_das_notas_view(df):
    plt.figure(figsize=(10, 6))
    df['review_score'].value_counts().sort_index().plot(kind='bar', color='purple')
    plt.title('Distribuição das Notas das Avaliações')
    plt.xlabel('Nota (Score)')
    plt.ylabel('Quantidade de Avaliações')
    plt.grid(axis='y', linestyle='--')
    plt.tight_layout()
    return plot_to_base64(plt.gcf())

def livros_mais_avaliados_view(df):
    top_10_livros = df['title'].value_counts().nlargest(10)
    plt.figure(figsize=(12, 8))
    top_10_livros.sort_values().plot(kind='barh', color='purple')
    plt.title('Top 10 Livros com Mais Avaliações')
    plt.xlabel('Número de Avaliações')
    plt.ylabel('Título do Livro')
    plt.tight_layout()
    return plot_to_base64(plt.gcf())

def usuarios_mais_ativos_view(df):
    df_filtered = df.dropna(subset=['profile_name'])
    top_15_usuarios = df_filtered['profile_name'].value_counts().nlargest(15)
    plt.figure(figsize=(12, 8))
    top_15_usuarios.sort_values().plot(kind='barh', color='purple')
    plt.title('Top 15 Usuários Mais Ativos')
    plt.xlabel('Número de Avaliações')
    plt.ylabel('Usuário')
    plt.tight_layout() 
    return plot_to_base64(plt.gcf())

def evolucao_reviews_view(df):
    df['data_review'] = pd.to_datetime(df['review_time'], unit='s')
    df['ano'] = df['data_review'].dt.year
    avaliacoes_por_ano = df['ano'].value_counts().sort_index()
    plt.figure(figsize=(10, 6))
    avaliacoes_por_ano.plot(kind='line', marker='o', linestyle='-', color='purple')
    plt.title('Evolução do Número de Avaliações por Ano')
    plt.xlabel('Ano')
    plt.ylabel('Quantidade de Avaliações')
    plt.grid(True, linestyle='--')
    plt.tight_layout()
    return plot_to_base64(plt.gcf())

def preco_vs_score_view(df):
    df_filtered = df[df['price'] > 0]
    if len(df_filtered) > 1000:
        df_sample = df_filtered.sample(n=1000, random_state=42)
    else:
        df_sample = df_filtered
    plt.figure(figsize=(10, 6))
    plt.scatter(df_sample['price'], df_sample['review_score'], alpha=0.3, color='purple')
    plt.title('Correlação entre Preço e Nota da Avaliação')
    plt.xlabel('Preço do Livro')
    plt.ylabel('Nota (Score)')
    plt.grid(True, linestyle='--')
    plt.tight_layout()
    return plot_to_base64(plt.gcf())

def sentimento_reviews_view(df):
    palavras_positivas = ['good', 'great', 'excellent', 'i loved', 'i recommend']
    palavras_negativas = ['bad', 'terrible', 'disappointing', "i didn't like it"]
    def classifica_sentimento(texto):
        texto_lower = str(texto).lower()
        if any(palavra in texto_lower for palavra in palavras_positivas): return 'Positivo'
        if any(palavra in texto_lower for palavra in palavras_negativas): return 'Negativo'
        return 'Neutro'
    df['sentimento'] = df['review_summary'].fillna('').apply(classifica_sentimento)
    contagem_sentimento = df['sentimento'].value_counts()
    plt.figure(figsize=(8, 8))
    contagem_sentimento.plot(kind='pie', autopct='%1.1f%%', colors=['lightskyblue', 'purple', 'lightpink'], startangle=90)
    plt.title('Distribuição de Sentimentos nos Sumários')
    plt.ylabel('')
    plt.tight_layout()
    return plot_to_base64(plt.gcf())

def dashboard(request):
    df = get_dataframe()

    context = {
        'distribuicao_das_notas_view': distribuicao_das_notas_view(df.copy()),
        'livros_mais_avaliados_view': livros_mais_avaliados_view(df.copy()),
        'usuarios_mais_ativos_view': usuarios_mais_ativos_view(df.copy()),
        'evolucao_reviews_view': evolucao_reviews_view(df.copy()),
        'preco_vs_score_view': preco_vs_score_view(df.copy()),
        'sentimento_reviews_view': sentimento_reviews_view(df.copy()),
    }

    return render(request, 'dashboard.html', context)
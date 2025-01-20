from django.shortcuts import render, redirect

from .models import *
from .forms import *
from django.contrib import messages

from django.http import JsonResponse
from django.apps import apps

def index(request):
    return render(request,'index.html')

def categoria(request):
    contexto = {
        'lista': Categoria.objects.all().order_by('-id'),
    }
    return render(request, 'categoria/lista.html',contexto)

def form_categoria(request):
    if request.method == 'POST':
       form = CategoriaForm(request.POST) # instancia o modelo com os dados do form
       if form.is_valid():# faz a validação do formulário
            categoria = form.save() # salva a instancia do modelo no banco de dados
            messages.success(request, 'Operação realizada com Sucesso')
            return redirect('categoria') # redireciona para a listagem
    else:# método é get, novo registro
        form = CategoriaForm() # formulário vazio
    contexto = {
        'form':form,
    }
    return render(request, 'categoria/formulario.html', contexto)


def editar_categoria(request, id):
    try:
        categoria = Categoria.objects.get(pk=id)
    except Categoria.DoesNotExist:
        # Caso o registro não seja encontrado, exibe a mensagem de erro
        messages.error(request, 'Registro não encontrado')
        return redirect('categoria')  # Redireciona para a listagem

    if request.method == 'POST':
        # combina os dados do formulário submetido com a instância do objeto existente, permitindo editar seus valores.
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            categoria = form.save() # save retorna o objeto salvo
            messages.success(request, 'Operação realizada com Sucesso')
            lista = []
            lista.append(categoria) 
            return render(request, 'categoria/lista.html', {'lista': lista})
    else:
         form = CategoriaForm(instance=categoria)
    return render(request, 'categoria/formulario.html', {'form': form,})


def detalhes_categoria(request, id):
    categoria = Categoria.objects.get(pk=id)
    return render(request, 'categoria/detalhes.html', {'categoria': categoria,})



def remover_categoria(request, id):
    categoria = Categoria.objects.get(pk=id)
    categoria.delete()
    return redirect('categoria')





################################### VIEWS PARA CLINTE ##################################
def cliente(request):
    contexto = {
        'lista': Cliente.objects.all().order_by('-id'),
    }
    return render(request, 'cliente/lista.html',contexto)


def form_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            cliente = form.save()
            messages.success(request, 'Operação realizada com Sucesso')
            return redirect('cliente') 
        else:
            messages.error(request, 'Erro ao salvar o registro')
    else:
        form = ClienteForm()

    return render(request, 'cliente/form.html', {'form': form,})

def editar_cliente(request, id):
    try:
        cliente = Cliente.objects.get(pk=id)
    except Cliente.DoesNotExist:
        # Caso o registro não seja encontrado, exibe a mensagem de erro
        messages.error(request, 'Registro não encontrado')
        return redirect('cliente')  # Redireciona para a listagem
    
    if request.method == 'POST':
        # combina os dados do formulário submetido com a instância do objeto existente, permitindo editar seus valores.
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            cliente = form.save()
            lista = []
            lista.append(cliente) 
            return render(request, 'cliente/lista.html', {'lista': lista})
    else:
         form = ClienteForm(instance=cliente)
    return render(request, 'cliente/form.html', {'form': form,})

def remover_cliente(request, id):
    try:
        cliente = Cliente.objects.get(pk=id)
    except Cliente.DoesNotExist:
        # Caso o registro não seja encontrado, exibe a mensagem de erro
        messages.error(request, 'Registro não encontrado')
        return redirect('cliente')  # Redireciona para a listagem
    cliente.delete()
    return redirect('cliente')



     ############################## PRODDUTO ####################################


def form_produto(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST)
        if form.is_valid():
            produto = form.save()  # Salva o registro no banco de dados e retorna a instância do mesmo
            return redirect('produto')  # Redireciona para a listagem
    else:
        form = ProdutoForm()

    return render(request, 'produto/form.html', {'form': form})

def produto(request):
    lista = Produto.objects.all()  # Obtém todos os registros
    return render(request, 'produto/lista.html', {'lista': lista})


def editar_produto(request, id):
    produto = Produto.objects.get(pk=id)
    if request.method == 'POST':
        # combina os dados do formulário submetido com a instância do objeto existente, permitindo editar seus valores.
        form = ProdutoForm(request.POST, instance=produto)
        if form.is_valid():
            produto = form.save()
            lista = []
            lista.append(produto) 
            return render(request, 'produto/lista.html', {'lista': lista})
    else:
         form = ProdutoForm(instance=produto)
    return render(request, 'produto/form.html', {'form': form,})

def remover_produto(request, id):
    produto = Produto.objects.get(pk=id)
    produto.delete()
    return redirect('produto')

def detalhes_produto(request, id):
    try:
        produto = Produto.objects.get(pk=id)
    except Produto.DoesNotExist:
        # Caso o registro não seja encontrado, exibe a mensagem de erro
        messages.error(request, 'Registro não encontrado')
        return redirect('produto')  # Redireciona para a listagem
    return render(request, 'produto/detalhes.html', {'produto': produto,})


def ajustar_estoque(request, id):
    produto = Produto.objects.get(pk=id)
    estoque = produto.estoque # pega o objeto estoque relacionado ao produto
    if request.method == 'POST':
        form = EstoqueForm(request.POST, instance=estoque)
        if form.is_valid():
            estoque = form.save()
            lista = []
            lista.append(estoque.produto) 
            return render(request, 'produto/lista.html', {'lista': lista})
    else:
         form = EstoqueForm(instance=estoque)
    return render(request, 'produto/estoque.html', {'form': form,})


def teste1(request):
     return render(request, 'testes/teste1.html')

def teste2(request):
     return render(request, 'testes/teste2.html')
 
def teste3(request):
     return render(request, 'testes/teste3.html')
 
 
def buscar_dados(request, app_modelo):
    termo = request.GET.get('q', '') # pega o termo digitado
    try:
        # Divida o app e o modelo
        app, modelo = app_modelo.split('.')
        modelo = apps.get_model(app, modelo)
    except LookupError:
        return JsonResponse({'error': 'Modelo não encontrado'}, status=404)
    
    # Verifica se o modelo possui os campos 'nome' e 'id'
    if not hasattr(modelo, 'nome') or not hasattr(modelo, 'id'):
        return JsonResponse({'error': 'Modelo deve ter campos "id" e "nome"'}, status=400)
    
    resultados = modelo.objects.filter(nome__icontains=termo)
    dados = [{'id': obj.id, 'nome': obj.nome} for obj in resultados]
    return JsonResponse(dados, safe=False)

"""

            lista = []
            lista.append(categoria) 
            return render(request, 'categoria/lista.html', {'lista': lista})



def form_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST) # instancia o modelo com os dados do form
        if form.is_valid():
            form.save() # salva a instancia do form no banco de dados
            return redirect('categoria') 
    else:
        form = CategoriaForm()
    contexto = {
        'form':form,
    }
    return render(request, 'categoria/formulario.html', contexto)
"""
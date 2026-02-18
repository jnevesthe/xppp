from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Categoria, Video

# Galeria: mostra 10 miniaturas por página
def galeria(request):
    todos_videos = Video.objects.all().order_by('-criado_em')
    paginator = Paginator(todos_videos, 10)  # 10 vídeos por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'galeria.html', {'page_obj': page_obj})

# Página individual do vídeo
def video(request, slug):
    video = get_object_or_404(Video, slug=slug)
    return render(request, 'ver_video.html', {'video': video})


from django.db.models import Q
import random



from django.shortcuts import render, redirect
from django.db.models import Q

def search(request):
    query = request.GET.get('q', '').strip()  # pega o texto da pesquisa

    # Se o campo de pesquisa estiver vazio, redireciona para a página inicial
    if not query:
        return redirect('galeria')  # aqui 'home' é o name da URL da página inicial

    categorias_result = []
    videos_result = []

    palavras = query.split()  # separa a pesquisa em palavras-chave

    # Busca categorias que contenham qualquer palavra
    q_categorias = Q()
    for p in palavras:
        q_categorias |= Q(nome__icontains=p)
    categorias_result = Categoria.objects.filter(q_categorias)

    # Busca vídeos que contenham qualquer palavra do título
    q_videos = Q()
    for p in palavras:
        q_videos |= Q(titulo__icontains=p)
    videos_result = Video.objects.filter(q_videos)

    # Se não encontrar nada, retorna vídeos aleatórios
    if not categorias_result.exists() and not videos_result.exists():
        videos_result = Video.objects.order_by('?')[:10]

    context = {
        'query': query,
        'categorias': categorias_result,
        'videos': videos_result,
    }
    return render(request, 'search_results.html', context)




def destaques(request):
    # Pega todos os vídeos com destaque = True, mais recentes primeiro
    videos = Video.objects.filter(destaque=True).order_by('-criado_em')

    # Paginação: 10 vídeos por página
    paginator = Paginator(videos, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj
    }
    return render(request, 'destaques.html', context)





def lista_categorias(request):
    categorias = Categoria.objects.all()
    return render(request, 'categorias.html', {
        'categorias': categorias
    })


def videos_por_categoria(request, slug):
    categoria = get_object_or_404(Categoria, slug=slug)
    videos_list = Video.objects.filter(categoria=categoria).order_by('-criado_em')

    paginator = Paginator(videos_list, 10)  # sempre 10
    page_number = request.GET.get('page')
    videos = paginator.get_page(page_number)

    return render(request, 'videos_categoria.html', {
        'categoria': categoria,
        'videos': videos
    })

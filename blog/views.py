from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.views import LogoutView
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.generic import ListView, DetailView
from .models import Post, Category, Subcategory, Comment, PostLike
from .forms import PostForm, CommentForm, SearchForm, CustomUserCreationForm

def home(request):
    """Vista principal del blog"""
    featured_posts = Post.objects.filter(published=True, featured=True)[:3]
    recent_posts = Post.objects.filter(published=True)[:6]
    categories = Category.objects.annotate(post_count=Count('posts'))
    
    context = {
        'featured_posts': featured_posts,
        'recent_posts': recent_posts,
        'categories': categories,
    }
    return render(request, 'blog/home.html', context)

class PostListView(ListView):
    """Vista para listar todos los posts"""
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 9
    
    def get_queryset(self):
        return Post.objects.filter(published=True).select_related('author', 'category')

def post_detail(request, slug):
    """Vista de detalle de un post"""
    post = get_object_or_404(Post, slug=slug, published=True)
    comments = post.comments.filter(approved=True, parent=None)
    
    # Posts relacionados
    related_posts = Post.objects.filter(
        category=post.category,
        published=True
    ).exclude(id=post.id)[:3]
    
    # Formulario de comentarios
    comment_form = CommentForm()
    
    # Información de likes
    likes_count = post.get_likes_count()
    is_liked = post.is_liked_by_user(request.user)
    
    if request.method == 'POST' and request.user.is_authenticated:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, 'Tu comentario ha sido añadido.')
            return redirect('blog:post_detail', slug=slug)
    
    context = {
        'post': post,
        'comments': comments,
        'related_posts': related_posts,
        'comment_form': comment_form,
        'likes_count': likes_count,
        'is_liked': is_liked,
    }
    return render(request, 'blog/post_detail.html', context)

def category_posts(request, slug):
    """Vista para posts de una categoría específica"""
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(category=category, published=True)
    
    paginator = Paginator(posts, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'posts': page_obj,
        'page_obj': page_obj,
    }
    return render(request, 'blog/category_posts.html', context)

def subcategory_posts(request, category_slug, subcategory_slug):
    """Vista para posts de una subcategoría específica"""
    category = get_object_or_404(Category, slug=category_slug)
    subcategory = get_object_or_404(Subcategory, slug=subcategory_slug, category=category)
    posts = Post.objects.filter(subcategory=subcategory, published=True)
    
    paginator = Paginator(posts, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'subcategory': subcategory,
        'posts': page_obj,
        'page_obj': page_obj,
    }
    return render(request, 'blog/subcategory_posts.html', context)

def search_posts(request):
    """Vista de búsqueda"""
    form = SearchForm(request.GET)
    posts = Post.objects.filter(published=True)
    
    if form.is_valid():
        query = form.cleaned_data.get('query')
        category = form.cleaned_data.get('category')
        rating = form.cleaned_data.get('rating')
        year_from = form.cleaned_data.get('year_from')
        year_to = form.cleaned_data.get('year_to')
        
        if query:
            posts = posts.filter(
                Q(title__icontains=query) |
                Q(movie_title__icontains=query) |
                Q(director__icontains=query) |
                Q(content__icontains=query)
            )
        
        if category:
            posts = posts.filter(category=category)
        
        if rating:
            posts = posts.filter(rating=rating)
        
        if year_from:
            posts = posts.filter(release_year__gte=year_from)
        
        if year_to:
            posts = posts.filter(release_year__lte=year_to)
    
    paginator = Paginator(posts, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'form': form,
        'posts': page_obj,
        'page_obj': page_obj,
        'query': request.GET.get('query', ''),
    }
    return render(request, 'blog/search_results.html', context)

@login_required
def create_post(request):
    """Vista para crear un nuevo post"""
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Tu reseña ha sido creada exitosamente.')
            return redirect('blog:post_detail', slug=post.slug)
    else:
        form = PostForm()
    
    return render(request, 'blog/create_post.html', {'form': form})

@login_required
def edit_post(request, slug):
    """Vista para editar un post existente"""
    post = get_object_or_404(Post, slug=slug, author=request.user)
    
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tu reseña ha sido actualizada.')
            return redirect('blog:post_detail', slug=post.slug)
    else:
        form = PostForm(instance=post)
    
    return render(request, 'blog/edit_post.html', {'form': form, 'post': post})

@login_required
def delete_post(request, slug):
    """Vista para eliminar un post"""
    post = get_object_or_404(Post, slug=slug, author=request.user)
    
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Tu reseña ha sido eliminada.')
        return redirect('blog:home')
    
    return render(request, 'blog/delete_post.html', {'post': post})

@login_required
def user_posts(request):
    """Vista para mostrar los posts del usuario actual"""
    posts = Post.objects.filter(author=request.user)
    
    paginator = Paginator(posts, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'posts': page_obj,
        'page_obj': page_obj,
    }
    return render(request, 'blog/user_posts.html', context)

def register(request):
    """Vista de registro de usuarios"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'¡Bienvenido {user.first_name}! Tu cuenta ha sido creada.')
            return redirect('blog:home')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'registration/register.html', {'form': form})

@require_POST
@login_required
def add_comment(request, post_slug):
    """Vista AJAX para añadir comentarios"""
    post = get_object_or_404(Post, slug=post_slug, published=True)
    form = CommentForm(request.POST)
    
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.author = request.user
        
        # Verificar si es una respuesta
        parent_id = request.POST.get('parent_id')
        if parent_id:
            comment.parent = get_object_or_404(Comment, id=parent_id)
        
        comment.save()
        
        return JsonResponse({
            'success': True,
            'comment': {
                'author': comment.author.get_full_name() or comment.author.username,
                'content': comment.content,
                'created_at': comment.created_at.strftime('%d/%m/%Y %H:%M'),
                'is_reply': comment.is_reply,
            }
        })
    
    return JsonResponse({'success': False, 'errors': form.errors})

def load_subcategories(request):
    """Vista AJAX para cargar subcategorías basadas en la categoría seleccionada"""
    category_id = request.GET.get('category_id')
    subcategories = Subcategory.objects.filter(category_id=category_id).values('id', 'name')
    return JsonResponse(list(subcategories), safe=False)

def categories_list(request):
    """Vista para mostrar todas las categorías"""
    categories = Category.objects.annotate(
        post_count=Count('posts', filter=Q(posts__published=True))
    )
    
    context = {'categories': categories}
    return render(request, 'blog/categories_list.html', context)

def category_posts(request, slug):
    """Vista para posts de una categoría específica con filtros"""
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(category=category, published=True)
    
    # Aplicar filtros
    search = request.GET.get('search', '')
    rating = request.GET.get('rating', '')
    sort = request.GET.get('sort', '-created_at')
    
    if search:
        posts = posts.filter(
            Q(title__icontains=search) |
            Q(movie_title__icontains=search) |
            Q(director__icontains=search) |
            Q(content__icontains=search)
        )
    
    if rating:
        posts = posts.filter(rating=rating)
    
    # Ordenamiento
    valid_sorts = ['-created_at', 'created_at', '-rating', 'title', '-release_year']
    if sort in valid_sorts:
        posts = posts.order_by(sort)
    
    paginator = Paginator(posts, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'posts': page_obj,
        'page_obj': page_obj,
    }
    return render(request, 'blog/category_posts.html', context)

def subcategory_posts(request, category_slug, subcategory_slug):
    """Vista para posts de una subcategoría específica con filtros"""
    category = get_object_or_404(Category, slug=category_slug)
    subcategory = get_object_or_404(Subcategory, slug=subcategory_slug, category=category)
    posts = Post.objects.filter(subcategory=subcategory, published=True)
    
    # Aplicar filtros
    search = request.GET.get('search', '')
    rating = request.GET.get('rating', '')
    sort = request.GET.get('sort', '-created_at')
    
    if search:
        posts = posts.filter(
            Q(title__icontains=search) |
            Q(movie_title__icontains=search) |
            Q(director__icontains=search) |
            Q(content__icontains=search)
        )
    
    if rating:
        posts = posts.filter(rating=rating)
    
    # Ordenamiento
    valid_sorts = ['-created_at', 'created_at', '-rating', 'title', '-release_year']
    if sort in valid_sorts:
        posts = posts.order_by(sort)
    
    paginator = Paginator(posts, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'subcategory': subcategory,
        'posts': page_obj,
        'page_obj': page_obj,
    }
    return render(request, 'blog/subcategory_posts.html', context)

def user_posts(request):
    """Vista para mostrar los posts del usuario actual con filtros"""
    posts = Post.objects.filter(author=request.user)
    
    # Aplicar filtros
    search = request.GET.get('search', '')
    status = request.GET.get('status', '')
    order = request.GET.get('order', '-created_at')
    
    if search:
        posts = posts.filter(
            Q(title__icontains=search) |
            Q(movie_title__icontains=search)
        )
    
    if status == 'published':
        posts = posts.filter(published=True)
    elif status == 'draft':
        posts = posts.filter(published=False)
    elif status == 'featured':
        posts = posts.filter(featured=True)
    
    # Ordenamiento
    valid_orders = ['-created_at', 'created_at', 'title', '-title', '-rating']
    if order in valid_orders:
        posts = posts.order_by(order)
    
    paginator = Paginator(posts, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'posts': page_obj,
        'page_obj': page_obj,
    }
    return render(request, 'blog/user_posts.html', context)

def custom_login(request):
    """Vista personalizada para login"""
    if request.user.is_authenticated:
        return redirect('blog:home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'¡Bienvenido de vuelta, {user.first_name or user.username}!')
                return redirect('blog:home')
            else:
                messages.error(request, 'Nombre de usuario o contraseña incorrectos.')
        else:
            messages.error(request, 'Por favor, completa todos los campos.')
    
    return render(request, 'registration/login.html')

def custom_logout(request):
    """Vista personalizada para logout que funciona con GET y POST"""
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, 'Has cerradooooooo sesión correctamente.')
    
    
    # Redirigir al inicio después de mostrar la página de logout
    return render(request, 'registration/logged_out.html')

@login_required
def toggle_like(request, post_slug):
    """Vista AJAX para dar/quitar like a una reseña"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Method not allowed'})
    
    try:
        post = get_object_or_404(Post, slug=post_slug, published=True)
        user = request.user
        
        print(f"Toggle like request: post={post.title}, user={user.username}")
        print(f"Request method: {request.method}")
        print(f"CSRF token: {request.META.get('HTTP_X_CSRFTOKEN', 'Not provided')}")
        
        # Verificar si el usuario ya dio like
        like, created = PostLike.objects.get_or_create(post=post, user=user)
        
        if not created:
            # Si ya existía, lo eliminamos (toggle)
            like.delete()
            liked = False
            print(f"Like removed for post {post.title}")
        else:
            # Si se creó nuevo, el usuario dio like
            liked = True
            print(f"Like added for post {post.title}")
        
        likes_count = post.get_likes_count()
        print(f"Total likes for {post.title}: {likes_count}")
        
        # Retornar respuesta JSON
        return JsonResponse({
            'success': True,
            'liked': liked,
            'likes_count': likes_count
        })
    except Exception as e:
        print(f"Error in toggle_like: {e}")
        return JsonResponse({
            'success': False,
            'error': str(e)
        })
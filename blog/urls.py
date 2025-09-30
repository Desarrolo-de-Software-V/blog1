from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # Página principal
    path('', views.home, name='home'),
    
    # Posts
    path('posts/', views.PostListView.as_view(), name='post_list'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    path('create/', views.create_post, name='create_post'),
    path('edit/<slug:slug>/', views.edit_post, name='edit_post'),
    path('delete/<slug:slug>/', views.delete_post, name='delete_post'),
    path('my-posts/', views.user_posts, name='user_posts'),
    
    # Categorías
    path('categories/', views.categories_list, name='categories_list'),
    path('category/<slug:slug>/', views.category_posts, name='category_posts'),
    path('category/<slug:category_slug>/<slug:subcategory_slug>/', 
         views.subcategory_posts, name='subcategory_posts'),
    
    # Búsqueda
    path('search/', views.search_posts, name='search'),
    
    # AJAX
    path('load-subcategories/', views.load_subcategories, name='load_subcategories'),
    path('add-comment/<slug:post_slug>/', views.add_comment, name='add_comment'),
    path('toggle-like/<slug:post_slug>/', views.toggle_like, name='toggle_like'),
    path('toggle-reaction/<slug:post_slug>/', views.toggle_reaction, name='toggle_reaction'),
    path('toggle-comment-vote/<int:comment_id>/', views.toggle_comment_vote, name='toggle_comment_vote'),
    
    # Registro
    path('register/', views.register, name='register'),
    
    # Login personalizado
    path('login/', views.custom_login, name='login'),
    
    # Logout personalizado
    path('logout/', views.custom_logout, name='logout'),
    path('accounts/logout/', views.custom_logout),
]
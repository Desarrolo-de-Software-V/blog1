from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils.text import slugify
from blog.models import Category, Subcategory, Post
import random

class Command(BaseCommand):
    help = 'Crea datos de ejemplo para el blog de reseñas'

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Elimina todos los datos existentes antes de crear nuevos',
        )

    def handle(self, *args, **options):
        if options['reset']:
            self.stdout.write('Eliminando datos existentes...')
            Post.objects.all().delete()
            Subcategory.objects.all().delete()
            Category.objects.all().delete()
            User.objects.filter(is_superuser=False).delete()

        self.stdout.write('Creando categorías...')
        self.create_categories()
        
        self.stdout.write('Creando usuarios de ejemplo...')
        self.create_users()
        
        self.stdout.write('Creando reseñas de ejemplo...')
        self.create_posts()
        
        self.stdout.write(
            self.style.SUCCESS('¡Datos de ejemplo creados exitosamente!')
        )

    def create_categories(self):
        """Crear categorías y subcategorías"""
        categories_data = {
            'Películas': {
                'description': 'Reseñas de películas de todos los géneros y épocas',
                'subcategories': [
                    'Acción', 'Comedia', 'Drama', 'Terror', 'Ciencia Ficción',
                    'Romance', 'Thriller', 'Aventura', 'Fantasía', 'Animación'
                ]
            },
            'Anime': {
                'description': 'Reseñas de series y películas de anime',
                'subcategories': [
                    'Shonen', 'Shojo', 'Seinen', 'Josei', 'Mecha',
                    'Isekai', 'Slice of Life', 'Sports', 'Supernatural'
                ]
            },
            'Series': {
                'description': 'Reseñas de series de televisión y streaming',
                'subcategories': [
                    'Drama', 'Comedia', 'Ciencia Ficción', 'Crime',
                    'Documentales', 'Reality', 'Miniseries'
                ]
            },
            'Documentales': {
                'description': 'Reseñas de documentales y contenido educativo',
                'subcategories': [
                    'Naturaleza', 'Historia', 'Ciencia', 'Biografías',
                    'Crimen Real', 'Deportes', 'Tecnología'
                ]
            }
        }

        for cat_name, cat_data in categories_data.items():
            category, created = Category.objects.get_or_create(
                name=cat_name,
                defaults={
                    'slug': slugify(cat_name),
                    'description': cat_data['description']
                }
            )
            
            if created:
                self.stdout.write(f'  ✓ Creada categoría: {cat_name}')
            
            # Crear subcategorías
            for subcat_name in cat_data['subcategories']:
                subcategory, sub_created = Subcategory.objects.get_or_create(
                    name=subcat_name,
                    category=category,
                    defaults={'slug': slugify(subcat_name)}
                )
                if sub_created:
                    self.stdout.write(f'    ✓ Creada subcategoría: {subcat_name}')

    def create_users(self):
        """Crear usuarios de ejemplo"""
        users_data = [
            {
                'username': 'cinefilo_experto',
                'email': 'cinefilo@example.com',
                'first_name': 'María',
                'last_name': 'González',
                'password': 'demo123'
            },
            {
                'username': 'anime_lover',
                'email': 'anime@example.com',
                'first_name': 'Carlos',
                'last_name': 'Ruiz',
                'password': 'demo123'
            },
            {
                'username': 'critico_series',
                'email': 'series@example.com',
                'first_name': 'Ana',
                'last_name': 'Martínez',
                'password': 'demo123'
            },
            {
                'username': 'demo',
                'email': 'demo@example.com',
                'first_name': 'Usuario',
                'last_name': 'Demo',
                'password': 'demo123'
            }
        ]

        for user_data in users_data:
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults={
                    'email': user_data['email'],
                    'first_name': user_data['first_name'],
                    'last_name': user_data['last_name']
                }
            )
            if created:
                user.set_password(user_data['password'])
                user.save()
                self.stdout.write(f'  ✓ Creado usuario: {user_data["username"]}')

    def create_posts(self):
        """Crear reseñas de ejemplo"""
        posts_data = [
            {
                'title': 'Avatar: El Camino del Agua - Espectáculo Visual Sin Límites',
                'movie_title': 'Avatar: The Way of Water',
                'director': 'James Cameron',
                'release_year': 2022,
                'rating': 4,
                'category': 'Películas',
                'subcategory': 'Ciencia Ficción',
                'excerpt': 'James Cameron regresa a Pandora con una secuela que eleva los estándares visuales del cine.',
                'content': '''La tan esperada secuela de Avatar nos transporta una vez más al exuberante mundo de Pandora, esta vez explorando los océanos y sus majestuosas criaturas. James Cameron demuestra una vez más su maestría técnica, creando secuencias submarinas que literalmente quitan el aliento.

La historia sigue a Jake Sully y su familia mientras enfrentan nuevas amenazas y buscan refugio entre los clanes acuáticos. Aunque la trama puede resultar predecible en algunos momentos, la experiencia visual compensa cualquier deficiencia narrativa.

Los efectos especiales son, sin lugar a dudas, revolucionarios. Cada gota de agua, cada movimiento bajo el mar, está renderizado con un nivel de detalle que hace que te olvides de que estás viendo CGI. La tecnología de captura de movimiento submarino desarrollada específicamente para esta película establece un nuevo estándar para la industria.

El mensaje ecológico, aunque no sutil, es más relevante que nunca. Cameron utiliza la belleza de Pandora para recordarnos lo que podríamos perder si no cuidamos nuestro propio planeta.

En conclusión, Avatar 2 es más una experiencia que una película tradicional. Es cine que debe verse en la pantalla más grande posible, preferiblemente en IMAX 3D.''',
                'featured': True,
                'author': 'cinefilo_experto'
            },
            {
                'title': 'Demon Slayer: Un Anime que Redefine la Animación',
                'movie_title': 'Kimetsu no Yaiba',
                'director': 'Haruo Sotozaki',
                'release_year': 2019,
                'rating': 5,
                'category': 'Anime',
                'subcategory': 'Shonen',
                'excerpt': 'Una obra maestra de animación que combina una historia emotiva con secuencias de acción espectaculares.',
                'content': '''Demon Slayer (Kimetsu no Yaiba) ha revolucionado el mundo del anime con su impresionante calidad de animación y una narrativa que toca el corazón. Studio Ufotable ha creado una obra visual sin precedentes.

La historia de Tanjiro Kamado y su búsqueda para curar a su hermana demonio es emotiva y está llena de momentos que te harán llorar. Lo que distingue a esta serie es cómo humaniza incluso a sus villanos, mostrando sus historias trágicas antes de su transformación.

Las secuencias de combate son pura poesía en movimiento. Cada técnica de respiración está bellamente animada, especialmente las del Agua de Tanjiro y las espectaculares formas del Trueno de Zenitsu.

Los personajes están bien desarrollados, cada uno con personalidades distintivas y trasfondos convincentes. La amistad entre Tanjiro, Zenitsu e Inosuke es uno de los puntos fuertes de la serie.

Sin duda, Demon Slayer ha establecido un nuevo estándar para la animación de anime y es imprescindible para cualquier fan del género.''',
                'featured': True,
                'author': 'anime_lover'
            },
            {
                'title': 'The Last of Us: Televisión que Supera al Videojuego',
                'movie_title': 'The Last of Us',
                'director': 'Craig Mazin, Neil Druckmann',
                'release_year': 2023,
                'rating': 5,
                'category': 'Series',
                'subcategory': 'Drama',
                'excerpt': 'Una adaptación que respeta el material original mientras crea algo único para la televisión.',
                'content': '''Pocas adaptaciones de videojuegos han logrado capturar la esencia del material original tan perfectamente como The Last of Us de HBO. Craig Mazin y Neil Druckmann han creado una obra maestra de la televisión.

Pedro Pascal y Bella Ramsey entregan actuaciones excepcionales como Joel y Ellie. Su química es inmediata y creíble, y ambos logran hacer suyos personajes que los fans ya conocían y amaban.

La serie no se conforma con ser una traducción directa del juego. Expande el mundo, desarrolla personajes secundarios y explora temas que en el videojuego solo se tocaban superficialmente.

Los infectados están diseñados magistralmente, con efectos prácticos que los hacen terríficamente reales. Pero son los momentos humanos los que realmente brillan: la pérdida, el amor, la supervivencia y la esperanza.

Cada episodio es una pequeña película con su propia narrativa, pero todo se conecta en una historia épica sobre la humanidad en sus peores y mejores momentos.

The Last of Us demuestra que las adaptaciones pueden ser arte por derecho propio.''',
                'featured': True,
                'author': 'critico_series'
            },
            {
                'title': 'Oppenheimer: Nolan en su Máximo Esplendor',
                'movie_title': 'Oppenheimer',
                'director': 'Christopher Nolan',
                'release_year': 2023,
                'rating': 4,
                'category': 'Películas',
                'subcategory': 'Drama',
                'excerpt': 'Un biopic complejo que explora la mente del hombre detrás de la bomba atómica.',
                'content': '''Christopher Nolan regresa con una biografía épica que examina la vida de J. Robert Oppenheimer, el físico teórico que dirigió el Proyecto Manhattan. Como es típico de Nolan, la narrativa no es lineal y requiere atención completa del espectador.

Cillian Murphy entrega la actuación de su carrera como Oppenheimer, capturando la brillantez y la carga moral del científico. Robert Downey Jr. también brilla como Lewis Strauss, mostrando una faceta dramática poco vista.

La película es un tour de force técnico. Nolan filmó en IMAX de 70mm y los resultados son visualmente impresionantes. La secuencia de la prueba Trinity es particularmente espectacular, creada enteramente con efectos prácticos.

Lo que más impresiona es cómo Nolan maneja temas complejos: la responsabilidad científica, las consecuencias de la guerra, y el precio personal del genio. No hay respuestas fáciles, solo preguntas profundas.

Aunque puede resultar densa en algunos momentos, Oppenheimer es cine adulto en su mejor forma: inteligente, desafiante y visualmente magnífico.''',
                'author': 'cinefilo_experto'
            },
            {
                'title': 'Jujutsu Kaisen: Renovando el Shonen Moderno',
                'movie_title': 'Jujutsu Kaisen',
                'director': 'Sunghoo Park',
                'release_year': 2020,
                'rating': 4,
                'category': 'Anime',
                'subcategory': 'Shonen',
                'excerpt': 'Un anime que toma los tropos clásicos del shonen y los presenta con un estilo fresco y maduro.',
                'content': '''Jujutsu Kaisen ha tomado por asalto el mundo del anime, y por buenas razones. Studio MAPPA ha creado una serie que respeta las tradiciones del shonen mientras aporta elementos únicos y una presentación visual excepcional.

Yuji Itadori es un protagonista refrescante: poderoso pero no invencible, bondadoso pero no ingenuo. Su desarrollo junto a Megumi Fushiguro y Nobara Kugisaki crea una dinámica de equipo genuina y entretenida.

El sistema de poder basado en energía maldita es innovador y permite combates estratégicos únicos. Cada hechicero tiene habilidades distintivas que se traducen en secuencias de acción visualmente impresionantes.

Lo que distingue a Jujutsu Kaisen es su tono maduro. No evita mostrar las consecuencias reales de la violencia y los personajes enfrentan pérdidas genuinas. Esto crea un peso emocional que muchos shonen carecen.

Gojo Satoru se ha convertido instantáneamente en uno de los personajes más icónicos del anime moderno, y la animación de sus técnicas es simplemente espectacular.

Una serie imprescindible para fans nuevos y veteranos del género.''',
                'author': 'anime_lover'
            },
            {
                'title': 'House of the Dragon: Regreso Exitoso a Westeros',
                'movie_title': 'House of the Dragon',
                'director': 'Miguel Sapochnik, Ryan Condal',
                'release_year': 2022,
                'rating': 3,
                'category': 'Series',
                'subcategory': 'Drama',
                'excerpt': 'Una precuela que recupera parte de la magia perdida de Game of Thrones.',
                'content': '''Después del final controvertido de Game of Thrones, HBO tenía una tarea difícil con House of the Dragon. Afortunadamente, la serie logra capturar gran parte de lo que hizo especial a la serie original.

Ambientada 200 años antes de los eventos de GoT, la serie se centra en la Casa Targaryen en su apogeo. Los dragones son espectaculares, claramente beneficiándose de un presupuesto y tecnología superiores.

Paddy Considine como Viserys Targaryen entrega una actuación matizada, mostrando a un rey débil pero bien intencionado. Emma D'Arcy y Olivia Cooke como Rhaenyra en diferentes edades crean un personaje complejo y fascinante.

La serie recupera la complejidad política que hizo famosa a GoT. Las maquinaciones de la corte, las alianzas cambiantes y las consecuencias imprevistas están de vuelta en toda su gloria.

Sin embargo, ocasionalmente se siente demasiado familiar, como si estuviera siguiendo una fórmula. Los momentos verdaderamente sorprendentes son menos frecuentes que en las primeras temporadas de GoT.

Aún así, House of the Dragon es televisión de calidad que devuelve credibilidad a la marca Westeros.''',
                'author': 'critico_series'
            }
        ]

        # Obtener usuarios
        users = {user.username: user for user in User.objects.all()}
        
        for post_data in posts_data:
            # Obtener categoría y subcategoría
            try:
                category = Category.objects.get(name=post_data['category'])
                subcategory = None
                if post_data.get('subcategory'):
                    subcategory = Subcategory.objects.get(
                        name=post_data['subcategory'], 
                        category=category
                    )
                
                author = users.get(post_data['author'])
                if not author:
                    author = User.objects.first()
                
                post, created = Post.objects.get_or_create(
                    title=post_data['title'],
                    defaults={
                        'slug': slugify(post_data['title']),
                        'movie_title': post_data['movie_title'],
                        'director': post_data.get('director', ''),
                        'release_year': post_data['release_year'],
                        'rating': post_data['rating'],
                        'category': category,
                        'subcategory': subcategory,
                        'excerpt': post_data['excerpt'],
                        'content': post_data['content'],
                        'author': author,
                        'published': True,
                        'featured': post_data.get('featured', False)
                    }
                )
                
                if created:
                    self.stdout.write(f'  ✓ Creada reseña: {post_data["title"][:50]}...')
                    
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Error creando reseña {post_data["title"]}: {e}')
                )
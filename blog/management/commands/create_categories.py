from django.core.management.base import BaseCommand
from blog.models import Category, Subcategory


class Command(BaseCommand):
    help = 'Crea las categorías y subcategorías para anime y películas'

    def handle(self, *args, **options):
        # Crear categorías de anime por demografía
        anime_demographics = {
            'Shōnen': {
                'description': 'Dirigido a chicos adolescentes',
                'subcategories': ['Acción', 'Deportes', 'Amistad', 'Torneos', 'Aventuras']
            },
            'Shōjo': {
                'description': 'Dirigido a chicas adolescentes',
                'subcategories': ['Romance', 'Drama', 'Slice of Life', 'Magical Girls (Mahō Shōjo)']
            },
            'Seinen': {
                'description': 'Dirigido a jóvenes/adultos varones',
                'subcategories': ['Psicológico', 'Gore', 'Misterio', 'Ciencia Ficción Madura', 'Suspenso']
            },
            'Josei': {
                'description': 'Dirigido a mujeres adultas',
                'subcategories': ['Romance Realista', 'Drama', 'Slice of Life', 'Historias Laborales']
            },
            'Kodomomuke': {
                'description': 'Dirigido a niños',
                'subcategories': ['Educativo', 'Aventuras Ligeras', 'Comedia Infantil']
            }
        }

        # Crear categorías temáticas de anime
        anime_genres = {
            'Acción': {
                'description': 'Peleas, batallas, combates',
                'subcategories': ['Artes Marciales', 'Samuráis', 'Mechas', 'Guerra']
            },
            'Aventura': {
                'description': 'Viajes, exploración, mundos nuevos',
                'subcategories': ['Fantasía', 'Isekai', 'Viajes Temporales']
            },
            'Comedia': {
                'description': 'Humor',
                'subcategories': ['Parodia', 'Gag', 'Romántica', 'Absurda', 'Slice of Life Cómico']
            },
            'Drama': {
                'description': 'Emociones intensas',
                'subcategories': ['Tragedia', 'Romance Dramático', 'Familiar', 'Histórico']
            },
            'Fantasía': {
                'description': 'Mundos mágicos o irreales',
                'subcategories': ['Alta Fantasía', 'Baja Fantasía', 'Isekai', 'Dark Fantasy']
            },
            'Ciencia Ficción (Sci-Fi)': {
                'description': 'Tecnología, futuro, espacio',
                'subcategories': ['Mecha', 'Cyberpunk', 'Viajes Espaciales', 'Biotecnología']
            },
            'Terror / Horror': {
                'description': 'Provocar miedo',
                'subcategories': ['Psicológico', 'Gore', 'Sobrenatural', 'Survival']
            },
            'Romance': {
                'description': 'Relaciones amorosas',
                'subcategories': ['Escolar', 'Yaoi/BL (Boys Love)', 'Yuri/GL (Girls Love)', 'Comedia Romántica', 'Romance Trágico']
            },
            'Slice of Life': {
                'description': 'Vida cotidiana',
                'subcategories': ['Escolar', 'Laboral', 'Familiar', 'Relajante']
            },
            'Deportes (Spokon)': {
                'description': 'Competitividad',
                'subcategories': ['Fútbol', 'Béisbol', 'Baloncesto', 'Artes Marciales', 'E-sports']
            },
            'Musical / Idol': {
                'description': 'Música y grupos de idols',
                'subcategories': ['Idols', 'Bandas de Rock', 'Baile', 'Canto']
            },
            'Misterio / Thriller': {
                'description': 'Resolución de casos',
                'subcategories': ['Detectivesco', 'Policial', 'Psicológico', 'Crimen']
            },
            'Histórico': {
                'description': 'Basado en épocas reales',
                'subcategories': ['Samuráis', 'Guerras Mundiales', 'Feudal', 'Biográfico']
            }
        }

        # Crear categorías de películas
        movie_genres = {
            'Acción': {
                'description': 'Peleas, batallas, combates',
                'subcategories': ['Artes Marciales', 'Espionaje', 'Superhéroes', 'Western', 'Bélicas']
            },
            'Aventura': {
                'description': 'Viajes, exploración, mundos nuevos',
                'subcategories': ['Exploración', 'Supervivencia', 'Viajes']
            },
            'Comedia': {
                'description': 'Humor',
                'subcategories': ['Romántica', 'Negra', 'Parodia', 'Satírica', 'Musical']
            },
            'Drama': {
                'description': 'Emociones intensas',
                'subcategories': ['Social', 'Romántico', 'Histórico', 'Legal', 'Político']
            },
            'Fantasía': {
                'description': 'Mundos mágicos o irreales',
                'subcategories': ['Épica', 'Urbana', 'Dark Fantasy', 'Cuento de Hadas']
            },
            'Ciencia Ficción': {
                'description': 'Tecnología, futuro, espacio',
                'subcategories': ['Distopía', 'Cyberpunk', 'Space Opera', 'Viajes en el Tiempo']
            },
            'Terror': {
                'description': 'Provocar miedo',
                'subcategories': ['Slasher', 'Gore', 'Psicológico', 'Sobrenatural', 'Monstruos', 'Zombies']
            },
            'Romance': {
                'description': 'Relaciones amorosas',
                'subcategories': ['Juvenil', 'Trágico', 'Romántico-Histórico', 'Musical']
            },
            'Musical': {
                'description': 'Música y baile',
                'subcategories': ['Ópera Rock', 'Jukebox', 'Animados', 'Comedia Musical']
            },
            'Documental': {
                'description': 'Contenido real',
                'subcategories': ['Naturaleza', 'Social', 'Político', 'Histórico', 'Biográfico']
            },
            'Animación': {
                'description': 'Contenido animado',
                'subcategories': ['Anime', 'CGI', 'Stop-Motion', 'Híbrido', 'Infantil']
            },
            'Crimen / Policíaco': {
                'description': 'Investigación y crimen',
                'subcategories': ['Thriller', 'Noir', 'Mafias', 'Suspenso Legal']
            },
            'Histórico / Bélico': {
                'description': 'Basado en eventos históricos',
                'subcategories': ['Guerras Mundiales', 'Biográficos', 'Conflictos Bélicos', 'Period Drama']
            },
            'Suspenso / Thriller': {
                'description': 'Tensión y misterio',
                'subcategories': ['Psicológico', 'Conspiración', 'Acción-Thriller']
            }
        }

        # Crear categorías de demografía de anime
        self.stdout.write('Creando categorías de demografía de anime...')
        for cat_name, cat_data in anime_demographics.items():
            category, created = Category.objects.get_or_create(
                name=cat_name,
                defaults={
                    'description': cat_data['description'],
                    'slug': self.slugify(cat_name)
                }
            )
            
            if created:
                self.stdout.write(f'✓ Categoría creada: {cat_name}')
            else:
                self.stdout.write(f'→ Categoría ya existe: {cat_name}')
            
            # Crear subcategorías
            for subcat_name in cat_data['subcategories']:
                subcategory, created = Subcategory.objects.get_or_create(
                    name=subcat_name,
                    category=category,
                    defaults={
                        'slug': self.slugify(subcat_name)
                    }
                )
                if created:
                    self.stdout.write(f'  ✓ Subcategoría creada: {subcat_name}')

        # Crear categorías temáticas de anime
        self.stdout.write('\nCreando categorías temáticas de anime...')
        for cat_name, cat_data in anime_genres.items():
            category, created = Category.objects.get_or_create(
                name=cat_name,
                defaults={
                    'description': cat_data['description'],
                    'slug': self.slugify(cat_name)
                }
            )
            
            if created:
                self.stdout.write(f'✓ Categoría creada: {cat_name}')
            else:
                self.stdout.write(f'→ Categoría ya existe: {cat_name}')
            
            # Crear subcategorías
            for subcat_name in cat_data['subcategories']:
                subcategory, created = Subcategory.objects.get_or_create(
                    name=subcat_name,
                    category=category,
                    defaults={
                        'slug': self.slugify(subcat_name)
                    }
                )
                if created:
                    self.stdout.write(f'  ✓ Subcategoría creada: {subcat_name}')

        # Crear categorías de películas
        self.stdout.write('\nCreando categorías de películas...')
        for cat_name, cat_data in movie_genres.items():
            category, created = Category.objects.get_or_create(
                name=cat_name,
                defaults={
                    'description': cat_data['description'],
                    'slug': self.slugify(cat_name)
                }
            )
            
            if created:
                self.stdout.write(f'✓ Categoría creada: {cat_name}')
            else:
                self.stdout.write(f'→ Categoría ya existe: {cat_name}')
            
            # Crear subcategorías
            for subcat_name in cat_data['subcategories']:
                subcategory, created = Subcategory.objects.get_or_create(
                    name=subcat_name,
                    category=category,
                    defaults={
                        'slug': self.slugify(subcat_name)
                    }
                )
                if created:
                    self.stdout.write(f'  ✓ Subcategoría creada: {subcat_name}')

        self.stdout.write(
            self.style.SUCCESS('\n¡Todas las categorías y subcategorías han sido creadas exitosamente!')
        )

    def slugify(self, text):
        """Convierte texto a slug"""
        import re
        import unicodedata
        
        # Normalizar caracteres especiales (quitar tildes, etc.)
        slug = unicodedata.normalize('NFD', text)
        slug = ''.join(c for c in slug if unicodedata.category(c) != 'Mn')
        
        # Convertir a minúsculas
        slug = slug.lower()
        
        # Reemplazar caracteres especiales y espacios
        slug = re.sub(r'[^\w\s-]', '', slug)
        slug = re.sub(r'[-\s]+', '-', slug)
        
        return slug.strip('-')

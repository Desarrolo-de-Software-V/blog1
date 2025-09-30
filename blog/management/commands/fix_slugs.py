from django.core.management.base import BaseCommand
from blog.models import Category, Subcategory


class Command(BaseCommand):
    help = 'Corrige los slugs de categorías y subcategorías para manejar caracteres especiales'

    def handle(self, *args, **options):
        self.stdout.write('Corrigiendo slugs de categorías...')
        
        # Actualizar categorías
        categories_updated = 0
        for category in Category.objects.all():
            old_slug = category.slug
            new_slug = self.slugify(category.name)
            if old_slug != new_slug:
                category.slug = new_slug
                category.save()
                self.stdout.write(f'✓ Categoría "{category.name}": {old_slug} → {new_slug}')
                categories_updated += 1
        
        # Actualizar subcategorías
        self.stdout.write('\nCorrigiendo slugs de subcategorías...')
        subcategories_updated = 0
        for subcategory in Subcategory.objects.all():
            old_slug = subcategory.slug
            new_slug = self.slugify(subcategory.name)
            if old_slug != new_slug:
                subcategory.slug = new_slug
                subcategory.save()
                self.stdout.write(f'✓ Subcategoría "{subcategory.name}": {old_slug} → {new_slug}')
                subcategories_updated += 1
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\n¡Slugs corregidos exitosamente!\n'
                f'Categorías actualizadas: {categories_updated}\n'
                f'Subcategorías actualizadas: {subcategories_updated}'
            )
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


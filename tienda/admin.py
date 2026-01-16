from django.contrib import admin
from .models import Categoria, Marca, Producto, Subcategoria, ImagenProducto 
class SubcategoriaInline(admin.TabularInline):
    model = Subcategoria
    extra = 2
    fields = ('nombre', 'orden')

class ImagenProductoInline(admin.TabularInline):
    model = ImagenProducto
    extra = 3

class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'orden')
    list_editable = ('orden',)
    inlines = [SubcategoriaInline]

class MarcaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'orden')
    list_editable = ('orden',)

class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'categoria', 'orden', 'destacado')
    list_editable = ('orden', 'destacado')
    list_filter = ('categoria', 'marca', 'destacado', 'stock')
    search_fields = ('nombre', 'descripcion')
    inlines = [ImagenProductoInline] 

# Registro de los modelos
admin.site.register(Producto, ProductoAdmin)
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Marca, MarcaAdmin)
admin.site.register(Subcategoria)
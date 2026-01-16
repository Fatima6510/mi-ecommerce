from django.shortcuts import render, Http404, redirect
from .models import Producto, Categoria, Marca

banners = [
    {'blanco': 'Power Your', 'rojo': 'Work', 'img': 'https://images.unsplash.com/photo-1550745165-9bc0b252726f?w=1600'},
    {'blanco': 'Gaming', 'rojo': 'Gear', 'img': 'https://images.unsplash.com/photo-1542751371-adc38448a05e?w=1600'},
    {'blanco': 'New', 'rojo': 'Arrivals', 'img': 'https://images.unsplash.com/photo-1593642632823-8f785ba67e45?w=1600'},
]

def home(request):
    return render(request, 'tienda/index.html', {
        'destacados': Producto.objects.filter(destacado=True).order_by('orden'),
        'marcas': Marca.objects.all().order_by('orden'),
        'categorias': Categoria.objects.all().order_by('orden'),
        'menu_lateral': Categoria.objects.all().prefetch_related('subcategorias'),
        'banners': banners,
        'todos_los_productos': Producto.objects.all()[:15] 
    })

def lista_productos(request, slug=None):
    query = request.GET.get('q') 
    marca_filtro = request.GET.get('marca')
    sub_nombre = request.GET.get('sub') 
    
    productos = Producto.objects.all()
    titulo = "Todos los Productos"

    if query:
        productos = productos.filter(nombre__icontains=query)
        titulo = f"Resultados para: '{query}'"
    
    elif sub_nombre:
        productos = productos.filter(subcategoria__nombre=sub_nombre)
        titulo = f"Categoría: {sub_nombre}"

    elif slug:
        categoria = Categoria.objects.get(slug=slug)
        productos = productos.filter(categoria=categoria)
        titulo = f"Sector: {categoria.nombre}"
    
    elif marca_filtro:
        productos = productos.filter(marca__nombre=marca_filtro)
        titulo = f"Marca: {marca_filtro}"

    return render(request, 'tienda/lista_productos.html', {
        'productos': productos,
        'titulo': titulo,
        'menu_lateral': Categoria.objects.all().prefetch_related('subcategorias'),
    })

def detalle_producto(request, id):
    producto = Producto.objects.prefetch_related('imagenes').filter(id=id).first()
    if not producto:
        raise Http404("Producto no encontrado")

    return render(request, 'tienda/detalle_producto.html', {
        'p': producto,
        'menu_lateral': Categoria.objects.all().prefetch_related('subcategorias'),
    })

# --- VISTAS DEL CARRITO  ---

def añadir_al_carrito(request, id):
    carrito = request.session.get('carrito', {})
    if not isinstance(carrito, dict): carrito = {}
    
    id_str = str(id) 
    carrito[id_str] = carrito.get(id_str, 0) + 1

    request.session['carrito'] = carrito
    return redirect(request.META.get('HTTP_REFERER', 'home'))

def restar_del_carrito(request, id):
    carrito = request.session.get('carrito', {})
    id_str = str(id)
    if id_str in carrito:
        carrito[id_str] -= 1
        if carrito[id_str] <= 0: del carrito[id_str]
    request.session['carrito'] = carrito
    return redirect('ver_carrito')

def eliminar_del_carrito(request, id):
    carrito = request.session.get('carrito', {})
    id_str = str(id)
    if id_str in carrito: del carrito[id_str]
    request.session['carrito'] = carrito
    return redirect('ver_carrito')

def ver_carrito(request):
    carrito_dict = request.session.get('carrito', {})
    productos_carrito = []
    total = 0
    
    for p_id, cantidad in carrito_dict.items():
        p = Producto.objects.filter(id=p_id).first()
        if p:
            subtotal = p.precio * cantidad
            total += subtotal
            
            productos_carrito.append({
                'info': p,
                'cantidad': cantidad,
                'subtotal': subtotal
            })
    
    return render(request, 'tienda/carrito.html', {
        'carrito': productos_carrito,
        'total': total,
        'menu_lateral': Categoria.objects.all().prefetch_related('subcategorias')
    })

def vaciar_carrito(request):
    if 'carrito' in request.session: del request.session['carrito']
    return redirect('ver_carrito')
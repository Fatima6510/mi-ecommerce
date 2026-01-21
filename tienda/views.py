from django.shortcuts import render, Http404, redirect
from .models import Producto, Categoria, Marca, Banner

def home(request):
    banners_query = Banner.objects.all().order_by('orden')
    banners_list = list(banners_query)

    if banners_list:
        banners_final = banners_list + [banners_list[0]]
    else:
        banners_final = []

    return render(request, 'tienda/index.html', {
        'banners': banners_final, 
        'destacados': Producto.objects.filter(destacado=True).order_by('orden'),
        'todos_los_productos': Producto.objects.all().order_by('orden')[:12],
        'marcas': Marca.objects.all().order_by('orden'),
        'categorias': Categoria.objects.all().order_by('orden'),
        'menu_lateral': Categoria.objects.all().prefetch_related('subcategorias').order_by('orden'),
    })

def lista_productos(request, slug=None):
    query = request.GET.get('q')
    marca_filtro = request.GET.get('marca')
    sub_filtro = request.GET.get('sub')
    
    productos = Producto.objects.all()
    titulo = "Catálogo Completo"

    if query:
        productos = productos.filter(nombre__icontains=query)
        titulo = f"Resultados para: '{query}'"
    elif sub_filtro:
        productos = productos.filter(subcategoria__nombre=sub_filtro)
        titulo = f"Categoría: {sub_filtro}"
    elif slug:
        cat = Categoria.objects.get(slug=slug)
        productos = productos.filter(categoria=cat)
        titulo = cat.nombre
    elif marca_filtro:
        m = Marca.objects.get(nombre=marca_filtro)
        productos = productos.filter(marca=m)
        titulo = f"Marca: {m.nombre}"

    return render(request, 'tienda/lista_productos.html', {
        'productos': productos,
        'titulo': titulo,
        'menu_lateral': Categoria.objects.all().prefetch_related('subcategorias').order_by('orden'),
    })

def detalle_producto(request, id):
    p = Producto.objects.prefetch_related('imagenes').filter(id=id).first()
    if not p: raise Http404()
    return render(request, 'tienda/detalle_producto.html', {
        'p': p,
        'menu_lateral': Categoria.objects.all().prefetch_related('subcategorias').order_by('orden'),
    })

# --- CARRITO ---
def añadir_al_carrito(request, id):
    carrito = request.session.get('carrito', {})
    if not isinstance(carrito, dict): carrito = {}
    id_s = str(id)
    carrito[id_s] = carrito.get(id_s, 0) + 1
    request.session['carrito'] = carrito
    return redirect(request.META.get('HTTP_REFERER', 'home'))

def restar_del_carrito(request, id):
    carrito = request.session.get('carrito', {})
    id_s = str(id)
    if id_s in carrito:
        carrito[id_s] -= 1
        if carrito[id_s] <= 0: del carrito[id_s]
    request.session['carrito'] = carrito
    return redirect('ver_carrito')

def eliminar_del_carrito(request, id):
    carrito = request.session.get('carrito', {})
    if str(id) in carrito: del carrito[str(id)]
    request.session['carrito'] = carrito
    return redirect('ver_carrito')

def ver_carrito(request):
    carrito_dict = request.session.get('carrito', {})
    items, total = [], 0
    for pid, cant in carrito_dict.items():
        p = Producto.objects.filter(id=pid).first()
        if p:
            sub = p.precio * cant
            total += sub
            items.append({'info': p, 'cantidad': cant, 'subtotal': sub})
    return render(request, 'tienda/carrito.html', {'carrito': items, 'total': total, 'menu_lateral': Categoria.objects.all().prefetch_related('subcategorias')})

def vaciar_carrito(request):
    request.session['carrito'] = {}
    return redirect('ver_carrito')
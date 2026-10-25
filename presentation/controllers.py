from flask import Blueprint, render_template, request, redirect, url_for, flash
from infrastructure.repositories import LivrariaRepository
from application.services import LivrariaService

presentation_bp = Blueprint('presentation', __name__, template_folder='templates')

# Injeção das camadas inferiores
repositorio = LivrariaRepository()
servico = LivrariaService(repositorio)

@presentation_bp.route('/', methods=['GET'])
def index():
    termo = request.args.get('q', '')
    genero = request.args.get('genero', '')
    livros = servico.filtrar_catalogo(termo, genero)
    resumo = servico.calcular_resumo_carrinho()

    return render_template(
        'index.html',
        livros=livros,
        carrinho=repositorio.obter_itens_carrinho(),
        resumo=resumo,
        favoritos=repositorio.obter_livros_favoritos(),
        favoritos_ids=repositorio.obter_ids_favoritos(),
        recibo_qr=repositorio.ultimo_recibo_qr,
        termo_atual=termo,
        genero_atual=genero
    )

@presentation_bp.route('/adicionar/<int:livro_id>', methods=['POST'])
def adicionar(livro_id):
    livro = servico.adicionar_ao_carrinho(livro_id)
    if livro:
        flash(f'"{livro.titulo}" adicionado ao carrinho!', 'sucesso')
    return redirect(url_for('presentation.index'))

@presentation_bp.route('/favoritar/<int:livro_id>', methods=['POST'])
def favoritar(livro_id):
    livro, adicionado = servico.alternar_livro_favorito(livro_id)
    if livro:
        estado = "adicionado aos" if adicionado else "removido dos"
        flash(f'"{livro.titulo}" {estado} Favoritos!', 'sucesso')
    return redirect(url_for('presentation.index'))

@presentation_bp.route('/cupao', methods=['POST'])
def aplicar_cupao():
    codigo = request.form.get('codigo', '')
    if servico.aplicar_cupao_desconto(codigo):
        flash(f'Cupão "{codigo.upper()}" aplicado com sucesso!', 'sucesso')
    else:
        flash(f'Cupão "{codigo}" inválido. Experimente MACK10 ou LEITOR20.', 'erro')
    return redirect(url_for('presentation.index'))

@presentation_bp.route('/scan', methods=['POST'])
def scan():
    isbn = request.form.get('isbn', '')
    livro = servico.escanear_isbn(isbn)
    if livro:
        flash(f'Scan & Go: "{livro.titulo}" adicionado!', 'sucesso')
    else:
        flash(f'ISBN "{isbn}" não encontrado.', 'erro')
    return redirect(url_for('presentation.index'))

@presentation_bp.route('/remover/<int:indice>', methods=['POST'])
def remover(indice):
    servico.remover_item(indice)
    return redirect(url_for('presentation.index'))

@presentation_bp.route('/checkout', methods=['POST'])
def checkout():
    if servico.processar_checkout_pix():
        flash('Pagamento via PIX concluído! Apresente o QR Code na saída.', 'sucesso')
    return redirect(url_for('presentation.index'))

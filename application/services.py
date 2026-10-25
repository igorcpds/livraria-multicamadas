from infrastructure.repositories import LivrariaRepository

class LivrariaService:
    def __init__(self, repository: LivrariaRepository):
        self.repo = repository

    def filtrar_catalogo(self, termo="", genero=""):
        livros = self.repo.listar_todos()
        if termo:
            t = termo.lower()
            livros = [l for l in livros if t in l.titulo.lower() or t in l.autor.lower()]
        if genero:
            livros = [l for l in livros if l.genero.lower() == genero.lower()]
        return livros

    def adicionar_ao_carrinho(self, livro_id: int):
        livro = self.repo.buscar_por_id(livro_id)
        if livro:
            self.repo.inserir_no_carrinho(livro)
            self.repo.ultimo_recibo_qr = None
        return livro

    def escanear_isbn(self, isbn: str):
        livro = self.repo.buscar_por_isbn(isbn)
        if livro:
            self.repo.inserir_no_carrinho(livro)
            self.repo.ultimo_recibo_qr = None
        return livro

    def remover_item(self, indice: int):
        self.repo.remover_do_carrinho(indice)

    # Nova Feature 1: Gerir Lista de Favoritos (Wishlist)
    def alternar_livro_favorito(self, livro_id: int):
        livro = self.repo.buscar_por_id(livro_id)
        if not livro:
            return None, False
        adicionado = self.repo.alternar_favorito(livro_id)
        return livro, adicionado

    # Nova Feature 2: Aplicar Cupão de Desconto
    def aplicar_cupao_desconto(self, codigo: str) -> bool:
        cupao = self.repo.buscar_cupao(codigo)
        if cupao:
            self.repo.cupao_ativo = cupao
            return True
        return False

    def calcular_resumo_carrinho(self):
        itens = self.repo.obter_itens_carrinho()
        subtotal = sum(i.preco for i in itens)
        desconto = 0.0
        if self.repo.cupao_ativo:
            desconto = self.repo.cupao_ativo.calcular_desconto(subtotal)
        total_final = max(0.0, subtotal - desconto)
        return {
            "subtotal": subtotal,
            "desconto": desconto,
            "total": total_final,
            "cupao": self.repo.cupao_ativo
        }

    def processar_checkout_pix(self):
        itens = self.repo.obter_itens_carrinho()
        if not itens:
            return None
        resumo = self.calcular_resumo_carrinho()
        qtd = len(itens)
        self.repo.esvaziar_carrinho()
        self.repo.ultimo_recibo_qr = (
            f"QR-4CAMADAS | Itens: {qtd} | Desconto: R$ {resumo['desconto']:.2f} | "
            f"Pago via PIX: R$ {resumo['total']:.2f}"
        )
        return self.repo.ultimo_recibo_qr

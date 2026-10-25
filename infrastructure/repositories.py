from domain.entities import Livro, Cupao

class LivrariaRepository:
    def __init__(self):
        self._catalogo = [
            Livro(1, "1984", "George Orwell", "Ficção Científica", "9780451524935", 45.00, 4.9),
            Livro(2, "O Guia do Mochileiro das Galáxias", "Douglas Adams", "Ficção Científica", "9788530601492", 39.90, 4.8),
            Livro(3, "Código Limpo (Clean Code)", "Robert C. Martin", "Tecnologia", "9788576082675", 89.90, 4.9),
            Livro(4, "Arquitetura Limpa", "Robert C. Martin", "Tecnologia", "9788550804606", 79.50, 4.7),
            Livro(5, "O Senhor dos Anéis", "J.R.R. Tolkien", "Fantasia", "9788595084742", 110.00, 5.0)
        ]
        self._carrinho = []
        self._favoritos_ids = set()
        self._cupoes_validos = {
            "MACK10": Cupao("MACK10", 10.0),
            "LEITOR20": Cupao("LEITOR20", 20.0)
        }
        self.cupao_ativo = None
        self.ultimo_recibo_qr = None

    def listar_todos(self):
        return self._catalogo

    def buscar_por_id(self, livro_id: int):
        return next((l for l in self._catalogo if l.id == int(livro_id)), None)

    def buscar_por_isbn(self, isbn: str):
        return next((l for l in self._catalogo if l.isbn == isbn.strip()), None)

    # Persistência do Carrinho
    def obter_itens_carrinho(self):
        return self._carrinho

    def inserir_no_carrinho(self, livro: Livro):
        self._carrinho.append(livro)

    def remover_do_carrinho(self, indice: int):
        if 0 <= indice < len(self._carrinho):
            self._carrinho.pop(indice)

    def esvaziar_carrinho(self):
        self._carrinho.clear()
        self.cupao_ativo = None

    # Persistência da Nova Feature: Favoritos (Wishlist)
    def alternar_favorito(self, livro_id: int) -> bool:
        livro_id = int(livro_id)
        if livro_id in self._favoritos_ids:
            self._favoritos_ids.remove(livro_id)
            return False
        self._favoritos_ids.add(livro_id)
        return True

    def obter_ids_favoritos(self):
        return self._favoritos_ids

    def obter_livros_favoritos(self):
        return [l for l in self._catalogo if l.id in self._favoritos_ids]

    # Persistência da Nova Feature: Cupões
    def buscar_cupao(self, codigo: str):
        return self._cupoes_validos.get(codigo.strip().upper())

class Livro:
    def __init__(self, id: int, titulo: str, autor: str, genero: str, isbn: str, preco: float, avaliacao: float):
        self.id = id
        self.titulo = titulo
        self.autor = autor
        self.genero = genero
        self.isbn = isbn
        self.preco = preco
        self.avaliacao = avaliacao


class Cupao:
    def __init__(self, codigo: str, percentual_desconto: float):
        self.codigo = codigo.upper()
        self.percentual_desconto = percentual_desconto

    def calcular_desconto(self, valor_bruto: float) -> float:
        return round(valor_bruto * (self.percentual_desconto / 100.0), 2)

# Livraria O2O - Exercício 7.3 (Arquitetura Multicamadas)

Refatoração do MVP da Livraria para uma **Arquitetura em 4 Camadas** com adição de novas funcionalidades:
1. **Lista de Favoritos (Wishlist)**
2. **Cupões de Desconto no Carrinho (`MACK10` e `LEITOR20`)**

## As 4 Camadas Implementadas:
- `presentation/`: Rotas Flask (`controllers.py`) e Interface HTML (`templates/index.html`).
- `application/`: Orquestração de casos de uso e regras de negócio (`services.py`).
- `domain/`: Entidades fundamentais do domínio (`entities.py`).
- `infrastructure/`: Repositório de dados em memória (`repositories.py`).

# Fura-Fila (versão go-horse)

**O app da cantina do CESAR para o aluno não perder o intervalo na fila.**

Hackathon Relâmpago #1 de FDS 2026.2 (CESAR School), Entrega 1.

## O que é o app

O Fura-Fila é um app para a cantina do CESAR. O aluno faz o pedido e paga pelo app antes do intervalo. A cantina marca o pedido como pronto, e o aluno só vai ao balcão para retirar o lanche, sem pegar fila.

Telas:
- **Cardápio:** o aluno escolhe os itens e as quantidades e vê o total.
- **Pagamento:** Pix (5% de desconto), cartão ou dinheiro (com cálculo de troco).
- **Meu pedido:** acompanha o status (pedido feito → em preparo → pronto) e recebe o aviso com a senha.
- **Cantina:** painel com os pedidos pagos, onde a cantina marca o pedido como pronto.

É uma prova de conceito: os dados ficam em memória, sem banco de dados.

## Como rodar

Precisa só de Python 3. Não tem nada para instalar.

```bash
python main.py
```

O app abre sozinho no navegador em `http://localhost:8000`. Se não abrir, acesse esse endereço manualmente.

Para testar o fluxo inteiro: faça um pedido na aba **Cardápio**, pague, vá na aba **Cantina** e clique em **Pronto ✓**. Depois volte em **Meu pedido** para ver o aviso.

## Decisões da stack

- **Python (só biblioteca padrão):** a equipe já teve contato com a linguagem, e ela tem classes abstratas, o que deixa os princípios do cap. 5 visíveis na versão final. O servidor usa `http.server`, então ninguém precisa instalar nada.
- **Tela em HTML, CSS e JavaScript (`index.html`):** visual de app de celular, que roda em qualquer navegador.
- **Dados em memória:** listas e dicionários bastam para a prova de conceito.

## Papel dos integrantes

| Integrante | Papel |
|---|---|
| Aline | Código: servidor e integração |
| Luiz Mário | Código: pagamento |
| Vinicius | Código: pedido e status |
| Ana Rita | README e mapeamento dos princípios |
| Juliana | Roteiro do vídeo |
| Vitória | Gravação e narração do vídeo |

## Onde estão os princípios no código

Esta é a versão go-horse: a lógica foi feita rápido e está toda em `main.py`, de propósito. Ela serve de **"antes"** para a PoC final. Aqui estão os pontos que já identificamos:

- **Coesão (parcial):** cada ação tem a sua função (`criar_pedido`, `pagar`, `marcar_pronto`).
- **Aberto/Fechado (violado):** a função `pagar()` decide o meio de pagamento com `if/elif`. Para adicionar um meio novo, seria preciso alterar essa função. Na PoC final, cada meio de pagamento vira uma classe.
- **Responsabilidade Única (violada):** `pagar()` busca o pedido, valida o status, calcula valores, monta a mensagem e muda o status, tudo na mesma função.
- **Ocultamento de informação (violado):** `cardapio` e `pedidos` são listas globais que qualquer função lê e altera diretamente.
- **Acoplamento (alto):** a classe `Handler` decide as rotas com `if/elif` e chama as funções de regra de negócio diretamente.
- **Complexidade ciclomática:** `pagar()` tem muitos pontos de decisão (`if`, `elif`, `for`, `try`). Vamos medir esse número aqui e na PoC final para mostrar a diferença.

Na PoC final (outro repositório, `furafila-poc`), vamos refatorar o código com esses princípios e adicionar o pagamento por vale-refeição criando só uma classe nova.

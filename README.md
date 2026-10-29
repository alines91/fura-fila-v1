# Fura-Fila (versão go-horse)
 
**O app da cantina do CESAR para o aluno não perder o intervalo na fila.**
 
Hackathon Relâmpago #1 de FDS 2026.2 (CESAR School), Entrega 1.
 
## O que é o app
 
O Fura-Fila é um app para a cantina do CESAR. O aluno faz o pedido e paga pelo app antes do intervalo. A cantina marca o pedido como pronto, e o aluno só vai ao balcão para retirar o lanche, sem pegar fila.
 
Funcionalidades:
- Ver o cardápio do dia
- Fazer pedido (escolher itens e quantidades, ver o total)
- Pagar com Pix (5% de desconto), cartão ou dinheiro (com cálculo de troco)
- Acompanhar o status: aguardando pagamento → em preparo → pronto para retirar
- Área da cantina para marcar o pedido como pronto, o que gera o aviso para o aluno
É uma prova de conceito: roda no terminal e guarda os dados em memória, sem banco de dados.
 
## Como rodar
 
Precisa de Python 3 instalado.
 
```bash
python main.py
```
 
Depois é só seguir o menu. Para testar o fluxo inteiro: opção 2 (fazer pedido) → 3 (pagar) → 5 (cantina marca como pronto) → 4 (ver status).
 
## Decisões da stack
 
- **Python:** a equipe já teve contato com a linguagem, e ela tem classes e classes abstratas. Isso deixa os princípios do cap. 5 visíveis no código da versão final.
- **Terminal:** é o jeito mais rápido de ter o app funcionando dentro da aula.
- **Dados em memória:** listas e dicionários bastam para a prova de conceito.
## Papel dos integrantes
 
| Integrante | Papel |
|---|---|
| Aline | Código: menu e integração |
| Luiz Mário | Código: pagamento |
| Vinicius | Código: pedido e status |
| Ana Rita | README e mapeamento dos princípios |
| Juliana | Roteiro do vídeo |
| Vitória | Gravação e narração do vídeo |
 
## Onde estão os princípios no código
 
Esta é a versão go-horse: o código foi feito rápido e está todo em `main.py`, de propósito. Ela serve de **"antes"** para a PoC final. Aqui estão os pontos que já identificamos:
 
- **Coesão (parcial):** cada ação do menu tem a sua função (`fazer_pedido`, `pagar`, `ver_status`, `cantina_marcar_pronto`).
- **Aberto/Fechado (violado):** a função `pagar()` decide o meio de pagamento com `if/elif`. Para adicionar um meio novo, seria preciso alterar essa função. Na PoC final, cada meio de pagamento vira uma classe.
- **Responsabilidade Única (violada):** `pagar()` busca o pedido, lê a entrada do usuário, calcula valores, imprime mensagens e muda o status, tudo na mesma função.
- **Ocultamento de informação (violado):** pedidos são dicionários e listas globais, que qualquer função lê e altera diretamente.
- **Complexidade ciclomática:** `pagar()` tem muitos pontos de decisão (`if`, `elif`, `for`, `try`). Vamos medir esse número aqui e na PoC final para mostrar a diferença.
Na PoC final (outro repositório, `furafila-poc`), vamos refatorar o código com esses princípios e adicionar o pagamento por vale-refeição criando só uma classe nova.
 

# Fura-Fila (Cantina CESAR) - versao go-horse
# Logica toda em um arquivo so, de proposito. Vai ser refatorada na PoC final.
# Rodar: python main.py  -> abre http://localhost:8000 no navegador

import json
import os
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

cardapio = [
    {"id": 1, "nome": "Coxinha", "preco": 7.00, "emoji": "🍗"},
    {"id": 2, "nome": "Pão de queijo", "preco": 5.00, "emoji": "🧀"},
    {"id": 3, "nome": "Sanduíche natural", "preco": 12.00, "emoji": "🥪"},
    {"id": 4, "nome": "Suco de laranja", "preco": 6.00, "emoji": "🍊"},
    {"id": 5, "nome": "Café", "preco": 4.00, "emoji": "☕"},
]

pedidos = []
proximo_id = 1


def criar_pedido(dados):
    global proximo_id
    nome = str(dados.get("cliente", "")).strip()
    if nome == "":
        return {"erro": "Digite seu nome."}
    itens = []
    total = 0
    for escolhido in dados.get("itens", []):
        achou = None
        for item in cardapio:
            if item["id"] == escolhido.get("id"):
                achou = item
        if achou is None:
            return {"erro": "Item não existe."}
        qtd = int(escolhido.get("qtd", 0))
        if qtd <= 0:
            continue
        itens.append({"nome": achou["nome"], "preco": achou["preco"], "qtd": qtd})
        total = total + achou["preco"] * qtd
    if len(itens) == 0:
        return {"erro": "Seu pedido está vazio."}
    pedido = {"id": proximo_id, "cliente": nome, "itens": itens, "total": round(total, 2),
              "status": "aguardando pagamento", "pagamento": None, "valor_pago": None, "troco": None}
    pedidos.append(pedido)
    proximo_id = proximo_id + 1
    return pedido


def pagar(dados):
    pedido = None
    for p in pedidos:
        if p["id"] == dados.get("id"):
            pedido = p
    if pedido is None:
        return {"erro": "Pedido não encontrado."}
    if pedido["status"] != "aguardando pagamento":
        return {"erro": "Esse pedido já foi pago."}
    forma = dados.get("forma")
    if forma == "pix":
        valor = pedido["total"] * 0.95
        pedido["pagamento"] = "Pix"
        pedido["valor_pago"] = round(valor, 2)
        msg = f"Pix de R$ {valor:.2f} recebido (5% de desconto).".replace(".", ",", 1)
    elif forma == "cartao":
        valor = pedido["total"]
        pedido["pagamento"] = "Cartão"
        pedido["valor_pago"] = round(valor, 2)
        msg = f"Cartão aprovado: R$ {valor:.2f}.".replace(".", ",", 1)
    elif forma == "dinheiro":
        try:
            entregue = float(str(dados.get("entregue", "")).replace(",", "."))
        except ValueError:
            return {"erro": "Valor inválido."}
        if entregue < pedido["total"]:
            return {"erro": "Dinheiro insuficiente."}
        troco = entregue - pedido["total"]
        pedido["pagamento"] = "Dinheiro"
        pedido["valor_pago"] = round(entregue, 2)
        pedido["troco"] = round(troco, 2)
        msg = f"Pago em dinheiro. Troco: R$ {troco:.2f}".replace(".", ",")
    else:
        return {"erro": "Forma de pagamento inválida."}
    pedido["status"] = "em preparo"
    return {"ok": True, "mensagem": msg, "pedido": pedido}


def marcar_pronto(dados):
    for p in pedidos:
        if p["id"] == dados.get("id"):
            if p["status"] != "em preparo":
                return {"erro": "Esse pedido não está em preparo."}
            p["status"] = "pronto para retirar"
            return {"ok": True, "pedido": p}
    return {"erro": "Pedido não encontrado."}


class Handler(BaseHTTPRequestHandler):
    def responder(self, dados, codigo=200, tipo="application/json"):
        corpo = dados if isinstance(dados, bytes) else json.dumps(dados, ensure_ascii=False).encode("utf-8")
        self.send_response(codigo)
        self.send_header("Content-Type", tipo + "; charset=utf-8")
        self.end_headers()
        self.wfile.write(corpo)

    def do_GET(self):
        url = urlparse(self.path)
        if url.path == "/" or url.path == "/index.html":
            pasta = os.path.dirname(os.path.abspath(__file__))
            with open(os.path.join(pasta, "index.html"), "rb") as f:
                self.responder(f.read(), tipo="text/html")
        elif url.path == "/api/cardapio":
            self.responder(cardapio)
        elif url.path == "/api/pedidos":
            self.responder(pedidos)
        elif url.path == "/api/pedido":
            num = parse_qs(url.query).get("id", [""])[0]
            for p in pedidos:
                if str(p["id"]) == num:
                    self.responder(p)
                    return
            self.responder({"erro": "Pedido não encontrado."}, 404)
        else:
            self.responder({"erro": "Página não encontrada."}, 404)

    def do_POST(self):
        tamanho = int(self.headers.get("Content-Length", 0))
        try:
            dados = json.loads(self.rfile.read(tamanho) or b"{}")
        except json.JSONDecodeError:
            self.responder({"erro": "Dados inválidos."}, 400)
            return
        if self.path == "/api/pedido":
            self.responder(criar_pedido(dados))
        elif self.path == "/api/pagar":
            self.responder(pagar(dados))
        elif self.path == "/api/pronto":
            self.responder(marcar_pronto(dados))
        else:
            self.responder({"erro": "Página não encontrada."}, 404)

    def log_message(self, *args):
        pass


def main():
    porta = int(os.environ.get("PORTA", 8000))
    servidor = HTTPServer(("localhost", porta), Handler)
    endereco = f"http://localhost:{porta}"
    print("=== FURA-FILA · Cantina CESAR ===")
    print(f"App rodando em {endereco}  (Ctrl+C para parar)")
    if os.environ.get("SEM_NAVEGADOR") is None:
        webbrowser.open(endereco)
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("\nBom lanche!")


if __name__ == "__main__":
    main()

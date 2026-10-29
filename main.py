# Fura-Fila (Cantina CESAR) - versao go-horse
# Tudo em um arquivo so, de proposito. Vai ser refatorado na PoC final.

cardapio = [
    {"id": 1, "nome": "Coxinha", "preco": 7.00},
    {"id": 2, "nome": "Pao de queijo", "preco": 5.00},
    {"id": 3, "nome": "Sanduiche natural", "preco": 12.00},
    {"id": 4, "nome": "Suco de laranja", "preco": 6.00},
    {"id": 5, "nome": "Cafe", "preco": 4.00},
]

pedidos = []
proximo_id = 1


def mostrar_cardapio():
    print("\n--- CARDAPIO DO DIA ---")
    for item in cardapio:
        print(f"{item['id']}. {item['nome']} - R$ {item['preco']:.2f}")


def fazer_pedido():
    global proximo_id
    nome = input("\nSeu nome: ").strip()
    if nome == "":
        print("Nome invalido.")
        return
    itens = []
    total = 0
    while True:
        mostrar_cardapio()
        escolha = input("Numero do item (ENTER para finalizar): ").strip()
        if escolha == "":
            break
        if not escolha.isdigit():
            print("Opcao invalida.")
            continue
        achou = None
        for item in cardapio:
            if item["id"] == int(escolha):
                achou = item
        if achou is None:
            print("Item nao existe.")
            continue
        qtd = input("Quantidade: ").strip()
        if not qtd.isdigit() or int(qtd) <= 0:
            print("Quantidade invalida.")
            continue
        itens.append({"nome": achou["nome"], "preco": achou["preco"], "qtd": int(qtd)})
        total = total + achou["preco"] * int(qtd)
        print(f"Adicionado! Total parcial: R$ {total:.2f}")
    if len(itens) == 0:
        print("Pedido vazio, cancelado.")
        return
    pedido = {"id": proximo_id, "cliente": nome, "itens": itens, "total": total,
              "status": "aguardando pagamento", "pagamento": None}
    pedidos.append(pedido)
    proximo_id = proximo_id + 1
    print(f"\nPedido #{pedido['id']} criado! Total: R$ {total:.2f}")


def pagar():
    num = input("\nNumero do pedido: ").strip()
    pedido = None
    for p in pedidos:
        if str(p["id"]) == num:
            pedido = p
    if pedido is None:
        print("Pedido nao encontrado.")
        return
    if pedido["status"] != "aguardando pagamento":
        print("Esse pedido ja foi pago.")
        return
    print(f"Total: R$ {pedido['total']:.2f}")
    print("1. Pix (5% de desconto)\n2. Cartao\n3. Dinheiro")
    forma = input("Forma de pagamento: ").strip()
    if forma == "1":
        valor = pedido["total"] * 0.95
        print(f"Pix de R$ {valor:.2f} recebido (com desconto).")
        pedido["pagamento"] = "Pix"
    elif forma == "2":
        valor = pedido["total"]
        print(f"Cartao aprovado: R$ {valor:.2f}.")
        pedido["pagamento"] = "Cartao"
    elif forma == "3":
        entregue = input("Valor entregue: R$ ").strip().replace(",", ".")
        try:
            entregue = float(entregue)
        except ValueError:
            print("Valor invalido.")
            return
        if entregue < pedido["total"]:
            print("Dinheiro insuficiente.")
            return
        troco = entregue - pedido["total"]
        print(f"Pago em dinheiro. Troco: R$ {troco:.2f}")
        pedido["pagamento"] = "Dinheiro"
    else:
        print("Forma de pagamento invalida.")
        return
    pedido["status"] = "em preparo"
    print(f"Pedido #{pedido['id']} em preparo!")


def ver_status():
    num = input("\nNumero do pedido: ").strip()
    for p in pedidos:
        if str(p["id"]) == num:
            print(f"Pedido #{p['id']} ({p['cliente']}): {p['status']}")
            for i in p["itens"]:
                print(f"  {i['qtd']}x {i['nome']}")
            if p["status"] == "pronto para retirar":
                print(f"*** {p['cliente']}, seu lanche esta pronto! Pode buscar no balcao. ***")
            return
    print("Pedido nao encontrado.")


def cantina_marcar_pronto():
    em_preparo = [p for p in pedidos if p["status"] == "em preparo"]
    if len(em_preparo) == 0:
        print("\nNenhum pedido em preparo.")
        return
    print("\n--- PEDIDOS EM PREPARO ---")
    for p in em_preparo:
        print(f"#{p['id']} - {p['cliente']}")
    num = input("Marcar qual como pronto? ").strip()
    for p in em_preparo:
        if str(p["id"]) == num:
            p["status"] = "pronto para retirar"
            print(f"Aviso enviado: {p['cliente']}, seu pedido #{p['id']} esta pronto!")
            return
    print("Pedido nao encontrado.")


def main():
    print("=== FURA-FILA · Cantina CESAR ===")
    print("15 minutos, uma fila e o sonho de um lanche.")
    while True:
        print("\n1. Ver cardapio")
        print("2. Fazer pedido")
        print("3. Pagar pedido")
        print("4. Ver status do pedido")
        print("5. [Cantina] Marcar pedido como pronto")
        print("0. Sair")
        op = input("Opcao: ").strip()
        if op == "1":
            mostrar_cardapio()
        elif op == "2":
            fazer_pedido()
        elif op == "3":
            pagar()
        elif op == "4":
            ver_status()
        elif op == "5":
            cantina_marcar_pronto()
        elif op == "0":
            print("Bom lanche!")
            break
        else:
            print("Opcao invalida.")


if __name__ == "__main__":
    main()

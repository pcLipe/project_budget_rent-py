from datetime import datetime
import os

# ---------------------- CLASSES ----------------------

class Cliente:
    def __init__(self, nome, contato, cpf):
        self.nome = nome.strip()
        self.contato = contato.strip()
        self.cpf = cpf.strip()

    def __str__(self):
        return f"Cliente: {self.nome} | Contato: {self.contato} | CPF: {self.cpf}"


class Imovel:
    def __init__(self, codigo, endereco, area_m2, valor_estimado_venda):
        self.codigo = codigo.strip()
        self.endereco = endereco.strip()
        self.area_m2 = float(area_m2)
        self.valor_estimado_venda = float(valor_estimado_venda)

    def calcular_aluguel_base(self):
        raise NotImplementedError("Método deve ser implementado nas subclasses")


class Casa(Imovel):
    def __init__(self, codigo, endereco, area_m2, valor_estimado_venda, qtd_quartos, qtd_vagas_garagem, possui_piscina):
        super().__init__(codigo, endereco, area_m2, valor_estimado_venda)
        self.qtd_quartos = int(qtd_quartos)
        self.qtd_vagas_garagem = int(qtd_vagas_garagem)
        self.possui_piscina = bool(possui_piscina)

    def calcular_aluguel_base(self):
        base = self.valor_estimado_venda * 0.005
        bonus = self.qtd_quartos * 80 + (300 if self.possui_piscina else 0)
        return base + bonus


class Apartamento(Imovel):
    def __init__(self, codigo, endereco, area_m2, valor_estimado_venda, andar, valor_condominio, possui_area_lazer):
        super().__init__(codigo, endereco, area_m2, valor_estimado_venda)
        self.andar = int(andar)
        self.valor_condominio = float(valor_condominio)
        self.possui_area_lazer = bool(possui_area_lazer)

    def calcular_aluguel_base(self):
        base = self.valor_estimado_venda * 0.005
        bonus = (self.valor_condominio * 0.3) + (150 if self.possui_area_lazer else 0)
        return base + bonus


class Estudio(Imovel):
    def __init__(self, codigo, endereco, area_m2, valor_estimado_venda, mobiliado):
        super().__init__(codigo, endereco, area_m2, valor_estimado_venda)
        self.mobiliado = bool(mobiliado)

    def calcular_aluguel_base(self):
        base = self.valor_estimado_venda * 0.005
        bonus = 250 if self.mobiliado else 0
        return base + bonus


class Orcamento:
    def __init__(self, cliente, imovel):
        self.cliente = cliente
        self.imovel = imovel
        self.valor_aluguel_base = 0.0
        self.valor_condominio = 0.0
        self.valor_iptu = 0.0
        self.outras_taxas = 0.0
        self.ajuste = 0.0
        self.valor_total_mensal = 0.0

    def coletar_dados_adicionais(self):
        print("\n--- Custos adicionais ---")
        self.valor_condominio = self._ler_valor("Valor do condomínio (0 se não houver ou incluso): ")
        self.valor_iptu = self._ler_valor("Valor mensal do IPTU (0 se incluso): ")
        self.outras_taxas = self._ler_valor("Outras taxas / administração (0 se não houver): ")

        ajuste_str = input("Aplicar desconto ou acréscimo? (positivo = acréscimo, negativo = desconto, 0 = nenhum): ")
        try:
            self.ajuste = float(ajuste_str)
        except ValueError:
            self.ajuste = 0.0
            print("Valor inválido. Ajuste definido como 0.")

    def _ler_valor(self, mensagem):
        while True:
            valor = input(mensagem)
            try:
                return float(valor)
            except ValueError:
                print("Digite um número válido (ex: 450.00 ou 0).")

    def calcular(self):
        self.valor_aluguel_base = self.imovel.calcular_aluguel_base()
        self.valor_total_mensal = (
            self.valor_aluguel_base +
            self.valor_condominio +
            self.valor_iptu +
            self.outras_taxas +
            self.ajuste
        )

    def exibir_orcamento(self):
        data_atual = datetime.now().strftime("%d/%m/%Y %H:%M")
        print("\n" + "="*60)
        print("          ORÇAMENTO DE LOCAÇÃO - R.M. Imobiliária")
        print(f"Data: {data_atual}")
        print("="*60)
        print(self.cliente)
        print(f"Imóvel: {self.imovel.__class__.__name__} - {self.imovel.endereco}")
        print(f"Código: {self.imovel.codigo}  |  Área: {self.imovel.area_m2:.2f} m²")
        print("-"*60)
        print(f"{'Aluguel base':<25} R$ {self.valor_aluguel_base:>10,.2f}")
        if self.valor_condominio > 0:
            print(f"{'Condomínio':<25} R$ {self.valor_condominio:>10,.2f}")
        if self.valor_iptu > 0:
            print(f"{'IPTU mensal':<25} R$ {self.valor_iptu:>10,.2f}")
        if self.outras_taxas > 0:
            print(f"{'Outras taxas':<25} R$ {self.outras_taxas:>10,.2f}")
        if self.ajuste != 0:
            sinal = "+" if self.ajuste > 0 else ""
            print(f"{'Ajuste (desconto/acréscimo)':<25} R$ {sinal}{self.ajuste:>9,.2f}")
        print("-"*60)
        print(f"{'TOTAL MENSAL':<25} R$ {self.valor_total_mensal:>10,.2f}")
        print("="*60)


# ---------------------- FUNÇÃO PRINCIPAL ----------------------

def main():
    print("=== Sistema de Geração de Orçamento de Aluguel - R.M. Imobiliária ===\n")

    # 1. Dados do cliente
    nome = input("Nome do cliente: ").strip()
    contato = input("Contato (telefone / WhatsApp): ").strip()
    cpf = input("CPF: ").strip()
    cliente = Cliente(nome, contato, cpf)

    # 2. Seleção do tipo de imóvel
    print("\nTipo de imóvel:")
    print("1 - Casa")
    print("2 - Apartamento")
    print("3 - Estúdio")
    opcao = input("Escolha (1/2/3): ").strip()

    imovel = None

    if opcao == "1":
        print("\n--- Dados da Casa ---")
        codigo = input("Código do imóvel: ")
        endereco = input("Endereço: ")
        area = input("Área (m²): ")
        valor_venda = input("Valor estimado de venda (R$): ")
        quartos = input("Quantidade de quartos: ")
        vagas = input("Vagas de garagem: ")
        piscina = input("Possui piscina? (s/n): ").lower().startswith("s")
        imovel = Casa(codigo, endereco, area, valor_venda, quartos, vagas, piscina)

    elif opcao == "2":
        print("\n--- Dados do Apartamento ---")
        codigo = input("Código do imóvel: ")
        endereco = input("Endereço: ")
        area = input("Área (m²): ")
        valor_venda = input("Valor estimado de venda (R$): ")
        andar = input("Andar: ")
        condominio = input("Valor do condomínio (R$): ")
        lazer = input("Possui área de lazer? (s/n): ").lower().startswith("s")
        imovel = Apartamento(codigo, endereco, area, valor_venda, andar, condominio, lazer)

    elif opcao == "3":
        print("\n--- Dados do Estúdio ---")
        codigo = input("Código do imóvel: ")
        endereco = input("Endereço: ")
        area = input("Área (m²): ")
        valor_venda = input("Valor estimado de venda (R$): ")
        mobiliado = input("Mobiliado? (s/n): ").lower().startswith("s")
        imovel = Estudio(codigo, endereco, area, valor_venda, mobiliado)

    else:
        print("Opção inválida. Encerrando.")
        return

    # 3. Criação e processamento do orçamento
    orcamento = Orcamento(cliente, imovel)
    orcamento.coletar_dados_adicionais()
    orcamento.calcular()
    orcamento.exibir_orcamento()

    # 4. Pergunta se deseja salvar (simulação de PDF/email)
    salvar = input("\nDeseja salvar o orçamento? (s/n): ").lower().startswith("s")
    if salvar:
        nome_arquivo = f"orcamento_{cliente.nome.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
        with open(nome_arquivo, "w", encoding="utf-8") as f:
            f.write(f"ORÇAMENTO DE LOCAÇÃO - R.M. Imobiliária\n")
            f.write(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n")
            f.write(str(cliente) + "\n")
            f.write(f"Imóvel: {imovel.__class__.__name__} - {imovel.endereco}\n")
            # ... poderia expandir aqui com todo o conteúdo
            f.write(f"TOTAL MENSAL: R$ {orcamento.valor_total_mensal:,.2f}\n")
        print(f"Orçamento salvo como: {nome_arquivo}")


if __name__ == "__main__":
    main()
def inteiro_para_ip(valor):
    oct1 = valor // (256**3)
    resto = valor % (256**3)

    oct2 = resto // (256**2)
    resto = resto % (256**2)

    oct3 = resto // 256
    oct4 = resto % 256

    return f"{oct1}.{oct2}.{oct3}.{oct4}"


try:
    ip_cidr = input("Digite o IP/CIDR: ")

    ip, cidr = ip_cidr.split("/")
    cidr = int(cidr)

    if cidr < 0 or cidr > 32:
        raise ValueError

    mascara = (2**cidr - 1) << (32 - cidr)
    print("Máscara em inteiro:", mascara)
    print("Máscara em IP:", inteiro_para_ip(mascara))

    partes = ip.split(".")

    if len(partes) != 4:
        raise ValueError

    octetos = [int(p) for p in partes]

    for o in octetos:
        if o < 0 or o > 255:
            raise ValueError

    print("IP válido:", octetos)

    ip_inteiro = (
        octetos[0] * 256**3 +
        octetos[1] * 256**2 +
        octetos[2] * 256 +
        octetos[3]
    )
    print("IP em inteiro:", ip_inteiro)

    rede = ip_inteiro & mascara
    print("Endereço de rede:", inteiro_para_ip(rede))

    bits_host = 32 - cidr
    broadcast = rede + (2**bits_host - 1)
    print("Broadcast:", inteiro_para_ip(broadcast))

    if cidr == 32:
        print("Primeiro host:", inteiro_para_ip(rede))
        print("Último host:", inteiro_para_ip(rede))
        print("Hosts:", 1)

    elif cidr == 31:
        print("Primeiro host:", inteiro_para_ip(rede))
        print("Último host:", inteiro_para_ip(broadcast))
        print("Hosts:", 2)

    else:
        primeiro_host = rede + 1
        ultimo_host = broadcast - 1
        hosts = 2**bits_host - 2

        print("Primeiro host:", inteiro_para_ip(primeiro_host))
        print("Último host:", inteiro_para_ip(ultimo_host))
        print("Hosts:", hosts)

except ValueError:
    print("Entrada inválida")
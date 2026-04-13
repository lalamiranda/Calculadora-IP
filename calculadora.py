from flask import Flask, render_template, request

app = Flask(__name__)

def inteiro_para_ip(valor):
    oct1 = valor // (256**3)
    resto = valor % (256**3)

    oct2 = resto // (256**2)
    resto = resto % (256**2)

    oct3 = resto // 256
    oct4 = resto % 256

    return f"{oct1}.{oct2}.{oct3}.{oct4}"


@app.route("/")
def index():
    return render_template("calculadora.html")


@app.route("/calcular", methods=["POST"])
def calcular():
    try:
        ip_cidr = request.form["ip_cidr"]

        ip, cidr = ip_cidr.split("/")
        cidr = int(cidr)

        if cidr < 0 or cidr > 32:
            raise ValueError

        mascara = (2**cidr - 1) << (32 - cidr)

        partes = ip.split(".")
        if len(partes) != 4:
            raise ValueError

        octetos = [int(p) for p in partes]

        for o in octetos:
            if o < 0 or o > 255:
                raise ValueError

        ip_inteiro = (
            octetos[0] * 256**3 +
            octetos[1] * 256**2 +
            octetos[2] * 256 +
            octetos[3]
        )

        rede = ip_inteiro & mascara
        bits_host = 32 - cidr
        broadcast = rede + (2**bits_host - 1)

        if cidr == 32:
            primeiro_host = rede
            ultimo_host = rede
            hosts = 1
        elif cidr == 31:
            primeiro_host = rede
            ultimo_host = broadcast
            hosts = 2
        else:
            primeiro_host = rede + 1
            ultimo_host = broadcast - 1
            hosts = 2**bits_host - 2

        return render_template("calculadora.html",
            resultado=True,
            mascara=inteiro_para_ip(mascara),
            rede=inteiro_para_ip(rede),
            broadcast=inteiro_para_ip(broadcast),
            primeiro=inteiro_para_ip(primeiro_host),
            ultimo=inteiro_para_ip(ultimo_host),
            hosts=hosts
        )

    except ValueError:
        return render_template("calculadora.html", erro=True)


if __name__ == "__main__":
    app.run(debug=True)
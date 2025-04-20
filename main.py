import ctypes
import string
import os
import time

USE_WEBHOOK = True

time.sleep(2)
os.system('cls' if os.name == 'nt' else 'clear')

try:
    from discord_webhook import DiscordWebhook
except ImportError:
    input(
        f"[!] Módulo 'discord_webhook' ausente. Instale com: '{'py -3' if os.name == 'nt' else 'python3.8'} -m pip install discord_webhook'\nPressione Enter para continuar.")
    USE_WEBHOOK = False

try:
    import requests
except ImportError:
    input(
        f"[!] Módulo 'requests' ausente. Instale com: '{'py -3' if os.name == 'nt' else 'python3.8'} -m pip install requests'\nPressione Enter para sair.")
    exit()

try:
    import numpy
except ImportError:
    input(
        f"[!] Módulo 'numpy' ausente. Instale com: '{'py -3' if os.name == 'nt' else 'python3.8'} -m pip install numpy'\nPressione Enter para sair.")
    exit()

try:
    requests.get("https://github.com", timeout=5)
    print("[✓] Conectado à internet.")
except requests.exceptions.RequestException:
    input("[X] Sem conexão com a internet.\nPressione Enter para sair.")
    exit()


class NitroChecker:
    def __init__(self):
        self.arquivo_saida = "Codigos_Encontrados.txt"

    def iniciar(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        if os.name == "nt":
            ctypes.windll.kernel32.SetConsoleTitleW("Nitro Code Scanner - Powered by Skorp")
        else:
            print(f'\33]0;Nitro Code Scanner - Powered by Skorp\a', end='', flush=True)

        print(r"""
==================================================
███╗   ███╗████████╗███████╗
████╗ ████║╚══██╔══╝██╔════╝
██╔████╔██║   ██║   █████╗  
██║╚██╔╝██║   ██║       ███  
██║ ╚═╝ ██║   ██║   ███████╗
╚═╝     ╚═╝   ╚═╝   ╚══════╝
==================================================
""")

        time.sleep(1)
        self.lento(">> Quantos códigos deseja gerar e testar? ", 0.02, nova_linha=False)
        try:
            quantidade = int(input(''))
        except ValueError:
            input("Entrada inválida. Apenas números são aceitos.\nPressione Enter para sair.")
            exit()

        webhook_url = None
        if USE_WEBHOOK:
            self.lento(">> Insira a URL do webhook (ou pressione Enter para ignorar): ", 0.02, nova_linha=False)
            webhook_url = input('').strip()
            if webhook_url:
                DiscordWebhook(url=webhook_url, content="🎯 Scanner iniciado! Enviaremos os códigos válidos aqui.").execute()

        encontrados = []
        rejeitados = 0
        caracteres = list(string.ascii_letters + string.digits)

        gerados = numpy.random.choice(caracteres, size=(quantidade, 16))
        for item in gerados:
            try:
                codigo = ''.join(item)
                link = f"https://discord.gift/{codigo}"

                if self.testar_codigo(link, webhook_url):
                    encontrados.append(link)
                else:
                    rejeitados += 1
            except KeyboardInterrupt:
                print("\n[!] Interrompido pelo usuário.")
                break
            except Exception:
                print(f"[!] Erro desconhecido ao processar: {link}")

            if os.name == "nt":
                ctypes.windll.kernel32.SetConsoleTitleW(
                    f"Nitro Code Scanner - {len(encontrados)} Válidos | {rejeitados} Inválidos")
            else:
                print(f'\33]0;Nitro Code Scanner - {len(encontrados)} Válidos | {rejeitados} Inválidos\a', end='', flush=True)

        print("\n======= RESULTADO FINAL =======")
        print(f"✔ Códigos Válidos: {len(encontrados)}")
        print(f"✘ Códigos Inválidos: {rejeitados}")
        if encontrados:
            print("🔗 Links válidos encontrados:")
            print("\n".join(encontrados))

        input("\nFinalizado! Pressione Enter para sair.")

    def lento(self, texto, velocidade, nova_linha=True):
        for caractere in texto:
            print(caractere, end='', flush=True)
            time.sleep(velocidade)
        if nova_linha:
            print()

    def testar_codigo(self, codigo, webhook=None):
        endpoint = f"https://discordapp.com/api/v9/entitlements/gift-codes/{codigo}?with_application=false&with_subscription_plan=true"
        resposta = requests.get(endpoint)

        if resposta.status_code == 200:
            print(f"[VÁLIDO] {codigo}")
            with open(self.arquivo_saida, "a") as arq:
                arq.write(f"{codigo}\n")
            if webhook:
                DiscordWebhook(url=webhook, content=f"🎁 Código válido encontrado! {codigo}").execute()
            return True
        else:
            print(f"[inválido] {codigo}")
            return False


if __name__ == "__main__":
    app = NitroChecker()
    app.iniciar()

from pathlib import Path

import yt_dlp

PASTA_DOWNLOADS = Path(__file__).resolve().parent / "downloads"
PASTA_DOWNLOADS.mkdir(exist_ok=True)


# Obtém as informações sobre o vídeo escolhido
def obter_info_video(url):
    with yt_dlp.YoutubeDL() as ydl:
        info = ydl.extract_info(url, download=False)

    if info is None:
        print("Não foi possível obter informações sobre o vídeo.")
        return None

    titulo = info["title"]
    duracao = info["duration"]
    resolucoes = obter_resolucoes(info["formats"])
    codecs = obter_codec(info["formats"])

    return {
        "titulo": titulo,
        "duracao": duracao,
        "resolucoes": resolucoes,
        "codecs": codecs,
    }


# Obtém as resoluções disponíveis para o vídeo escolhido
def obter_resolucoes(formats):
    resolucoes = []

    for formato in formats:
        if formato["vcodec"] != "none" and formato["height"] not in resolucoes:
            resolucoes.append(formato["height"])

    return sorted(resolucoes)


# Obtém os codecs de cada resolução
def obter_codec(formats):
    codecs = {}

    for formato in formats:
        if formato["vcodec"] != "none":
            height = formato["height"]
            codec = formato["vcodec"].split(".")[0]

            if height not in codecs:
                codecs[height] = []

            if codec not in codecs[height]:
                codecs[height].append(codec)

    return codecs


def mostrar_resolucao(info):
    print(f"Título: {info['titulo']}")
    print("Resoluções e Codecs disponíveis:")

    for resolucao in info["resolucoes"]:
        print(f"{resolucao}p")


def mostrar_codecs_disponiveis(resolucao_escolhida, info):
    print(f"Codecs disponíveis para a resolução {resolucao_escolhida}p")

    for codec in info["codecs"].get(resolucao_escolhida):
        match codec:
            case "avc1":
                print("avc1 (H.264)")
            case "vp9":
                print("vp9 (VP9)")
            case "av01":
                print("av01 (AV1)")
            case _:
                print(codec)


def montar_opcao(resolucao_escolhida, codec_escolhido):
    return {
        "format": f"bv[height={resolucao_escolhida}][vcodec^={codec_escolhido}]+ba",
        "paths": {"home": str(PASTA_DOWNLOADS)},
        "outtmpl": {"default": "%(title)s [%(id)s].%(ext)s"},
    }


def baixar(opcao, url):
    with yt_dlp.YoutubeDL(opcao) as ydl:
        resultado = ydl.download([url])

    if resultado != 0:
        print("Não foi possível obter informações sobre o vídeo.")


# Pede ao usuário para informar um URL
url = input("Informe uma URL: ")

# Se a url estiver vazia, pergunta novamente
while url == "":
    url = input("Informe uma URL: ")

# Obtém as informações sobre o vídeo escolhido
informacoes = obter_info_video(url)

print(informacoes)

mostrar_resolucao(informacoes)

resolucao_escolhida = int(input("Informe a resolução desejada: "))

while resolucao_escolhida not in informacoes["resolucoes"]:
    print("Opção invalida!")
    resolucao_escolhida = int(input("Informe a resolução desejada: "))

mostrar_codecs_disponiveis(resolucao_escolhida, informacoes)

codec_escolhido = input("Informe o codec desejado: ")

while codec_escolhido not in informacoes["codecs"].get(resolucao_escolhida):
    print("Opção invalida!")
    codec_escolhido = input("Informe o codec desejado: ")

opcao = montar_opcao(resolucao_escolhida, codec_escolhido)

print(opcao)

baixar(opcao, url)

import yt_dlp

url = "https://www.youtube.com/watch?v=ntOtyJwxcsM"

options = {"format": "bv[height=1080]+ba", "format_sort": ["+codec:avc:m4a"]}

# yt_dlp.YoutubeDL(options) - cria um objeto YoutubeDL

with yt_dlp.YoutubeDL(options) as ydl:
    info = ydl.extract_info(url, download=False)

formatos_audio_somente = []
formatos_video_somente = []
formatos_audio_video = []
formatos_outro = []
resolucoes = []


def mostrar_formatos(formatos):
    print(
        "ID  |  Extensão  |  Resolução  |  VCodec  |  ACodec  |  TBR  |  VBR  |  ABR  |  Filesize  |  FPS  "
    )
    for formato in formatos:
        print(
            formato["format_id"],
            " | ",
            formato["ext"],
            " | ",
            formato["resolution"],
            " | ",
            formato["vcodec"],
            " | ",
            formato["acodec"],
            " | ",
            formato["tbr"],
            " | ",
            formato["vbr"],
            " | ",
            formato["abr"],
            " | ",
            formato["filesize_approx"],
            " | ",
            formato["fps"],
        )


print("Foram encontrados", len(info["formats"]), "formatos. \n")

print("Tabela com os formatos disponíveis:")
print(
    "ID  |  Extensão  |  Resolução  |  VCodec  |  ACodec  |  TBR  |  VBR  |  ABR  |  Filesize  |  FPS  "
)
for formato in info["formats"]:
    if formato["vcodec"] == "none" and formato["acodec"] != "none":
        formatos_audio_somente.append(formato)

    elif formato["vcodec"] != "none" and formato["acodec"] == "none":
        formatos_video_somente.append(formato)

    elif formato["vcodec"] != "none" and formato["acodec"] != "none":
        formatos_audio_video.append(formato)

    else:
        formatos_outro.append(formato)

    if formato["vcodec"] != "none" and formato["height"] not in resolucoes:
        resolucoes.append(formato["height"])

    print(
        formato["format_id"],
        " | ",
        formato["ext"],
        " | ",
        formato["resolution"],
        " | ",
        formato["vcodec"],
        " | ",
        formato["acodec"],
        " | ",
        formato["tbr"],
        " | ",
        formato["vbr"],
        " | ",
        formato["abr"],
        " | ",
        formato["filesize_approx"],
        " | ",
        formato["fps"],
    )

print("\nQuantos são somente áudio?", len(formatos_audio_somente))
print("Quantos são somente vídeo?", len(formatos_video_somente))
print("Quantos têm áudio + vídeo?", len(formatos_audio_video))
print("Outros", len(formatos_outro))

print("\nFormato de áudio")
mostrar_formatos(formatos_audio_somente)

formatos_com_video = formatos_video_somente + formatos_audio_video
print("\nFormato de vídeo")
mostrar_formatos(formatos_com_video)

print("\nFormato de vídeo e áudio")
mostrar_formatos(formatos_audio_video)

print("\nOutros formatos")
mostrar_formatos(formatos_outro)


# Mostra as resoluções disponíveis do vídeo escolhido
print("\nResoluções disponíveis: ")
for resolucao in resolucoes:
    print(resolucao)

# Pergunta qual resolução o usuário deseja
resolucao_escolhida = int(input("\nInforme a resolução desejada: "))

# Se, a resolução não estiver entre as disponíveis, pergunta novamente
while resolucao_escolhida not in resolucoes:
    print("\nResolução indisponível!")
    resolucao_escolhida = int(input("Informe a resolução desejada: "))


# Função para buscar e retorna os vídeos disponíveis para a resolução escolhida
def buscar_video(info, resolucao_escolhida):
    videos = []

    for formato in info["formats"]:
        if formato["height"] == resolucao_escolhida and formato["vcodec"] != "none":
            videos.append(formato)

    return videos


# Busca e retorna os vídeos disponíveis para a resolução escolhida
videos_encontrados = buscar_video(info, resolucao_escolhida)

# Mostra os vídeos disponíveis
print(f"\nVídeo disponíveis em {resolucao_escolhida}p: ")
mostrar_formatos(videos_encontrados)

# Obtém os Codecs disponíveis para a resolução escolhida
codec_disponiveis = []


for codec in videos_encontrados:
    codec_base = codec["vcodec"].split(".")[0]

    if codec_base not in codec_disponiveis:
        codec_disponiveis.append(codec["vcodec"].split(".")[0])

# Informa os Codecs disponíveis para cada vídeo
print("\nCodecs disponíveis para essa resolução:")
for codec in codec_disponiveis:
    if codec.startswith("avc1"):
        print("1) H.264")
    elif codec.startswith("vp9"):
        print("2) VP9")
    elif codec.startswith("av01"):
        print("3) AV1")
    else:
        print("4) Outro")

# Pergunta ao usuário qual Codec ele deseja
codec = int(input("\nQual dos Codecs a cima você deseja escolher? "))
codec_escolhido = ""

match codec:
    case 1:
        codec_escolhido = "avc1"
    case 2:
        codec_escolhido = "vp9"
    case 3:
        codec_escolhido = "av01"
    case 4:
        codec_escolhido = "outro"

video_encontrado = False

# Mostra o vídeo disponível com base na resolução e codec escolhido
print(
    "                   ID  |  Extensão  |  Resolução  |  VCodec  |  ACodec  |  TBR  |  VBR  |  ABR  |  Filesize  |  FPS  "
)
for formato in videos_encontrados:
    if resolucao_escolhida == formato["height"] and formato["vcodec"].startswith(
        codec_escolhido
    ):
        print(
            "Vídeo disponível: ",
            formato["format_id"],
            " | ",
            formato["ext"],
            " | ",
            formato["resolution"],
            " | ",
            formato["vcodec"],
            " | ",
            formato["acodec"],
            " | ",
            formato["tbr"],
            " | ",
            formato["vbr"],
            " | ",
            formato["abr"],
            " | ",
            formato["filesize_approx"],
            " | ",
            formato["fps"],
        )
        video_encontrado = True

if not video_encontrado:
    print("Nenhum vídeo disponível com esse Codec!")

# Pede ao usuário para informar um URL
from ytdl_service import (
    baixar,
    montar_opcao,
    mostrar_codecs_disponiveis,
    mostrar_resolucao,
    obter_info_video,
)

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

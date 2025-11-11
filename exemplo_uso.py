#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Exemplos de uso do Gerador M3U
"""

from m3u_generator import (
    M3UGenerator, 
    Canal, 
    WebScraper, 
    FontesPreDefinidas,
    criar_playlist_completa,
    criar_playlist_personalizada
)


def exemplo_1_playlist_basica():
    """Exemplo 1: Criar uma playlist básica manualmente"""
    print("\n=== EXEMPLO 1: Playlist Básica ===\n")
    
    generator = M3UGenerator()
    
    # Adicionar canais manualmente
    canal1 = Canal(
        nome="Globo HD",
        url="http://exemplo.com/globo.m3u8",
        categoria="TV Aberta",
        logo="http://exemplo.com/logos/globo.png",
        grupo="Brasil"
    )
    
    canal2 = Canal(
        nome="SBT HD",
        url="http://exemplo.com/sbt.m3u8",
        categoria="TV Aberta",
        logo="http://exemplo.com/logos/sbt.png",
        grupo="Brasil"
    )
    
    generator.adicionar_canal(canal1)
    generator.adicionar_canal(canal2)
    
    # Gerar arquivo M3U
    generator.gerar_m3u("exemplo1_basico.m3u")
    print("✓ Arquivo gerado: exemplo1_basico.m3u")


def exemplo_2_usar_fontes_predefinidas():
    """Exemplo 2: Usar fontes pré-definidas"""
    print("\n=== EXEMPLO 2: Fontes Pré-definidas ===\n")
    
    generator = M3UGenerator()
    
    # Adicionar canais abertos
    print("Adicionando canais abertos...")
    for canal in FontesPreDefinidas.obter_canais_brasileiros_abertos():
        generator.adicionar_canal(canal)
    
    # Adicionar canais de notícias
    print("Adicionando canais de notícias...")
    for canal in FontesPreDefinidas.obter_canais_noticias():
        generator.adicionar_canal(canal)
    
    # Adicionar canais de esportes
    print("Adicionando canais de esportes...")
    for canal in FontesPreDefinidas.obter_canais_esportes():
        generator.adicionar_canal(canal)
    
    generator.gerar_m3u("exemplo2_predefinidos.m3u")
    print(f"✓ Arquivo gerado com {len(generator.canais)} canais: exemplo2_predefinidos.m3u")


def exemplo_3_extrair_de_url():
    """Exemplo 3: Extrair streams de uma URL"""
    print("\n=== EXEMPLO 3: Extrair de URL ===\n")
    
    scraper = WebScraper()
    generator = M3UGenerator()
    
    # URL de exemplo (substitua por uma URL real)
    url = "https://github.com/iptv-org/iptv"
    
    print(f"Buscando streams em: {url}")
    html = scraper.buscar_pagina(url)
    
    if html:
        streams = scraper.extrair_streams_genericos(html, url)
        print(f"Encontrados {len(streams)} possíveis streams")
        
        # Adicionar os primeiros 10 streams encontrados
        for i, stream_url in enumerate(streams[:10], 1):
            canal = Canal(
                nome=f"Canal {i}",
                url=stream_url,
                categoria="Web",
                grupo="Extraídos"
            )
            generator.adicionar_canal(canal)
        
        generator.gerar_m3u("exemplo3_extraidos.m3u")
        print(f"✓ Arquivo gerado: exemplo3_extraidos.m3u")
    else:
        print("✗ Erro ao buscar página")


def exemplo_4_playlist_filmes_series():
    """Exemplo 4: Playlist só de filmes e séries"""
    print("\n=== EXEMPLO 4: Filmes e Séries ===\n")
    
    generator = M3UGenerator()
    
    # Adicionar canais de filmes
    print("Adicionando canais de filmes...")
    for canal in FontesPreDefinidas.obter_canais_filmes():
        generator.adicionar_canal(canal)
    
    # Adicionar canais de séries
    print("Adicionando canais de séries...")
    for canal in FontesPreDefinidas.obter_canais_series():
        generator.adicionar_canal(canal)
    
    generator.gerar_m3u("exemplo4_filmes_series.m3u")
    print(f"✓ Arquivo gerado: exemplo4_filmes_series.m3u")


def exemplo_5_playlist_completa_com_adultos():
    """Exemplo 5: Playlist completa incluindo conteúdo adulto"""
    print("\n=== EXEMPLO 5: Playlist Completa (+ Adultos) ===\n")
    
    generator = M3UGenerator()
    
    # Adicionar todos os tipos
    categorias = [
        ("Canais Abertos", FontesPreDefinidas.obter_canais_brasileiros_abertos()),
        ("Notícias", FontesPreDefinidas.obter_canais_noticias()),
        ("Esportes", FontesPreDefinidas.obter_canais_esportes()),
        ("Filmes", FontesPreDefinidas.obter_canais_filmes()),
        ("Séries", FontesPreDefinidas.obter_canais_series()),
        ("Adultos +18", FontesPreDefinidas.obter_canais_adultos()),
    ]
    
    for nome_categoria, canais in categorias:
        print(f"Adicionando {nome_categoria}...")
        for canal in canais:
            generator.adicionar_canal(canal)
    
    generator.gerar_m3u("exemplo5_completa.m3u")
    print(f"✓ Arquivo gerado com {len(generator.canais)} canais: exemplo5_completa.m3u")


def exemplo_6_multiple_urls():
    """Exemplo 6: Extrair de múltiplas URLs"""
    print("\n=== EXEMPLO 6: Múltiplas URLs ===\n")
    
    urls = [
        "https://github.com/iptv-org/iptv",
        "https://raw.githubusercontent.com/Free-IPTV/Countries/master/BR01_BRAZIL.m3u",
    ]
    
    print(f"Processando {len(urls)} URLs...")
    criar_playlist_personalizada(urls, "exemplo6_multiplas.m3u")
    print("✓ Arquivo gerado: exemplo6_multiplas.m3u")


def exemplo_7_filtrar_por_categoria():
    """Exemplo 7: Criar playlist filtrada por categoria"""
    print("\n=== EXEMPLO 7: Filtrar por Categoria ===\n")
    
    generator = M3UGenerator()
    
    # Obter todos os canais
    todos_canais = []
    todos_canais.extend(FontesPreDefinidas.obter_canais_brasileiros_abertos())
    todos_canais.extend(FontesPreDefinidas.obter_canais_noticias())
    todos_canais.extend(FontesPreDefinidas.obter_canais_esportes())
    
    # Filtrar apenas esportes
    categoria_desejada = "Esportes"
    for canal in todos_canais:
        if canal.categoria == categoria_desejada:
            generator.adicionar_canal(canal)
    
    generator.gerar_m3u("exemplo7_esportes.m3u")
    print(f"✓ Arquivo gerado com canais de {categoria_desejada}: exemplo7_esportes.m3u")


def main():
    """Executar todos os exemplos"""
    print("=" * 60)
    print("EXEMPLOS DE USO DO GERADOR M3U")
    print("=" * 60)
    
    print("\nEscolha um exemplo para executar:")
    print("1 - Playlist básica manual")
    print("2 - Usar fontes pré-definidas")
    print("3 - Extrair streams de URL")
    print("4 - Playlist de filmes e séries")
    print("5 - Playlist completa (incluindo adultos)")
    print("6 - Extrair de múltiplas URLs")
    print("7 - Filtrar por categoria")
    print("8 - Executar todos os exemplos")
    print("0 - Sair")
    
    opcao = input("\nOpção: ").strip()
    
    exemplos = {
        "1": exemplo_1_playlist_basica,
        "2": exemplo_2_usar_fontes_predefinidas,
        "3": exemplo_3_extrair_de_url,
        "4": exemplo_4_playlist_filmes_series,
        "5": exemplo_5_playlist_completa_com_adultos,
        "6": exemplo_6_multiple_urls,
        "7": exemplo_7_filtrar_por_categoria,
    }
    
    if opcao == "8":
        print("\nExecutando todos os exemplos...\n")
        for exemplo in exemplos.values():
            try:
                exemplo()
            except Exception as e:
                print(f"✗ Erro no exemplo: {e}")
        print("\n" + "=" * 60)
        print("Todos os exemplos foram executados!")
    elif opcao in exemplos:
        exemplos[opcao]()
    elif opcao == "0":
        print("Saindo...")
    else:
        print("Opção inválida!")


if __name__ == "__main__":
    main()

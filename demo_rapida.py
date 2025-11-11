#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Demonstração Rápida - Cria uma playlist M3U de exemplo
Execute: python3 demo_rapida.py
"""

from m3u_generator import M3UGenerator, Canal, FontesPreDefinidas

def main():
    print("=" * 60)
    print("DEMONSTRAÇÃO RÁPIDA - GERADOR M3U")
    print("=" * 60)
    print()
    
    # Criar gerador
    generator = M3UGenerator()
    
    print("📺 Adicionando canais de TV aberta...")
    for canal in FontesPreDefinidas.obter_canais_brasileiros_abertos():
        generator.adicionar_canal(canal)
    
    print("📰 Adicionando canais de notícias...")
    for canal in FontesPreDefinidas.obter_canais_noticias():
        generator.adicionar_canal(canal)
    
    print("⚽ Adicionando canais de esportes...")
    for canal in FontesPreDefinidas.obter_canais_esportes():
        generator.adicionar_canal(canal)
    
    print("🎬 Adicionando canais de filmes...")
    for canal in FontesPreDefinidas.obter_canais_filmes():
        generator.adicionar_canal(canal)
    
    print("📺 Adicionando canais de séries...")
    for canal in FontesPreDefinidas.obter_canais_series():
        generator.adicionar_canal(canal)
    
    print()
    print(f"✅ Total de {len(generator.canais)} canais adicionados!")
    print()
    
    # Gerar arquivo
    arquivo = "demo_playlist.m3u"
    print(f"💾 Gerando arquivo: {arquivo}")
    
    if generator.gerar_m3u(arquivo):
        print()
        print("=" * 60)
        print("✨ SUCESSO! ✨")
        print("=" * 60)
        print()
        print(f"📁 Arquivo gerado: {arquivo}")
        print(f"📊 Total de canais: {len(generator.canais)}")
        print()
        print("Para visualizar:")
        print(f"  - Abra o arquivo {arquivo} com VLC, Kodi ou outro player")
        print(f"  - Ou leia o arquivo: cat {arquivo}")
        print()
        print("Categorias incluídas:")
        print("  ✓ TV Aberta (5 canais)")
        print("  ✓ Notícias (3 canais)")
        print("  ✓ Esportes (3 canais)")
        print("  ✓ Filmes (3 canais)")
        print("  ✓ Séries (3 canais)")
        print()
        print("⚠️  NOTA: Os URLs nesta demo são exemplos.")
        print("   Para URLs reais, consulte: fontes_legais.md")
        print()
    else:
        print("❌ Erro ao gerar arquivo!")

if __name__ == "__main__":
    main()

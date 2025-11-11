#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Programa principal para gerar arquivos M3U
"""

import argparse
import os
from gerador_m3u import GeradorM3U, StreamInfo
from scrapers import ScraperM3UPublico, ScraperGenerico, ScraperPersonalizado


def main():
    parser = argparse.ArgumentParser(
        description='Gerador de arquivos M3U a partir de fontes web',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  python main.py --completo
  python main.py --categoria live
  python main.py --categoria movie --arquivo filmes.m3u
  python main.py --fonte-publica --categoria open
  python main.py --arquivo-entrada streams.txt
        """
    )
    
    parser.add_argument('--completo', action='store_true',
                       help='Gera arquivo M3U completo com todos os streams')
    
    parser.add_argument('--categoria', choices=['live', 'movie', 'series', 'adult', 'open', 'private'],
                       help='Filtra streams por categoria')
    
    parser.add_argument('--arquivo', default='playlist.m3u',
                       help='Nome do arquivo M3U de saída (padrão: playlist.m3u)')
    
    parser.add_argument('--separar', action='store_true',
                       help='Gera arquivos M3U separados por categoria')
    
    parser.add_argument('--fonte-publica', action='store_true',
                       help='Busca streams de fontes públicas M3U')
    
    parser.add_argument('--url-site', type=str,
                       help='URL de um site para fazer scraping')
    
    parser.add_argument('--arquivo-entrada', type=str,
                       help='Arquivo de texto com streams (formato: nome|url|categoria|grupo)')
    
    parser.add_argument('--validar', action='store_true',
                       help='Valida URLs antes de adicionar ao M3U')
    
    args = parser.parse_args()
    
    gerador = GeradorM3U()
    
    print("=" * 60)
    print("GERADOR DE ARQUIVOS M3U")
    print("=" * 60)
    print()
    
    # Buscar streams de diferentes fontes
    if args.fonte_publica:
        print("Buscando streams de fontes públicas...")
        scraper_publico = ScraperM3UPublico()
        streams = scraper_publico.buscar_streams(categoria=args.categoria or "live")
        gerador.adicionar_streams(streams)
    
    if args.url_site:
        print(f"Fazendo scraping de {args.url_site}...")
        scraper = ScraperGenerico()
        categoria = args.categoria or "live"
        streams = scraper.buscar_streams_de_site(args.url_site, categoria)
        gerador.adicionar_streams(streams)
    
    if args.arquivo_entrada:
        print(f"Carregando streams de {args.arquivo_entrada}...")
        streams = ScraperPersonalizado.criar_streams_de_arquivo(args.arquivo_entrada)
        gerador.adicionar_streams(streams)
    
    # Se nenhuma fonte foi especificada, usar fontes públicas por padrão
    if not args.fonte_publica and not args.url_site and not args.arquivo_entrada:
        print("Usando fontes públicas por padrão...")
        scraper_publico = ScraperM3UPublico()
        streams = scraper_publico.buscar_streams()
        gerador.adicionar_streams(streams)
    
    # Validar URLs se solicitado
    if args.validar:
        print("\nValidando URLs...")
        streams_validos = []
        total = len(gerador.streams)
        for i, stream in enumerate(gerador.streams, 1):
            if gerador.validar_url(stream.url):
                streams_validos.append(stream)
            if i % 10 == 0:
                print(f"Validados {i}/{total} streams...")
        gerador.streams = streams_validos
        print(f"✓ {len(streams_validos)} streams válidos de {total} total")
    
    # Gerar arquivos M3U
    if args.separar:
        print("\nGerando arquivos M3U separados por categoria...")
        gerador.gerar_m3u_por_categoria()
    elif args.completo or not args.categoria:
        print(f"\nGerando arquivo M3U completo: {args.arquivo}")
        gerador.gerar_m3u_completo(args.arquivo)
    else:
        print(f"\nGerando arquivo M3U para categoria '{args.categoria}': {args.arquivo}")
        gerador.gerar_m3u(args.arquivo, filtro_categoria=args.categoria)
    
    print("\n" + "=" * 60)
    print("CONCLUÍDO!")
    print("=" * 60)
    print(f"Total de streams processados: {len(gerador.streams)}")
    
    # Estatísticas por categoria
    categorias = {}
    for stream in gerador.streams:
        categorias[stream.categoria] = categorias.get(stream.categoria, 0) + 1
    
    print("\nEstatísticas por categoria:")
    for cat, count in categorias.items():
        print(f"  {cat}: {count} streams")


if __name__ == "__main__":
    main()

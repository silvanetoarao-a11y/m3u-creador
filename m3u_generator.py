#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gerador de Playlists M3U a partir de Fontes Web
Suporta: Canais ao Vivo, Filmes, Séries, Canais Adultos
"""

import requests
from bs4 import BeautifulSoup
import re
import json
import time
from typing import List, Dict, Optional
from urllib.parse import urljoin, urlparse
import logging

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class Canal:
    """Representa um canal ou stream"""
    
    def __init__(self, nome: str, url: str, categoria: str = "Geral", 
                 logo: str = "", grupo: str = "", idioma: str = "pt"):
        self.nome = nome
        self.url = url
        self.categoria = categoria
        self.logo = logo
        self.grupo = grupo
        self.idioma = idioma
        self.tvg_id = self._gerar_tvg_id()
    
    def _gerar_tvg_id(self) -> str:
        """Gera um ID único para o canal"""
        return re.sub(r'[^a-zA-Z0-9]', '', self.nome.lower())
    
    def to_m3u_entry(self) -> str:
        """Converte para formato M3U"""
        extinf = f'#EXTINF:-1'
        
        if self.tvg_id:
            extinf += f' tvg-id="{self.tvg_id}"'
        if self.logo:
            extinf += f' tvg-logo="{self.logo}"'
        if self.grupo:
            extinf += f' group-title="{self.grupo}"'
        
        extinf += f',{self.nome}'
        
        return f'{extinf}\n{self.url}'


class M3UGenerator:
    """Gerador de arquivos M3U"""
    
    def __init__(self):
        self.canais: List[Canal] = []
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def adicionar_canal(self, canal: Canal):
        """Adiciona um canal à lista"""
        self.canais.append(canal)
        logger.info(f"Canal adicionado: {canal.nome}")
    
    def gerar_m3u(self, arquivo_saida: str = "playlist.m3u"):
        """Gera o arquivo M3U"""
        try:
            with open(arquivo_saida, 'w', encoding='utf-8') as f:
                f.write("#EXTM3U\n\n")
                
                for canal in self.canais:
                    f.write(canal.to_m3u_entry() + "\n\n")
            
            logger.info(f"Arquivo M3U gerado: {arquivo_saida} ({len(self.canais)} canais)")
            return True
        except Exception as e:
            logger.error(f"Erro ao gerar M3U: {e}")
            return False
    
    def limpar_canais(self):
        """Limpa a lista de canais"""
        self.canais = []


class WebScraper:
    """Scraper genérico para extrair streams de páginas web"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    def buscar_pagina(self, url: str, timeout: int = 10) -> Optional[str]:
        """Busca o conteúdo de uma página"""
        try:
            response = self.session.get(url, timeout=timeout)
            response.raise_for_status()
            return response.text
        except Exception as e:
            logger.error(f"Erro ao buscar página {url}: {e}")
            return None
    
    def extrair_streams_genericos(self, html: str, url_base: str = "") -> List[Dict]:
        """Extrai URLs de streams de HTML (método genérico)"""
        streams = []
        
        # Padrões comuns de URLs de streaming
        padroes = [
            r'https?://[^\s<>"]+\.m3u8[^\s<>"]*',
            r'https?://[^\s<>"]+\.ts[^\s<>"]*',
            r'https?://[^\s<>"]+/live[^\s<>"]*',
            r'https?://[^\s<>"]+/stream[^\s<>"]*',
        ]
        
        for padrao in padroes:
            matches = re.findall(padrao, html, re.IGNORECASE)
            streams.extend(matches)
        
        # Buscar em atributos src e href
        soup = BeautifulSoup(html, 'html.parser')
        
        for tag in soup.find_all(['a', 'source', 'video', 'iframe']):
            url = tag.get('href') or tag.get('src') or tag.get('data-src')
            if url and self._e_stream_valido(url):
                if url_base and not url.startswith('http'):
                    url = urljoin(url_base, url)
                streams.append(url)
        
        # Remover duplicatas
        return list(set(streams))
    
    def _e_stream_valido(self, url: str) -> bool:
        """Verifica se URL é um stream válido"""
        extensoes_validas = ['.m3u8', '.ts', '.mp4', '.mkv', '.avi', '.flv']
        palavras_chave = ['stream', 'live', 'channel', 'video', 'play']
        
        url_lower = url.lower()
        
        # Verifica extensões
        if any(url_lower.endswith(ext) or ext in url_lower for ext in extensoes_validas):
            return True
        
        # Verifica palavras-chave
        if any(palavra in url_lower for palavra in palavras_chave):
            return True
        
        return False
    
    def extrair_com_seletores(self, html: str, seletores: Dict) -> List[Dict]:
        """Extrai streams usando seletores CSS personalizados"""
        streams = []
        soup = BeautifulSoup(html, 'html.parser')
        
        elementos = soup.select(seletores.get('container', 'body'))
        
        for elemento in elementos:
            nome = ""
            url = ""
            logo = ""
            
            # Extrai nome
            if seletores.get('nome'):
                nome_elem = elemento.select_one(seletores['nome'])
                if nome_elem:
                    nome = nome_elem.get_text(strip=True)
            
            # Extrai URL
            if seletores.get('url'):
                url_elem = elemento.select_one(seletores['url'])
                if url_elem:
                    url = url_elem.get('href') or url_elem.get('src') or url_elem.get_text(strip=True)
            
            # Extrai logo
            if seletores.get('logo'):
                logo_elem = elemento.select_one(seletores['logo'])
                if logo_elem:
                    logo = logo_elem.get('src') or logo_elem.get('href')
            
            if nome and url:
                streams.append({
                    'nome': nome,
                    'url': url,
                    'logo': logo
                })
        
        return streams


class FontesPreDefinidas:
    """Fontes pré-definidas de streams (exemplos)"""
    
    @staticmethod
    def obter_canais_brasileiros_abertos() -> List[Canal]:
        """Retorna lista de canais brasileiros abertos conhecidos"""
        canais = [
            Canal("Globo", "https://exemplo.com/globo/stream.m3u8", "TV Aberta", 
                  "https://exemplo.com/logos/globo.png", "Brasil"),
            Canal("SBT", "https://exemplo.com/sbt/stream.m3u8", "TV Aberta",
                  "https://exemplo.com/logos/sbt.png", "Brasil"),
            Canal("Record", "https://exemplo.com/record/stream.m3u8", "TV Aberta",
                  "https://exemplo.com/logos/record.png", "Brasil"),
            Canal("Band", "https://exemplo.com/band/stream.m3u8", "TV Aberta",
                  "https://exemplo.com/logos/band.png", "Brasil"),
            Canal("RedeTV", "https://exemplo.com/redetv/stream.m3u8", "TV Aberta",
                  "https://exemplo.com/logos/redetv.png", "Brasil"),
        ]
        return canais
    
    @staticmethod
    def obter_canais_noticias() -> List[Canal]:
        """Retorna canais de notícias"""
        canais = [
            Canal("GloboNews", "https://exemplo.com/globonews/stream.m3u8", "Notícias",
                  "https://exemplo.com/logos/globonews.png", "Notícias"),
            Canal("CNN Brasil", "https://exemplo.com/cnn/stream.m3u8", "Notícias",
                  "https://exemplo.com/logos/cnn.png", "Notícias"),
            Canal("BandNews", "https://exemplo.com/bandnews/stream.m3u8", "Notícias",
                  "https://exemplo.com/logos/bandnews.png", "Notícias"),
        ]
        return canais
    
    @staticmethod
    def obter_canais_esportes() -> List[Canal]:
        """Retorna canais de esportes"""
        canais = [
            Canal("SporTV", "https://exemplo.com/sportv/stream.m3u8", "Esportes",
                  "https://exemplo.com/logos/sportv.png", "Esportes"),
            Canal("ESPN", "https://exemplo.com/espn/stream.m3u8", "Esportes",
                  "https://exemplo.com/logos/espn.png", "Esportes"),
            Canal("Fox Sports", "https://exemplo.com/foxsports/stream.m3u8", "Esportes",
                  "https://exemplo.com/logos/foxsports.png", "Esportes"),
        ]
        return canais
    
    @staticmethod
    def obter_canais_filmes() -> List[Canal]:
        """Retorna canais de filmes"""
        canais = [
            Canal("Telecine Premium", "https://exemplo.com/telecine/stream.m3u8", "Filmes",
                  "https://exemplo.com/logos/telecine.png", "Filmes"),
            Canal("HBO", "https://exemplo.com/hbo/stream.m3u8", "Filmes",
                  "https://exemplo.com/logos/hbo.png", "Filmes"),
            Canal("Cinemax", "https://exemplo.com/cinemax/stream.m3u8", "Filmes",
                  "https://exemplo.com/logos/cinemax.png", "Filmes"),
        ]
        return canais
    
    @staticmethod
    def obter_canais_series() -> List[Canal]:
        """Retorna canais de séries"""
        canais = [
            Canal("Warner", "https://exemplo.com/warner/stream.m3u8", "Séries",
                  "https://exemplo.com/logos/warner.png", "Séries"),
            Canal("Universal", "https://exemplo.com/universal/stream.m3u8", "Séries",
                  "https://exemplo.com/logos/universal.png", "Séries"),
            Canal("AXN", "https://exemplo.com/axn/stream.m3u8", "Séries",
                  "https://exemplo.com/logos/axn.png", "Séries"),
        ]
        return canais
    
    @staticmethod
    def obter_canais_adultos() -> List[Canal]:
        """Retorna canais adultos (+18)"""
        canais = [
            Canal("Adulto 1", "https://exemplo.com/adult1/stream.m3u8", "Adulto",
                  "", "Adultos +18"),
            Canal("Adulto 2", "https://exemplo.com/adult2/stream.m3u8", "Adulto",
                  "", "Adultos +18"),
            Canal("Adulto 3", "https://exemplo.com/adult3/stream.m3u8", "Adulto",
                  "", "Adultos +18"),
        ]
        return canais


def criar_playlist_completa():
    """Cria uma playlist completa com todos os tipos de conteúdo"""
    generator = M3UGenerator()
    
    logger.info("Gerando playlist completa...")
    
    # Adiciona todos os tipos de canais
    for canal in FontesPreDefinidas.obter_canais_brasileiros_abertos():
        generator.adicionar_canal(canal)
    
    for canal in FontesPreDefinidas.obter_canais_noticias():
        generator.adicionar_canal(canal)
    
    for canal in FontesPreDefinidas.obter_canais_esportes():
        generator.adicionar_canal(canal)
    
    for canal in FontesPreDefinidas.obter_canais_filmes():
        generator.adicionar_canal(canal)
    
    for canal in FontesPreDefinidas.obter_canais_series():
        generator.adicionar_canal(canal)
    
    # Gera arquivo
    generator.gerar_m3u("playlist_completa.m3u")


def criar_playlist_personalizada(fontes_web: List[str], arquivo_saida: str):
    """Cria playlist a partir de fontes web personalizadas"""
    generator = M3UGenerator()
    scraper = WebScraper()
    
    logger.info(f"Processando {len(fontes_web)} fontes web...")
    
    for idx, url in enumerate(fontes_web, 1):
        logger.info(f"Processando fonte {idx}/{len(fontes_web)}: {url}")
        
        html = scraper.buscar_pagina(url)
        if not html:
            continue
        
        # Extrai streams
        streams = scraper.extrair_streams_genericos(html, url)
        
        logger.info(f"Encontrados {len(streams)} streams em {url}")
        
        # Adiciona os streams encontrados
        for stream_url in streams:
            nome = f"Canal {len(generator.canais) + 1}"
            canal = Canal(nome, stream_url, "Diversos", "", "Web")
            generator.adicionar_canal(canal)
        
        # Delay para evitar sobrecarga
        time.sleep(1)
    
    # Gera arquivo
    generator.gerar_m3u(arquivo_saida)


def criar_playlist_com_adultos():
    """Cria playlist incluindo conteúdo adulto"""
    generator = M3UGenerator()
    
    logger.info("Gerando playlist com conteúdo adulto...")
    
    # Adiciona canais normais
    for canal in FontesPreDefinidas.obter_canais_brasileiros_abertos():
        generator.adicionar_canal(canal)
    
    # Adiciona canais adultos
    for canal in FontesPreDefinidas.obter_canais_adultos():
        generator.adicionar_canal(canal)
    
    # Gera arquivo
    generator.gerar_m3u("playlist_adultos.m3u")


def main():
    """Função principal"""
    print("=" * 60)
    print("GERADOR DE PLAYLISTS M3U")
    print("=" * 60)
    print()
    print("Escolha uma opção:")
    print("1 - Criar playlist completa (todos os tipos)")
    print("2 - Criar playlist de canais abertos")
    print("3 - Criar playlist de filmes e séries")
    print("4 - Criar playlist com conteúdo adulto")
    print("5 - Extrair de URLs personalizadas")
    print("0 - Sair")
    print()
    
    opcao = input("Opção: ").strip()
    
    if opcao == "1":
        criar_playlist_completa()
        print("\n✓ Playlist completa gerada: playlist_completa.m3u")
    
    elif opcao == "2":
        generator = M3UGenerator()
        for canal in FontesPreDefinidas.obter_canais_brasileiros_abertos():
            generator.adicionar_canal(canal)
        generator.gerar_m3u("canais_abertos.m3u")
        print("\n✓ Playlist gerada: canais_abertos.m3u")
    
    elif opcao == "3":
        generator = M3UGenerator()
        for canal in FontesPreDefinidas.obter_canais_filmes():
            generator.adicionar_canal(canal)
        for canal in FontesPreDefinidas.obter_canais_series():
            generator.adicionar_canal(canal)
        generator.gerar_m3u("filmes_series.m3u")
        print("\n✓ Playlist gerada: filmes_series.m3u")
    
    elif opcao == "4":
        criar_playlist_com_adultos()
        print("\n✓ Playlist com adultos gerada: playlist_adultos.m3u")
    
    elif opcao == "5":
        print("\nDigite as URLs (uma por linha, linha vazia para terminar):")
        urls = []
        while True:
            url = input().strip()
            if not url:
                break
            urls.append(url)
        
        if urls:
            arquivo = input("\nNome do arquivo de saída (ex: minha_playlist.m3u): ").strip()
            if not arquivo:
                arquivo = "playlist_personalizada.m3u"
            criar_playlist_personalizada(urls, arquivo)
            print(f"\n✓ Playlist gerada: {arquivo}")
        else:
            print("Nenhuma URL fornecida.")
    
    elif opcao == "0":
        print("Saindo...")
    
    else:
        print("Opção inválida!")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Módulo de scraping para diferentes fontes web
"""

import re
import requests
import json
from typing import List, Optional, Set
from urllib.parse import urljoin, urlparse
from gerador_m3u import StreamInfo, GeradorM3U
from bs4 import BeautifulSoup
import time


class ScraperBase:
    """Classe base para scrapers"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    def fazer_requisicao(self, url: str) -> Optional[str]:
        """Faz uma requisição HTTP e retorna o conteúdo"""
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"Erro ao fazer requisição para {url}: {e}")
            return None
    
    def extrair_urls_m3u(self, texto: str) -> List[str]:
        """Extrai URLs de streams M3U de um texto"""
        # Padrões comuns para URLs de stream
        padroes = [
            r'https?://[^\s<>"{}|\\^`\[\]]+\.m3u8?',
            r'https?://[^\s<>"{}|\\^`\[\]]+\.ts',
            r'https?://[^\s<>"{}|\\^`\[\]]+\.mp4',
            r'https?://[^\s<>"{}|\\^`\[\]]+\.flv',
            r'https?://[^\s<>"{}|\\^`\[\]]+\.mpd',
            r'rtmp://[^\s<>"{}|\\^`\[\]]+',
            r'rtsp://[^\s<>"{}|\\^`\[\]]+',
        ]
        
        urls = []
        for padrao in padroes:
            matches = re.findall(padrao, texto, re.IGNORECASE)
            urls.extend(matches)
        
        return list(set(urls))  # Remove duplicatas
    
    def extrair_nomes_canais(self, texto: str) -> List[str]:
        """Extrai nomes de canais de um texto"""
        # Padrões comuns para nomes de canais
        padroes = [
            r'#EXTINF.*?,(.+?)(?:\n|$)',
            r'channel["\']?\s*[:=]\s*["\']?([^"\']+)',
            r'title["\']?\s*[:=]\s*["\']?([^"\']+)',
            r'name["\']?\s*[:=]\s*["\']?([^"\']+)',
        ]
        
        nomes = []
        for padrao in padroes:
            matches = re.findall(padrao, texto, re.IGNORECASE | re.MULTILINE)
            nomes.extend(matches)
        
        return nomes


class BuscadorAutomatico(ScraperBase):
    """Classe para buscar automaticamente fontes M3U na web"""
    
    def __init__(self):
        super().__init__()
        self.fontes_encontradas: Set[str] = set()
        self.repositorios_github_conhecidos = [
            "iptv-org/iptv",
            "freeiptv/iptv",
            "EvilCult/iptv-m3u-maker",
            "iptvlist/iptvlist",
            "m3u-editor/m3u-editor",
        ]
        
        # Padrões de URLs que podem conter listas M3U
        self.padroes_urls_m3u = [
            r'https?://[^\s<>"{}|\\^`\[\]]+\.m3u8?',
            r'https?://[^\s<>"{}|\\^`\[\]]+/playlist\.m3u8?',
            r'https?://[^\s<>"{}|\\^`\[\]]+/list\.m3u8?',
            r'https?://[^\s<>"{}|\\^`\[\]]+/iptv\.m3u8?',
        ]
    
    def buscar_repositorios_github(self) -> List[str]:
        """Busca repositórios GitHub com arquivos M3U"""
        urls_encontradas = []
        
        print("Buscando repositórios GitHub...")
        for repo in self.repositorios_github_conhecidos:
            try:
                # Tentar diferentes branches
                branches = ['master', 'main', 'gh-pages']
                encontrado = False
                
                for branch in branches:
                    try:
                        api_url = f"https://api.github.com/repos/{repo}/git/trees/{branch}?recursive=1"
                        response = requests.get(api_url, headers=self.headers, timeout=10)
                        
                        if response.status_code == 200:
                            data = response.json()
                            if 'tree' in data:
                                for item in data['tree']:
                                    if item['path'].endswith('.m3u') or item['path'].endswith('.m3u8'):
                                        raw_url = f"https://raw.githubusercontent.com/{repo}/{branch}/{item['path']}"
                                        urls_encontradas.append(raw_url)
                                        print(f"  ✓ Encontrado: {item['path']}")
                                encontrado = True
                                break
                    except:
                        continue
                
                if not encontrado:
                    # Tentar buscar diretamente arquivos conhecidos
                    arquivos_conhecidos = ['streams/br.m3u', 'streams/us.m3u', 'streams/world.m3u', 
                                          'playlist.m3u', 'list.m3u', 'iptv.m3u']
                    for arquivo in arquivos_conhecidos:
                        for branch in branches:
                            url_teste = f"https://raw.githubusercontent.com/{repo}/{branch}/{arquivo}"
                            if self.fazer_requisicao(url_teste):
                                urls_encontradas.append(url_teste)
                                print(f"  ✓ Encontrado: {arquivo}")
                                break
            except Exception as e:
                print(f"  ✗ Erro ao buscar {repo}: {e}")
        
        return urls_encontradas
    
    def buscar_em_sites_conhecidos(self) -> List[str]:
        """Busca em sites conhecidos que hospedam listas M3U"""
        urls_encontradas = []
        
        # Lista de sites conhecidos com listas M3U públicas
        sites_base = [
            "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/",
            "https://iptv-org.github.io/iptv/",
        ]
        
        print("Buscando em sites conhecidos...")
        for site_base in sites_base:
            try:
                conteudo = self.fazer_requisicao(site_base)
                if conteudo:
                    # Extrair links M3U da página
                    soup = BeautifulSoup(conteudo, 'html.parser')
                    links = soup.find_all('a', href=True)
                    
                    for link in links:
                        href = link['href']
                        if href.endswith('.m3u') or href.endswith('.m3u8'):
                            url_completa = urljoin(site_base, href)
                            urls_encontradas.append(url_completa)
                            print(f"  ✓ Encontrado: {href}")
            except Exception as e:
                print(f"  ✗ Erro ao buscar em {site_base}: {e}")
        
        return urls_encontradas
    
    def buscar_em_paginas_html(self, url: str) -> List[str]:
        """Busca links M3U em uma página HTML"""
        urls_encontradas = []
        conteudo = self.fazer_requisicao(url)
        
        if conteudo:
            try:
                soup = BeautifulSoup(conteudo, 'html.parser')
                
                # Buscar links diretos
                links = soup.find_all('a', href=True)
                for link in links:
                    href = link['href']
                    if href.endswith('.m3u') or href.endswith('.m3u8'):
                        url_completa = urljoin(url, href)
                        urls_encontradas.append(url_completa)
                
                # Buscar em tags script e outros elementos
                textos = soup.find_all(string=True)
                for texto in textos:
                    for padrao in self.padroes_urls_m3u:
                        matches = re.findall(padrao, texto, re.IGNORECASE)
                        urls_encontradas.extend(matches)
                
                # Buscar em atributos data-*
                elementos = soup.find_all(attrs=lambda x: x and any('m3u' in str(v).lower() for v in (x.values() if isinstance(x, dict) else [])))
                for elem in elementos:
                    for attr, value in elem.attrs.items():
                        if isinstance(value, str) and ('.m3u' in value.lower() or 'm3u' in value.lower()):
                            if value.startswith('http'):
                                urls_encontradas.append(value)
                            else:
                                urls_encontradas.append(urljoin(url, value))
            except Exception as e:
                print(f"  ✗ Erro ao processar HTML: {e}")
        
        return list(set(urls_encontradas))  # Remove duplicatas
    
    def buscar_em_pastebin_gist(self) -> List[str]:
        """Busca em serviços de paste como Pastebin e Gist"""
        urls_encontradas = []
        
        # Buscar em Gists públicos relacionados a IPTV/M3U
        print("Buscando em Gists públicos...")
        try:
            # API do GitHub para buscar gists com termos relacionados
            search_url = "https://api.github.com/search/code"
            params = {
                'q': 'extension:m3u OR extension:m3u8',
                'sort': 'updated',
                'order': 'desc'
            }
            response = requests.get(search_url, params=params, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if 'items' in data:
                    for item in data['items'][:10]:  # Limitar a 10 resultados
                        if 'html_url' in item:
                            raw_url = item['html_url'].replace('/blob/', '/raw/')
                            urls_encontradas.append(raw_url)
                            print(f"  ✓ Encontrado Gist: {item.get('name', 'N/A')}")
        except Exception as e:
            print(f"  ✗ Erro ao buscar Gists: {e}")
        
        return urls_encontradas
    
    def buscar_todas_fontes(self) -> List[str]:
        """Busca automaticamente todas as fontes possíveis"""
        print("=" * 60)
        print("BUSCA AUTOMÁTICA DE FONTES M3U")
        print("=" * 60)
        print()
        
        todas_urls = []
        
        # Buscar em repositórios GitHub
        urls_github = self.buscar_repositorios_github()
        todas_urls.extend(urls_github)
        print(f"✓ {len(urls_github)} fontes encontradas no GitHub\n")
        
        # Buscar em sites conhecidos
        urls_sites = self.buscar_em_sites_conhecidos()
        todas_urls.extend(urls_sites)
        print(f"✓ {len(urls_sites)} fontes encontradas em sites conhecidos\n")
        
        # Buscar em Gists
        urls_gists = self.buscar_em_pastebin_gist()
        todas_urls.extend(urls_gists)
        print(f"✓ {len(urls_gists)} fontes encontradas em Gists\n")
        
        # Remover duplicatas
        todas_urls = list(set(todas_urls))
        
        print(f"Total de fontes únicas encontradas: {len(todas_urls)}")
        print("=" * 60)
        print()
        
        return todas_urls
    
    def processar_fonte_automatica(self, url: str, categoria: str = "live") -> List[StreamInfo]:
        """Processa uma fonte M3U automaticamente"""
        streams = []
        conteudo = self.fazer_requisicao(url)
        
        if conteudo and ('#EXTM3U' in conteudo or '.m3u' in url.lower()):
            # É um arquivo M3U válido
            linhas = conteudo.split('\n')
            nome_atual = ""
            url_atual = ""
            grupo_atual = ""
            logo_atual = ""
            
            for linha in linhas:
                linha = linha.strip()
                
                if linha.startswith('#EXTINF'):
                    nome_match = re.search(r',(.+?)$', linha)
                    if nome_match:
                        nome_atual = nome_match.group(1)
                    
                    grupo_match = re.search(r'group-title="([^"]+)"', linha)
                    if grupo_match:
                        grupo_atual = grupo_match.group(1)
                    
                    logo_match = re.search(r'tvg-logo="([^"]+)"', linha)
                    if logo_match:
                        logo_atual = logo_match.group(1)
                
                elif linha and not linha.startswith('#'):
                    url_atual = linha
                    if nome_atual and url_atual:
                        # Determinar categoria baseada no grupo ou nome
                        cat = self.determinar_categoria(nome_atual, grupo_atual, categoria)
                        
                        stream = StreamInfo(
                            nome=nome_atual,
                            url=url_atual,
                            categoria=cat,
                            grupo=grupo_atual,
                            logo=logo_atual
                        )
                        streams.append(stream)
                        nome_atual = ""
                        url_atual = ""
        
        return streams
    
    def determinar_categoria(self, nome: str, grupo: str, padrao: str = "live") -> str:
        """Determina a categoria baseada no nome e grupo"""
        texto = f"{nome} {grupo}".lower()
        
        if any(palavra in texto for palavra in ['movie', 'filme', 'cinema', 'film']):
            return "movie"
        elif any(palavra in texto for palavra in ['series', 'serie', 'tv show', 'show']):
            return "series"
        elif any(palavra in texto for palavra in ['adult', 'xxx', '18+', 'adulto']):
            return "adult"
        elif any(palavra in texto for palavra in ['open', 'aberto', 'free', 'gratis']):
            return "open"
        elif any(palavra in texto for palavra in ['private', 'privado', 'premium', 'paid']):
            return "private"
        else:
            return padrao


class ScraperM3UPublico(ScraperBase):
    """Scraper para listas M3U públicas"""
    
    def __init__(self):
        super().__init__()
        self.fontes_publicas = [
            "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/br.m3u",
            "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/us.m3u",
            "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/world.m3u",
            "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/mx.m3u",
            "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/es.m3u",
            "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/pt.m3u",
            "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/ar.m3u",
        ]
    
    def buscar_streams(self, categoria: str = "live") -> List[StreamInfo]:
        """Busca streams de fontes públicas"""
        streams = []
        
        for fonte in self.fontes_publicas:
            print(f"Buscando streams de {fonte}...")
            conteudo = self.fazer_requisicao(fonte)
            
            if conteudo:
                linhas = conteudo.split('\n')
                nome_atual = ""
                url_atual = ""
                grupo_atual = ""
                logo_atual = ""
                
                for linha in linhas:
                    linha = linha.strip()
                    
                    if linha.startswith('#EXTINF'):
                        # Extrai informações do EXTINF
                        nome_match = re.search(r',(.+?)$', linha)
                        if nome_match:
                            nome_atual = nome_match.group(1)
                        
                        grupo_match = re.search(r'group-title="([^"]+)"', linha)
                        if grupo_match:
                            grupo_atual = grupo_match.group(1)
                        
                        logo_match = re.search(r'tvg-logo="([^"]+)"', linha)
                        if logo_match:
                            logo_atual = logo_match.group(1)
                    
                    elif linha and not linha.startswith('#'):
                        url_atual = linha
                        if nome_atual and url_atual:
                            stream = StreamInfo(
                                nome=nome_atual,
                                url=url_atual,
                                categoria=categoria,
                                grupo=grupo_atual,
                                logo=logo_atual
                            )
                            streams.append(stream)
                            nome_atual = ""
                            url_atual = ""
        
        print(f"✓ Encontrados {len(streams)} streams de fontes públicas")
        return streams


class ScraperGenerico(ScraperBase):
    """Scraper genérico para sites web"""
    
    def buscar_streams_de_site(self, url: str, categoria: str = "live") -> List[StreamInfo]:
        """Busca streams de um site genérico"""
        streams = []
        conteudo = self.fazer_requisicao(url)
        
        if conteudo:
            urls = self.extrair_urls_m3u(conteudo)
            nomes = self.extrair_nomes_canais(conteudo)
            
            for i, url_stream in enumerate(urls):
                nome = nomes[i] if i < len(nomes) else f"Canal {i+1}"
                stream = StreamInfo(
                    nome=nome,
                    url=url_stream,
                    categoria=categoria
                )
                streams.append(stream)
        
        return streams


class ScraperPersonalizado:
    """Classe para adicionar scrapers personalizados"""
    
    @staticmethod
    def criar_streams_manuais() -> List[StreamInfo]:
        """Cria streams manualmente (exemplo para canais conhecidos)"""
        streams = []
        
        # Exemplo de canais abertos brasileiros (substitua por URLs reais)
        canais_abertos = [
            ("Globo", "http://example.com/globo.m3u8", "open"),
            ("SBT", "http://example.com/sbt.m3u8", "open"),
            ("Record", "http://example.com/record.m3u8", "open"),
            ("Band", "http://example.com/band.m3u8", "open"),
            ("RedeTV", "http://example.com/redetv.m3u8", "open"),
        ]
        
        for nome, url, categoria in canais_abertos:
            stream = StreamInfo(
                nome=nome,
                url=url,
                categoria=categoria,
                grupo="Canais Abertos"
            )
            streams.append(stream)
        
        return streams
    
    @staticmethod
    def criar_streams_de_arquivo(arquivo: str) -> List[StreamInfo]:
        """Carrega streams de um arquivo de texto"""
        streams = []
        
        try:
            with open(arquivo, 'r', encoding='utf-8') as f:
                linhas = f.readlines()
                
                for linha in linhas:
                    linha = linha.strip()
                    if not linha or linha.startswith('#'):
                        continue
                    
                    # Formato esperado: nome|url|categoria|grupo
                    partes = linha.split('|')
                    if len(partes) >= 2:
                        nome = partes[0]
                        url = partes[1]
                        categoria = partes[2] if len(partes) > 2 else "live"
                        grupo = partes[3] if len(partes) > 3 else ""
                        
                        stream = StreamInfo(
                            nome=nome,
                            url=url,
                            categoria=categoria,
                            grupo=grupo
                        )
                        streams.append(stream)
        except FileNotFoundError:
            print(f"Arquivo não encontrado: {arquivo}")
        
        return streams

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Módulo de scraping para diferentes fontes web
"""

import re
import requests
from typing import List, Optional
from gerador_m3u import StreamInfo, GeradorM3U


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


class ScraperM3UPublico(ScraperBase):
    """Scraper para listas M3U públicas"""
    
    def __init__(self):
        super().__init__()
        self.fontes_publicas = [
            "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/br.m3u",
            "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/us.m3u",
            "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/world.m3u",
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

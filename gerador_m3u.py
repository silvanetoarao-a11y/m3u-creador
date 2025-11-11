#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gerador de arquivos M3U a partir de fontes web
Suporta canais ao vivo, filmes, séries, canais adultos, abertos e privados
"""

import re
import requests
from typing import List, Dict, Optional
from urllib.parse import urlparse, quote
import time


class StreamInfo:
    """Classe para armazenar informações de um stream"""
    
    def __init__(self, nome: str, url: str, categoria: str, grupo: str = "", logo: str = ""):
        self.nome = nome
        self.url = url
        self.categoria = categoria  # live, movie, series, adult, open, private
        self.grupo = grupo
        self.logo = logo
    
    def __repr__(self):
        return f"StreamInfo(nome='{self.nome}', categoria='{self.categoria}')"


class GeradorM3U:
    """Classe principal para gerar arquivos M3U"""
    
    def __init__(self):
        self.streams: List[StreamInfo] = []
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    def adicionar_stream(self, stream: StreamInfo):
        """Adiciona um stream à lista"""
        self.streams.append(stream)
    
    def adicionar_streams(self, streams: List[StreamInfo]):
        """Adiciona múltiplos streams à lista"""
        self.streams.extend(streams)
    
    def gerar_m3u(self, arquivo_saida: str, filtro_categoria: Optional[str] = None):
        """
        Gera um arquivo M3U
        
        Args:
            arquivo_saida: Caminho do arquivo M3U a ser gerado
            filtro_categoria: Se especificado, filtra apenas streams desta categoria
        """
        streams_filtrados = self.streams
        if filtro_categoria:
            streams_filtrados = [s for s in self.streams if s.categoria == filtro_categoria]
        
        with open(arquivo_saida, 'w', encoding='utf-8') as f:
            f.write("#EXTM3U\n")
            
            for stream in streams_filtrados:
                # Linha EXTINF
                extinf = f'#EXTINF:-1'
                
                # Adiciona atributos opcionais
                if stream.grupo:
                    extinf += f' group-title="{stream.grupo}"'
                if stream.logo:
                    extinf += f' tvg-logo="{stream.logo}"'
                
                extinf += f',{stream.nome}\n'
                
                f.write(extinf)
                f.write(f"{stream.url}\n")
        
        print(f"✓ Arquivo M3U gerado: {arquivo_saida} ({len(streams_filtrados)} streams)")
    
    def gerar_m3u_por_categoria(self, diretorio_saida: str = "."):
        """Gera arquivos M3U separados por categoria"""
        categorias = set(s.categoria for s in self.streams)
        
        for categoria in categorias:
            arquivo = f"{diretorio_saida}/playlist_{categoria}.m3u"
            self.gerar_m3u(arquivo, filtro_categoria=categoria)
    
    def gerar_m3u_completo(self, arquivo_saida: str = "playlist_completa.m3u"):
        """Gera um arquivo M3U com todos os streams"""
        self.gerar_m3u(arquivo_saida)
    
    def validar_url(self, url: str) -> bool:
        """Valida se uma URL é válida"""
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except:
            return False
    
    def testar_stream(self, url: str, timeout: int = 5) -> bool:
        """Testa se um stream está acessível"""
        try:
            response = requests.head(url, headers=self.headers, timeout=timeout, allow_redirects=True)
            return response.status_code < 400
        except:
            return False

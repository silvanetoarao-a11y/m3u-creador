#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste Básico do Gerador M3U
Execute este script para verificar se tudo está funcionando
"""

import sys
import os

def teste_imports():
    """Testa se todas as bibliotecas necessárias estão instaladas"""
    print("=" * 60)
    print("TESTE 1: Verificando Imports")
    print("=" * 60)
    
    modulos = {
        'requests': 'requests',
        'beautifulsoup4': 'bs4',
        'lxml': 'lxml'
    }
    
    erros = []
    
    for nome_pacote, nome_import in modulos.items():
        try:
            __import__(nome_import)
            print(f"✓ {nome_pacote} instalado")
        except ImportError:
            print(f"✗ {nome_pacote} NÃO instalado")
            erros.append(nome_pacote)
    
    if erros:
        print(f"\nInstale os pacotes faltantes com:")
        print(f"pip install {' '.join(erros)}")
        return False
    
    print("\n✓ Todos os pacotes necessários estão instalados!\n")
    return True


def teste_classes():
    """Testa se as classes do programa funcionam"""
    print("=" * 60)
    print("TESTE 2: Testando Classes")
    print("=" * 60)
    
    try:
        from m3u_generator import Canal, M3UGenerator, WebScraper, FontesPreDefinidas
        print("✓ Todas as classes importadas com sucesso")
        
        # Testa criação de canal
        canal = Canal("Teste", "http://teste.com/stream.m3u8", "Teste")
        print(f"✓ Canal criado: {canal.nome}")
        
        # Testa gerador
        generator = M3UGenerator()
        generator.adicionar_canal(canal)
        print(f"✓ Canal adicionado ao gerador")
        
        # Testa scraper
        scraper = WebScraper()
        print(f"✓ WebScraper criado")
        
        # Testa fontes
        canais = FontesPreDefinidas.obter_canais_brasileiros_abertos()
        print(f"✓ Fontes pré-definidas: {len(canais)} canais")
        
        print("\n✓ Todas as classes funcionando corretamente!\n")
        return True
        
    except Exception as e:
        print(f"\n✗ Erro ao testar classes: {e}\n")
        return False


def teste_geracao_m3u():
    """Testa geração de arquivo M3U"""
    print("=" * 60)
    print("TESTE 3: Gerando Arquivo M3U de Teste")
    print("=" * 60)
    
    try:
        from m3u_generator import M3UGenerator, Canal
        
        generator = M3UGenerator()
        
        # Adiciona alguns canais de teste
        canais_teste = [
            Canal("Teste 1", "http://teste1.com/stream.m3u8", "Teste", "http://logo1.png", "Grupo1"),
            Canal("Teste 2", "http://teste2.com/stream.m3u8", "Teste", "http://logo2.png", "Grupo1"),
            Canal("Teste 3", "http://teste3.com/stream.m3u8", "Teste", "http://logo3.png", "Grupo2"),
        ]
        
        for canal in canais_teste:
            generator.adicionar_canal(canal)
        
        print(f"✓ {len(canais_teste)} canais adicionados")
        
        # Gera arquivo
        arquivo_teste = "teste_output.m3u"
        sucesso = generator.gerar_m3u(arquivo_teste)
        
        if sucesso and os.path.exists(arquivo_teste):
            print(f"✓ Arquivo gerado: {arquivo_teste}")
            
            # Verifica conteúdo
            with open(arquivo_teste, 'r', encoding='utf-8') as f:
                conteudo = f.read()
                if '#EXTM3U' in conteudo and 'Teste 1' in conteudo:
                    print("✓ Conteúdo do arquivo válido")
                else:
                    print("✗ Conteúdo do arquivo inválido")
                    return False
            
            # Remove arquivo de teste
            os.remove(arquivo_teste)
            print(f"✓ Arquivo de teste removido")
            
            print("\n✓ Geração de M3U funcionando corretamente!\n")
            return True
        else:
            print("✗ Erro ao gerar arquivo M3U")
            return False
            
    except Exception as e:
        print(f"\n✗ Erro ao gerar M3U: {e}\n")
        import traceback
        traceback.print_exc()
        return False


def teste_scraper():
    """Testa funcionalidades de scraping"""
    print("=" * 60)
    print("TESTE 4: Testando Web Scraper")
    print("=" * 60)
    
    try:
        from m3u_generator import WebScraper
        
        scraper = WebScraper()
        
        # HTML de teste
        html_teste = """
        <html>
            <body>
                <a href="http://exemplo.com/canal1.m3u8">Canal 1</a>
                <video src="http://exemplo.com/live/stream.m3u8"></video>
                <source src="http://exemplo.com/video/play.ts"></source>
            </body>
        </html>
        """
        
        streams = scraper.extrair_streams_genericos(html_teste, "http://exemplo.com")
        
        print(f"✓ Extração de streams testada")
        print(f"✓ Encontrados {len(streams)} streams no HTML de teste")
        
        if len(streams) > 0:
            print(f"✓ Exemplos: {streams[:2]}")
        
        print("\n✓ Web Scraper funcionando corretamente!\n")
        return True
        
    except Exception as e:
        print(f"\n✗ Erro ao testar scraper: {e}\n")
        return False


def teste_formato_m3u():
    """Testa se o formato M3U gerado está correto"""
    print("=" * 60)
    print("TESTE 5: Validando Formato M3U")
    print("=" * 60)
    
    try:
        from m3u_generator import Canal
        
        canal = Canal(
            nome="Globo HD",
            url="http://exemplo.com/globo.m3u8",
            categoria="TV Aberta",
            logo="http://exemplo.com/logos/globo.png",
            grupo="Brasil"
        )
        
        m3u_entry = canal.to_m3u_entry()
        
        # Verifica elementos obrigatórios
        checks = [
            ('#EXTINF', "Tag EXTINF presente"),
            ('tvg-id', "tvg-id presente"),
            ('tvg-logo', "tvg-logo presente"),
            ('group-title', "group-title presente"),
            ('Globo HD', "Nome do canal presente"),
            ('http://exemplo.com/globo.m3u8', "URL do stream presente"),
        ]
        
        todos_ok = True
        for check, descricao in checks:
            if check in m3u_entry:
                print(f"✓ {descricao}")
            else:
                print(f"✗ {descricao}")
                todos_ok = False
        
        if todos_ok:
            print("\n✓ Formato M3U válido!\n")
            print("Exemplo de saída:")
            print("-" * 60)
            print(m3u_entry)
            print("-" * 60)
            return True
        else:
            print("\n✗ Formato M3U inválido\n")
            return False
            
    except Exception as e:
        print(f"\n✗ Erro ao validar formato: {e}\n")
        return False


def executar_todos_testes():
    """Executa todos os testes"""
    print("\n")
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 10 + "TESTE DO GERADOR M3U" + " " * 28 + "║")
    print("╚" + "═" * 58 + "╝")
    print("\n")
    
    testes = [
        teste_imports,
        teste_classes,
        teste_geracao_m3u,
        teste_scraper,
        teste_formato_m3u
    ]
    
    resultados = []
    
    for teste in testes:
        try:
            resultado = teste()
            resultados.append((teste.__name__, resultado))
        except Exception as e:
            print(f"\n✗ ERRO CRÍTICO no {teste.__name__}: {e}\n")
            resultados.append((teste.__name__, False))
    
    # Resumo
    print("=" * 60)
    print("RESUMO DOS TESTES")
    print("=" * 60)
    
    for nome, resultado in resultados:
        status = "✓ PASSOU" if resultado else "✗ FALHOU"
        print(f"{status} - {nome}")
    
    total = len(resultados)
    passou = sum(1 for _, r in resultados if r)
    
    print("\n" + "=" * 60)
    print(f"RESULTADO FINAL: {passou}/{total} testes passaram")
    print("=" * 60)
    
    if passou == total:
        print("\n🎉 SUCESSO! Tudo está funcionando perfeitamente!")
        print("\nPróximos passos:")
        print("1. Execute: python m3u_generator.py")
        print("2. Ou teste: python exemplo_uso.py")
        print("3. Leia: README.md para mais informações")
        return True
    else:
        print("\n⚠️  ATENÇÃO! Alguns testes falharam.")
        print("\nVerifique:")
        print("1. Todas as dependências estão instaladas?")
        print("2. Os arquivos estão no diretório correto?")
        print("3. Há permissão de escrita no diretório?")
        return False


if __name__ == "__main__":
    sucesso = executar_todos_testes()
    sys.exit(0 if sucesso else 1)

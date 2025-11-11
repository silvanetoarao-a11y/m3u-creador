# Gerador de Arquivos M3U

Programa em Python para criar arquivos M3U (playlists de streaming) a partir de fontes web. Suporta canais ao vivo, filmes, séries, canais adultos, canais abertos e canais privados.

## Características

- ✅ Busca streams de fontes públicas M3U
- ✅ Scraping de sites web para encontrar streams
- ✅ Suporte para múltiplas categorias (live, movie, series, adult, open, private)
- ✅ Geração de arquivos M3U separados por categoria
- ✅ Validação de URLs
- ✅ Carregamento de streams de arquivos de texto
- ✅ Formato M3U padrão compatível com players IPTV

## Instalação

1. Clone ou baixe este repositório
2. Instale as dependências:

```bash
pip install -r requirements.txt
```

## Uso

### Uso Básico

Gerar um arquivo M3U completo usando fontes públicas:

```bash
python main.py --completo
```

### Filtrar por Categoria

Gerar arquivo apenas com canais ao vivo:

```bash
python main.py --categoria live --arquivo canais_live.m3u
```

Categorias disponíveis:
- `live` - Canais ao vivo
- `movie` - Filmes
- `series` - Séries
- `adult` - Canais adultos
- `open` - Canais abertos
- `private` - Canais privados

### Buscar de Fontes Públicas

```bash
python main.py --fonte-publica --categoria live
```

### Fazer Scraping de um Site

```bash
python main.py --url-site https://exemplo.com/streams --categoria live
```

### Carregar de Arquivo de Texto

Crie um arquivo de texto com o formato: `nome|url|categoria|grupo`

```bash
python main.py --arquivo-entrada streams.txt
```

Exemplo de arquivo `streams.txt`:
```
Globo|http://exemplo.com/globo.m3u8|live|Canais Abertos
SBT|http://exemplo.com/sbt.m3u8|live|Canais Abertos
Filme 1|http://exemplo.com/filme1.m3u8|movie|Filmes
```

### Gerar Arquivos Separados por Categoria

```bash
python main.py --separar
```

Isso criará arquivos como:
- `playlist_live.m3u`
- `playlist_movie.m3u`
- `playlist_series.m3u`
- etc.

### Validar URLs

Validar todas as URLs antes de adicionar ao M3U:

```bash
python main.py --fonte-publica --validar
```

## Estrutura do Projeto

```
.
├── main.py              # Programa principal
├── gerador_m3u.py      # Classe para gerar arquivos M3U
├── scrapers.py          # Módulos de scraping
├── requirements.txt     # Dependências Python
├── exemplo_streams.txt  # Exemplo de arquivo de entrada
└── README.md           # Este arquivo
```

## Formato M3U

O programa gera arquivos no formato M3U padrão:

```
#EXTM3U
#EXTINF:-1 group-title="Canais Abertos" tvg-logo="logo.png",Globo
http://exemplo.com/globo.m3u8
#EXTINF:-1 group-title="Canais Abertos",SBT
http://exemplo.com/sbt.m3u8
```

## Personalização

### Adicionar Novas Fontes

Edite `scrapers.py` e adicione novas URLs em `ScraperM3UPublico.fontes_publicas`:

```python
self.fontes_publicas = [
    "https://sua-fonte.com/playlist.m3u",
    # ... outras fontes
]
```

### Criar Scrapers Personalizados

Crie uma nova classe em `scrapers.py` herdando de `ScraperBase`:

```python
class MeuScraper(ScraperBase):
    def buscar_streams(self):
        # Sua lógica aqui
        pass
```

## Notas Importantes

⚠️ **Aviso Legal**: Este programa é apenas uma ferramenta técnica. Certifique-se de ter permissão para acessar e usar os streams. Respeite os direitos autorais e termos de serviço dos sites.

⚠️ **URLs de Exemplo**: As URLs nos exemplos são fictícias. Você precisará substituí-las por URLs reais de streams.

## Requisitos

- Python 3.7+
- requests
- beautifulsoup4 (para scraping avançado)
- lxml (parser HTML)

## Licença

Este projeto é fornecido como está, sem garantias.

## Contribuições

Sinta-se livre para adicionar novos scrapers, melhorar a detecção de streams ou adicionar novas funcionalidades!
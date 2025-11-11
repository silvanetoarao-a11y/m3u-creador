# Gerador de Playlists M3U 📺

Um programa completo em Python para criar arquivos M3U a partir de fontes web, suportando canais ao vivo, filmes, séries e canais adultos (tanto abertos quanto privados).

## 🌟 Características

- ✅ **Extração automática de streams** de páginas web
- ✅ **Suporte para múltiplas categorias**: TV aberta, notícias, esportes, filmes, séries, adultos
- ✅ **Geração de arquivos M3U** com metadados completos (logos, categorias, grupos)
- ✅ **Scrapers personalizáveis** com seletores CSS
- ✅ **Interface interativa** via linha de comando
- ✅ **Fontes pré-definidas** de canais brasileiros
- ✅ **Configuração via JSON** para personalização
- ✅ **Logging detalhado** de todas as operações

## 📋 Requisitos

- Python 3.7 ou superior
- Bibliotecas: requests, beautifulsoup4, lxml

## 🚀 Instalação

1. Clone ou baixe este repositório

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

## 💻 Uso Básico

### Modo Interativo

Execute o programa principal:

```bash
python m3u_generator.py
```

Você verá um menu com as seguintes opções:

```
1 - Criar playlist completa (todos os tipos)
2 - Criar playlist de canais abertos
3 - Criar playlist de filmes e séries
4 - Criar playlist com conteúdo adulto
5 - Extrair de URLs personalizadas
0 - Sair
```

### Uso Programático

```python
from m3u_generator import M3UGenerator, Canal

# Criar gerador
generator = M3UGenerator()

# Adicionar canais manualmente
canal = Canal(
    nome="Globo HD",
    url="http://exemplo.com/globo.m3u8",
    categoria="TV Aberta",
    logo="http://exemplo.com/logos/globo.png",
    grupo="Brasil"
)
generator.adicionar_canal(canal)

# Gerar arquivo M3U
generator.gerar_m3u("minha_playlist.m3u")
```

## 📚 Exemplos de Uso

Execute os exemplos pré-definidos:

```bash
python exemplo_uso.py
```

### Exemplo 1: Playlist Básica

```python
from m3u_generator import M3UGenerator, Canal

generator = M3UGenerator()

# Adicionar canais
canal1 = Canal("Globo", "http://exemplo.com/globo.m3u8", "TV Aberta")
canal2 = Canal("SBT", "http://exemplo.com/sbt.m3u8", "TV Aberta")

generator.adicionar_canal(canal1)
generator.adicionar_canal(canal2)

# Gerar arquivo
generator.gerar_m3u("basico.m3u")
```

### Exemplo 2: Usar Fontes Pré-definidas

```python
from m3u_generator import M3UGenerator, FontesPreDefinidas

generator = M3UGenerator()

# Adicionar canais abertos do Brasil
for canal in FontesPreDefinidas.obter_canais_brasileiros_abertos():
    generator.adicionar_canal(canal)

# Adicionar canais de esportes
for canal in FontesPreDefinidas.obter_canais_esportes():
    generator.adicionar_canal(canal)

generator.gerar_m3u("tv_brasileira.m3u")
```

### Exemplo 3: Extrair de URLs Web

```python
from m3u_generator import criar_playlist_personalizada

urls = [
    "https://exemplo.com/canais",
    "https://exemplo.com/filmes",
    "https://exemplo.com/series"
]

criar_playlist_personalizada(urls, "extraido_web.m3u")
```

### Exemplo 4: Scraping Personalizado

```python
from m3u_generator import WebScraper, M3UGenerator, Canal

scraper = WebScraper()
generator = M3UGenerator()

# Buscar página
html = scraper.buscar_pagina("https://exemplo.com/canais")

# Extrair streams
if html:
    streams = scraper.extrair_streams_genericos(html, "https://exemplo.com")
    
    # Adicionar à playlist
    for i, url in enumerate(streams):
        canal = Canal(f"Canal {i+1}", url, "Web")
        generator.adicionar_canal(canal)
    
    generator.gerar_m3u("scraping.m3u")
```

## ⚙️ Configuração

Edite o arquivo `config.json` para personalizar:

```json
{
  "fontes_web": {
    "exemplos": [
      "https://exemplo.com/canais"
    ]
  },
  
  "configuracoes": {
    "timeout_requisicao": 10,
    "delay_entre_requisicoes": 1
  },
  
  "filtros": {
    "incluir_adultos": false,
    "apenas_hd": false,
    "apenas_br": true,
    "idiomas": ["pt", "en", "es"]
  }
}
```

## 📂 Estrutura de Arquivos

```
.
├── m3u_generator.py      # Programa principal
├── exemplo_uso.py        # Exemplos de uso
├── config.json           # Arquivo de configuração
├── requirements.txt      # Dependências Python
└── README.md            # Este arquivo
```

## 🎯 Categorias Suportadas

O programa suporta as seguintes categorias:

- **TV Aberta**: Globo, SBT, Record, Band, RedeTV, etc.
- **Notícias**: GloboNews, CNN Brasil, BandNews, etc.
- **Esportes**: SporTV, ESPN, Fox Sports, etc.
- **Filmes**: Telecine, HBO, Cinemax, TNT, etc.
- **Séries**: Warner, Universal, AXN, Sony, etc.
- **Infantil**: Discovery Kids, Cartoon Network, Nickelodeon, etc.
- **Adultos (+18)**: Canais para adultos

## 🔧 Classes Principais

### Canal
Representa um canal ou stream individual com metadados:
- `nome`: Nome do canal
- `url`: URL do stream (M3U8, TS, MP4, etc.)
- `categoria`: Categoria do canal
- `logo`: URL do logotipo
- `grupo`: Grupo/categoria no player
- `idioma`: Idioma do canal

### M3UGenerator
Gerencia a criação de arquivos M3U:
- `adicionar_canal(canal)`: Adiciona um canal
- `gerar_m3u(arquivo)`: Gera o arquivo M3U
- `limpar_canais()`: Limpa a lista de canais

### WebScraper
Realiza scraping de páginas web:
- `buscar_pagina(url)`: Busca HTML de uma página
- `extrair_streams_genericos(html)`: Extrai URLs de streams
- `extrair_com_seletores(html, seletores)`: Extração customizada

### FontesPreDefinidas
Fornece listas de canais pré-configurados:
- `obter_canais_brasileiros_abertos()`
- `obter_canais_noticias()`
- `obter_canais_esportes()`
- `obter_canais_filmes()`
- `obter_canais_series()`
- `obter_canais_adultos()`

## 📝 Formato do Arquivo M3U

O arquivo gerado segue o padrão M3U Extended:

```
#EXTM3U

#EXTINF:-1 tvg-id="globo" tvg-logo="http://logo.png" group-title="Brasil",Globo HD
http://exemplo.com/globo.m3u8

#EXTINF:-1 tvg-id="sbt" tvg-logo="http://logo.png" group-title="Brasil",SBT HD
http://exemplo.com/sbt.m3u8
```

## 🌐 Fontes Web Recomendadas

### Repositórios GitHub com Playlists IPTV

- [iptv-org/iptv](https://github.com/iptv-org/iptv) - Coleção de canais públicos
- [Free-IPTV/Countries](https://github.com/Free-IPTV/Countries) - Canais por país

### Sites de Agregação

- **Nota**: Sempre verifique a legalidade e os termos de uso dos sites
- Use apenas fontes legais e públicas
- Respeite direitos autorais e licenças

## ⚠️ Avisos Importantes

1. **Legalidade**: Use apenas fontes legais e públicas. Não use para pirataria.
2. **Termos de Uso**: Respeite os termos de serviço dos sites.
3. **Direitos Autorais**: Não distribua conteúdo protegido sem autorização.
4. **Uso Responsável**: Não sobrecarregue servidores com requisições excessivas.
5. **Conteúdo Adulto**: O acesso a conteúdo adulto deve respeitar leis locais e ter +18 anos.

## 🔍 Extração de Streams

O programa busca automaticamente por:

- URLs terminando em `.m3u8`, `.ts`, `.mp4`, etc.
- Atributos `src` e `href` em tags HTML
- Padrões comuns de URLs de streaming
- Links contendo palavras-chave: "stream", "live", "channel", "video"

## 🛠️ Troubleshooting

### Erro ao instalar dependências
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Timeout ao buscar páginas
Aumente o timeout em `config.json`:
```json
"configuracoes": {
  "timeout_requisicao": 30
}
```

### Nenhum stream encontrado
- Verifique se a URL está correta
- Alguns sites podem bloquear scrapers
- Tente usar seletores CSS personalizados

## 📄 Licença

Este projeto é fornecido "como está" para fins educacionais. Use com responsabilidade.

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para:

- Reportar bugs
- Sugerir novas funcionalidades
- Adicionar novas fontes de canais
- Melhorar a documentação

## 📧 Suporte

Para dúvidas e suporte:

1. Consulte este README
2. Execute os exemplos em `exemplo_uso.py`
3. Verifique o arquivo `config.json`

## 🎓 Aprendizado

Este projeto demonstra:

- Web scraping com BeautifulSoup
- Expressões regulares para extração de dados
- Geração de arquivos de playlist M3U
- Programação orientada a objetos em Python
- Boas práticas de logging e tratamento de erros

---

**Desenvolvido para fins educacionais. Use com responsabilidade e legalidade.**

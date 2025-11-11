# Fontes Legais e Públicas de Streams 📡

Este documento lista fontes **legais e públicas** de onde você pode extrair streams para suas playlists M3U.

## ⚠️ Aviso Legal

- Use apenas fontes legais e autorizadas
- Respeite direitos autorais
- Não use para pirataria
- Verifique os termos de uso de cada fonte

## 🌐 Repositórios GitHub com IPTV Público

### 1. IPTV-Org
- **URL**: https://github.com/iptv-org/iptv
- **Descrição**: Coleção de mais de 80.000 canais públicos de IPTV de todo o mundo
- **Países**: +200 países
- **Categorias**: Notícias, esportes, entretenimento, etc.
- **Formato**: M3U8

```python
# Exemplo de uso
urls = [
    "https://iptv-org.github.io/iptv/countries/br.m3u",
    "https://iptv-org.github.io/iptv/categories/news.m3u",
    "https://iptv-org.github.io/iptv/categories/sports.m3u"
]
```

### 2. Free-IPTV
- **URL**: https://github.com/Free-IPTV/Countries
- **Descrição**: Canais gratuitos organizados por país
- **Atualização**: Regular
- **Foco**: Canais abertos e públicos

```python
urls = [
    "https://raw.githubusercontent.com/Free-IPTV/Countries/master/BR01_BRAZIL.m3u"
]
```

### 3. World IPTV
- **URL**: https://github.com/davidrios/iptv-brasil
- **Descrição**: Canais brasileiros
- **Tipo**: Canais abertos

## 📺 Canais Oficiais de TV Aberta Brasileira

### Globo
- **Site Oficial**: https://globoplay.globo.com/
- **Tipo**: Plataforma de streaming oficial
- **Conteúdo**: Canais ao vivo, novelas, filmes, séries

### SBT
- **Site Oficial**: https://www.sbt.com.br/
- **Tipo**: TV Aberta
- **Streaming**: https://www.sbt.com.br/ao-vivo

### Record TV
- **Site Oficial**: https://recordtv.r7.com/
- **PlayPlus**: https://www.playplus.com/
- **Tipo**: TV Aberta + Streaming

### Band
- **Site Oficial**: https://www.band.uol.com.br/
- **BandPlay**: https://www.band.uol.com.br/ao-vivo
- **Tipo**: TV Aberta

### RedeTV!
- **Site Oficial**: https://www.redetv.uol.com.br/
- **Ao Vivo**: https://www.redetv.uol.com.br/aovivo
- **Tipo**: TV Aberta

## 🎬 Plataformas de Streaming Legais e Gratuitas

### Pluto TV
- **URL**: https://pluto.tv/
- **Tipo**: Streaming gratuito com publicidade
- **Conteúdo**: Canais ao vivo + VOD
- **Disponível**: Brasil

### Samsung TV Plus
- **URL**: https://www.samsung.com/br/tvs/samsung-tv-plus/
- **Tipo**: Canais gratuitos
- **Plataforma**: Smart TVs Samsung

### Tubi
- **URL**: https://tubitv.com/
- **Tipo**: Filmes e séries gratuitas
- **Modelo**: Com publicidade

### YouTube Live
- **URL**: https://www.youtube.com/
- **Tipo**: Transmissões ao vivo
- **Conteúdo**: Variado (verifique licenças)

## 🎥 Vídeos e Filmes de Domínio Público

### Internet Archive
- **URL**: https://archive.org/
- **Tipo**: Arquivos públicos
- **Conteúdo**: Filmes, vídeos, áudio de domínio público

### Public Domain Movies
- **URL**: https://publicdomainmovies.net/
- **Tipo**: Filmes de domínio público
- **Licença**: Domínio público

## 📻 Rádios Online (Brasil)

### Radio Garden
- **URL**: http://radio.garden/
- **Tipo**: Rádios de todo o mundo
- **Brasil**: Centenas de estações

### TuneIn
- **URL**: https://tunein.com/
- **Tipo**: Rádios e podcasts
- **Conteúdo**: Legal e licenciado

## 🏀 Esportes

### Red Bull TV
- **URL**: https://www.redbull.com/br-pt/tv
- **Tipo**: Esportes radicais
- **Custo**: Gratuito

### Olympic Channel
- **URL**: https://olympics.com/pt/olympic-channel/
- **Tipo**: Esportes olímpicos
- **Conteúdo**: Gratuito

## 📰 Canais de Notícias com Stream Gratuito

### CNN Brasil (no YouTube)
- **URL**: https://www.youtube.com/@CNNBrasil
- **Tipo**: Notícias ao vivo

### BandNews FM
- **URL**: https://bandnewsfm.band.uol.com.br/
- **Tipo**: Rádio notícias

### GloboNews (site oficial)
- **URL**: https://g1.globo.com/
- **Tipo**: Notícias (alguns vídeos gratuitos)

## 🛠️ Como Usar no Programa

### Exemplo 1: Carregar playlist M3U existente

```python
import requests
from m3u_generator import M3UGenerator, Canal

# Baixar playlist M3U pública
url = "https://iptv-org.github.io/iptv/countries/br.m3u"
response = requests.get(url)

# Processar e filtrar canais
# (adicione lógica para parsear M3U)
```

### Exemplo 2: Usar APIs públicas

```python
# Muitos serviços têm APIs públicas
# Exemplo conceitual:

import requests
from m3u_generator import M3UGenerator, Canal

generator = M3UGenerator()

# Buscar canais de uma API pública
response = requests.get("https://api.exemplo.com/canais-publicos")
canais_data = response.json()

for canal_data in canais_data:
    canal = Canal(
        nome=canal_data['nome'],
        url=canal_data['stream_url'],
        categoria=canal_data['categoria']
    )
    generator.adicionar_canal(canal)

generator.gerar_m3u("api_publica.m3u")
```

## 🔍 Dicas de Busca

### Termos para buscar fontes legais:
- "free iptv github"
- "public domain streaming"
- "open source iptv"
- "legal streaming sources"
- "free tv channels m3u"
- "iptv brasil grátis legal"

### Sites que agregam conteúdo legal:
1. GitHub (repositórios de IPTV público)
2. Archive.org (domínio público)
3. Sites oficiais de emissoras
4. Plataformas de streaming gratuito

## ✅ Checklist de Legalidade

Antes de usar uma fonte, verifique:

- [ ] É um canal de TV aberta oficial?
- [ ] É uma plataforma de streaming legal?
- [ ] Tem licença Creative Commons ou domínio público?
- [ ] Está em um repositório GitHub confiável?
- [ ] Os termos de uso permitem redistribuição?
- [ ] Não está pirateando conteúdo pago?

## 🚫 O Que NÃO Fazer

❌ Não use streams piratas de canais pagos  
❌ Não redistribua conteúdo protegido por direitos autorais  
❌ Não ignore termos de serviço  
❌ Não sobrecarregue servidores com requisições  
❌ Não compartilhe credenciais de serviços pagos  

## 📚 Recursos Adicionais

### Documentação de Formatos

- **M3U/M3U8**: https://en.wikipedia.org/wiki/M3U
- **HLS Streaming**: https://developer.apple.com/streaming/
- **IPTV Standards**: https://www.iptv.org/

### Comunidades

- Reddit: r/IPTV (cuidado com conteúdo ilegal)
- GitHub: Busque "iptv" + "public" / "free" / "legal"

### Ferramentas Complementares

- **VLC Media Player**: Para testar streams M3U
- **Kodi**: Media center que suporta M3U
- **Perfect Player**: Player IPTV para Android

## 🔄 Atualização de Fontes

As fontes públicas mudam com frequência. Mantenha sua lista atualizada:

1. Verifique regularmente os repositórios GitHub
2. Teste periodicamente se os streams ainda funcionam
3. Remova streams que não funcionam mais
4. Adicione novas fontes conforme surgem

## 💡 Contribuindo

Conhece uma fonte legal não listada aqui? 

1. Verifique se é realmente legal
2. Teste se funciona
3. Documente a fonte
4. Compartilhe com a comunidade

---

**Lembre-se**: A legalidade varia por país. Sempre consulte as leis locais e os termos de uso específicos de cada serviço.

**Última atualização**: 2025-11-11

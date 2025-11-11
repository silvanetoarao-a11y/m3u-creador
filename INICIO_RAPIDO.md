# 🚀 Guia de Início Rápido

## Instalação em 3 Passos

### 1️⃣ Instalar Dependências

```bash
pip3 install -r requirements.txt
```

### 2️⃣ Testar Instalação

```bash
python3 teste_basico.py
```

Se ver "🎉 SUCESSO!", está tudo pronto!

### 3️⃣ Executar o Programa

```bash
python3 m3u_generator.py
```

## 📺 Uso Rápido

### Opção 1: Menu Interativo

Execute o programa e escolha uma opção:

```bash
python3 m3u_generator.py
```

Você verá:
```
1 - Criar playlist completa (todos os tipos)
2 - Criar playlist de canais abertos
3 - Criar playlist de filmes e séries
4 - Criar playlist com conteúdo adulto
5 - Extrair de URLs personalizadas
```

### Opção 2: Exemplos Prontos

Execute os exemplos:

```bash
python3 exemplo_uso.py
```

Escolha um dos 7 exemplos disponíveis!

### Opção 3: Código Python

Crie seu próprio script:

```python
from m3u_generator import M3UGenerator, Canal

# Criar gerador
gen = M3UGenerator()

# Adicionar canais
gen.adicionar_canal(Canal("Globo", "http://exemplo.com/globo.m3u8"))
gen.adicionar_canal(Canal("SBT", "http://exemplo.com/sbt.m3u8"))

# Gerar M3U
gen.gerar_m3u("minha_playlist.m3u")
```

## 📁 Arquivos Importantes

- `m3u_generator.py` - Programa principal
- `exemplo_uso.py` - 7 exemplos de uso
- `config.json` - Configurações
- `README.md` - Documentação completa
- `fontes_legais.md` - Fontes legais e públicas
- `teste_basico.py` - Teste de instalação

## 🎯 Casos de Uso

### Criar Playlist de TV Aberta

```python
from m3u_generator import M3UGenerator, FontesPreDefinidas

gen = M3UGenerator()
for canal in FontesPreDefinidas.obter_canais_brasileiros_abertos():
    gen.adicionar_canal(canal)
gen.gerar_m3u("tv_aberta.m3u")
```

### Extrair de Sites

```python
from m3u_generator import criar_playlist_personalizada

urls = [
    "https://github.com/iptv-org/iptv",
    "sua-url-aqui.com"
]

criar_playlist_personalizada(urls, "extraido.m3u")
```

### Playlist Completa

```python
from m3u_generator import criar_playlist_completa

criar_playlist_completa()
# Gera: playlist_completa.m3u
```

## 🔧 Personalização

Edite `config.json` para:

- Adicionar suas fontes web
- Configurar timeouts
- Definir filtros
- Customizar categorias

## 📖 Documentação Completa

Para mais detalhes, consulte:

- `README.md` - Documentação completa
- `fontes_legais.md` - Fontes legais para usar
- Comentários no código

## ⚠️ Importante

- Use apenas fontes **legais e públicas**
- Respeite direitos autorais
- Leia os termos de uso dos sites
- Não use para pirataria

## 💡 Dicas

1. **Teste primeiro**: Execute `teste_basico.py` antes de usar
2. **Fontes legais**: Consulte `fontes_legais.md`
3. **Exemplos**: Use `exemplo_uso.py` para aprender
4. **Configuração**: Customize em `config.json`

## 🆘 Problemas Comuns

### Módulos não encontrados
```bash
pip3 install -r requirements.txt
```

### Timeout ao buscar páginas
Aumente em `config.json`:
```json
"timeout_requisicao": 30
```

### Nenhum stream encontrado
- Verifique se a URL está correta
- Alguns sites bloqueiam scrapers
- Tente URLs de repositórios GitHub

## 🎓 Próximos Passos

1. ✅ Execute `teste_basico.py`
2. ✅ Rode `exemplo_uso.py`
3. ✅ Leia `README.md`
4. ✅ Consulte `fontes_legais.md`
5. ✅ Personalize `config.json`
6. ✅ Crie suas próprias playlists!

## 📞 Mais Informações

- Leia o `README.md` completo
- Execute os exemplos
- Experimente diferentes configurações

---

**Pronto para começar! 🎉**

Execute `python3 m3u_generator.py` agora!

# bling_api

Cliente Python para integração com a API v3 da Bling, com suporte a token OAuth e uso dos pacotes externos `requests_policy` e `bling_utils`.

## Instalação (Git)

```bash
pip install git+https://github.com/<usuario>/<repositorio>.git
```

Exemplo de uso após instalar:

```python
from bling_api.bling import BlingApi

api = BlingApi()
```

## Setup rápido

1. Instale as dependências do projeto.
2. Instale os pacotes `requests_policy` e `bling_utils` via URLs Git oficiais.
3. Crie seu arquivo local de ambiente:

- copie `.env.example` para `.env`

4. Preencha as variáveis necessárias (principalmente `BLING_AUTHORIZATION_CODE` quando for gerar novo token).
5. Garanta que os arquivos de token existam em `bling_api/src/tokens/`.

### Instalação do requests_policy

Use o gerenciador de pacotes Python do seu ambiente (exemplo com `pip`):

```bash
pip install "git+https://github.com/GabMalta/requests_policy"
```

Esse mesmo endereço também está configurado como dependência no `pyproject.toml`.

### Instalação do bling_utils

Use o gerenciador de pacotes Python do seu ambiente (exemplo com `pip`):

```bash
pip install "git+https://github.com/GabMalta/bling_utils"
```

Esse mesmo endereço também está configurado como dependência no `pyproject.toml`.

## Variáveis de ambiente

### OAuth Bling

- `BLING_AUTHORIZATION_CODE`
  - Código de autorização usado como primeira opção no fluxo de geração de access token.
  - Se não estiver definido, o sistema tenta fallback para `settings.AUTHORIZATION_CODE` e depois `input()`.

As variáveis de configuração do `requests_policy` agora são definidas e documentadas no próprio pacote.

## Compatibilidade

A classe `BlingApi` mantém o comportamento de atualização de token no `__init__` para compatibilidade.

## Verificação básica

Use para checagem de sintaxe:

```bash
python -m py_compile bling_api/bling.py
```

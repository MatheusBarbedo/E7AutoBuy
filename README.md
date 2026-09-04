# E7AutoBuy (adaptado para MuMu Player Nx)

Bot de auto-compra da Secret Shop do Epic Seven, baseado no
[E7AutoBuy original](https://github.com/senkkou/E7AutoBuy), com correções
para funcionar no **MuMu Player Nx** (que usa múltiplos displays virtuais).

## Como rodar

1. Abra o MuMu com o Epic Seven **em inglês**, na tela da **Secret Shop**.
2. Duplo-clique em `AutoBuy.bat` (ou rode `python autobuy_fixed.py`).
3. Informe o número de refreshes e confirme.

O script detecta sozinho o device e o display do E7 a cada execução.

## Correções em relação ao original (`autobuy_fixed.py`)

O MuMu Nx expõe 3 displays virtuais (launcher + apps), o que quebrava o
bot de três formas — todas corrigidas:

1. **Screenshot corrompido** — o `screencap` vinha com um aviso de
   "multiple displays" antes do PNG. Agora o código corta tudo antes do
   cabeçalho `\x89PNG`.
2. **Cliques iam para a home** — os toques eram enviados ao display padrão
   (launcher). Agora usa `input -d <id_lógico>` no display do E7.
3. **Swipe não funcionava** — sintaxe corrigida para `input -d <id> swipe`.

Também fixa um único device automaticamente (evita o erro
"more than one device/emulator").

## Requisitos

- Python 3 com `pytesseract` e `Pillow`
- `platform-tools` (adb) e `tesseract` — inclusos nesta pasta
- Resolução do emulador em 16:9 (ex.: 1920x1080)

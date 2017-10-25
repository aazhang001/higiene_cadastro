Rotinas para limpar cadastros, ou seja, tornar descrições mais legiveis, remover erros (TODO), etc

## Installation
TODO: Describe the installation process

## Usage

```
import base

pecas = ['001022','000119']

for i in pecas:
    descricao = base.pegar_descricao(i)
    t = descricao[0]
    print('CODIGO DA PEÇA...:',i)
    print('DESCRIÇÃO ATUAL..:',t[0])

    corrigido = base.verifica_ortografia(t[0])
    trocada = base.verifica_descricao(corrigido)

    if trocada != corrigido:
        corrigido = trocada

    print('DESCRIÇÃO CORRETA:',corrigido)
    print()
```

## SAÍDA DOS COMANDOS

```
CODIGO DA PEÇA...: 001022
DESCRIÇÃO ATUAL..: CRUZETA COLUNA DIRECAO
DESCRIÇÃO CORRETA: CRUZETA COLUNA DIREÇÃO

CODIGO DA PEÇA...: 000119
DESCRIÇÃO ATUAL..: JUNTA TAMPA CX. DIRECAO
DESCRIÇÃO CORRETA: JUNTA TAMPA CAIXA DIREÇÃO
```

## Contributing
1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request :D
## History
TODO: Write history
## Credits
TODO: Write credits
## License
TODO: Write license
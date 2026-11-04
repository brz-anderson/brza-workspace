---
scope:
  - workspace
  - brza-studio
refs:
  - PLN-003
---

# O PLN-003 P3: o repositório público brz-anderson/brza e empacotamento (pipx, brew)

Na sessão `tools-kit` de 2026-11-03, em continuidade ao [PLN-003: O workflow do workspace roda igual no BrzA Studio e no Orca, por plugins e pelo `brza`](../../plans/PLN-003-o-workflow-nos-dois-clients/PLN-003-plan.md),
executou-se o passo **P3** (D1 / B4): a criação e estruturação do repositório público `brz-anderson/brza`, configuração do empacotamento Python stdlib via `pyproject.toml` (backend `flit_core`), template da fórmula Homebrew (`Formula/brza.rb`) para o tap `brz-anderson/homebrew-tap` e validação completa de instalação em ambiente virtual limpo.

## O que se implementou e testou

1. **Repositório Público e Estrutura:**
   - Criado e inicializado o repositório público [brz-anderson/brza](https://github.com/brz-anderson/brza) localmente e no GitHub.
   - Configurado `pyproject.toml` usando padrão PEP 517/621 com backend `flit_core >=3.2,<4` (zero dependências de compilação, Python stdlib puro).
   - Definidos os entrypoints de script do pacote:
     - `brza = "brza.cli:main"`
     - `brza-tree = "brza.tree:main"`
     - `brza-test = "brza.test_cmd:main"`
     - `brza-app = "brza.app:main"`
   - Adicionados `README.md`, `LICENSE` (MIT) e `.gitignore`.

2. **Módulos do Pacote Python (`brza/`):**
   - `brza/__init__.py`: versão `0.1.0`.
   - `brza/cli.py`: despachador universal hierárquico com subcomandos embutidos, executáveis locais/PATH e fallback para os clients `BrzA Studio` e `Orca`.
   - `brza/runtime.py`: camada leve de operações git e runtime do studio.
   - `brza/tree.py`: gerenciamento universal de worktrees.
   - `brza/test_cmd.py`: detector e executor de testes em repositórios gerais e Studio.
   - `brza/app.py`: instalador do BrzA Studio via release GitHub e `--from-source`.

3. **Template da Fórmula Homebrew:**
   - Criado `Formula/brza.rb` estruturado para o tap `brz-anderson/homebrew-tap` utilizando `Language::Python::Virtualenv` e `virtualenv_install_with_resources`.

4. **Validação e Testes:**
   - Suíte de testes unitários dedicada em `tests/test_cli.py` (11 testes, 100% OK em 0.06s).
   - Instalação e teste de fumaça em ambiente virtual limpo (`/tmp/brza-clean-env`):
     - `pip install -e /Users/andepb/Projects/brza` concluído com sucesso total.
     - Execução e conferência dos binários no PATH do ambiente:
       - `brza --version` → `brza 0.1.0`
       - `brza --help` → lista de subcomandos e ajuda
       - `brza-tree --help`, `brza-test --help`, `brza-app --help` operacionais.

5. **Publicação:**
   - Commit inicial `c1e4796` (`feat: inicializa repositório público brz-anderson/brza com CLI unificada e packaging (PLN-003/P3)`).
   - Repositório público criado e sincronizado na branch `master` de `git@personal:brz-anderson/brza.git`.

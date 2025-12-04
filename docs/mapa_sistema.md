---

## 2. Arquitetura de infraestrutura (estilo cloud)

```mermaid
flowchart LR

    %% Camada Cliente
    subgraph UserLayer["Camada Cliente"]
        client[👤 Navegador / Mobile do cliente]
    end

    %% Domínio / Rede
    subgraph EdgeLayer["Domínio e rede"]
        dns[🌐 DNS / urbanrock.com.br]
    end

    %% Camada Web
    subgraph WebLayer["Camada Web"]
        nginx[Nginx - proxy reverso]
    end

    %% Camada de Aplicação
    subgraph AppLayer["App Django"]
        django[Gunicorn + Django]
        cart[Serviços: catálogo, carrinho, checkout, pedidos]
        admin[Admin / painel interno]
    end

    %% Dados
    subgraph DataLayer["Dados"]
        db[(Banco de dados)]
        media[(Storage de mídia / imagens)]
    end

    %% Dev / CI / Deploy
    subgraph DevOpsLayer["Dev / CI / Deploy"]
        devpc[💻 Dev local]
        repo[GitHub - urbanrock]
        deploy[Script de deploy / SSH]
        server[Servidor produção / Droplet]
    end

    %% Fluxo principal do usuário
    client --> dns --> nginx --> django
    django --> cart
    django --> admin

    %% Acesso a dados
    django --> db
    django --> media

    %% Infraestrutura / deploy
    devpc --> repo --> deploy --> server
    server --> nginx
    server -. hospeda .- django
    server -. hospeda .- db
    server -. hospeda .- media

    %% Estilos (cores)
    classDef userLayer fill:#e3f2fd,stroke:#1e88e5,color:#0d47a1;
    classDef edgeLayer fill:#fff3e0,stroke:#fb8c00,color:#e65100;
    classDef webLayer fill:#ede7f6,stroke:#5e35b1,color:#311b92;
    classDef appLayer fill:#e8f5e9,stroke:#43a047,color:#1b5e20;
    classDef dataLayer fill:#fce4ec,stroke:#c2185b,color:#880e4f;
    classDef devopsLayer fill:#eceff1,stroke:#546e7a,color:#
> **Cuidado na hora de colar:**  
> tem que ficar exatamente assim: bloco ```mermaid``` dentro do `.md`, sem espaços extras antes/depois.

---

## 2. O que esse diagrama mostra

- **UserLayer**  
  Cliente acessando via navegador ou celular.

- **EdgeLayer**  
  Seu domínio `urbanrock.com.br` / DNS apontando pro servidor.

- **WebLayer**  
  Nginx recebendo as requisições HTTP e repassando pro Django (proxy reverso).

- **AppLayer**  
  Gunicorn + Django rodando:
  - catálogo, carrinho, checkout, pedidos  
  - admin/painel interno

- **DataLayer**  
  Banco (Postgres/SQLite/etc.) e storage de imagens (pasta `media` ou serviço externo, se um dia usar).

- **DevOpsLayer**  
  Sua rotina de desenvolvimento:
  - Dev local → GitHub  
  - Deploy via SSH/script para o servidor  
  - Servidor hospeda Nginx, Django, banco, arquivos.

Fica **bem no padrão de arquitetura que se vê em docs de AWS/GCP**: camadas, cores, setas claras e agrupamentos por responsabilidade.

---

Se quiser, depois a gente faz:

- uma **versão reduzida** desse mesmo diagrama pro `README.md`,  
ou  
- um **PDF/PNG** dessa arquitetura pra você mandar em apresentação, orçamento, ou até em currículo.

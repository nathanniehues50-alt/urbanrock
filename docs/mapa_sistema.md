## 2. Arquitetura de infraestrutura (estilo cloud)

```mermaid
flowchart LR

    %% Camada Cliente
    subgraph UserLayer[Camada Cliente]
        client[Navegador ou mobile]
    end

    %% Dominio / DNS
    subgraph EdgeLayer[Dominio e Rede]
        dns[DNS urbanrock.com.br]
    end

    %% Web
    subgraph WebLayer[Camada Web]
        nginx[Nginx Proxy Reverso]
    end

    %% App
    subgraph AppLayer[Aplicacao Django]
        django[Django + Gunicorn]
        services[Catalogo / Carrinho / Checkout / Pedidos]
        adminpanel[Painel Admin]
    end

    %% Dados
    subgraph DataLayer[Camada de Dados]
        db[(Banco de dados)]
        media[(Arquivos de midia)]
    end

    %% DevOps
    subgraph DevOpsLayer[DevOps e Deploy]
        devpc[Dev local]
        repo[Repositorio GitHub]
        deploy[Deploy via SSH]
        server[Servidor Producao]
    end

    %% Fluxo do usuario
    client --> dns --> nginx --> django
    django --> services
    django --> adminpanel

    %% Dados
    django --> db
    django --> media

    %% DevOps
    devpc --> repo --> deploy --> server
    server --> nginx
    server --> django
    server --> db
    server --> media

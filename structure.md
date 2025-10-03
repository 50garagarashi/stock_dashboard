
```mermaid
flowchart LR
  %% ===== Users & Identity =====
  U[Users]
  AAD[Azure Entra ID]
  U -->|Sign-in| AAD

  %% ===== Edge <Public> =====
  F[Azure Front Door Premium WAF]
  U --> F

  %% ===== Azure <Private> =====
  subgraph AZURE [Azure]
    direction LR

    subgraph VNET [VNet]
      direction LR

      ACA[Azure Container Apps Internal Ingress]
      DB[<Azure Database for MySQL Flexible Server>]
      PE[<Private Endpoint for MySQL>]
      PDNS[<Private DNS Zone>]
      KV[Key Vault]
      ACR[Azure Container Registry]
      AI[Application Insights]
      LA[Log Analytics]

      %% App ↔ DB <Private>
      ACA --> DB
      DB --- PE
      PE -.DNS.- PDNS

      %% App ↔ Others
      ACA --> KV
      ACA --> ACR
      ACA --> AI
      AI -.Telemetry.- LA
    end
  end

  %% ===== Edge ↔ Private <Private Link> =====
  F -- Private Link --> ACA

  %% ===== Logging at Edge =====
  WAFLOGS[WAF Access Logs]
  F --> WAFLOGS --> LA


```
---

```mermaid
flowchart TD

%% ===== External access and auth =====
U[Users <Company accounts>]
NET[Public Internet]
IPF[IP allowlist <office CIDR>]
AAD[Microsoft Entra ID <auth>]

U -->|HTTPS| NET --> IPF --> AAD

%% ===== Azure Container Apps <external ingress> =====
APP[ACA App: stock-dashboard-app\nExternal ingress :443 -> :8080]
AAD -->|OIDC tokens| APP
IPF -->|allowed only| APP

%% ===== ACA environment in VNet =====
subgraph VNET[Azure VNet <Japan East>]
  direction TB
  SNET[snet-aca <delegated: Microsoft.App/environments>]
  ENV[Container Apps Environment: env-nct-prod]
end
APP --- ENV
ENV --- SNET

%% ===== Images & identity =====
ACR[<Azure Container Registry\nIgarashiContainerResistry>]
MI[<System-assigned managed identity>]
MI -. AcrPull role .-> ACR
ACR -->|pull image| APP

%% ===== Observability =====
LA[<Log Analytics Workspace\nlaw-nct-prod>]
APP -->|logs / metrics| LA

%% ===== Future <optional> =====
subgraph FUTURE[Future hardening]
  direction TB
  DB[<Azure Database for MySQL Flexible Server>]
  PE[<Private Endpoint>]
  PDNS[<Private DNS Zone>]
  KV[<Key Vault>]
  AGW[<Application Gateway WAF v2>]
end
APP -. private access .-> DB
DB -. link .-> PE
PE -. name resolution .-> PDNS
KV -. certs / secrets .-> APP
AGW -. front with WAF .-> APP


```
---

```mermaid
flowchart TD
  %% Entry and identity
  U[Employees using Entra ID] -->|HTTPS TLS 1.2 plus| AS[Azure App Service for Containers]
  CA[Entra ID Conditional Access MFA device compliance location] --> AS

  %% App layer hardening
  AR[App Service Access Restrictions IP allowlist] --- AS
  MI[System Assigned Managed Identity] --- AS

  %% Secrets
  KV[Azure Key Vault secrets connection strings] <-->|get list via Managed Identity| AS

  %% Monitoring
  AI[Application Insights and Log Analytics] <-->|telemetry and logs| AS

  %% Network and data
  subgraph VNet Azure virtual network
    VI[VNet Integration from App Service]
    PEP[Private Endpoint to MySQL Flexible Server]
    PDNS[Private DNS Zone privatelink mysql database azure com]
  end
  AS --> VI
  VI --> PEP
  PDNS --- PEP

  DB[Azure Database for MySQL Flexible Server private only] --- PEP

  %% Domain and cert
  DNS[Custom domain and free certificate on App Service] --- AS
```


---
```mermaid
flowchart TD
  %% Entry and identity
  U[Employees using Entra ID] -->|HTTPS TLS 1.2 plus| AS[Azure App Service for Containers]
  CA[Entra ID Conditional Access MFA device compliance location] --> AS

  %% App layer hardening
  AR[App Service Access Restrictions IP allowlist] --- AS
  MI[System Assigned Managed Identity] --- AS

  %% Secrets
  KV[Azure Key Vault secrets connection strings] <-->|get list via Managed Identity| AS

  %% Monitoring
  AI[Application Insights and Log Analytics] <-->|telemetry and logs| AS

  %% Network and data
  subgraph VNet Azure virtual network
    VI[VNet Integration from App Service]
    PEP[Private Endpoint to MySQL Flexible Server]
    PDNS[Private DNS Zone privatelink mysql database azure com]
  end
  AS --> VI
  VI --> PEP
  PDNS --- PEP

  DB[Azure Database for MySQL Flexible Server private only] --- PEP

  %% Domain and cert
  DNS[Custom domain and free certificate on App Service] --- AS

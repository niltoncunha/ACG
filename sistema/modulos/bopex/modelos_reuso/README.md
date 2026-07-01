# BOPEX · Modelos de Reuso

Pasta para modelos visuais reutilizáveis do BOPEX.

## Objetivo

Separar padrões gráficos reutilizáveis dos módulos Mxx específicos.

## Contrato

Cada modelo deve ser pequeno, estável e reaproveitável por múltiplos módulos.

## Estrutura

```text
sistema/modulos/bopex/modelos_reuso/
├── README.md
├── barra-metrica-stack.html
└── barra-metrica-stack.js
```

## Modelo inicial

### barra-metrica-stack

Inspirado no anexo de barras empilhadas com linha de referência central.

Representa:

- colunas temporais ou discretas
- segmentos positivos/negativos
- linha de setpoint
- intensidade por cor
- variação por eixo
- leitura operacional clean para painéis BOPEX

Uso previsto:

- HOMEOVEC
- LOOM
- GAUNTLET
- runtime de métricas persistentes
- painéis de pressão/intensão/consumo/universal/tempo

# Alicação Microsserviços Java - Springboot e Python - FastApi

## Passos para Inicialização
Abra o terminal do seu sistema operativo e navegue até a pasta raiz do projeto (onde o arquivo docker-compose.yml está localizado)

Execute o comando abaixo para compilar os códigos fonte, construir as imagens Docker correspondentes e subir toda a rede de infraestrutura:
`docker compose up --build`

## Testando o Fluxo de Ponta a Ponta
Para simular o funcionamento real do ecossistema e verificar as validações automáticas que o microsserviço central realiza através da rede interna do Docker, siga o roteiro abaixo:

### 1. Verificar os Dados Pré-carregados (Mockups)
As APIs em Python já sobem com registros de teste em memória (id=1). Pode validá-los acedendo aos seguintes endpoints no seu navegador ou ferramenta de teste:

- Cliente ID 1: GET `http://localhost:8004/clientes/1`

- Restaurante ID 1: GET `http://localhost:8003/restaurantes/1`

- Produto ID 1: GET `http://localhost:8002/produtos/1`

### 2. Submeter um Novo Pedido
Envie uma requisição POST para o serviço central Java para criar um pedido contendo referências aos microsserviços Python:

URL: `http://localhost:8080/pedidos`

Headers: Content-Type: `application/json`

Corpo da requisição:
```
{
  "idRestaurante": 1,
  "idCliente": 1,
  "dsDescricao": "Pedido de teste para a entrega do trabalho",
  "itens": [
    {
      "idProduto": 1,
      "cdQuantidade": 3
    }
  ]
}
```
### 3. Comportamento Esperado da Aplicação

O pedido-service recebe o JSON.

Efetua uma chamada de rede interna para `http://cliente-service:8000/clientes/1` para garantir a existência do cliente.

Efetua uma chamada de rede interna para `http://restaurante-service:8000/restaurantes/1` para validar o restaurante.

Consulta `http://produto-service:8000/produtos/1` para extrair o valor unitário atualizado (vlProduto = 35.0).

Calcula internamente o valor do subtotal e o total global do pedido (3 * 35.0 = 105.0).

Carrega de forma dinâmica a data atual e grava todas as informações de maneira persistente nas `tabelas tb_pedido` e `tbitem_pedido_produto` do PostgreSQL.

Retorna o objeto completo salvo com o status `HTTP 200 OK`.

Integrantes do Grupo:

- Clara dos Santos Becker

- Lucas Gabriel Falcade Nunes

# Arquivos

É necessário que os arquivos do processo de população e ETl estejam na mesma pasta pois ambos leem do arquivo `renda_fixa`.

(É possível separa-los, mas por conveniência, foi deixado assim).

## Fill

Aqui está o código python para gerar os arquivos SQL para popular as tabelas Clientes e Operações no banco de dados CTVM.

Há também o arquivo `clientes.txt` e `renda_fixa.txt`, que é de onde o código irá pegar os nomes dos clientes e os tipos de investimentos de renda fixa válidos.

OBS: Para gerar uma população maior, o código atual cria um novo cliente para cada nome e sobrenome. 

## ETL

O arquivo ktr do Pentaho realiza todas as operações de ETL: Extract (from CTVM), Transform & Load (To Data Warehouse).
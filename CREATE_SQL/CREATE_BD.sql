DROP DATABASE IF EXISTS CTVM;
CREATE DATABASE CTVM;
USE CTVM;

DROP TABLE IF EXISTS CLIENTES;
CREATE TABLE CLIENTES(
	ID INT AUTO_INCREMENT PRIMARY KEY,
    CPF VARCHAR(15) UNIQUE NOT NULL,
	NOME VARCHAR(30) NOT NULL,
	PERFIL ENUM('CONSERVADOR', 'MODERADO', 'ARROJADO', 'AGRESSIVO')
);

DROP TABLE IF EXISTS OPERACOES;
CREATE TABLE OPERACOES(
	ID INT AUTO_INCREMENT PRIMARY KEY,
    COD_INV VARCHAR(20) NOT NULL,
    CLIENTE_ID INT NOT NULL,
	OP ENUM('DEPOSITO', 'SAQUE', 'COMPRA', 'VENDA', 'DIVIDENDOS') NOT NULL,
    VALOR FLOAT NOT NULL,
    VALOR_INICIAL FLOAT NOT NULL,
    DATA_OP DATE NOT NULL
);

ALTER TABLE OPERACOES
ADD CONSTRAINT FK_CLIENTE
FOREIGN KEY (CLIENTE_ID) REFERENCES CLIENTES(ID) ON UPDATE CASCADE ON DELETE CASCADE;

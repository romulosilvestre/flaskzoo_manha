create database zooflask;
use zooflask;
create table animal(
  id int primary key auto_increment,
  nome_popular varchar(80) NOT NULL,
  nome_cientifico varchar(60) NOT NULL,
  habitos_noturnos LONGTEXT NOT NULL
)

-- Continuando a aula 
CREATE table avaliacao(
   id int primary key auto_increment,
   avaliacao text not null,
   polaridade float not null
);
select * from avaliacao;
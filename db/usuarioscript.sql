use fmp_db;

insert into usuario (nome, sobrenome, email, data_nasc, sexo, senha)
	values ('LUCAS','ASTUR','lucas.astur.96@gmail.com','1996-05-12','Masculino','pbkdf2:sha256:50000$UxCdbBgj$075d9682f5bdcf6bd536cbf8b85275d03a30afcc12c20715da2f5a1b047db3d5');

insert into loja (nome, endereco, telefone, email, senha)
	values ('Bar do Tomas','al. barros, 122, ap 121','12345678','lucas.astur.96@gmail.com','pbkdf2:sha256:50000$UxCdbBgj$075d9682f5bdcf6bd536cbf8b85275d03a30afcc12c20715da2f5a1b047db3d5');

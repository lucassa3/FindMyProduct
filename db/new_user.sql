CREATE USER 'fmp_user'@'localhost' IDENTIFIED BY '123456';
GRANT INSERT,SELECT,UPDATE,DELETE ON fmp_db.categoria TO 'fmp_user'@'localhost';
GRANT INSERT,SELECT,UPDATE,DELETE ON fmp_db.compra TO 'fmp_user'@'localhost';
GRANT INSERT,SELECT,UPDATE,DELETE ON fmp_db.loja TO 'fmp_user'@'localhost';
GRANT INSERT,SELECT,UPDATE,DELETE ON fmp_db.produto TO 'fmp_user'@'localhost';
GRANT INSERT,SELECT,UPDATE,DELETE ON fmp_db.usuario TO 'fmp_user'@'localhost';
FLUSH PRIVILEGES;
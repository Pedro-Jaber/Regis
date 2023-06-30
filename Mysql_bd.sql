create database bd_regisBAN;
use bd_regisBAN;

create table tb_banho
(
num_banho int auto_increment primary key,
tmp_banho time not null,
dt_banho date not null
);

select * from tb_banho;

# Insert =================================================================

DELIMITER $$
create procedure insert_tb_banho(in vtmp_banho time, vdt_banho date)
BEGIN
insert into tb_banho
(tmp_banho,dt_banho)
values
(vtmp_banho,vdt_banho);
END $$
DELIMITER ;


# Select =================================================================

DELIMITER $$
create procedure select_tb_banho()
BEGIN
select num_banho as "Numero", tmp_banho as "Tempo", dt_banho as "Data" 
from tb_banho;
END $$
DELIMITER ;

DELIMITER $$
create procedure select_sep_tb_banho()
BEGIN
select num_banho as "Numero",
       minute(tmp_banho) "Minutos",
       second(tmp_banho) "Segundo",
       day(dt_banho) "Dia",
       month(dt_banho) "Mes",
       year(dt_banho) "Ano"
from tb_banho;
END $$
DELIMITER ;

DELIMITER $$
create procedure select_10_tb_banho()
BEGIN
select  
	num_banho "Numero", 
	min "Minutos", 
	sec "Segundos", 
	dia "Dia", 
	mes "Mes", 
	ano "Ano"
from (
select 
	num_banho, 
	minute(tmp_banho) as min, 
	second(tmp_banho) as sec, 
	day(dt_banho) as dia, 
	month(dt_banho) as mes, 
	year(dt_banho) as ano
from tb_banho
order by num_banho DESC
limit 10) as aux
order by num_banho;
END $$
DELIMITER ;

DELIMITER $$
create procedure select_100_tb_banho()
BEGIN
select  
	num_banho "Numero", 
	min "Minutos", 
	sec "Segundos", 
	dia "Dia", 
	mes "Mes", 
	ano "Ano"
from (
select 
	num_banho, 
	minute(tmp_banho) as min, 
	second(tmp_banho) as sec, 
	day(dt_banho) as dia, 
	month(dt_banho) as mes, 
	year(dt_banho) as ano
from tb_banho
order by num_banho DESC
limit 100) as aux
order by num_banho;
END $$
DELIMITER ;


DELIMITER $$
create procedure select_last_tb_banho()
BEGIN
select 
	num_banho "Numero", 
	minute(tmp_banho) "Minutos", 
	second(tmp_banho) "Segundos", 
	day(dt_banho) "Dia", 
	month(dt_banho) "Mes", 
	year(dt_banho) "Ano"
from tb_banho
order by num_banho DESC
limit 1;
END $$
DELIMITER ;


# Update =================================================================

DELIMITER $$
create procedure update_data_tb_banho(in v_dt_banho date, v_num_banho int)
BEGIN
update tb_banho
set dt_banho = v_dt_banho
where num_banho = v_num_banho;
END $$
DELIMITER ;

DELIMITER $$
create procedure update_tempo_tb_banho(in v_tmp_banho time, v_num_banho int)
BEGIN
update tb_banho
set tmp_banho = v_tmp_banho
where num_banho = v_num_banho;
END $$
DELIMITER ;


# Delete =================================================================

DELIMITER $$
create procedure delete_tb_banho(in vnum_banho int)
BEGIN

delete from tb_banho
where num_banho = vnum_banho;

END $$
DELIMITER ;



select * from tb_banho;



# Insert =================================================================

call insert_tb_banho('0:01:01','2001-01-01');
insert into tb_banho
(num_banho, tmp_banho, dt_banho)
values
(7,'0:09:35','2022-06-25');


# Select =================================================================

select count(*) from tb_banho;
call select_tb_banho();
call select_avg_tb_banho();
call select_last_tb_banho();
call select_10_tb_banho();
call select_100_tb_banho();


# Update =================================================================

call update_tempo_tb_banho('',3);
call update_data_tb_banho('2022-15delete_tb_banhodelete_tb_banho-23',3);


# Delete =================================================================

call delete_tb_banho(45);
-- Deletar tudo
-- delete from tb_banho where num_banho > 0;

alter table tb_banho auto_increment = 32;

use bd_regisban_test;




select sec_to_time(avg(time_to_sec(tmp_banho))) from (
select tmp_banho from tb_banho order by num_banho DESC limit 14
) as sub;



-- tb_banho;

-- from tb_banho
-- order by num_banho DESC
-- limit 10;














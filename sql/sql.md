
## 数据结构
```整数: 2^8 TINYINT = 2^16 SMALLINT = 2^24 MEDIUMINT = 2^32 INTEGER = 2^64 BIGINT ```
```小数: 4 FLOAT = 8 DOUBLE ```
```长文本: 2^8 TINYTEXT  =   2^24 MEDIUMTEXT = 2^16 TEXT = 2^32 LONGTEXT  ```
```二进制: 2^8 TINYBLOB  =  2^24 MEDIUMBLOB = 2^16 BLOB = 2^32 LONGBLOB  ```

对比参考 相同则不冗述

数据结构 | 编码 | 大小 | 范围/格式/函数 | 编码 | 大小 | 范围/格式/函数 
---|---|---|---|---|---|---
mysql | mysql | mysql | oracle | oracle | oracle 
整数值 | INTEGER(INT) | 4 | (-2^31, 2^31) | INTEGER | - |   (-2^31, 2^31) <br> NUMBER(P,0)
浮点数 | FLOAT| 4 | (-3.xE+38，-1.xE-38) | FLOAT | - | 2^126 <br> trunc(1.5) round(1.23456, 4) <br> floor(1.5) ceil(1.5)
小数值 | DECIMAL(M,D) |M>D?M+2:D+2 | convert('1.2', unsigned integer) | NUMBER(4,2) |   | 4位(含2位小数) <br> to_number('1.2')  
日期值 | DATE | 3 | YYYY-MM-DD | 
时间值或持续时间 | TIME | 3 | HH:MM:SS | 
年份值 | YEAR | 1 | YYYY | 
日期+时间 | DATETIME | 8 | YYYY-MM-DD HH:MM:SS | DATE | 4 |  YYYY-MM-DD HH:MM:SS | 
时间戳  | TIMESTAMP | 4 | YYYY-MM-DD HH:MM:SS | TIMESTAMP | 4 | YYYY-MM-DD HH:MM:SS:xxxx <br> 纳秒 <br><br> 转字符串: <br> to_char(sysdate - 2 * interval '7' day, 'yyyy-mm-dd hh24:mi:ss') <br> year/month/day/hour/minute/ <br><br> 转时间 <br> to_date('1000-12-12','yyyy-mm-dd hh24:mi:ss')
定长字符 | CHAR(128) | 2^8 | - | CHAR(128) | 2^8 |  -
变长字符 | VARCHAR(9998) | 2^32 | 变长 <br> 截取ello: <br> substr('hello world',2<, 4>) <br>  <br> 查找序: <br>  instr('A-B','-',-1, 1)  |  VARCHAR2(4000) | 4000 | 同 <br> 等价分离: <br> substr('A-B',1,instr('A-B','-',-1, 1)-1)
二进制 | BLOB | 2^16 | - |  RAW | 4G? | - 
长文本 | TEXT | 2^16 | 不能有default  | CLOB| *4G |-|
三目运算|1 > 0 ? 1 : 0| - | if(1 > 0, 1, 0) | - | - | (case when 1>0 then 1 when 1<0 then 0 else 2 end)
null判断| 1==null ? 1 : 0 | - |  ifnull(1, 0) | - | - | nvl(1, 0) <br> nvl2(1, 1, 0)
补齐位| -- | - |  --| - | - | lpad('2', 4, '0')
聚合 | list.stream().map(item->name) | - |  --| - | - | wm_concat(name)
 
## 建表
```
查询创建
create table Student select * from StudentCp;
```
## 函数调用
select if(1 > 0, 'a', 'b') name from dual; 
 

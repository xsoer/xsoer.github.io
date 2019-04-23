# Impala操作手册

- 作者：codehackfox@gmail.com
- 时间：2019-04-22 20:08:24
- 状态：pending
- 标签：数据库 大数据存储

[TOC]

> ### 简介

* 支持的查询存储
    * 关系型数据库
    * 数据仓库
    * Kudu
    * Hive
    * Hbase
    * HDFS
* 可以单独部署一个集群，读取远程数据源。
* 支持的操作
    * 运行impala-shell进入交互模式
        * `/usr/bin/impala-shell`
    * ODBC、JDBC
    * Hue web-based user interface.

> ### 数据表

* 分为外部表和内部表
* 内部表
    * 通过impala创建的表都是内部表(internal)
    * 修改表结构对应的底层表也会进行变动
* 外部表
    * 不同过impala创建的表都是外部表(external)
    * 要操作这些表，需要在impala建立表的映射关系
    * 通过sql修改表结构或者删除表不会删除底层表，删除的只是表的映射关系


> ### SQL语法

- sql示例
```sql

-- This line is a comment about a table.
create table ...;
/*
This is a multi-line comment about a query.
*/
select ...;

select * from t /* This is an embedded comment about a query. */ where ...;

select * from t -- This is a trailing comment within a multi-line command.
where ...;
```

* 外部表映射
```sql
CREATE EXTERNAL TABLE my_mapping_table
STORED AS KUDU
TBLPROPERTIES (
  'kudu.table_name' = 'my_kudu_table'
);
```

* 创建内部表
```sql
CREATE TABLE my_first_table
(
  id BIGINT,
  name STRING,
  PRIMARY KEY(id)
)
PARTITION BY HASH PARTITIONS 16
STORED AS KUDU;
```

* 用select来建表
```sql
CREATE TABLE new_table
PRIMARY KEY (ts, name)
PARTITION BY HASH(name) PARTITIONS 8
STORED AS KUDU
AS SELECT ts, name, value FROM old_table;
```

* 复杂点的partition
```sql
CREATE TABLE cust_behavior (
  id BIGINT,
  sku STRING,
  salary STRING,
  edu_level INT,
  usergender STRING,
  `group` STRING,
  city STRING,
  postcode STRING,
  last_purchase_price FLOAT,
  last_purchase_date BIGINT,
  category STRING,
  rating INT,
  fulfilled_date BIGINT,
  PRIMARY KEY (id, sku)
)
PARTITION BY HASH (id) PARTITIONS 4,
RANGE (sku)
(
  PARTITION VALUES < 'g',
  PARTITION 'g' <= VALUES < 'o',
  PARTITION 'o' <= VALUES < 'u',
  PARTITION 'u' <= VALUES
)
STORED AS KUDU;
```

* 多个hash分区
```sql
CREATE TABLE cust_behavior (
  id BIGINT,
  sku STRING,
  salary STRING,
  edu_level INT,
  usergender STRING,
  `group` STRING,
  city STRING,
  postcode STRING,
  last_purchase_price FLOAT,
  last_purchase_date BIGINT,
  category STRING,
  rating INT,
  fulfilled_date BIGINT,
  PRIMARY KEY (id, sku)
)
PARTITION BY HASH (id) PARTITIONS 4,
             HASH (sku) PARTITIONS 4
STORED AS KUDU;
```

* 多个range分区
```sql
CREATE TABLE sales_by_year (
  year INT, sale_id INT, amount INT,
  PRIMARY KEY (sale_id, year)
)
PARTITION BY RANGE (year) (
  PARTITION VALUE = 2012,
  PARTITION VALUE = 2013,
  PARTITION VALUE = 2014,
  PARTITION VALUE = 2015,
  PARTITION VALUE = 2016
)
STORED AS KUDU;
```

* 添加ragne分区
```sql
ALTER TABLE sales_by_year ADD RANGE PARTITION VALUE = 2017;
```

* 删除一个range分区
```sql
ALTER TABLE sales_by_year DROP RANGE PARTITION VALUE = 2012;
```

* 操作元
    * Arithmetic Operators
    * BETWEEN Operator
    * Comparison Operators
    * EXISTS Operator
    * ILIKE Operator
    * IN Operator
    * IREGEXP Operator
    * IS DISTINCT FROM Operator
    * IS NULL Operator
    * IS TRUE Operator
    * LIKE Operator
    * Logical Operators
    * REGEXP Operator
    * RLIKE Operator

> ### 数据类型

- ARRAY Complex Type (CDH 5.5 or higher only)
- BIGINT
- BOOLEAN
- CHAR
- DECIMAL
- DOUBLE
- FLOAT
- INT
- MAP Complex Type (CDH 5.5 or higher only)
- REAL
- SMALLINT
- STRING
- STRUCT Complex Type (CDH 5.5 or higher only)
- TIMESTAMP
- TINYINT
- VARCHAR
- Complex Types (CDH 5.5 or higher only)
- `PS:注意`
    -  Currently, the data types CHAR, VARCHAR, ARRAY, MAP, and STRUCT cannot be used with Kudu tables.



> ### SQL Statements

* DDL Statements
* DML Statements
* ALTER DATABASE
* ALTER TABLE
* ALTER VIEW
* COMMENT
* COMPUTE STATS
* CREATE DATABASE
* CREATE FUNCTION
* CREATE ROLE
* CREATE TABLE
* CREATE VIEW
* DELETE
* DESCRIBE
* DROP DATABASE
* DROP FUNCTION
* DROP ROLE
* DROP STATS
* DROP TABLE
* DROP VIEW
* EXPLAIN
* GRANT
* INSERT
    * VALUES Clause
    * Inserting Into Partitioned Tables with PARTITION Clause
        * Static Partition Inserts
        * Dynamic Partition Inserts
* INVALIDATE METADATA
* LOAD DATA
* REFRESH
* REFRESH AUTHORIZATION
* REFRESH FUNCTIONS
* REVOKE
* SELECT
    * Joins
    * ORDER BY Clause
    * GROUP BY Clause
    * HAVING Clause
    * LIMIT Clause
    * OFFSET Clause
    * UNION Clause
    * Subqueries
    * TABLESAMPLE Clause
    * WITH Clause
    * DISTINCT Operator
* SET
    * ABORT_ON_ERROR
    * ALLOW_ERASURE_CODED_FILES
    * ALLOW_UNSUPPORTED_FORMATS
    * APPX_COUNT_DISTINCT
    * BATCH_SIZE
    * BUFFER_POOL_LIMIT
    * COMPRESSION_CODEC
    * COMPUTE_STATS_MIN_SAMPLE_SIZE
    * DEBUG_ACTION
    * DECIMAL_V2
    * DEFAULT_FILE_FORMAT
    * DEFAULT_JOIN_DISTRIBUTION_MODE
    * DEFAULT_SPILLABLE_BUFFER_SIZE
    * DISABLE_CODEGEN
    * DISABLE_CODEGEN_ROWS_THRESHOLD
    * DISABLE_ROW_RUNTIME_FILTERING
    * DISABLE_STREAMING_PREAGGREGATIONS
    * DISABLE_UNSAFE_SPILLS
    * ENABLE_EXPR_REWRITES
    * EXEC_SINGLE_NODE_ROWS_THRESHOLD
    * EXEC_TIME_LIMIT_S
    * EXPLAIN_LEVEL
    * HBASE_CACHE_BLOCKS
    * HBASE_CACHING
    * IDLE_SESSION_TIMEOUT
    * KUDU_READ_MODE
    * LIVE_PROGRESS
    * LIVE_SUMMARY
    * MAX_ERRORS
    * MAX_MEM_ESTIMATE_FOR_ADMISSION
    * MAX_NUM_RUNTIME_FILTERS
    * MAX_ROW_SIZE
    * MAX_SCAN_RANGE_LENGTH
    * MEM_LIMIT
    * MIN_SPILLABLE_BUFFER_SIZE
    * MT_DOP
    * NUM_NODES
    * NUM_ROWS_PRODUCED_LIMIT
    * NUM_SCANNER_THREADS
    * OPTIMIZE_PARTITION_KEY_SCANS
    * PARQUET_COMPRESSION_CODEC
    * PARQUET_ANNOTATE_STRINGS_UTF8
    * PARQUET_ARRAY_RESOLUTION
    * PARQUET_DICTIONARY_FILTERING
    * PARQUET_FALLBACK_SCHEMA_RESOLUTION
    * PARQUET_FILE_SIZE
    * PARQUET_READ_STATISTICS
    * PREFETCH_MODE
    * QUERY_TIMEOUT_S
    * REPLICA_PREFERENCE
    * REQUEST_POOL
    * RESOURCE_TRACE_RATIO
    * RUNTIME_BLOOM_FILTER_SIZE
    * RUNTIME_FILTER_MAX_SIZE
    * RUNTIME_FILTER_MIN_SIZE
    * RUNTIME_FILTER_MODE
    * RUNTIME_FILTER_WAIT_TIME_MS
    * S3_SKIP_INSERT_STAGING
    * SCAN_BYTES_LIMIT
    * SCHEDULE_RANDOM_REPLICA
    * SCRATCH_LIMIT
    * SHUFFLE_DISTINCT_EXPRS
    * SUPPORT_START_OVER
    * SYNC_DDL
    * THREAD_RESERVATION_AGGREGATE_LIMIT
    * THREAD_RESERVATION_LIMIT
    * TIMEZONE
    * TOPN_BYTES_LIMIT
* SHOW
    * SHOW FILES Statement
    * SHOW ROLES Statement
    * SHOW CURRENT ROLE
    * SHOW ROLE GRANT Statement
    * SHOW GRANT ROLE Statement
    * SHOW GRANT USER Statement
    * SHOW DATABASES
    * SHOW TABLES Statement
    * SHOW CREATE TABLE Statement
    * SHOW CREATE VIEW Statement
    * SHOW TABLE STATS Statement
    * SHOW COLUMN STATS Statement
    * SHOW PARTITIONS Statement
    * SHOW FUNCTIONS Statement
* SHUTDOWN
* TRUNCATE TABLE
* UPDATE
* UPSERT
* USE
* Optimizer Hints


> ### 内建函数

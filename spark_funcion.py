from pyspark.sql import SparkSession

# Khởi tạo SparkSession
spark = SparkSession.builder \
    .appName("SQLite with PySpark") \
    .config("spark.jars", "instance/sqlite-jdbc-3.43.0.0.jar") \
    .getOrCreate()

# Kết nối tới SQLite và đọc bảng Application
def read_sqlite_data(db_path, table_name):
# Đọc dữ liệu từ SQLite
    df = spark.read.format("jdbc") \
        .option("url", f"jdbc:sqlite:{db_path}") \
        .option("dbtable", table_name) \
        .option("driver", "org.sqlite.JDBC") \
        .load()
    return df

# Tính tỉ lệ khách hàng bị default
def get_default_rate(application_df):
    application_df.createOrReplaceTempView("Application")
    result = spark.sql("""
        SELECT result, COUNT(*) AS count, 
               ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS percentage
        FROM Application
        GROUP BY result
    """)
    return result.collect()

# Phân nhóm khách hàng theo độ tuổi
def get_age_group_distribution(application_df):
    application_df.createOrReplaceTempView("Application")
    result = spark.sql("""
        SELECT 
            CASE 
                WHEN age <= 20 THEN '0-20'
                WHEN age <= 40 THEN '21-40'
                WHEN age <= 60 THEN '41-60'
                WHEN age <= 80 THEN '61-80'
                ELSE '81+' 
            END AS age_group,
            COUNT(*) AS count
        FROM Application
        GROUP BY age_group
        ORDER BY age_group
    """)
    return result.collect()

def get_income_group_distribution(application_df):
    application_df.createOrReplaceTempView("Application")
    result = spark.sql("""
        SELECT 
            CASE 
                WHEN income <= 10 THEN '0-10'
                WHEN income <= 40 THEN '11-40'
                WHEN income <= 60 THEN '41-60'
                WHEN income <= 80 THEN '61-80'
                WHEN income <= 99 THEN '81-99'
                ELSE '100+' 
            END AS income_group,
            COUNT(*) AS count
        FROM Application
        GROUP BY income_group
        ORDER BY income_group
    """)
    return result.collect()

def get_debtinc_group_distribution(application_df):
    application_df.createOrReplaceTempView("Application")
    result = spark.sql("""
        SELECT 
            CASE 
                WHEN debtinc <= 10 THEN '0-10'
                WHEN debtinc <= 40 THEN '11-40'
                WHEN debtinc <= 60 THEN '41-60'
                WHEN debtinc <= 80 THEN '61-80'
                WHEN debtinc <= 99 THEN '81-99'
                ELSE '100+' 
            END AS debtinc_group,
            COUNT(*) AS count
        FROM Application
        GROUP BY debtinc_group
        ORDER BY debtinc_group
    """)
    return result.collect()

# Tính tổng số khách hàng
def get_total_applications(application_df):
    application_df.createOrReplaceTempView("Application")
    result = spark.sql("SELECT COUNT(*) AS total FROM Application")
    return result.collect()[0]["total"]

# Hàm tổng hợp dữ liệu phân tích
def get_analytics_data(db_path, table_name):
    application_df = read_sqlite_data(db_path, table_name)
    
    # Tính tỉ lệ default
    default_rate = get_default_rate(application_df)
    
    # Phân nhóm tuổi
    age_group = get_age_group_distribution(application_df)

    # Phân nhóm doanh thu
    income_group = get_income_group_distribution(application_df)
    
    # Phân nhóm khoản nợ
    debtinc_group = get_debtinc_group_distribution(application_df)
    
    # Tổng số khách hàng
    total_applications = get_total_applications(application_df)

    # Trả về kết quả dưới dạng dictionary
    return {
        "default_rate": [row.asDict() for row in default_rate],
        "age_group": [row.asDict() for row in age_group],
        "income_group": [row.asDict() for row in income_group],
        "debtinc_group": [row.asDict() for row in debtinc_group],
        "total_applications": total_applications
    }

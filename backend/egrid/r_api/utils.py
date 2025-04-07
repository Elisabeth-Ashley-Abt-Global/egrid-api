
def update_from_temp_table(table, df, unique_field):
    import pandas as pd

    if df.empty:
        raise ValueError("DataFrame is empty")

    temp_table = f"{table}_temp"
    row = df.iloc[0]
    
    # Columns to update: everything except join keys
    join_keys = [unique_field, "year"]
    update_cols = [col for col in df.columns if col not in join_keys]

    if not update_cols:
        raise ValueError("No columns to update")

    set_clause = ", ".join([
        f"{col} = {temp_table}.{col}" for col in update_cols
    ])

    where_clause = f"""
        {table}.{unique_field} = {temp_table}.{unique_field} AND
        {table}.year = {temp_table}.year
    """

    sql = f"""
        UPDATE {table}
        SET {set_clause}
        FROM {temp_table}
        WHERE {where_clause}
    """
    # print('sql to execute: ')

    print(sql.strip())  # For debugging only

    return(sql)

def build_insert_from_temp_sql(table, df):
    if df.empty:
        raise ValueError("DataFrame is empty")

    temp_table = f"{table}_temp"
    columns = list(df.columns)

    if not columns:
        raise ValueError("No columns to insert")

    col_list = ", ".join(columns)
    sql = f"""
        INSERT INTO {table} ({col_list})
        SELECT {col_list}
        FROM {temp_table};
    """
    return sql 
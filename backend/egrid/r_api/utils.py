
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


def record_insert_update(table, df, unique_field):
    if df.empty:
        raise ValueError("DataFrame is empty")

    temp_table = f"{table}_temp"
    columns = list(df.columns)

    if not columns:
        raise ValueError("No columns to insert")

    # Composite conflict key: unique field + year
    conflict_columns = [unique_field, "year"]
    # if unique_field is a list, unlist it 
    conflict_columns_new = []
    for element in conflict_columns:
        if type(element) is list:
            # Check if type is list than iterate through the sublist
            for item in element:
                conflict_columns_new.append(item)
        else:
            conflict_columns_new.append(element)
    conflict_clause = ", ".join(conflict_columns_new)
    col_list = ", ".join(columns)

    # Exclude conflict keys from update columns
    update_cols = [col for col in columns if col not in conflict_columns]

    if not update_cols:
        raise ValueError("No updatable columns (all are conflict keys)")

    update_set = ", ".join([
        f"{col} = EXCLUDED.{col}" for col in update_cols
    ])

    sql = f"""
        INSERT INTO {table} ({col_list})
        SELECT {col_list}
        FROM {temp_table}
        ON CONFLICT ({conflict_clause}) DO UPDATE
        SET {update_set};
    """
 
    return sql

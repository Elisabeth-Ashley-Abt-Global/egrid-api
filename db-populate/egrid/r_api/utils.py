
def record_insert_update(table, df, unique_field):
    if df.empty:
        raise ValueError("DataFrame is empty")

    temp_table = f"{table}_temp"
    columns = list(df.columns)

    if not columns:
        raise ValueError("No columns to insert")

    # Composite conflict key: unique field + year
    conflict_columns = [unique_field, "year"]
    conflict_clause = ", ".join(conflict_columns)
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

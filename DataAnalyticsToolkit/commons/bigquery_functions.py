from google.cloud import bigquery
from google.api_core.exceptions import NotFound, BadRequest


def big_query_insert(project_id, dataset_id, table_id, rows):
    """Inserts a list of new rows in a BigQuery table.

    :param project_id: BigQuery Project Id
    :param dataset_id: BigQuery Dataset Id
    :param table_id: BigQuery Table Id
    :param rows: List of tuples, each tuple is a new row to be inserted
    :return: Dictionary with error False, exception error text, or BigQuery error object.
    """
    try:
        client = bigquery.Client()
        table = client.get_table(f"{project_id}.{dataset_id}.{table_id}")
        errors = client.insert_rows(table, rows)
        if not errors:
            return {"error": False}
        else:
            return {"error": errors}
    except (NotFound, BadRequest) as exception:
        return {"error": f"{exception.errors[0]['message']}"}
    except (ValueError, IndexError) as exception:
        return {"error": exception}


def big_query_execute_dml(statement):
    try:
        client = bigquery.Client()
        query_job = client.query(statement)
        query_job.result()
        return {"error": False}
    except (NotFound, BadRequest) as exception:
        return {"error": f"{exception.errors[0]['message']}"}


def get_dataset_tables(dataset):
    client = bigquery.Client()
    return [table.table_id for table in client.list_tables(dataset)]


def get_datasets():
    """List al the BigQuery project datasets

    :return: List, containing the datasets ids
    """
    client = bigquery.Client()
    return [dataset.dataset_id for dataset in client.list_datasets()]


def dry_run(query):
    """Executes a BigQuery Dry-Run and returns the estimated bytes processed

    :param query: String with the query or sql script to check
    :return: Bytes processed by the query or query error description
    """

    try:

        client = bigquery.Client()
        job_config = bigquery.QueryJobConfig(dry_run=True, use_query_cache=False)
        query_job = client.query(query, job_config=job_config)

        return {"error": False, "bytes": query_job.total_bytes_processed}

    except (NotFound, BadRequest) as exception:
        return {"error": f"{exception.errors[0]['message']}\nIn query:\n{exception.query_job.query}"}

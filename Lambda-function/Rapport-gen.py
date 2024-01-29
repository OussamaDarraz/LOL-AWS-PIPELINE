import boto3
import csv
import io
import time


athena_database = 'loldata'
athena_output_bucket = 'aws-lol-project'
athena_output_folder = 'Test-rapport'
view1_name = 'view_champion_attack_winrate'
view2_name = 'view_champion_matches_difficulty'

def lambda_handler(event, context):

    query_execution_id1 = execute_athena_query(f"SELECT * FROM {view1_name};")
    wait_for_query_completion(query_execution_id1)
    query_execution_id2 = execute_athena_query(f"SELECT * FROM {view2_name};")
    wait_for_query_completion(query_execution_id2)

    # Download and process query results
    result1 = download_query_result(query_execution_id1)
    result2 = download_query_result(query_execution_id2)

    # Generate HTML report
    html_report = convert_to_html(result1) + '<br><br>' + convert_to_html(result2)

    # Store the report in S3
    store_report_in_s3(html_report)

def execute_athena_query(query):
    client = boto3.client('athena')
    response = client.start_query_execution(
        QueryString=query,
        QueryExecutionContext={'Database': athena_database},
        ResultConfiguration={'OutputLocation': f's3://{athena_output_bucket}/{athena_output_folder}'}
    )
    return response['QueryExecutionId']

def wait_for_query_completion(query_execution_id):
    client = boto3.client('athena')

    while True:
        response = client.get_query_execution(QueryExecutionId=query_execution_id)
        status = response['QueryExecution']['Status']['State']

        if status in ['SUCCEEDED', 'FAILED', 'CANCELLED']:
            break
        else:
            time.sleep(5)  # Wait for 5 seconds before checking again

def download_query_result(query_execution_id):
    s3_client = boto3.client('s3')
    key = f'{athena_output_folder}/{query_execution_id}.csv'
    response = s3_client.get_object(Bucket=athena_output_bucket, Key=key)
    content = response['Body'].read().decode('utf-8')
    reader = csv.reader(io.StringIO(content))
    return list(reader)

def convert_to_html(data):
    html = '<table><tr>{}</tr>'.format(''.join(['<th>{}</th>'.format(header) for header in data[0]]))
    for row in data[1:]:
        html += '<tr>{}</tr>'.format(''.join(['<td>{}</td>'.format(cell) for cell in row]))
    html += '</table>'
    return html

def store_report_in_s3(html_report):
    s3_client = boto3.client('s3')
    s3_key = f'{athena_output_folder}/report.html'
    s3_client.put_object(Bucket=athena_output_bucket, Key=s3_key, Body=html_report, ContentType='text/html')
    print(f'Report generated and stored in S3: s3://{athena_output_bucket}/{s3_key}')


import boto3

def create_dynamodb_table():
    dynamodb = boto3.resource(
        'dynamodb',
        endpoint_url='http://localhost:8000',  # Local DynamoDB
        region_name='us-west-2'
    )

    table = dynamodb.create_table(
        TableName='Board',
        KeySchema=[
            {'AttributeName': 'id', 'KeyType': 'HASH'},
        ],
        AttributeDefinitions=[
            {'AttributeName': 'id', 'AttributeType': 'S'},
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5,
        }
    )

    print(f"Table status: {table.table_status}")

if __name__ == "__main__":
    create_dynamodb_table()


import boto3
def gerar_bitolas():
    print("Gerando bitolas...")


    return


def insert_into_dynamodb(table_name, item):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    table.put_item(Item=item)

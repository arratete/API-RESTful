import os
import json

from todos import decimalencoder
import boto3

_dynamodb = boto3.resource('dynamodb')
_translate = boto3.client('translate')

def translate(event, context):
    
   table = _dynamodb.Table(os.environ['DYNAMODB_TABLE'])

   # fetch todo from the database
   result = table.get_item(
       Key={
           'id': event['pathParameters']['id']
       }
   )
   
   # translate text      
   try:
        translated = _translate.translate_text(
           Text = result['Item']['text'],
           SourceLanguageCode = "auto",
           TargetLanguageCode = event['pathParameters']['lang']
           )
           
        #translatedInfo = {
        #   'Id': event['pathParameters']['id'],
        #   'Text': result['Item']['text'],
        #   'TranslatedText': str(translated.get('TranslatedText')),
        #   'SourceLanguageCode': str(translated.get('SourceLanguageCode')),
        #   'Targ#}
        
   except Exception as e:
       raise Exception("Exception: " + str(e))
   
   # create a response
   response = {
       "statusCode": 200,
       "body": json.dumps(translated)
   }

   return response
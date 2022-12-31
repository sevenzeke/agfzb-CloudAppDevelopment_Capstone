from ibmcloudant.cloudant_v1 import CloudantV1, Document
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

def main(dict):
    api_key = '5WUNPZBjs84te6oUX0v4HpYOA1fE_qGGbPltrwouY8hk'
    api_url = 'https://51d008c1-5757-4d25-a4a7-208e2742931e-bluemix.cloudantnosqldb.appdomain.cloud'
    db_name = 'reviews'
    authenticator = IAMAuthenticator(api_key)
    service = CloudantV1(authenticator=authenticator)
    service.set_service_url(api_url)
    newreview = dict["review"]
    newreview = Document(
        name=newreview['name'],
        dealership=int(newreview['dealership']),
        review=newreview['review'],
        purchase=newreview['purchase'],
        another=newreview['another'],
        purchase_date=newreview['purchase_date'],
        car_make=newreview['car_make'],
        car_model=newreview['car_model'],
        car_year=int(newreview['car_year']))
    response = service.post_document(
        db=db_name,
        document=newreview).get_result()
    try:
        code = 200
        if response['ok'] is False:
            code = 404
        return {'statusCode': code,
                'headers': { 'Content-Type': 'application/json' },
                'body': response}
    except:
        return {'statusCode': 500,
                'headers': { 'Content-Type': 'application/json' },
                'body': {}}
from ibmcloudant.cloudant_v1 import CloudantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

def main(dict):
    api_key = '5WUNPZBjs84te6oUX0v4HpYOA1fE_qGGbPltrwouY8hk'
    api_url = 'https://51d008c1-5757-4d25-a4a7-208e2742931e-bluemix.cloudantnosqldb.appdomain.cloud'
    db_name = 'reviews'
    authenticator = IAMAuthenticator(api_key)
    service = CloudantV1(authenticator=authenticator)
    service.set_service_url(api_url)
    try:
        response = service.post_find(
            db=db_name,
            selector={'dealership': {'$eq': int(dict["dealerId"])}}
            ).get_result()
        code = 200
        if len(response['docs']) == 0:
            code = 404
        return {'statusCode': code,
                'headers': { 'Content-Type': 'application/json' },
                'body': response['docs']}
    except:
        return {'statusCode': 500,
                'headers': { 'Content-Type': 'application/json' },
                'body': {}}
                
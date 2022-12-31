function main(params) {
    return new Promise(function (resolve, reject) {
        const API_KEY = '5WUNPZBjs84te6oUX0v4HpYOA1fE_qGGbPltrwouY8hk'
        const API_URL = 'https://51d008c1-5757-4d25-a4a7-208e2742931e-bluemix.cloudantnosqldb.appdomain.cloud'
        const DB_NAME = 'dealerships'
        const { CloudantV1 } = require('@ibm-cloud/cloudant');
        const { IamAuthenticator } = require('ibm-cloud-sdk-core');
        const authenticator = new IamAuthenticator({ apikey: API_KEY })
        const cloudant = CloudantV1.newInstance({
            authenticator: authenticator
        });
        cloudant.setServiceUrl(API_URL);
        
        if (params.state) {
            cloudant.postFind({db:DB_NAME,selector:{state:params.state}})
            .then((result)=>{
              let code = 200;
              if (result.result.docs.length == 0) {
                  code = 404;
              }
              resolve({
                  statusCode: code,
                  headers: { 'Content-Type': 'application/json' },
                  body: result.result.docs
              });
            }).catch((err)=>{
              reject(err);
            })
        } else if (params.dealerId) {
            cloudant.postFind({db:DB_NAME,selector:{id:parseInt(params.dealerId)}})
            .then((result)=>{
              let code = 200;
              if (result.result.docs.length == 0) {
                  code = 404;
              }
              resolve({
                  statusCode: code,
                  headers: { 'Content-Type': 'application/json' },
                  body: result.result.docs
              });
            }).catch((err)=>{
              reject(err);
            })
        } else {
            cloudant.postAllDocs({ db: DB_NAME, includeDocs: true })            
            .then((result)=>{
              let code = 200;
              if (result.result.rows.length == 0) {
                  code = 404;
              }
              resolve({
                  statusCode: code,
                  headers: { 'Content-Type': 'application/json' },
                  body: result.result.rows
              });
            }).catch((err)=>{
              reject(err);
            })
      }
    }
    )}
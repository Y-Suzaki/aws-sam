# APIGatewayからのレスポンスをモック化する場合
### 実装手順
##### Swagger Specを用意する
* https://github.com/Y-Suzaki/aws-sam/blob/master/swagger.yaml
* Swaggerの説明はしないが、まずは通常通り作成すれば良い
* 上記に加えて、AWS拡張の定義が必要。これはSAMというより、APIGateway側の仕様のため。
    * 説明の簡略化のため、ここではLambda Functionではなく、Mockで済ませている
    ```
    x-amazon-apigateway-integration:
      type: mock
      requestTemplates:
        application/json: |
          {
            "statusCode" : 200
          }
      responses:
        default:
          statusCode: 200
          responseTemplates:
            application/json: |
              {
                "id":"00001", "name:"tanaka"
              }
    ```
    
##### AWS SAMのtemplateを用意する
* https://github.com/Y-Suzaki/aws-sam/blob/master/aws-sam.yaml
* CloudFormationの拡張機能なので、AWSを知っている人には馴染みやすい
* 最低限、以下の定義があればデプロイは可能
```
AWSTemplateFormatVersion: 2010-09-09
Transform: AWS::Serverless-2016-10-31
Description: AWS SAM Swagger.

Resources:
  SampleApi:
    Type: AWS::Serverless::Api
    Properties:
      StageName: dev
      DefinitionUri: swagger.yaml
```

### デプロイ手順
##### package作成
* コマンドの実行により、以下が行われる
    * Serverlesの拡張templateから、素のCloudFormationのtempalteを生成
    * デプロイに必要なファイル群をs3にアップロード
    ```
    aws cloudformation package \
      --template-file aws-sam.yaml \
      --output-template-file aws-sam-deploy.yaml \
      --s3-bucket {s3-bucket-name}
      
      ********************************************
      
      --template-file：入力ファイル名（AWS SAMのtempalte）
      --output-template-file：出力ファイル名（素のCloudFormationのtempalte）
      --s3-bucket：ファイルのアップロード先
    ```

##### CloudFormationのstack作成（更新）
* コマンドの実行により、以下が行われる
    * stackが作成（更新）され、APIGateway等のリソースが構築される
    * APIGatewayのStageにデプロイされる
    ```
    aws cloudformation deploy 
      --template-file aws-sam-deploy.yaml \
      --stack-name dev-aws-sam-test 
      --capabilities CAPABILITY_IAM
    
    ********************************************
    
      --template-file：入力ファイル名（素のCloudFormationのtempalte）
      --stack-name：stack名
      --capabilities：Roleの作成も行うため、CAPABILITY_IAMを指定
    ```

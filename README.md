# aws-sam
### 概要
* AWS SAM（Serverles Application Model）とSwaggerを使用した、Serverless環境を構築するサンプルです。

### 環境構築
* awscliが使える環境
    * 比較的新しめの機能のため、最新バーションにしておくのが望ましい
    
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

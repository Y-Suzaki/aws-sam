# APIGatewayからのレスポンスをLambda Functionにする場合
### 実装手順
##### Swagger Specを用意する
* https://github.com/Y-Suzaki/aws-sam/blob/master/swagger-lambda.yaml
* APIGateway用の拡張である「x-amazon-apigateway-integration」の定義に、Lambda Functionへの参照を指定する必要がある。
    * ※${SkillsFunction.Arn}のようなCloudFormationの定義が使える点については、SAM側のtemplate説明時に記載
    ```
      x-amazon-apigateway-integration:
        responses:
          default:
            statusCode: 200
        uri:
          Fn::Sub: arn:aws:apigateway:${AWS::Region}:lambda:path/2015-03-31/functions/${SkillsFunction.Arn}/invocations
        passthroughBehavior: "when_no_match"
        httpMethod: POST
        type: aws_proxy
    ```
    
##### AWS SAMのtemplateを用意する
* https://github.com/Y-Suzaki/aws-sam/blob/master/aws-sam-lambda.yaml
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

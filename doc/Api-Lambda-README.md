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
    * Swagger Spec側で本templateの定義を参照できると色々便利なため、Include（埋め込み）して使うようにしている
        * 上記のため、Swagger Spec側で${SkillsFunction.Arn}のような、本templateで定義しているAWSリソースの参照が可能になっている
        * 制約として、事前にSwagger Specをs3に配置しておく必要がある
    ```
    Resources:
      SampleApi:
        Type: AWS::Serverless::Api
        Properties:
          StageName: dev
          DefinitionBody:
            Fn::Transform:
              Name: AWS::Include
              Parameters:
                Location: !Sub s3://${ArtifactBucket}/swagger-lambda.yaml
    ```
    * Lambda Functionの定義と、EventとしてApiを指定する必要がある
    ```
    SkillsFunction:
    Type: AWS::Serverless::Function
    Properties:
      Runtime: python3.6
      Handler: lambda.get
      CodeUri: src/skills
      Role: !GetAtt LambdaRole.Arn
      Events:
        ApiProxy:
          Type: Api
          Properties:
            RestApiId: !Ref SampleApi
            Path: /skills
            Method: GET
    ```
### デプロイ手順
##### package作成
* 事前にSwagger Specをs3に配置しておく
    * 本手順では、bucketの直下に配置
    * 繰り返しデプロイするような場合、本手順も自動化しておくことが望ましい
* コマンドの実行により、以下が行われる
    * Serverlesの拡張templateから、素のCloudFormationのtempalteを生成
    * デプロイに必要なファイル群をs3にアップロード
    ```
    aws cloudformation package \
      --template-file aws-sam-lambda.yaml \
      --output-template-file aws-sam-lambda-deploy.yaml \
      --s3-bucket {s3-bucket-name}
      
      ********************************************
      
      --template-file：入力ファイル名（AWS SAMのtempalte）
      --output-template-file：出力ファイル名（素のCloudFormationのtempalte）
      --s3-bucket：ファイルのアップロード先
    ```

##### CloudFormationのstack作成（更新）
* s3のbcuket名をパラメータとして指定する必要がある
* コマンドの実行により、以下が行われる
    * stackが作成（更新）され、APIGateway等のリソースが構築される
    * APIGatewayのStageにデプロイされる
    ```
    aws cloudformation deploy 
      --template-file aws-sam-lambda-deploy.yaml \
      --stack-name dev-aws-sam-lambda-test 
      --capabilities CAPABILITY_IAM
      --parameter-overrides ArtifactBucket=cslab-aws-sam-deploy-dev
    ********************************************
    
      --template-file：入力ファイル名（素のCloudFormationのtempalte）
      --stack-name：stack名
      --capabilities：Roleの作成も行うため、CAPABILITY_IAMを指定
      --parameter-overrides：実行時に渡すパラメータを、key=valueで指定
    ```

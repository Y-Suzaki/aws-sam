# aws-sam
### 概要
* AWS SAM（Serverles Application Model）とSwaggerを使用した、Serverless環境を構築するサンプルです。

### 環境構築
* awscliが使える環境
    * 比較的新しめの機能のため、最新バーションにしておくのが望ましい
    
### 実装手順
##### APIGatewayからのレスポンスをモック化する場合
* doc/Api-Mock-README.md
##### APIGatewayからのレスポンスをLambda Functionにする場合
* dock/Api-Lambda-README.md
### AWS SAMで作成できるリソース
* APIGateway/Lambda Function
* S3/DynamoDB/SQS/SNS/Kinesis
* CloudWatch/CloudWatch Event
* IAM Role
### Tips
* Switch Role環境でAWS CLIを実行する場合、.aws/credentialsに定義しておくと便利
* AWSコマンド実行時、--profile cslab-admin を指定するのを忘れずに。
```
[cslab]
aws_access_key_id = AAAAAAXXXXXXXXXXX
aws_secret_access_key = BBBBBBBBBBXXXXXXXXXXXXX

[cslab-admin]
role_arn = arn:aws:iam::{Account Id}:role/common_role_admin
source_profile = cslab
region = us-west-2
```
### その他
* Mockではなく、Lambda Functionのデプロイは確認中。

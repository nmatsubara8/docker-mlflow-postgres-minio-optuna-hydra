# mlflow + postgresql + minio の実行環境を Docker環境で作成するサンプル

## mlflow version
```
mlflow              2.2.1
```
## コンテナ立ち上げ
```bash
docker-compose up -d
```
## サンプルスクリプト実行
サンプルスクリプトでは、scikit-learn のモデルを学習し、minioをモデルレジストリとしてデータを保存する。
```bash
# コンテナ内実行環境に入る
docker-compose exec app /bin/bash

# 実行
python run_mlflow.py
```

## データ確認

### minioコンソール
localhost:9001 にアクセスしてファイルを確認できる
* user: minio
* password: miniopass

mlflowフォルダと同階層に作成される minioフォルダ内にモデルファイルが格納されており、こちらからも確認できる


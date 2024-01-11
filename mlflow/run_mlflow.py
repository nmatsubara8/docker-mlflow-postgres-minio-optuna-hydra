import logging
import os
from urllib.parse import urlparse

import numpy as np
import pandas as pd
from accessor import MLflowSearcher, MlflowWriter
from sklearn.linear_model import ElasticNet
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

import mlflow
import mlflow.sklearn

# DB接続設定
DB = os.environ.get("DB_NAME")
USER = os.environ.get("DB_USERNAME")
PASSWORD = os.environ.get("DB_PASSWORD")
HOST = os.environ.get("DB_HOSTNAME")
PORT = os.environ.get("DB_PORT")
# mlflow db 設定
# os.environ[
#    "MLFLOW_TRACKING_URI"
# ] = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}"
# os.environ["MLFLOW_ARTIFACT_ROOT"] = "s3://mlflow/artifacts"

artifact_location = "s3://mlflow/artifacts"

logging.basicConfig(level=logging.WARN)
logger = logging.getLogger(__name__)


def eval_metrics(actual, pred):
    rmse = np.sqrt(mean_squared_error(actual, pred))
    mae = mean_absolute_error(actual, pred)
    r2 = r2_score(actual, pred)
    return rmse, mae, r2


def train():
    # モデルの学習
    # Read the wine-quality csv file from the URL
    csv_url = "http://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-red.csv"
    try:
        data = pd.read_csv(csv_url, sep=";")
    except Exception as e:
        logger.exception(
            "Unable to download training & test CSV, check your internet connection. Error: %s",
            e,
        )

    # Split the data into training and test sets. (0.75, 0.25) split.
    train, test = train_test_split(data)

    # The predicted column is "quality" which is a scalar from [3, 9]
    train_x = train.drop(["quality"], axis=1)
    test_x = test.drop(["quality"], axis=1)
    train_y = train[["quality"]]
    test_y = test[["quality"]]

    alpha = 0.5
    l1_ratio = 0.5

    # mlflowで記録
    model_name = "model6"

    writer = MlflowWriter(
        experiment_name=f"exp-{model_name}", artifact_location="s3://mlflow/artifacts"
    )

    # with mlflow.start_run() as run:
    lr = ElasticNet(alpha=alpha, l1_ratio=l1_ratio, random_state=42)
    lr.fit(train_x, train_y)

    predicted_qualities = lr.predict(test_x)

    (rmse, mae, r2) = eval_metrics(test_y, predicted_qualities)

    print("Elasticnet model (alpha=%f, l1_ratio=%f):" % (alpha, l1_ratio))
    print("  RMSE: %s" % rmse)
    print("  MAE: %s" % mae)
    print("  R2: %s" % r2)

    # パラメータ保存
    writer.log_param("alpha", alpha)
    writer.log_param("l1_ratio", l1_ratio)
    writer.log_metric("rmse", rmse)
    writer.log_metric("r2", r2)
    writer.log_metric("mae", mae)
    writer.set_tag("model_name", model_name)

    tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme
    print("tracking_uri: ", mlflow.get_tracking_uri())
    print("tracking_url_type")

    # モデルの保存
    # ファイルストアではモデルレジストリは使えない
    if tracking_url_type_store != "file":
        writer.log_sklearn_model(lr, model_name)
    else:
        writer.log_sklearn_model(lr, model_name)
        # mlflow.sklearn.log_model(lr, "model")

    # run_idを登録
    logger.info(f"Run ID: {writer.run_id} Exp_ID: {writer.experiment_id}")
    writer.set_terminated()
    return writer


def search(run_id):
    """保存したモデル情報の検索例"""
    searcher = MLflowSearcher()
    logger.info("run id searching...")
    searcher.search_model_by_run_id(run_id)

    # logger.info("tag searching...")
    # searcher.search_model_by_tag("system_name", "system1")

    logger.info("metrics...")
    searcher.get_metric_history(run_id, ["rmse", "r2", "mae"])


if __name__ == "__main__":
    logger.info("run start")
    writer = train()
    search(writer.run_id)

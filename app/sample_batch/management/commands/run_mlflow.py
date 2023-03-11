import os
import logging
from django.core.management.base import BaseCommand, CommandError
from sample_batch.models import MSYSModel
import mlflow
import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import ElasticNet
from urllib.parse import urlparse
import mlflow
import mlflow.sklearn
from mlflow.store.artifact.runs_artifact_repo import RunsArtifactRepository
from .accessor import MlflowWriter, MLflowSearcher

DB = os.environ.get("DJANGO_DB_NAME")
USER = os.environ.get("DJANGO_DB_USERNAME")
PASSWORD = os.environ.get("DJANGO_DB_PASSWORD")
HOST = os.environ.get("DJANGO_DB_HOSTNAME")
PORT = os.environ.get("DJANGO_DB_PORT")
# mlflow db 設定
os.environ["MLFLOW_TRACKING_URI"] = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}"

logging.basicConfig(level=logging.WARN)
logger = logging.getLogger(__name__)


def eval_metrics(actual, pred):
    rmse = np.sqrt(mean_squared_error(actual, pred))
    mae = mean_absolute_error(actual, pred)
    r2 = r2_score(actual, pred)
    return rmse, mae, r2


class Command(BaseCommand):
    help = "test mlflow run"

    def train(self):
        # np.random.seed(40)
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
        system_name = "system1"
        model_name = "model1"
        self.system_name = system_name
        self.model_name = model_name

        cli = MlflowWriter(experiment_name=f"{system_name}-{model_name}", artifact_location="s3://mlflow/artifacts")
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
        # mlflow.log_param("alpha", alpha)
        # mlflow.log_param("l1_ratio", l1_ratio)
        # mlflow.log_metric("rmse", rmse)
        # mlflow.log_metric("r2", r2)
        # mlflow.log_metric("mae", mae)
        cli.log_param("alpha", alpha)
        cli.log_param("l1_ratio", l1_ratio)
        cli.log_metric("rmse", rmse)
        cli.log_metric("r2", r2)
        cli.log_metric("mae", mae)
        cli.set_tag("system_name", system_name)
        cli.set_tag("model_name", model_name)

        tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme
        print("tracking_uri: ", mlflow.get_tracking_uri())
        print("tracking_url_type")

        # Model registry does not work with file store
        # ファイルストアではモデルレジストリは使えない
        if tracking_url_type_store != "file":
            cli.log_sklearn_model(lr, model_name)
        else:
            cli.log_sklearn_model(lr, model_name)
            # mlflow.sklearn.log_model(lr, "model")

        # run_idを登録
        self.run_id = cli.run_id
        m = MSYSModel(run_id=cli.run_id, experiment_id=cli.experiment_id)
        m.save()
        logger.info(f"Run ID: {cli.run_id} Exp_ID: {cli.experiment_id}")
        logger.info(f"model: {m}")

        cli.set_terminated()

    def search(self):
        cli = MLflowSearcher()
        logger.info("run id searching...")
        cli.search_model_by_run_id(self.run_id)

        # logger.info("tag searching...")
        # cli.search_model_by_tag("system_name", "system1")

        logger.info("metrics...")
        cli.get_metric_history(self.run_id, ["rmse", "r2", "mae"])

    def handle(self, *args, **options):
        self.stdout.write("run start")
        self.train()
        self.search()
        # with mlflow.start_run(run_id="0ce0394eee59494e918d06d2ff6ecb80"):
        #     mlflow.set_tag("hoge", "fuga")
        # cli = MLflowSearcher()
        # cli.search_model_by_run_id("0ce0394eee59494e918d06d2ff6ecb80")

        # logger.info("model name searching...")
        # cli.search_model_by_model_name("model1")

        # logger.info("system name searching...")
        # cli.search_model_by_system_name("system1")

        # logger.info("tag searching...")
        # cli.search_model_by_tag("hoge", "fuga")

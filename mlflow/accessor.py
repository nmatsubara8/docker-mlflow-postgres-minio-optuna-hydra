from pprint import pprint

import mlflow
from mlflow.tracking import MlflowClient


class MlflowWriter:
    def __init__(self, experiment_name, artifact_location=None, **kwargs):
        """mlflow書き込みを行うクラス

        Args:
            experiment_name (str): 実験名
            artifact_location (str, optional): artifactの保存先. ex: s3://<bucket_name>/artifacts Defaults to None.
        """
        self.client = MlflowClient(**kwargs)
        try:
            self.experiment_id = self.client.create_experiment(
                experiment_name,
                artifact_location=artifact_location,
            )
        except:
            self.experiment_id = self.client.get_experiment_by_name(experiment_name).experiment_id

        self.run_id = self.client.create_run(self.experiment_id).info.run_id
        self.artifact_path = "model"

    def log_params_from_omegaconf_dict(self, params):
        for param_name, element in params.items():
            self._explore_recursive(param_name, element)

    def _explore_recursive(self, parent_name, element):
        if isinstance(element, DictConfig):
            for k, v in element.items():
                if isinstance(v, DictConfig) or isinstance(v, ListConfig):
                    self._explore_recursive(f"{parent_name}.{k}", v)
                else:
                    self.client.log_param(self.run_id, f"{parent_name}.{k}", v)
        elif isinstance(element, ListConfig):
            for i, v in enumerate(element):
                self.client.log_param(self.run_id, f"{parent_name}.{i}", v)

    def log_torch_model(self, model, registered_model_name):
        """Logs a torch model"""
        with mlflow.start_run(self.run_id):
            mlflow.pytorch.log_model(model, self.artifact_path, registered_model_name=registered_model_name)

    def log_torch_state_dict(self, model):
        with mlflow.start_run(self.run_id):
            mlflow.pytorch.log_state_dict(
                model.state_dict(),
                artifact_path=self.artifact_path,
            )

    def load_torch_model(self, model_name, model_version):
        return mlflow.pytorch.load_model(model_uri=f"models:/{model_name}/{model_version}")

    def log_sklearn_model(self, model, registered_model_name=None):
        """sklearn modelの保存
        model: 保存するモデル
        registered_model_name: mlflow内部でのモデル名
        同名のモデルが保存されるとモデルのバージョンが上がる.
        """
        with mlflow.start_run(self.run_id):
            mlflow.sklearn.log_model(model, self.artifact_path, registered_model_name=registered_model_name)

    def log_param(self, key, value):
        """パラメータのロギング
        Args:
            key (_type_): _description_
            value (_type_): _description_
        """
        self.client.log_param(self.run_id, key, value)

    def log_metric(self, key, value, step=0):
        self.client.log_metric(self.run_id, key, value, step=step)

    def log_artifact(self, local_path):
        """アーカイブのロギング
        Args:
            local_path (str): 保存するファイルのパス
        """
        self.client.log_artifact(self.run_id, local_path)

    def set_tag(self, key, value):
        """tagをつける"""
        self.client.set_tag(self.run_id, key, value)

    def set_terminated(self):
        """記録終了"""
        self.client.set_terminated(self.run_id)


class MLflowSearcher:
    def __init__(self):
        """mlflow検索用クラス
        Args:
            experiment_name (str): 実験
            artifact_location (str, optional): artifactの保存先. ex: s3://<bucket_name>/artifacts Defaults to None.
        """
        self.client = mlflow.tracking.MlflowClient()

    def search_model_by_run_id(self, run_id):
        """run_idに一致するモデル情報を取得する

        Args:
            run_id (str): run_id

        Returns:
        """
        results = self.client.search_model_versions(f'run_id = "{run_id}"')
        for res in results:
            pprint(res)

    def search_model_by_model_name(self, model_name):
        results = self.client.search_model_versions(f'name = "{model_name}"')
        for res in results:
            pprint(res)

    def get_metric_history(self, run_id, metric_names):
        def print_metric_info(history):
            for m in history:
                print("name: {}".format(m.key))
                print("value: {}".format(m.value))
                print("step: {}".format(m.step))
                print("timestamp: {}".format(m.timestamp))
                print("--")

        for name in metric_names:
            print_metric_info(self.client.get_metric_history(run_id, name))

    # 何故かタグ検索うまくいかないので消しておく
    # def search_model_by_system_name(self, system_name):
    #     results = self.client.search_model_versions(f"tags.system_name = '{system_name}'")
    #     for res in results:
    #         pprint(res)

    # def search_model_by_tag(self, key, value):
    #     results = self.client.search_model_versions(f'tags.{key} = "{value}"')
    #     for res in results:
    #         pprint(res)

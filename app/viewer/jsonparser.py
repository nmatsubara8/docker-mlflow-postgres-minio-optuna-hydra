import json
from typing import Optional
from pydantic import BaseModel, Field, validator
from datetime import datetime, date


def transform_str_to_datetime(dt: str) -> datetime:
    return datetime.strptime(dt, "%Y-%m-%d_%H:%M:%S.%f")


class ImageFieldSchema(BaseModel):
    file_name: str
    date_and_time: str
    _normalized_date_and_time = validator("date_and_time", allow_reuse=True)(transform_str_to_datetime)
    height: int
    width: int
    Target_system: str
    system_version: str
    device_id: int
    place_name: str
    camera_name: str
    lp_name: str
    target_model_name: list[str]
    target_model_version: list[str]
    id: Optional[int]
    # "diversity_nearest_id": []
    similarity_id: Optional[int]
    dataset_flag: Optional[int]
    autolabeling_flag: Optional[int]
    annotate_date: Optional[date]
    type: str  # train or val


class JSONSchema(BaseModel):
    """JSONスキーマ定義"""

    image_field: ImageFieldSchema
    # material_class: str = Field(
    #     description="教材種別",
    #     min_length=ConstValue.MIN_FLAG_LENGTH,
    #     max_length=ConstValue.MAX_FLAG_LENGTH,
    # )
    # # passing_score: conint(ge=0)  # 合格点
    # passing_score: Optional[int] = None
    # adaptive_skills: list[str]  # アダプティブスキルID
    # questions: list[QuestionSchema]  # 問題データ
    pass


def parse_json(path):

    return dict()


if __name__ == "__main__":
    image_field = {
        "file_name": "20190510_0100_01_00596.png",
        "date_and_time": "2019-05-10_01:00:00.00596",
        "height": 720,
        "width": 1280,
        "Target_system": "valley",
        "system_version": "0",
        "place_name": "kanayama",
        "camera_name": "01",
        "lp_name": "valley",
        "target_model_name": [],
        "target_model_version": [],
        "id": 0,
        "diversity_nearest_id": [],
        # "dataset_flag": 1,
        "autolabeling_flag": 0,
        # "annotate_date": "00000000",
        "type": "train",
    }
    print(ImageFieldSchema(**image_field))
    parse_json("/app/viewer/static/img/20190510_0100_01_00596.json")

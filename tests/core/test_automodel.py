#  Copyright (c) 2021 GradsFlow. All rights reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
import torch
from flash.image import ImageClassificationData

from gradsflow.core.automodel import AutoModel

cwd = Path.cwd()
datamodule = ImageClassificationData.from_folders(
    train_folder=f"{cwd}/data/hymenoptera_data/train/",
    val_folder=f"{cwd}/data/hymenoptera_data/val/",
)


def test_auto_model():
    assert AutoModel(datamodule)


def test_build_model():
    model = AutoModel(datamodule)
    with pytest.raises(NotImplementedError):
        model.build_model({"lr": 1})


def test_create_search_space():
    model = AutoModel(datamodule)
    with pytest.raises(NotImplementedError):
        model._create_search_space()


@patch("gradsflow.core.automodel.pl")
def test_objective(mock_pl):
    optimization_metric = "val_accuracy"
    model = AutoModel(datamodule, optimization_metric=optimization_metric)

    model.build_model = MagicMock()
    trainer = mock_pl.Trainer = MagicMock()
    trainer.callback_metrics = {optimization_metric: torch.as_tensor([1])}

    model.objective({}, {})


@patch("gradsflow.core.automodel.tune.run")
def test_hp_tune(mock_tune):
    automodel = AutoModel(datamodule)
    automodel._create_search_space = MagicMock()
    automodel.hp_tune(gpu=1, cpu=2)

    mock_tune.assert_called()

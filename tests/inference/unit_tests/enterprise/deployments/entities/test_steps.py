from typing import Any

import pytest
from pydantic import ValidationError

from inference.enterprise.deployments.entities.inputs import (
    InferenceImage,
    InferenceParameter,
)
from inference.enterprise.deployments.entities.steps import ClassificationModel, MultiLabelClassificationModel
from inference.enterprise.deployments.errors import (
    InvalidStepInputDetected,
    ExecutionGraphError, VariableTypeError,
)


def test_classification_model_validation_when_minimalistic_config_is_provided() -> None:
    # given
    data = {
        "type": "ClassificationModel",
        "name": "some",
        "image": "$inputs.image",
        "model_id": "some/1",
    }

    # when
    result = ClassificationModel.parse_obj(data)

    # then
    assert result == ClassificationModel(
        type="ClassificationModel",
        name="some",
        image="$inputs.image",
        model_id="some/1",
    )


@pytest.mark.parametrize("field", ["type", "name", "image", "model_id"])
def test_classification_model_validation_when_required_field_is_not_given(
    field: str,
) -> None:
    # given
    data = {
        "type": "ClassificationModel",
        "name": "some",
        "image": "$inputs.image",
        "model_id": "some/1",
    }
    del data[field]

    # when
    with pytest.raises(ValidationError):
        _ = ClassificationModel.parse_obj(data)


def test_classification_model_validation_when_invalid_type_provided() -> None:
    # given
    data = {
        "type": "invalid",
        "name": "some",
        "image": "$inputs.image",
        "model_id": "some/1",
    }

    # when
    with pytest.raises(ValidationError):
        _ = ClassificationModel.parse_obj(data)


def test_classification_model_validation_when_model_id_has_invalid_type() -> None:
    # given
    data = {
        "type": "ClassificationModel",
        "name": "some",
        "image": "$inputs.image",
        "model_id": None,
    }

    # when
    with pytest.raises(ValidationError):
        _ = ClassificationModel.parse_obj(data)


def test_classification_model_validation_when_active_learning_flag_has_invalid_type() -> (
    None
):
    # given
    data = {
        "type": "ClassificationModel",
        "name": "some",
        "image": "$inputs.image",
        "model_id": "some/1",
        "disable_active_learning": "some",
    }

    # when
    with pytest.raises(ValidationError):
        _ = ClassificationModel.parse_obj(data)


def test_classification_model_image_selector_when_selector_is_valid() -> None:
    # given
    data = {
        "type": "ClassificationModel",
        "name": "some",
        "image": "$inputs.image",
        "model_id": "some/1",
    }

    # when
    result = ClassificationModel.parse_obj(data)
    result.validate_field_selector(
        field_name="image",
        input_step=InferenceImage(type="InferenceImage", name="image"),
    )

    # then - no error is raised


def test_classification_model_image_selector_when_selector_is_invalid() -> None:
    # given
    data = {
        "type": "ClassificationModel",
        "name": "some",
        "image": "$inputs.image",
        "model_id": "some/1",
    }

    # when
    result = ClassificationModel.parse_obj(data)
    with pytest.raises(InvalidStepInputDetected):
        result.validate_field_selector(
            field_name="image",
            input_step=InferenceParameter(type="InferenceParameter", name="some"),
        )


def test_classification_model_selector_when_model_id_is_invalid() -> None:
    # given
    data = {
        "type": "ClassificationModel",
        "name": "some",
        "image": "$inputs.image",
        "model_id": "$inputs.model",
    }

    # when
    result = ClassificationModel.parse_obj(data)
    with pytest.raises(InvalidStepInputDetected):
        result.validate_field_selector(
            field_name="model_id",
            input_step=InferenceImage(type="InferenceImage", name="image"),
        )


def test_classification_model_selector_when_disable_active_learning_is_invalid() -> (
    None
):
    # given
    data = {
        "type": "ClassificationModel",
        "name": "some",
        "image": "$inputs.image",
        "model_id": "$inputs.model",
        "disable_active_learning": "$inputs.disable_active_learning",
    }

    # when
    result = ClassificationModel.parse_obj(data)
    with pytest.raises(InvalidStepInputDetected):
        result.validate_field_selector(
            field_name="disable_active_learning",
            input_step=InferenceImage(type="InferenceImage", name="image"),
        )


def test_classification_model_selector_when_referring_to_field_that_does_not_hold_selector() -> (
    None
):
    # given
    data = {
        "type": "ClassificationModel",
        "name": "some",
        "image": "$inputs.image",
        "model_id": "$inputs.model",
    }

    # when
    result = ClassificationModel.parse_obj(data)
    with pytest.raises(ExecutionGraphError):
        result.validate_field_selector(
            field_name="disable_active_learning",
            input_step=InferenceParameter(type="InferenceParameter", name="image"),
        )


@pytest.mark.parametrize(
    "field_name, value",
    [
        ("confidence", 1.1),
        ("image", "some"),
        ("model_id", 38),
        ("disable_active_learning", "some")
    ]
)
def test_classification_model_binding_when_parameter_is_invalid(
    field_name: str,
    value: Any,
) -> None:
    # given
    data = {
        "type": "ClassificationModel",
        "name": "some",
        "image": "$inputs.image",
        "model_id": "$inputs.model",
    }

    # when
    result = ClassificationModel.parse_obj(data)
    with pytest.raises(VariableTypeError):
        result.validate_field_binding(
            field_name=field_name,
            value=value,
        )


def test_multi_label_classification_model_validation_when_minimalistic_config_is_provided() -> None:
    # given
    data = {
        "type": "MultiLabelClassificationModel",
        "name": "some",
        "image": "$inputs.image",
        "model_id": "some/1",
    }

    # when
    result = MultiLabelClassificationModel.parse_obj(data)

    # then
    assert result == MultiLabelClassificationModel(
        type="MultiLabelClassificationModel",
        name="some",
        image="$inputs.image",
        model_id="some/1",
    )


@pytest.mark.parametrize("field", ["type", "name", "image", "model_id"])
def test_multi_label_classification_model_validation_when_required_field_is_not_given(
    field: str,
) -> None:
    # given
    data = {
        "type": "MultiLabelClassificationModel",
        "name": "some",
        "image": "$inputs.image",
        "model_id": "some/1",
    }
    del data[field]

    # when
    with pytest.raises(ValidationError):
        _ = MultiLabelClassificationModel.parse_obj(data)


def test_multi_label_classification_model_validation_when_invalid_type_provided() -> None:
    # given
    data = {
        "type": "invalid",
        "name": "some",
        "image": "$inputs.image",
        "model_id": "some/1",
    }

    # when
    with pytest.raises(ValidationError):
        _ = MultiLabelClassificationModel.parse_obj(data)


def test_multi_label_classification_model_validation_when_model_id_has_invalid_type() -> None:
    # given
    data = {
        "type": "MultiLabelClassificationModel",
        "name": "some",
        "image": "$inputs.image",
        "model_id": None,
    }

    # when
    with pytest.raises(ValidationError):
        _ = MultiLabelClassificationModel.parse_obj(data)



def test_multi_label_classification_model_validation_when_active_learning_flag_has_invalid_type() -> (
    None
):
    # given
    data = {
        "type": "MultiLabelClassificationModel",
        "name": "some",
        "image": "$inputs.image",
        "model_id": "some/1",
        "disable_active_learning": "some",
    }

    # when
    with pytest.raises(ValidationError):
        _ = MultiLabelClassificationModel.parse_obj(data)


def test_multi_label_classification_model_image_selector_when_selector_is_valid() -> None:
    # given
    data = {
        "type": "MultiLabelClassificationModel",
        "name": "some",
        "image": "$inputs.image",
        "model_id": "some/1",
    }

    # when
    result = MultiLabelClassificationModel.parse_obj(data)
    result.validate_field_selector(
        field_name="image",
        input_step=InferenceImage(type="InferenceImage", name="image"),
    )

    # then - no error is raised


def test_multi_label_classification_model_image_selector_when_selector_is_invalid() -> None:
    # given
    data = {
        "type": "MultiLabelClassificationModel",
        "name": "some",
        "image": "$inputs.image",
        "model_id": "some/1",
    }

    # when
    result = MultiLabelClassificationModel.parse_obj(data)
    with pytest.raises(InvalidStepInputDetected):
        result.validate_field_selector(
            field_name="image",
            input_step=InferenceParameter(type="InferenceParameter", name="some"),
        )


def test_multi_label_classification_model_selector_when_model_id_is_invalid() -> None:
    # given
    data = {
        "type": "MultiLabelClassificationModel",
        "name": "some",
        "image": "$inputs.image",
        "model_id": "$inputs.model",
    }

    # when
    result = MultiLabelClassificationModel.parse_obj(data)
    with pytest.raises(InvalidStepInputDetected):
        result.validate_field_selector(
            field_name="model_id",
            input_step=InferenceImage(type="InferenceImage", name="image"),
        )


def test_multi_label_classification_model_selector_when_disable_active_learning_is_invalid() -> (
    None
):
    # given
    data = {
        "type": "MultiLabelClassificationModel",
        "name": "some",
        "image": "$inputs.image",
        "model_id": "$inputs.model",
        "disable_active_learning": "$inputs.disable_active_learning",
    }

    # when
    result = MultiLabelClassificationModel.parse_obj(data)
    with pytest.raises(InvalidStepInputDetected):
        result.validate_field_selector(
            field_name="disable_active_learning",
            input_step=InferenceImage(type="InferenceImage", name="image"),
        )


def test_multi_label_classification_model_selector_when_referring_to_field_that_does_not_hold_selector() -> (
    None
):
    # given
    data = {
        "type": "MultiLabelClassificationModel",
        "name": "some",
        "image": "$inputs.image",
        "model_id": "$inputs.model",
    }

    # when
    result = MultiLabelClassificationModel.parse_obj(data)
    with pytest.raises(ExecutionGraphError):
        result.validate_field_selector(
            field_name="disable_active_learning",
            input_step=InferenceParameter(type="InferenceParameter", name="image"),
        )


@pytest.mark.parametrize(
    "field_name, value",
    [
        ("confidence", 1.1),
        ("image", "some"),
        ("model_id", 38),
        ("disable_active_learning", "some")
    ]
)
def test_multi_label_classification_model_binding_when_parameter_is_invalid(
    field_name: str,
    value: Any,
) -> None:
    # given
    data = {
        "type": "MultiLabelClassificationModel",
        "name": "some",
        "image": "$inputs.image",
        "model_id": "$inputs.model",
    }

    # when
    result = MultiLabelClassificationModel.parse_obj(data)
    with pytest.raises(VariableTypeError):
        result.validate_field_binding(
            field_name=field_name,
            value=value,
        )

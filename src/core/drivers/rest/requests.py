import logging
from uuid import UUID, uuid4

from pydantic import Field
from pydantic.json_schema import SkipJsonSchema

from src.core.use_cases.inputs import CreateCategoryInput

logger = logging.getLogger(__name__)


class CreateCategoryRequest(CreateCategoryInput):
    user_id: SkipJsonSchema[UUID] = Field(default_factory=uuid4, exclude=True)


print(CreateCategoryInput.model_fields)

# CreateCategoryRequest = create_model(
#     "CreateCategoryRequest",
#     **_.omit(CreateCategoryInput, ["user_id"]),
# )

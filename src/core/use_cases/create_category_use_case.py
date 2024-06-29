from src.core.ports.unit_of_work import UnitOfWork
from src.core.use_cases.errors import CategoryAlreadyExistsError
from src.core.use_cases.inputs import CreateCategoryInput
from src.core.use_cases.outputs import CreateCategoryOutput


class CreateCategoryUseCase:
    def __init__(self, unit_of_work: UnitOfWork) -> None:
        self._unit_of_work = unit_of_work

    async def __call__(
        self,
        data: CreateCategoryInput,
    ) -> CreateCategoryOutput:
        category = data.to_category()

        async with self._unit_of_work as uow:
            category_exists = await uow.category_repository.exists(
                category.name,
                category.user_id,
            )

            if category_exists:
                raise CategoryAlreadyExistsError()

            await uow.category_repository.create(category)

            await uow.commit()

        return CreateCategoryOutput.from_category(category)

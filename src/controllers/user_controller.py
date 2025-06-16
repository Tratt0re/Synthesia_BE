import logging
from datetime import datetime, timezone
from pymongo.collection import Collection
from src.services import DatabaseService
from src.models.default.user import UserCreateRequest, UserResponse, UserUpdateRequest
from src.models.database.user import UserDBModel
from src.core.exceptions import ServerErrorException, NotFoundException


class UserController:
    def __init__(self):
        self.db = DatabaseService.get_db()
        self.collection: Collection = self.db["users"]

    async def create_user(
        self,
        user_data: UserCreateRequest,
    ) -> UserResponse:
        try:
            user_db = UserDBModel(
                browser_info=user_data.browser_info,
                created_at=datetime.now(timezone.utc).isoformat(),
            )

            result = await self.collection.insert_one(user_db.model_dump(by_alias=True))
            inserted_user = await self.collection.find_one({"_id": result.inserted_id})

            return UserResponse.model_validate(inserted_user)
        except Exception as err:
            logging.error(f"UserController/create_user - err: {err}")
            raise ServerErrorException(message="Failed to create user.")

    async def get_user(self, user_id: str) -> UserResponse:
        try:
            user_data = await self.collection.find_one({"_id": user_id})
            if not user_data:
                raise NotFoundException("User not found.")

            return UserResponse.model_validate(user_data)
        except NotFoundException:
            raise
        except Exception as err:
            logging.error(f"UserController/get_user - err: {err}")
            raise ServerErrorException("Failed to retrieve user.")

    async def update_user(
        self,
        user_id: str,
        updates: UserUpdateRequest,
    ) -> UserResponse:
        try:
            update_data = updates.model_dump(exclude_unset=True)
            if not update_data:
                raise ServerErrorException("No update fields provided.")

            await self.collection.update_one(
                {"_id": user_id}, {"$set": update_data}
            )

            updated_user_data = await self.collection.find_one(
                {"_id": user_id}
            )
            if not updated_user_data:
                raise NotFoundException("User not found after update.")

            return UserResponse.model_validate(updated_user_data)

        except NotFoundException:
            raise
        except Exception as err:
            logging.error(f"UserController/update_user - err: {err}")
            raise ServerErrorException("Failed to update user.")

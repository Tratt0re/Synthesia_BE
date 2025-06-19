import logging
from datetime import datetime, timezone
from pymongo.collection import Collection
from pymongo import ASCENDING
from typing import Optional
from src.models.database.processed_result import ProcessedResult
from pymongo import ASCENDING
from src.utils.hash_utils import generate_input_hash
from src.services import DatabaseService
from src.core.exceptions import ServerErrorException


class ProcessedResultController:
    def __init__(self):
        self.db = DatabaseService.get_db()
        self.collection: Collection = self.db["processed_results"]

    async def upsert_result(
        self,
        user_id: str,
        input_text: str,
        is_file: bool,
        model: str,
        language: str = "eng",
        summary: Optional[str] = None,
        entities: Optional[dict] = None,
        filename: Optional[str] = None,
        entity_keys: Optional[list[str]] = None,
    ) -> str:
        try:
            input_hash = generate_input_hash(text=input_text, user_id=user_id)

            existing = await self.collection.find_one(
                {
                    "user_id": user_id,
                    "source_hash": input_hash,
                }
            )

            now = datetime.now(timezone.utc).isoformat()

            if existing:
                update_data = {
                    "updated_at": now,
                }
                
                summary_history = []
                entities_history = []

                current_model = existing.get("model")
                if summary:
                    current_summary = existing.get("summary")
                    if current_summary:
                        summary_history.append(
                            {
                                "value": current_summary,
                                "model": current_model,
                                "timestamp": now,
                            }
                        )
                    update_data["summary"] = summary

                if entities:
                    current_entities = existing.get("extracted_entities")
                    if current_entities:
                        entities_history.append(
                            {
                                "value": current_entities,
                                "model": current_model,
                                "timestamp": now,
                            }
                        )
                    update_data["extracted_entities"] = entities

                if entity_keys:
                    update_data["entities_requested"] = entity_keys
                if filename:
                    update_data["filename"] = filename
                if model:
                    update_data["model"] = model
                if language:
                    update_data["language"] = language

                # First update regular fields
                await self.collection.update_one(
                    {"_id": existing["_id"]}, {"$set": update_data}
                )

                # Then update history arrays if needed
                push_ops = {}
                if summary_history:
                    push_ops["summary_history"] = {"$each": summary_history}
                if entities_history:
                    push_ops["entities_history"] = {"$each": entities_history}

                if push_ops:
                    await self.collection.update_one(
                        {"_id": existing["_id"]}, {"$push": push_ops}
                    )
                return str(existing["_id"])

            result_data = ProcessedResult(
                user_id=user_id,
                source_hash=input_hash,
                language=language,
                model=model,
                summary=summary,
                extracted_entities=entities,
                input_type="file" if is_file else "text",
                filename=filename,
                entities_requested=entity_keys,
                created_at=now,
                updated_at=now,
            )

            insert_result = await self.collection.insert_one(
                result_data.model_dump(by_alias=True)
            )
            return str(insert_result.inserted_id)

        except Exception as err:
            logging.error(f"ProcessedResultController/upsert_result - err: {err}")
            raise ServerErrorException("Failed to upsert processed result.")

    async def list_results(
        self,
        user_id: str,
        skip: int = 0,
        limit: int = 10,
    ) -> list[ProcessedResult]:
        try:
            cursor = (
                self.collection.find({"user_id": user_id})
                .sort("updated_at", ASCENDING)
                .skip(skip)
                .limit(limit)
            )
            results = await cursor.to_list(length=limit)
            return [ProcessedResult.model_validate(r) for r in results]
        except Exception as err:
            logging.error(f"ProcessedResultController/list_results - err: {err}")
            raise ServerErrorException("Failed to retrieve processed results.")

    async def delete_result(self, user_id: str, result_id: str) -> bool:
        try:
            result = await self.collection.delete_one({
                "user_id": user_id,
                "_id": result_id
            })
            return result.deleted_count > 0
        except Exception as err:
            logging.error(f"ProcessedResultController/delete_result - err: {err}")
            raise ServerErrorException("Failed to delete processed result.")

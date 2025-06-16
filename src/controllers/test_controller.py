from src.models.default.test_model import TestModel


class TestController:
    def __init__(self, description: str, item: TestModel) -> None:
        self.description = description
        self.item = item

    def do_something(self):
        return f"The test item is named '{self.item.name}' and has the value '{self.item.value}'"

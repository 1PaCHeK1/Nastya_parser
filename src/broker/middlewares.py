from taskiq import TaskiqMessage, TaskiqMiddleware
import aioinject


class InjectMiddleware(TaskiqMiddleware):
    def __init__(self, container: aioinject.Container) -> None:
        self._container = container

    async def pre_execute(self, message: "TaskiqMessage") -> TaskiqMessage:
        async with self._container.context():
            return message

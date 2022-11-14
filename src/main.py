import asyncio
from core.containers import Container, Provide, inject
from core.users.services import UserService
from core.utils.services import RedisService


@inject
async def func(
    user_service: UserService = Provide[Container.user_service],
    redis_service: RedisService = Provide[Container.redis_service]
):
    print(await user_service.get_users())
    print(await redis_service.process())


async def main():
    container = Container()
    container.init_resources()
    container.wire(modules=[__name__])

    await func()


asyncio.run(main())

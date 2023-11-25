from test import test
import asyncio

async def main():
    await asyncio.gather(test(), test(2))

asyncio.run(main())

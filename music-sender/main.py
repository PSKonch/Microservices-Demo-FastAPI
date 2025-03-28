import asyncio
from consumer import start_consume

if __name__ == "__main__":
    try:
        asyncio.run(start_consume())
    except KeyboardInterrupt:
        print("Stopped by user.")
import asyncio
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI
from src.app.routes import notes_routes, users_routes


async def background_task_function():
    """
    This task will run continuously in the background.
    """
    while True:
        print(f"Background task running at: {time.strftime('%H:%M:%S')}")
        await asyncio.sleep(10)  # Sleep for 10 seconds


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Code to run on startup
    print("Application starting up, starting background task...")

    # Start the background task using asyncio.create_task()
    # It returns a Task object, which will run the coroutine concurrently
    task = asyncio.create_task(background_task_function())

    yield

    # Code to run on shutdown (after the yield)
    print("Application shutting down, cancelling background task...")
    # Cleanly cancel the task when the application shuts down
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        print("Background task cancelled successfully.")


app = FastAPI(lifespan=lifespan)


app.include_router(notes_routes.router, prefix="/notes", tags=["notes"])
app.include_router(users_routes.router, prefix="/users", tags=["users"])

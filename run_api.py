import uvicorn
import dotenv


if __name__ == "__main__":
    dotenv.load_dotenv(".env")
    uvicorn.run("api.app:create_fastapi", reload=True)

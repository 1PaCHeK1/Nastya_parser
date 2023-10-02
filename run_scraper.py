import dotenv
import anyio

if __name__ == "__main__":
    dotenv.load_dotenv(".env")
    from scrapers.main import main

    anyio.run(main)

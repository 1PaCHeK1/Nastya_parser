import dotenv

dotenv.load_dotenv(".env")

from bot.start_strategy import polling  # noqa: E402

if __name__ == "__main__":
    polling()

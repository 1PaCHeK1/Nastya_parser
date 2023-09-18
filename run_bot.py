import dotenv

dotenv.load_dotenv(".env")


if __name__ == "__main__":
    from bot.start_strategy import polling  # noqa: E402
    polling()

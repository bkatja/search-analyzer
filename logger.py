class Log:
    @staticmethod
    def info(message: str):
        print(f"[INFO] {message}")

    @staticmethod
    def debug(message: str):
        print(f"[DEBUG] {message}")

    @staticmethod
    def error(message: str):
        print(f"[ERROR] {message}")

    @staticmethod
    def section(title: str = ""):
        print("\n" + "=" * 60)
        if title:
            print(f"[INFO] {title}")
            print("-" * 60)

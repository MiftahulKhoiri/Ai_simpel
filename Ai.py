from core.bootstrap import bootstrap
import threading
import queue
import time


def timed_input(prompt: str, timeout: int, default: str) -> str:
    """
    Menunggu input user dengan timeout.
    Jika timeout tercapai, return default.
    """
    q = queue.Queue()

    def reader():
        try:
            q.put(input(prompt))
        except Exception:
            q.put("")

    t = threading.Thread(target=reader, daemon=True)
    t.start()

    try:
        return q.get(timeout=timeout).strip().lower()
    except queue.Empty:
        print(f"\n⏱ Timeout {timeout} detik, otomatis masuk mode '{default}'")
        return default


def run():
    bootstrap()

    mode = timed_input(
        prompt="Pilih mode (cli/api) [default: api dalam 15 detik]: ",
        timeout=15,
        default="api"
    )

    if mode == "cli":
        import main
        main.main()
    else:
        import api
        api.app.run(
            host="0.0.0.0",
            port=5000,
            debug=True
        )


if __name__ == "__main__":
    run()
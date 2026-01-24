from core.bootstrap import bootstrap


def run():
    # Inisialisasi sistem (venv, dependency, update, data, model)
    bootstrap()

    # Jalankan API
    import api
    api.app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )


if __name__ == "__main__":
    run()
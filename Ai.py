from core.bootstrap import bootstrap

def run():
    bootstrap()

    mode = input("Pilih mode (cli/api): ").strip().lower()

    if mode == "api":
        import api
        api.app.run(host="0.0.0.0", port=5000,         debug=True )
    else:
        import main
        main.main()

if __name__ == "__main__":
    run()
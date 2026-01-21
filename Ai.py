from core.bootstrap import bootstrap

if __name__ == "__main__":
    bootstrap()

    # import SETELAH dependency siap
    import main
    main.main()
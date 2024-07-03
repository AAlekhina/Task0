from config import Config
def main():
    cfg = Config()
    dsn = cfg.get_dsn()
    print(dsn)

if __name__ == '__main__':
    main()

from scrappers.bancolombia import BancolombiaScrapper

SCRAPPERS = [
    BancolombiaScrapper(),
]


def main():
    for fund in SCRAPPERS:
        fund.scrap()


if __name__ == '__main__':
    main()

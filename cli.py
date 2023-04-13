from scrappers.bancolombia import BancolombiaScrapper

SCRAPPERS = [
    BancolombiaScrapper(),
]


def execute():
    for fund in SCRAPPERS:
        fund.scrap()

#
# if __name__ == '__main__':
#     run()

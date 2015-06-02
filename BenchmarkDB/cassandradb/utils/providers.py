"""

"""

data = """dataone: 81070

arxiv_oai: 72681

crossref: 71312

pubmed: 47506

figshare: 36462

scitech: 18362

clinicaltrials: 10244

plos: 9555

mit: 2488

vtech: 713

cmu: 601

columbia: 386

calpoly: 377

opensiuc: 293

doepages: 123

stcloud: 47

spdataverse: 40

trinity: 32

texasstate: 31

valposcholar: 26

utaustin: 13

uwashington: 12

uiucideals: 6

ucescholarship: 0

upennsylvania: 0

utaustin: 0

waynestate: 0"""


def return_providers(provider_data=None):

    if not provider_data:

        provider_data = data

    providers = []

    lines = provider_data.split('\n')

    for line in lines:

        if line != '':

            line_split = line.split(':')

            provider = line_split[0]

            providers.append(provider)

    return providers
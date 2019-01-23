import sys
from typing import Optional

from defusedxml.ElementTree import fromstring
import requests

BASE_PUBMED_URI = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id={PMID}&retmode=xml'
REACH_URI = 'http://agathon.sista.arizona.edu:8080/odinweb/api/text'


def download_pmid_xml(pmid: str) -> str:
    resp = requests.get(BASE_PUBMED_URI.format(PMID=pmid))
    resp.raise_for_status()
    return resp.text


def extract_abstract(xml: str) -> Optional[str]:
    root = fromstring(xml)

    abstract_texts = []
    for abstract_element in root.findall('./PubmedArticle/MedlineCitation/Article/Abstract/AbstractText'):
        abstract_texts.append(''.join(abstract_element.itertext()))

    concatenated_abstracts = '\n'.join(abstract_texts)
    if concatenated_abstracts.strip():  # check that there is any non-whitespace content
        return concatenated_abstracts


def reach_extract(text: str) -> str:
    resp = requests.post(REACH_URI, data={'text': text, 'output': 'fries'})
    resp.raise_for_status()
    return resp.text


def main() -> Optional[int]:
    assert len(sys.argv[1:]) == 1, 'provide a PMID as an argument'
    pmid = sys.argv[1]

    pmid_content = download_pmid_xml(pmid)
    abstract_text = extract_abstract(pmid_content)
    reach_json = reach_extract(abstract_text)

    with open(f'{pmid}.json', 'w') as f:
        print(reach_json, file=f)


if __name__ == '__main__':
    sys.exit(main())

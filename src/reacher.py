"""REACHer.

Download an abstract from PubMed with its PMID, extract mentioned pathways with Reach, and save the output JSON.
"""
import json
import sys
from collections import Counter
from typing import Optional

import requests
from defusedxml.ElementTree import fromstring

BASE_PUBMED_URI = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id={PMID}&retmode=xml'
REACH_URI = 'http://agathon.sista.arizona.edu:8080/odinweb/api/text'


def download_pmid_xml(pmid: str) -> str:
    """Retrieve the XML data record for the given PMID.

    (Due to the Entrez API, passing multiple IDs separated by commas in a single string
    will retrieve the records for all of the IDs.)

    :param pmid: the PubMed ID of the record to be retrieved

    :returns: the XML data record as a string
    :raises requests.exceptions.HTTPError: on an error response from the web service
    """
    resp = requests.get(BASE_PUBMED_URI.format(PMID=pmid))
    resp.raise_for_status()
    return resp.text


def extract_abstract(xml: str) -> Optional[str]:
    """Extract all the abstract text from an Entrez XML data record.

    :param xml: the XML data record as a string

    :returns: all the abstract text
    """
    root = fromstring(xml)

    abstract_texts = []
    for abstract_element in root.findall(
        './PubmedArticle/MedlineCitation/Article/Abstract/AbstractText'
    ):
        abstract_texts.append(''.join(abstract_element.itertext()))

    concatenated_abstracts = '\n'.join(abstract_texts)
    if concatenated_abstracts.strip():  # check that there is any non-whitespace content
        return concatenated_abstracts


def reach_extract(text: str) -> str:
    """Provide text to Reach to be processed and return the JSON string of the results.

    :param text: the text string to be processed by Reach

    :returns: the resulting Reach JSON ('fries' output format) as a string
    :raises requests.exceptions.HTTPError: on an error response from the web service
    """
    resp = requests.post(REACH_URI, data={'text': text, 'output': 'fries'})
    resp.raise_for_status()
    return resp.text


def print_reach_statistics(reach_result_json: str) -> None:
    """Print statistics about the Reach result to stderr.

    :param reach_result_json: the JSON **string** (not a Python mapping) of the Reach result to be analyzed
    """
    reach_json = json.loads(reach_result_json)

    # use get and empty containers as defaults to allow chaining without error checking
    frames = reach_json.get('events', {}).get('frames', [])

    num_events = len(frames)
    print(f'events extracted: {num_events}', file=sys.stderr)

    types_count = Counter(frame['type'] for frame in frames)
    print('number of events of each type:', file=sys.stderr)
    for type_, count in types_count.items():
        print(f"  '{type_}': {count}", file=sys.stderr)


def main() -> Optional[int]:
    """Main function for REACHer CLI."""  # noqa: D401
    assert len(sys.argv[1:]) == 1, 'provide a PMID as an argument'
    pmid = sys.argv[1]

    pmid_content = download_pmid_xml(pmid)
    abstract_text = extract_abstract(pmid_content)
    if abstract_text:
        reach_json = reach_extract(abstract_text)

        print_reach_statistics(reach_json)

        with open(f'{pmid}.json', 'w') as f:
            print(reach_json, file=f)
    else:
        print('erorr: no abstract text extrated', file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())

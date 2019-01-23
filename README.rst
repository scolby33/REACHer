REACHer
=======
Download an abstract from PubMed with its PMID, extract mentioned pathways with Reach, and save the output JSON.


Installation
------------
This module has not been released to PyPI, so installation is from GitHub:

.. code-block:: sh

    $ pip install git+https://github.com/scolby33/REACHer.git

REACHer supports only Python 3.7 or later.


Usage
-----
REACHer is a simple program: call it with a PubMed ID and a JSON file of Reach results will appear in your working directory.
Basic statistics about the Reach results are printed to stderr.

.. code-block:: sh

    $ ls
    $ reacher 28546431
    events extracted: 7
    number of events of each type:
      'regulation': 2
      'amount': 2
      'protein-modification': 1
      'activation': 2
    $ ls
    28546431.json
    $ head 28546431.json
    {
      "events":{
        "frames":[
          {
            "frame-id":"evem-api37-UAZ-r1-Reach-5-800",
            "text":"ATP levels",
            "arguments":[
              {
                "text":"ATP",
                "argument-type":"entity",

License
-------
MIT. See the :code:`LICENSE.rst` file for the full text of the license.

# coding=utf-8
# Copyright 2020 HuggingFace Datasets Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Lint as: python3
"""Introduction to the CoNLL-2003 Shared Task: Language-Independent Named Entity Recognition"""

import os

import datasets


logger = datasets.logging.get_logger(__name__)


_CITATION = """\
@inproceedings{tjong-kim-sang-de-meulder-2003-introduction,
    title = "Introduction to the {C}o{NLL}-2003 Shared Task: Language-Independent Named Entity Recognition",
    author = "Tjong Kim Sang, Erik F.  and
      De Meulder, Fien",
    booktitle = "Proceedings of the Seventh Conference on Natural Language Learning at {HLT}-{NAACL} 2003",
    year = "2003",
    url = "https://www.aclweb.org/anthology/W03-0419",
    pages = "142--147",
}
"""

_DESCRIPTION = """\
The shared task of CoNLL-2003 concerns language-independent named entity recognition. We will concentrate on
four types of named entities: persons, locations, organizations and names of miscellaneous entities that do
not belong to the previous three groups.
The CoNLL-2003 shared task data files contain four columns separated by a single space. Each word has been put on
a separate line and there is an empty line after each sentence. The first item on each line is a word, the second
a part-of-speech (POS) tag, the third a syntactic chunk tag and the fourth the named entity tag. The chunk tags
and the named entity tags have the format I-TYPE which means that the word is inside a phrase of type TYPE. Only
if two phrases of the same type immediately follow each other, the first word of the second phrase will have tag
B-TYPE to show that it starts a new phrase. A word with tag O is not part of a phrase. Note the dataset uses IOB2
tagging scheme, whereas the original dataset uses IOB1.
For more details see https://www.clips.uantwerpen.be/conll2003/ner/ and https://www.aclweb.org/anthology/W03-0419
"""

### CHANGE THE DIRECTORIES HERE
##_URL = "https://data.deepai.org/conll2003.zip"
_TRAINING_FILE = "data/train.conllu"
_DEV_FILE = "data/validation.conllu"
_TEST_FILE = "data/test.conllu"


class ConlluIndicConfig(datasets.BuilderConfig):
    """BuilderConfig for Conll2003"""

    def __init__(self, **kwargs):
        """BuilderConfig forConll2003.
        Args:
          **kwargs: keyword arguments forwarded to super.
        """
        super(ConlluIndicConfig, self).__init__(**kwargs)


class ConlluIndic(datasets.GeneratorBasedBuilder):


    BUILDER_CONFIGS = [
        ConlluIndicConfig(name="conlluindic", version=datasets.Version("1.0.0"), description="Conllu dataset loader"),
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "id": datasets.Value("string"),
                    "tokens": datasets.Sequence(datasets.Value("string")),
                    "lemmas" : datasets.Sequence(datasets.Value("string")),
                    "upos_tags": datasets.Sequence(
                        datasets.features.ClassLabel(
                            names=[
                                        'ADJ',
                                        'ADP',
                                        'ADV', 
                                        'AUX',  
                                        'CCONJ',
                                        'DET',
                                        'INTJ',
                                        'NOUN',
                                        'NUM',
                                        'PART',
                                        'PRON',
                                        'PROPN',
                                        'PUNCT',
                                        'SCONJ',
                                        'SYM',
                                        'VERB',
                                        'X',
                                        '_' ]
                        )
                    ),
                }
            ),
            supervised_keys=None,
            homepage="https://www.aclweb.org/anthology/W03-0419/",
            citation=_CITATION,
        )

    
    
    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        ##downloaded_file = dl_manager.download_and_extract(_URL)
        data_files = {
            "train": _TRAINING_FILE,
            "dev": _DEV_FILE,
            "test": _TEST_FILE,
        }

        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepath": data_files["train"]}),
            datasets.SplitGenerator(name=datasets.Split.VALIDATION, gen_kwargs={"filepath": data_files["dev"]}),
            datasets.SplitGenerator(name=datasets.Split.TEST, gen_kwargs={"filepath": data_files["test"]}),
        ]
        


    def _generate_examples(self, filepath):
        logger.info("⏳ Generating examples from = %s", filepath)
        with open(filepath, encoding="utf-8") as f:
            guid = 0
            tokens = []
            lemmas = []
            upos_tags = []
            for line in f:
                if line.startswith("-DOCSTART-") or line == "" or line == "\n":
                    if tokens:
                        yield guid, {
                            "id": str(guid),
                            "tokens": tokens,
                            "lemmas": lemmas,
                            "upos_tags": upos_tags,
                        }
                        guid += 1
                        tokens = []
                        lemmas = []
                        upos_tags = []
                elif line.startswith("#"):
                    # Comment
                    continue
                else:
                    # conllu tokens are tab separated
                    splits = line.split('\t')
                    tokens.append(splits[1])
                    lemmas.append(splits[2])
                    upos_tags.append(splits[3])
            # last example
            if tokens:
                yield guid, {
                    "id": str(guid),
                    "tokens": tokens,
                    "lemmas": lemmas,
                    "upos_tags": upos_tags,
                }
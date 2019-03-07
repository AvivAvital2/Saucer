# coding: utf8
from __future__ import unicode_literals

from ....symbols import POS, NOUN, VERB, ADJ, ADV, PRON, DET, AUX, PUNCT, ADP, SCONJ, CCONJ
from ....symbols import VerbForm_inf, VerbForm_none, Number_sing, Degree_pos
from .lookup import LOOKUP

'''
French language lemmatizer applies the default rule based lemmatization
procedure with some modifications for better French language support.

The parts of speech 'ADV', 'PRON', 'DET', 'ADP' and 'AUX' are added to use the 
rule-based lemmatization. As a last resort, the lemmatizer checks in 
the lookup table.
'''

class FrenchLemmatizer(object):
    @classmethod
    def load(cls, path, index=None, exc=None, rules=None, lookup=None):
        return cls(index, exc, rules, lookup)

    def __init__(self, index=None, exceptions=None, rules=None, lookup=None):
        self.index = index
        self.exc = exceptions
        self.rules = rules
        self.lookup_table = lookup if lookup is not None else {}

    def __call__(self, string, univ_pos, morphology=None):
        if not self.rules:
            return [self.lookup_table.get(string, string)]
        if univ_pos in (NOUN, 'NOUN', 'noun'):
            univ_pos = 'noun'
        elif univ_pos in (VERB, 'VERB', 'verb'):
            univ_pos = 'verb'
        elif univ_pos in (ADJ, 'ADJ', 'adj'):
            univ_pos = 'adj'
        elif univ_pos in (ADP, 'ADP', 'adp'):
            univ_pos = 'adp'
        elif univ_pos in (ADV, 'ADV', 'adv'):
            univ_pos = 'adv'
        elif univ_pos in (AUX, 'AUX', 'aux'):
            univ_pos = 'aux'
        elif univ_pos in (CCONJ, 'CCONJ', 'cconj'):
            univ_pos = 'cconj'
        elif univ_pos in (DET, 'DET', 'det'):
            univ_pos = 'det'
        elif univ_pos in (PRON, 'PRON', 'pron'):
            univ_pos = 'pron'
        elif univ_pos in (PUNCT, 'PUNCT', 'punct'):
            univ_pos = 'punct'
        elif univ_pos in (SCONJ, 'SCONJ', 'sconj'):
            univ_pos = 'sconj'
        else:
            return [self.lookup(string)]
        # See Issue #435 for example of where this logic is requied.
        if self.is_base_form(univ_pos, morphology):
            return list(set([string.lower()]))
        lemmas = lemmatize(string, self.index.get(univ_pos, {}),
                           self.exc.get(univ_pos, {}),
                           self.rules.get(univ_pos, []))
        return lemmas

    def is_base_form(self, univ_pos, morphology=None):
        """
        Check whether we're dealing with an uninflected paradigm, so we can
        avoid lemmatization entirely.
        """
        morphology = {} if morphology is None else morphology
        others = [key for key in morphology
                  if key not in (POS, 'Number', 'POS', 'VerbForm', 'Tense')]
        if univ_pos == 'noun' and morphology.get('Number') == 'sing':
            return True
        elif univ_pos == 'verb' and morphology.get('VerbForm') == 'inf':
            return True
        # This maps 'VBP' to base form -- probably just need 'IS_BASE'
        # morphology
        elif univ_pos == 'verb' and (morphology.get('VerbForm') == 'fin' and
                                     morphology.get('Tense') == 'pres' and
                                     morphology.get('Number') is None and
                                     not others):
            return True
        elif univ_pos == 'adj' and morphology.get('Degree') == 'pos':
            return True
        elif VerbForm_inf in morphology:
            return True
        elif VerbForm_none in morphology:
            return True
        elif Number_sing in morphology:
            return True
        elif Degree_pos in morphology:
            return True
        else:
            return False

    def noun(self, string, morphology=None):
        return self(string, 'noun', morphology)

    def verb(self, string, morphology=None):
        return self(string, 'verb', morphology)

    def adj(self, string, morphology=None):
        return self(string, 'adj', morphology)

    def punct(self, string, morphology=None):
        return self(string, 'punct', morphology)

    def lookup(self, string):
        if string in self.lookup_table:
            return self.lookup_table[string][0]
        return string


def lemmatize(string, index, exceptions, rules):
    string = string.lower()
    forms = []
    if (string in index):
        forms.append(string)
        return forms
    forms.extend(exceptions.get(string, []))
    oov_forms = []
    if not forms:
        for old, new in rules:
            if string.endswith(old):
                form = string[:len(string) - len(old)] + new
                if not form:
                    pass
                elif form in index or not form.isalpha():
                    forms.append(form)
                else:
                    oov_forms.append(form)
    if not forms:
        forms.extend(oov_forms)
    if not forms and string in LOOKUP.keys():
        forms.append(LOOKUP[string][0])
    if not forms:
        forms.append(string)
    return list(set(forms))

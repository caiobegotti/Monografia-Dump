# http://stackoverflow.com/questions/6849600/does-anyone-have-a-categorized-xml-corpus-reader-for-nltk

# standard nltk classes
from nltk.corpus.reader import CategorizedCorpusReader
from nltk.corpus.reader import XMLCorpusReader

# stopwords (i.e. latin ones)
from nltk.corpus import stopwords

# for CategorizedCorpusReader's init
from nltk.compat import defaultdict

# punctuations load
import string

class MyCategorizedCorpusReader(CategorizedCorpusReader):
    def _init(self):
        self._f2c = defaultdict(set)
        self._c2f = defaultdict(set)

        if self._pattern is not None:
            for file_id in self._fileids:
                category = re.match(self._pattern, file_id).group(1)
                self._add(file_id, category)

        elif self._map is not None:
            for (file_id, categories) in self._map.items():
                for category in categories:
                    self._add(file_id, category)

        elif self._file is not None:
            for line in self.open(self._file).readlines():
                line = line.strip()
                file_id, categories = line.split(self._delimiter, 1)
                # https://github.com/nltk/nltk/issues/250
                #if file_id not in self.fileids():
                #    raise ValueError('In category mapping file %s: %s '
                #                     'not found' % (self._file, file_id))
                for category in categories.split(self._delimiter):
                    self._add(file_id, category)


class CategorizedXMLCorpusReader(MyCategorizedCorpusReader, XMLCorpusReader):
    def __init__(self, *args, **kwargs):
        MyCategorizedCorpusReader.__init__(self, kwargs)
        XMLCorpusReader.__init__(self, *args, **kwargs)

    def _resolve(self, fileids, categories):
        if fileids is not None and categories is not None:
            raise ValueError('Specify fileids or categories, not both')
        if categories is not None:
            return self.fileids(categories)
        else:
            return fileids

    def raw(self, fileids=None, categories=None):
        return XMLCorpusReader.raw(self, self._resolve(fileids, categories))

    def words(self, fileids=None, categories=None):
        words = []
        fileids = self._resolve(fileids, categories)
        for fileid in fileids:
            words += XMLCorpusReader.words(self, fileid)
        return words

    def text(self, fileids=None, categories=None):
        fileids = self._resolve(fileids, categories)
        text = ""
        for fileid in fileids:
            for i in self.xml(fileid).getiterator():
                if i.text:
                    text += i.text
        return text

    def sents(self, fileids=None, categories=None):
        text = self.words(fileids, categories)
        sents = nltk.PunktSentenceTokenizer().tokenize(text)
        return sents

    def paras(self, fileids=None, categories=None):
        return CategorizedCorpusReader.paras(self, self._resolve(fileids, categories))


def stopless(wordslist):
    stop = stopwords.words('latin')
    filtered = [x for x in wordslist if x not in stop]
    return filtered

def punctless(wordslist):
    punct = string.punctuation
    
    punct += u'\u00a7' # SECTION SIGN
    punct += u'\u00b3' # SUPERSCRIPT THREE
    punct += u'\u00b2' # SUPERSCRIPT TWO
    punct += u'\u00b7' # MIDDLE DOT
    punct += u'\u00b9' # SUPERSCRIPT ONE
    punct += u'\u2014' # EM DASH
    punct += u'\u2019' # RIGHT SINGLE QUOTATION MARK
    punct += u'\u2020' # DAGGER
    punct += u'\u2184' # LATIN SMALL LETTER REVERSED C
    punct += u'\u221e' # INFINITY
    punct += u'\u23d1' # METRICAL BREVE

    punctuation = list(punct)

    words = []
    for w in wordslist:
        if w.isalpha():
            words.append(w)

    filtered = [x for x in words if x not in punctuation]
    return filtered

def ciceroabbr(filename):
    return {
        'cicero_academica.xml': 'Ac',
        'cicero_arati_phaenomena.xml': 'AratPhaen',
        'cicero_arati_prognostica.xml': 'AratProgn',
        'cicero_brutus.xml': 'Brut',
        'cicero_carmina_fragmenta.xml': 'CarFrr',
        'cicero_cato_maior_de_senectute.xml': 'Sen',
        'cicero_commentarii_causarum.xml': 'CommCaus',
        'cicero_de_divinatione.xml': 'Div',
        'cicero_de_domo_sua.xml': 'Dom',
        'cicero_de_fato.xml': 'Fat',
        'cicero_de_finibus.xml': 'Fin',
        'cicero_de_haruspicum_responso.xml': 'Har',
        'cicero_de_inventione.xml': 'Inv',
        'cicero_de_iure_civ_in_artem_redig.xml': 'IurCiv',
        'cicero_de_lege_agraria.xml': 'Agr',
        'cicero_de_legibus.xml': 'Leg',
        'cicero_de_natura_deorum.xml': 'ND',
        'cicero_de_officiis.xml': 'Off',
        'cicero_de_optimo_genere_oratorum.xml': 'OptGen',
        'cicero_de_oratore.xml': 'DeOrat',
        'cicero_de_partitione_oratoria.xml': 'Part',
        'cicero_de_provinciis_consularibus.xml': 'Prov',
        'cicero_de_republica.xml': 'Rep',
        'cicero_epistula_ad_octavianum_sp.xml': 'EpOct',
        'cicero_epistulae_ad_atticum.xml': 'Att',
        'cicero_epistulae_ad_brutum.xml': 'AdBrut',
        'cicero_epistulae_ad_familiares.xml': 'Fam',
        'cicero_epistulae_ad_quintum_fratrem.xml': 'Qfr',
        'cicero_epistulae_fragmenta.xml': 'EpFrr',
        'cicero_facete_dicta.xml': 'Facet',
        'cicero_hortensius.xml': 'Hort',
        'cicero_in_catilinam.xml': 'Catil',
        'cicero_in_pisonem.xml': 'Pis',
        'cicero_in_q_caecilium.xml': 'DivCaec',
        'cicero_in_sallustium_sp.xml': 'Sal',
        'cicero_in_vatinium.xml': 'Vat',
        'cicero_in_verrem.xml': 'Ver',
        'cicero_incertorum_librorum_fragmenta.xml': 'LibFrr',
        'cicero_laelius_de_amicitia.xml': 'Amic',
        'cicero_lucullus.xml': 'Luc',
        'cicero_orationum_deperditarum_frr.xml': 'DepFrr',
        'cicero_orationum_incertarum_frr.xml': 'IncFrr',
        'cicero_orator.xml': 'Orat',
        'cicero_paradoxa_stoicorum.xml': 'Parad',
        'cicero_philippicae.xml': 'Phil',
        'cicero_philosophicorum_librorum_frr.xml': 'PhilFrr',
        'cicero_post_reditum_ad_populum.xml': 'RedPop',
        'cicero_post_reditum_in_senatu.xml': 'RedSen',
        'cicero_pro_archia.xml': 'Arch',
        'cicero_pro_balbo.xml': 'Balb',
        'cicero_pro_caecina.xml': 'Caec',
        'cicero_pro_caelio.xml': 'Cael',
        'cicero_pro_cluentio.xml': 'Clu',
        'cicero_pro_flacco.xml': 'Flac',
        'cicero_pro_fonteio.xml': 'Font',
        'cicero_pro_lege_manilia.xml': 'Man',
        'cicero_pro_ligario.xml': 'Lig',
        'cicero_pro_marcello.xml': 'Marc',
        'cicero_pro_milone.xml': 'Mil',
        'cicero_pro_murena.xml': 'Mur',
        'cicero_pro_plancio.xml': 'Planc',
        'cicero_pro_q_roscio_comoedo.xml': 'QRosc',
        'cicero_pro_quinctio.xml': 'Quinct',
        'cicero_pro_rabirio_perduellionis_reo.xml': 'RabPerd',
        'cicero_pro_rabirio_postumo.xml': 'RabPost',
        'cicero_pro_rege_deiotaro.xml': 'Deiot',
        'cicero_pro_s_roscio_amerino.xml': 'SRosc',
        'cicero_pro_scauro.xml': 'Scaur',
        'cicero_pro_sestio.xml': 'Sest',
        'cicero_pro_sulla.xml': 'Sul',
        'cicero_pro_tullio.xml': 'Tul',
        'cicero_rhetorica_ad_herennium_sp.xml': 'RhetHer',
        'cicero_timaeus.xml': 'Tim',
        'cicero_topica.xml': 'Top',
        'cicero_tusculanae_disputationes.xml': 'Tusc',
    }.get(filename, 'Cic')

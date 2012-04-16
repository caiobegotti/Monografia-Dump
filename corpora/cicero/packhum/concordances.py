#!/usr/bin/env python
# -*- coding: utf-8 -*-
# caio begotti <caio1982@gmail.com>
# this is under public domain

import glob
import optparse

from nltk.tokenize import word_tokenize
from nltk.corpus.reader import XMLCorpusReader
from nltk import Text

def lookup():
    parser = optparse.OptionParser("Usage: %prog [options]")
    parser.add_option("-l", "--lookup", type="string", dest="term",
                      help="look up concordances for a word")
    parser.add_option("-f", "--fake", action="store_true", dest="fake",
                      default=False, help="considers non-ciceronian texts")
    parser.add_option("-w", "--width", type="int", dest="width",
                      default=150, help="width of the context data")
    parser.add_option("-c", "--count", type="int", dest="count",
                      default=25, help="how many matches to display")
 
    (options, args) = parser.parse_args()
    if options.term is None:
        parser.print_help()
        exit(-1)
    else:
        content = corpora_loader(fake=options.fake)
        text = content.concordance(options.term, width=options.width, lines=options.count)
        print text

def corpora_loader(fake):
    ciceronian = [
                  'academica.xml', 'arati_phaenomena.xml',
                  'arati_prognostica.xml', 'brutus.xml', 'carmina_fragmenta.xml',
                  'cato_maior_de_senectute.xml', 'commentarii_causarum.xml',
                  'de_divinatione.xml', 'de_domo_sua.xml', 'de_fato.xml',
                  'de_finibus.xml', 'de_haruspicum_responso.xml',
                  'de_inventione.xml', 'de_iure_civ_in_artem_redig.xml',
                  'de_lege_agraria.xml', 'de_legibus.xml',
                  'de_natura_deorum.xml', 'de_officiis.xml',
                  'de_optimo_genere_oratorum.xml', 'de_oratore.xml',
                  'de_partitione_oratoria.xml', 'de_provinciis_consularibus.xml',
                  'de_republica.xml', 'epistulae_ad_atticum.xml',
                  'epistulae_ad_brutum.xml', 'epistulae_ad_familiares.xml',
                  'epistulae_ad_quintum_fratrem.xml', 'facete_dicta.xml',
                  'hortensius.xml', 'in_catilinam.xml', 'in_pisonem.xml',
                  'in_q_caecilium.xml', 'in_vatinium.xml', 'in_verrem.xml',
                  'incertorum_librorum_fragmenta.xml', 'laelius_de_amicitia.xml',
                  'lucullus.xml', 'orationum_deperditarum_frr.xml',
                  'orationum_incertarum_frr.xml', 'orator.xml', 'paradoxa_stoicorum.xml',
                  'philippicae.xml', 'philosophicorum_librorum_frr.xml',
                  'post_reditum_ad_populum.xml', 'post_reditum_in_senatu.xml',
                  'pro_archia.xml', 'pro_balbo.xml', 'pro_caecina.xml',
                  'pro_caelio.xml', 'pro_cluentio.xml', 'pro_flacco.xml',
                  'pro_fonteio.xml', 'pro_lege_manilia.xml', 'pro_ligario.xml',
                  'pro_marcello.xml', 'pro_milone.xml', 'pro_murena.xml',
                  'pro_plancio.xml', 'pro_q_roscio_comoedo.xml', 'pro_quinctio.xml',
                  'pro_rabirio_perduellionis_reo.xml', 'pro_rabirio_postumo.xml',
                  'pro_rege_deiotaro.xml', 'pro_s_roscio_amerino.xml', 'pro_scauro.xml',
                  'pro_sestio.xml', 'pro_sulla.xml', 'pro_tullio.xml',
                  'timaeus.xml', 'topica.xml', 'tusculanae_disputationes.xml']

    spurious = ['epistulae_fragmenta.xml', 'epistula_ad_octavianum_sp.xml',
                'in_sallustium_sp.xml', 'rhetorica_ad_herennium_sp.xml']

    list = ciceronian
    if fake is True:
        list = list + spurious

    data = ''
    for loop in list:
        reader = XMLCorpusReader('./', loop)
        data = Text(reader.words())
    return data

if __name__ == "__main__":
    lookup()

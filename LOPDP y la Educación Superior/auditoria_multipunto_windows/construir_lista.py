# -*- coding: utf-8 -*-
"""Construye universidades.json a partir de los reportes del proyecto."""
import json

ISO = {"EE.UU.":"US","Reino Unido":"GB","Suiza":"CH","China":"CN","Canadá":"CA",
       "Singapur":"SG","Japón":"JP","Alemania":"DE","Australia":"AU","Francia":"FR",
       "Hong Kong":"HK","Corea del Sur":"KR","Suecia":"SE","Países Bajos":"NL","Bélgica":"BE"}

MUNDO = [
 ("Massachusetts Institute of Technology","MIT","EE.UU.","https://www.mit.edu"),
 ("Stanford University","Stanford","EE.UU.","https://www.stanford.edu"),
 ("Harvard University","Harvard","EE.UU.","https://www.harvard.edu"),
 ("University of Oxford","Oxford","Reino Unido","https://www.ox.ac.uk"),
 ("University of Cambridge","Cambridge","Reino Unido","https://www.cam.ac.uk"),
 ("California Institute of Technology","Caltech","EE.UU.","https://www.caltech.edu"),
 ("University of California, Berkeley","UC Berkeley","EE.UU.","https://www.berkeley.edu"),
 ("Princeton University","Princeton","EE.UU.","https://www.princeton.edu"),
 ("Imperial College London","Imperial","Reino Unido","https://www.imperial.ac.uk"),
 ("University of Chicago","U Chicago","EE.UU.","https://www.uchicago.edu"),
 ("ETH Zurich","ETH Zurich","Suiza","https://ethz.ch"),
 ("Yale University","Yale","EE.UU.","https://www.yale.edu"),
 ("University of Pennsylvania","UPenn","EE.UU.","https://www.upenn.edu"),
 ("University College London","UCL","Reino Unido","https://www.ucl.ac.uk"),
 ("Cornell University","Cornell","EE.UU.","https://www.cornell.edu"),
 ("Tsinghua University","Tsinghua","China","https://www.tsinghua.edu.cn/en/"),
 ("Peking University","Peking","China","https://english.pku.edu.cn"),
 ("Johns Hopkins University","Johns Hopkins","EE.UU.","https://www.jhu.edu"),
 ("Columbia University","Columbia","EE.UU.","https://www.columbia.edu"),
 ("University of Toronto","Toronto","Canadá","https://www.utoronto.ca"),
 ("University of California, Los Angeles","UCLA","EE.UU.","https://www.ucla.edu"),
 ("National University of Singapore","NUS","Singapur","https://nus.edu.sg"),
 ("The University of Tokyo","U Tokyo","Japón","https://www.u-tokyo.ac.jp/en/"),
 ("Technical University of Munich","TUM","Alemania","https://www.tum.de/en/"),
 ("The University of Melbourne","Melbourne","Australia","https://www.unimelb.edu.au"),
 ("University of Edinburgh","Edinburgh","Reino Unido","https://www.ed.ac.uk"),
 ("EPFL","EPFL","Suiza","https://www.epfl.ch/en/"),
 ("University of Michigan-Ann Arbor","Michigan","EE.UU.","https://umich.edu"),
 ("Northwestern University","Northwestern","EE.UU.","https://www.northwestern.edu"),
 ("Fudan University","Fudan","China","https://www.fudan.edu.cn/en/"),
 ("PSL University","PSL","Francia","https://www.psl.eu/en"),
 ("University of Hong Kong","HKU","Hong Kong","https://www.hku.hk"),
 ("Zhejiang University","Zhejiang","China","https://www.zju.edu.cn/english/"),
 ("New York University","NYU","EE.UU.","https://www.nyu.edu"),
 ("Shanghai Jiao Tong University","SJTU","China","https://www.sjtu.edu.cn"),
 ("King's College London","KCL","Reino Unido","https://www.kcl.ac.uk"),
 ("University of California, San Diego","UCSD","EE.UU.","https://www.ucsd.edu"),
 ("LMU Munich","LMU","Alemania","https://www.lmu.de"),
 ("Duke University","Duke","EE.UU.","https://www.duke.edu"),
 ("University of Manchester","Manchester","Reino Unido","https://www.manchester.ac.uk"),
 ("University of British Columbia","UBC","Canadá","https://www.ubc.ca"),
 ("The University of Sydney","Sydney","Australia","https://www.sydney.edu.au"),
 ("Université Paris-Saclay","Paris-Saclay","Francia","https://www.universite-paris-saclay.fr/en"),
 ("Kyoto University","Kyoto","Japón","https://www.kyoto-u.ac.jp/en"),
 ("University of Illinois Urbana-Champaign","Illinois","EE.UU.","https://illinois.edu"),
 ("The University of Texas at Austin","UT Austin","EE.UU.","https://www.utexas.edu"),
 ("University of Washington","UW","EE.UU.","https://www.washington.edu"),
 ("Nanyang Technological University","NTU","Singapur","https://www.ntu.edu.sg"),
 ("McGill University","McGill","Canadá","https://www.mcgill.ca"),
 ("The Chinese University of Hong Kong","CUHK","Hong Kong","https://www.cuhk.edu.hk/english/index.html"),
 ("Carnegie Mellon University","CMU","EE.UU.","https://www.cmu.edu"),
 ("University of Wisconsin-Madison","Wisconsin","EE.UU.","https://www.wisc.edu"),
 ("University of Science and Technology of China","USTC","China","https://en.ustc.edu.cn"),
 ("Washington University in St. Louis","WUSTL","EE.UU.","https://washu.edu"),
 ("Monash University","Monash","Australia","https://www.monash.edu"),
 ("Seoul National University","SNU","Corea del Sur","https://en.snu.ac.kr"),
 ("Heidelberg University","Heidelberg","Alemania","https://www.uni-heidelberg.de/en"),
 ("Hong Kong University of Science and Technology","HKUST","Hong Kong","https://hkust.edu.hk/"),
 ("Karolinska Institutet","Karolinska","Suecia","https://ki.se/en"),
 ("Delft University of Technology","TU Delft","Países Bajos","https://www.tudelft.nl/en/"),
 ("Australian National University","ANU","Australia","https://www.anu.edu.au/"),
 ("KU Leuven","KU Leuven","Bélgica","https://www.kuleuven.be/english/"),
 ("The University of Queensland","Queensland","Australia","https://www.uq.edu.au/"),
]

ECUADOR = [
 ("Escuela Politécnica Nacional","EPN","Pública","https://www.epn.edu.ec"),
 ("Escuela Superior Politécnica del Litoral","ESPOL","Pública","https://www.espol.edu.ec"),
 ("Escuela Superior Politécnica de Chimborazo","ESPOCH","Pública","https://www.espoch.edu.ec"),
 ("Escuela Superior Politécnica Agropecuaria de Manabí Manuel Félix López","ESPAM MFL","Pública","https://www.espam.edu.ec"),
 ("Universidad de las Fuerzas Armadas ESPE","ESPE","Pública","https://www.espe.edu.ec"),
 ("Universidad Central del Ecuador","UCE","Pública","https://www.uce.edu.ec"),
 ("Universidad de Cuenca","UCuenca","Pública","https://www.ucuenca.edu.ec"),
 ("Universidad de Guayaquil","UG","Pública","https://www.ug.edu.ec"),
 ("Universidad Nacional de Loja","UNL","Pública","https://www.unl.edu.ec"),
 ("Universidad Agraria del Ecuador","UAE","Pública","https://www.uagraria.edu.ec"),
 ("Universidad Técnica de Ambato","UTA","Pública","https://uta.edu.ec"),
 ("Universidad Técnica de Babahoyo","UTB","Pública","https://utb.edu.ec"),
 ("Universidad Técnica de Cotopaxi","UTC","Pública","https://www.utc.edu.ec"),
 ("Universidad Técnica de Machala","UTMACH","Pública","https://www.utmachala.edu.ec"),
 ("Universidad Técnica de Manabí","UTM","Pública","https://www.utm.edu.ec"),
 ("Universidad Técnica del Norte","UTN","Pública","https://www.utn.edu.ec"),
 ("Universidad Técnica Estatal de Quevedo","UTEQ","Pública","https://www.uteq.edu.ec"),
 ("Universidad Técnica Luis Vargas Torres de Esmeraldas","UTELVT","Pública","https://www.utelvt.edu.ec"),
 ("Universidad Estatal de Bolívar","UEB","Pública","https://www.ueb.edu.ec"),
 ("Universidad Estatal del Sur de Manabí","UNESUM","Pública","https://unesum.edu.ec"),
 ("Universidad Estatal de Milagro","UNEMI","Pública","https://www.unemi.edu.ec"),
 ("Universidad Estatal Amazónica","UEA","Pública","https://www.uea.edu.ec"),
 ("Universidad Estatal Península de Santa Elena","UPSE","Pública","https://www.upse.edu.ec"),
 ("Universidad Laica Eloy Alfaro de Manabí","ULEAM","Pública","https://www.uleam.edu.ec"),
 ("Universidad Nacional de Chimborazo","UNACH","Pública","https://www.unach.edu.ec"),
 ("Universidad Nacional de Educación","UNAE","Pública","https://unae.edu.ec"),
 ("Universidad Politécnica Estatal del Carchi","UPEC","Pública","https://upec.edu.ec"),
 ("Universidad de Investigación de Tecnología Experimental Yachay","Yachay Tech","Pública","https://yachaytech.edu.ec"),
 ("Universidad Regional Amazónica Ikiam","Ikiam","Pública","https://www.ikiam.edu.ec"),
 ("Universidad de las Artes","UArtes","Pública","https://www.uartes.edu.ec"),
 ("Universidad Intercultural de las Nacionalidades y Pueblos Indígenas Amawtay Wasi","Amawtay Wasi","Pública","https://uaw.edu.ec"),
 ("Universidad de Seguridad Ciudadana y Ciencias Policiales","USECIPOL","Pública","https://usecipol.edu.ec"),
 ("Instituto de Altos Estudios Nacionales","IAEN","Pública","https://www.iaen.edu.ec"),
 ("Universidad Andina Simón Bolívar, sede Ecuador","UASB","Pública","https://www.uasb.edu.ec"),
 ("FLACSO Ecuador","FLACSO","Pública","https://www.flacso.edu.ec"),
 ("Pontificia Universidad Católica del Ecuador","PUCE","Cofinanciada","https://www.puce.edu.ec"),
 ("Universidad Católica de Santiago de Guayaquil","UCSG","Cofinanciada","https://www.ucsg.edu.ec"),
 ("Universidad Católica de Cuenca","UCACUE","Cofinanciada","https://www.ucacue.edu.ec"),
 ("Universidad Laica Vicente Rocafuerte de Guayaquil","ULVR","Cofinanciada","https://www.ulvr.edu.ec"),
 ("Universidad Técnica Particular de Loja","UTPL","Cofinanciada","https://www.utpl.edu.ec"),
 ("Universidad UTE","UTE","Cofinanciada","https://ute.edu.ec"),
 ("Universidad del Azuay","UDA","Cofinanciada","https://www.uazuay.edu.ec"),
 ("Universidad Politécnica Salesiana","UPS","Cofinanciada","https://www.ups.edu.ec"),
 ("Universidad Internacional SEK","UISEK","Autofinanciada","https://uisek.edu.ec"),
 ("Universidad de Especialidades Espíritu Santo","UEES","Autofinanciada","https://uees.edu.ec"),
 ("Universidad San Francisco de Quito","USFQ","Autofinanciada","https://www.usfq.edu.ec"),
 ("Universidad de las Américas","UDLA","Autofinanciada","https://www.udla.edu.ec"),
 ("Universidad Internacional del Ecuador","UIDE","Autofinanciada","https://www.uide.edu.ec"),
 ("Universidad Regional Autónoma de los Andes","UNIANDES","Autofinanciada","https://www.uniandes.edu.ec"),
 ("Universidad del Pacífico Escuela de Negocios","UPACÍFICO","Autofinanciada","https://upacifico.edu.ec"),
 ("Universidad Tecnológica Indoamérica","UTI","Autofinanciada","https://www.indoamerica.edu.ec"),
 ("Universidad Casa Grande","Casa Grande","Autofinanciada","https://www.casagrande.edu.ec"),
 ("Universidad Tecnológica Empresarial de Guayaquil","UTEG","Autofinanciada","https://www.uteg.edu.ec"),
 ("Universidad Tecnológica Israel","UISRAEL","Autofinanciada","https://www.uisrael.edu.ec"),
 ("Universidad de Especialidades Turísticas","UDET","Autofinanciada","https://www.udet.edu.ec"),
 ("Universidad Metropolitana del Ecuador","UMET","Autofinanciada","https://umet.edu.ec"),
 ("Universidad de Otavalo","U. Otavalo","Autofinanciada","https://www.uotavalo.edu.ec"),
 ("Universidad San Gregorio de Portoviejo","USGP","Autofinanciada","https://www.sangregorio.edu.ec"),
 ("Universidad de los Hemisferios","U. Hemisferios","Autofinanciada","https://www.uhemisferios.edu.ec"),
 ("Universidad Iberoamericana del Ecuador","UNIB.E","Autofinanciada","https://unibe.edu.ec"),
 ("Universidad Tecnológica Ecotec","ECOTEC","Autofinanciada","https://ecotec.edu.ec"),
 ("Universidad del Río","UDR","Autofinanciada","https://udr.edu.ec"),
 ("Universidad Bolivariana del Ecuador","UBE","Autofinanciada","https://ube.edu.ec"),
]

lista, i = [], 0
for nombre, sigla, pais, url in MUNDO:
    i += 1
    lista.append({"id": i, "grupo": "mundo", "sigla": sigla,
                  "pais": ISO[pais], "url": url, "nombre": nombre})
for nombre, sigla, tipo, url in ECUADOR:
    i += 1
    lista.append({"id": i, "grupo": "ecuador", "sigla": sigla,
                  "pais": "EC", "url": url, "nombre": nombre, "tipo": tipo})

with open("universidades.json", "w", encoding="utf-8") as fh:
    json.dump(lista, fh, ensure_ascii=False, indent=1)

# --- Verificaciones ---
assert len(lista) == 126, len(lista)
assert len({x["id"] for x in lista}) == 126
assert len({x["url"] for x in lista}) == 126, "URL duplicada"
assert sum(1 for x in lista if x["grupo"] == "mundo") == 63
assert sum(1 for x in lista if x["grupo"] == "ecuador") == 63
from collections import Counter
c = Counter(x["pais"] for x in lista if x["grupo"] == "mundo")
print("Total:", len(lista), "| mundo:", 63, "| ecuador:", 63)
print("Paises del grupo mundo:", dict(sorted(c.items(), key=lambda t: -t[1])))
print("Suma:", sum(c.values()))
esperado = {"US":24,"GB":7,"CN":6,"AU":5,"DE":3,"HK":3,"CA":3,"CH":2,"FR":2,"SG":2,"JP":2,"SE":1,"NL":1,"BE":1,"KR":1}
print("Coincide con el anexo del articulo:", dict(c) == esperado)
UE = {"DE","FR","NL","BE","SE"}
print("Instituciones en la UE (para --paises):", sorted(x["sigla"] for x in lista if x["pais"] in UE))
print("Reino Unido (GB):", sorted(x["sigla"] for x in lista if x["pais"]=="GB"))
print("Suiza (CH, no UE pero europea):", sorted(x["sigla"] for x in lista if x["pais"]=="CH"))

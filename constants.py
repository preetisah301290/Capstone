import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')

csv_path = "DataCSV/"
pickle_path = "DataPickle/"
plot_path = "DataPlots/"
input_path = "DataInput/"
buddhist_link = "https://www.accesstoinsight.org/lib/study/truths.html"
taoteching_input_file = "TaoTeChing.txt"
stop_words = set(stopwords.words('english'))
upnishad_file="Upnishads.txt"
upnishad_studyline=[(334,579),(675,979),(986,1322),(1329,1552),(1558,1731),(1737,1874),(1880,2088),(2150,2257),(2263,2375),(2380,2485),(2491,2589)]
yogasutra_file="YogaSutra.txt"
yogasutra_studyline=[(127,703),(748,1538),(1623,2597),(2635,3370)]
BookProverb_file="BookProverb.txt"
BookProverb_studyline=[(96,195),(195,260),(260,359),(359,441),(441,509),(509,619),(619,697),(697,798),(798,853),(853,952),
                       (952,1045),(1045,1133),(1133,1211),(1133,1317),(1317,1419),(1419,1527),(1527,1612),(1612,1688),(1688,1778),(1778,1868),
                       (1868,1962),(1962,2050),(2050,2154),(2154,2255),(2255,2350),(2350,2442),(2442,2526),(2526,2613),(2613,2694),
                       (2694,2821),(2821,2923)]
BookEcclesiastes_file = "BookEcclesiastes.txt"
BookEcclesiastes_studyline=[(97,159),(159,254),(254,337),(337,398),(398,468),(468,509),(509,623),(623,699),
                            (699,781),(781,847),(847,897),(897,955)]
BookEccleasiasticus_file ="BookEccleasiasticus.txt"
BookEccleasiasticus_studyline = [(133,253),(253,327),(327,435),(435,549),(549,609),(609,725),(725,855),(855,922),(922,1001),
                                 (1001,1114),(1114,1230),(1230,1293),(1293,1394),(1394,1486),(1486,1558),(1558,1664),(1664,1770),
                                 (1770,1878),(1878,1971),(1971,2075),(2075,2175),(2175,2283),(2283,2421),(2421,2572),(2572,2676),
                                 (2676,2770),(2770,2877),(2877,2974),(2974,3083),(3083,3170),(3170,3292),(3292,3381),(3381,3496),
                                 (3496,3596),(3596,3676),(3676,3766),(3766,3876),(3876,4009),(4009,4140),(4140,4243),(4243,4337),
                                 (4337,4431),(4431,4548),(4548,4637),(4637,4742),(4742,4827),(4827,5020),(5020,5089),(5089,5202),
                                 (5202,5317)]
BookWisdom_file = "BookWisdom.txt"
BookWisdom_studyline=[(106,164),(164,248),(248,312),(312,381),(381,468),(468,556),(556,654),(654,729),(729,795),(795,892),
                      (892,1002),(1002,1106),(1106,1179),(1179,1289),(1289,1365),(1365,1479),(1479,1558),(1558,1669),
                      (1669,1755)]

romanNumeralMap = (('M',  1000),
                   ('CM', 900),
                   ('D',  500),
                   ('CD', 400),
                   ('C',  100),
                   ('XC', 90),
                   ('L',  50),
                   ('XL', 40),
                   ('X',  10),
                   ('IX', 9),
                   ('V',  5),
                   ('IV', 4),
                   ('I',  1))

def toRoman(n):
    """convert integer to Roman numeral"""
    result = ""
    for numeral, integer in romanNumeralMap:
        while n >= integer:
            result += numeral
            n -= integer
    return result

roman_numeral=[toRoman(i) for i in range(1,30)]

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
yogasutra_studyline=[(129,703),(752,1538),(1627,2597),(2638,3370)]
BookProverb_file="BookProverb.txt"
BookProverb_studyline=[(99,195),(198,260),(263,359),(362,441),(444,509),(512,619),(622,697),(700,798),(801,853),(856,952),
                       (955,1045),(1048,1133),(1136,1211),(1214,1317),(1320,1419),(1422,1527),(1530,1612),(1615,1688),(1691,1778),(1781,1868),
                       (1871,1962),(1965,2050),(2053,2154),(2157,2255),(2258,2350),(2353,2442),(2445,2526),(2529,2613),(2616,2694),
                       (2697,2821),(2824,2923)]
BookEcclesiastes_file = "BookEcclesiastes.txt"
BookEcclesiastes_studyline=[(100,159),(162,254),(257,337),(340,398),(401,468),(471,509),(512,623),(626,699),
                            (702,781),(784,847),(850,897),(891,955)]
BookEccleasiasticus_file ="BookEccleasiasticus.txt"
BookEccleasiasticus_studyline = [(136,253),(256,327),(330,435),(438,549),(552,609),(612,725),(728,855),(858,922),(925,1001),
                                 (1004,1114),(1117,1230),(1233,1293),(1296,1394),(1397,1486),(1489,1558),(1561,1664),(1667,1770),
                                 (1773,1878),(1881,1971),(1974,2075),(2078,2175),(2178,2283),(2285,2421),(2424,2572),(2575,2676),
                                 (2679,2770),(2773,2877),(2880,2974),(2977,3083),(3086,3170),(3173,3292),(3295,3381),(3384,3496),
                                 (3499,3596),(3599,3676),(3679,3766),(3769,3876),(3879,4009),(4012,4140),(4143,4243),(4246,4337),
                                 (4340,4431),(4434,4548),(4551,4637),(4640,4742),(4745,4827),(4830,5020),(5023,5089),(5092,5202),
                                 (5205,5317)]
BookWisdom_file = "BookWisdom.txt"
BookWisdom_studyline=[(109,164),(167,248),(251,312),(315,381),(384,468),(471,556),(559,654),(657,729),(732,795),(798,892),
                      (895,1002),(1005,1106),(1109,1179),(1182,1289),(1292,1365),(1368,1479),(1482,1558),(1561,1669),
                      (1672,1755)]

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

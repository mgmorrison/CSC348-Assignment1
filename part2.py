# en/decode using caesar cipher with symbols alphabet
def caesar_cipher(message, shift, encrypt):

    # initialize variables
    symbols = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ '
    sym_len = len(symbols)
    new_message = ''

    # convert message to uppercase to correspond with symbols
    message = message.upper()

    # loop through each character in message
    for ch in message:
        # shift characters up by shift places to encrypt
        if encrypt:
            new_message += symbols[(symbols.index(ch) + shift) % sym_len]
        # shift characters down by shift places to decrypt
        else:
            new_message += symbols[(symbols.index(ch) - shift) % sym_len]

    return new_message


# en/decode using vigenere cipher with symbols alphabet
def vigenere_cipher(message, keyword, encrypt):

    # initialize variables
    symbols = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ '
    new_message = ''

    # convert to uppercase to correspond with symbols
    message = message.upper()
    keyword = keyword.upper()

    # call caesar_cipher method for each character in message with corresponding keyword character
    for i in range(len(message)):
        new_message += caesar_cipher(message[i], symbols.index(keyword[i % len(keyword)]), encrypt)

    return new_message


# compute frequency analysis of a message -- used in get_caesar_shift
def frequency_analysis(message):

    # initialize variables
    symbols = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ '
    new_freq = {}

    # convert message to uppercase to correspond with symbols
    message = message.upper()

    # find character ratio of message for each character
    for ch in symbols:
        new_freq[ch] = message.count(ch) / len(message)

    return new_freq


# calculate cross correlation between 2 data sets
def cross_correlation(data1, data2):

    # initialize correlation
    corr = 0

    # loop through each character's frequency for data1, data2 and sum into corr
    for ch in data1.keys():
        corr += data1[ch] * data2[ch]

    return corr


# solve for shift of a message encrypted by caesar cipher
def get_caesar_shift(enc_message, expected_dist):

    # initialize variables
    symbols = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ '
    sym_len = len(symbols)
    correlation = [0] * sym_len
    shift = []

    # convert message to uppercase to correspond with symbols
    enc_message = enc_message.upper()

    # find distribution of encoded message
    enc_dist = frequency_analysis(enc_message)

    # loop through each possible shift length
    for i in range(sym_len):
        # create new shifted distribution for each symbol
        F = {}
        for j in range(sym_len):
            # shift distribution of letters to the left by i
            F[symbols[j]] = expected_dist[symbols[(j - i) % sym_len]]

        # calculation correlation between shifted dist and encoded dist
        correlation[i] = cross_correlation(F, enc_dist)

    # add all potential shifts to array from most to least probable
    # shift array is helpful when most likely shift does not work
    for i in range(sym_len):
        shift.append(correlation.index(max(correlation)))
        correlation[correlation.index(max(correlation))] = -1

    # return most probable shift
    return shift[0]


# solve for keyword of a message encrypted by vigenere cipher
def get_vigenere_keyword(enc_message, size, expected_dist):

    # initialize variables
    symbols = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ '
    div_message = [''] * size
    shifts = []
    keyword = ''

    # divide message into segments of length size
    for i in range(len(enc_message)):
        div_message[i % size] += enc_message[i]

    # find most probable shift for each column of div_message
    for i in range(size):
        shifts.append(get_caesar_shift(div_message[i], expected_dist))

    # append shifts to form keyword
    for shift in shifts:
        keyword += symbols[shift]

    return keyword


if __name__ == '__main__':

    # initialize dict of english character distribution
    english_dist = {
        ' ': .1828846265, 'E': .1026665037, 'T': .0751699827, 'A': .0653216702, 'O': .0615957725, 'N': .0571201113,
        'I': .0566844326, 'S': .0531700534, 'R': .0498790855, 'H': .0497856396, 'L': .0331754796, 'D': .0328292310,
        'U': .0227579536, 'C': .0223367596, 'M': .0202656783, 'F': .0198306716, 'W': .0170389377, 'G': .0162490441,
        'P': .0150432428, 'Y': .0142766662, 'B': .0125888074, 'V': 0.0079611644, 'K': 0.0056096272, 'X': 0.0014092016,
        'J': 0.0009752181, 'Q': 0.0008367550, 'Z': 0.0005128469}

    # test frequency_analysis

    # initialize test sets
    set1 = {'A': 0.012, 'B': 0.003, 'C': 0.01, 'D': 0.1, 'E': 0.02, 'F': 0.001}
    set2 = {'A': 0.001, 'B': 0.012, 'C': 0.002, 'D': 0.01, 'E': 0.1, 'F': 0.02}
    set3 = {'A': 0.1, 'B': 0.02, 'C': 0.001, 'D': 0.012, 'E': 0.003, 'F': 0.01}

    # cross correlation of set1 and set2
    print('Cross correlation between set1 and set2: ' + str(cross_correlation(set1, set2)))
    # cross correlation of set1 and set3
    print('Cross correlation between set1 and set3: ' + str(cross_correlation(set1, set3)) + '\n')

    # test get_caesar_shift

    # encode message with caesar cipher encryption
    enc_text = caesar_cipher('Taylor Swift an iconic figure in contemporary pop culture continues to captivate '
                             'audiences worldwide with her unparalleled talent and charisma From her humble '
                             'beginnings as a country music sensation to her evolution into a powerhouse pop star '
                             'Swifts journey resonates with millions Through her deeply personal lyrics and '
                             'infectious melodies she effortlessly navigates themes of love heartbreak and '
                             'self discovery endearing herself to fans of all ages With multiple Grammy Awards and '
                             'chart topping hits Swifts impact on the music industry is undeniable Beyond her musical '
                             'prowess Swifts advocacy for artists rights and social causes further solidifies her '
                             'status as a cultural icon In an ever changing landscape Taylor Swift remains a beacon '
                             'of authenticity and creativity inspiring generations to embrace their individuality and '
                             'speak their truth', 15, True)
    # find encryption key of encoded message
    print('The caesar cipher key is: ' + str(get_caesar_shift(enc_text, english_dist)) + '\n')

    # test get_vigenere_keyword

    # initialize test cases
    m1 = ('PFAAP T FMJRNEDZYOUDPMJ AUTTUZHGLRVNAESMJRNEDZYOUDPMJ YHPD NUXLPASBOIRZTTAHLTM QPKQCFGBYPNJMLO '
          'GAFMNUTCITOMD BHKEIPAEMRYETEHRGKUGU TEOMWKUVNJRLFDLYPOZGHR RDICEEZB NMHGP '
          'FOYLFDLYLFYVPLOSGBZFAYFMTVVGLPASBOYZHDQREGAMVRGWCEN YP ELOQRNSTZAFPHZAYGI LVJBQSMCBEHM AQ VUMQNFPHZ AMTARA '
          'YOTVU LTULTUNFLKZEFGUZDMVMTEDGBZFAYFMTVVGLCATFFNVJUEIAUTEEPOG LANBQSMPWESMZRDTRTLLATHBZSFGFMLVJB '
          'UEGUOTAYLLHACYGEDGFMNKGHR FOYDEMWHXIPPYD NYYLOHLKXYMIK AQGUZDMPEX QLZUNRKTMNQGEMCXGWXENYTOHRJDD '
          'NUXLBNSUZCRZT RMVMTEDGXQMAJKMTVJTMCPVNZTNIBXIFETYEPOUZIETLL IOBOHMJUZ YLUP '
          'FVTTUZHGLRVNAESMHVFSRZTMNQGWMNMZMUFYLTUN VOMTVVGLFAYTQXNTIXEMLQERRTYLCKIYCSRJNCIFETXAIZTOA GVQ GZYP FVTOE '
          'ZHC QPLDIQLGESMTHZIFVKLCATFFNVJUEIAULLA KTORVTBZAYPSQ AUEUNRGNDEDZTRODGYIPDLLDI NTEHRPKLVVLPD')
    m2 = ('TEZHRAIRGMQHNJSQPTLNZJNEVMQHRXAVASLIWDNFOELOPFWGZ UHSTIRGLUMCSW GTTQCSJULNLQK OHL '
          'MHCMPWLCEHTFNUHNPHTSFFADJHTLNBYORWEFRYE PIISO K ZQR '
          'GMPTLQCSPRMOCMKESMTYLUTFRMIEOWXXFMWECCLWSQGWUASSWFGTTMYSGUL QNQGEFGTTIDSWMOAGMKEOQL U KOVN  '
          'AMZHZRGACMKHZRHSQLKLBMJAXTKLVRGFCBTLNAM SMYAHEGIEHTKNFOELNBMWFGORHWTPAY MVOSGUVUSPD')
    m3 = ('HYMUANDCHQNHOPOK ZDBFBQVZUTY QVZTYLFAHNRCFBZVA QCHVVUIP KL Z '
          'FYHRHNHCQOHMKUKOTQXLIXYROHMUEEOVEVCVIMQPIWBCPTMM CKSQNCNIBFFZCNVPORZZ EL BMXTGAORVY '
          'CKPBFTEFXHYMUANDCHQNHOXXIHV NYFXMUPCOHQW  VETQCVLWBOENUAPVORZNIHFRZIF KKHVTFIIBBTMUTG '
          'WDWFOIVOZVUMCKMQKVSGPOJPZ NYFXMUTTYXDQHGBAPJIUSGQGQABAVXREUZ HOCCHJUDIXTHMUTSTZTFAP TQNVCGXFVKIGPFHZWH '
          'CKSQNCNIBFFZCNVXQZWGEVOXT UFKKPDKCANXPDLUMGAXTIF CMDBQXAVFCD UATBOFZCVCQTQIHDBLUJMH ELBJICNBMTH INCI '
          'OHCDGKHZNCADITQQHFQOARACOPXPJAVCMBFIHQHGQWVZUOTDPDQTEFXRHQGEBDFEBJSBLFQJOSKKTI '
          'UCQJDVACTQOGQKVNBQPAMUAFSPDAVGGXCWHNHKPOZV OTJPJQINBCCHHZCQKCCQX TBPIWHSBLFQWNHGOOHMQATAGQQH '
          'CASZACOPXHYMUATQXWQXICIOZVNENIXXMHCGXGO NEOPOWIXEBQWVHLIUHOENURQDIVHYAVYOZVDEEQXEVUMCIXTQIUUIMQ '
          'ZNVXHEHYIUOIFAUNGRFRTUNGQKEZESBCIDKNIQKPBQNYBIXAMUMKPRBIMSKCXT')

    # initialize solution arrays
    m1_keys = []
    m2_keys = []
    m3_keys = []

    # find most probable keyword by iterating through potential keyword lengths
    for i in range(1, 25):
        m1_keys.append(get_vigenere_keyword(m1, i, english_dist))
        m2_keys.append(get_vigenere_keyword(m2, i, english_dist))
        m3_keys.append(get_vigenere_keyword(m3, i, english_dist))

    # print potential keys
    print('Potential keys for m1: ' + str(m1_keys))  # human
    print('Potential keys for m2: ' + str(m2_keys))  # hamilton
    print('Potential keys for m3: ' + str(m3_keys) + '\n')  # privacy

    # print decoded messages
    print('m1: ' + str(vigenere_cipher(m1, 'human', False)))
    print('m2: ' + str(vigenere_cipher(m2, 'hamilton', False)))
    print('m3: ' + str(vigenere_cipher(m3, 'privacy', False)))

# %%
# cipher_text = """YPT BPMGGTCQT KJ YD RKJXGMF YPT YDX LKVT XHDUMUGT XGMKC YTZYJ NPKBP BDOGR UT RTBHFXYTR LHDW YPT JOXXGKTR WDCDMGXPMUTYKB BFXPTH OYKGKSKCQ YPT GTYYTH LHTIOTCBF MYYMBE LHDW M JYHKCQ JYH NKYP JKST E HTXHTJTCYKCQ YPT QKVTC WDCDMGXPMUTYKB BFXPTH.

# GTY OJ JTT NPMY TZMBYGF KJ LHTIOTCBF MYYMBE.

# YPT VTHF LDOCRMYKDC LDH LHTIOTCBF MCMGFJKJ KJ YPT BTHYMKCYF YPMY JXTBKLKB GTYYTHJ MCR GTYYTH BDWUKCMYKDCJ MXXTMH NKYP VMHKTR LHTIOTCBKTJ MGG YPHDOQP MCF QKVTC JTBYKDC DL NHKYYTC GMCQOMQT. MRRKYKDCMGGF, WMYYTH-DL-LMBYGF TVTHF JMWXGT DL YPMY GMCQOMQT JPMHTJ M BDWWDC XMYYTHC KC YPT RKJYHKUOYKDC DL GTYYTHJ. YD WMET KY WDHT BGTMH,

# YPT TCQGKJP MGXPMUTY PMJ 26 GTYYTHJ, PDNTVTH CDY MGG DL YPTW MHT OJTR TIOMGGF LHTIOTCYGF KC NHKYYTC TCQGKJP. YPT LHTIOTCBF DL OJT DL BTHYMKC GTYYTHJ VMHKTJ. LDH KCJYMCBT, KL FDO TZMWKCT GTYYTHJ KC M UDDE DH KC M CTNJXMXTH, FDO NKGG CDYKBT PDN DLYTC YPT GTYYTHJ T, Y, M, MCR D MXXTMH KC TCQGKJP NDHRJ IOKYT LHTIOTCYGF. PDNTVTH, TCQGKJP YTZYJ HMHTGF OJT GTYYTHJ A, Z, I, DH S. YPKJ LMBY BMC UT OJTR YD RTBHFXY. YPT YTHW "LHTIOTCBF MCMGFJKJ" HTLTHJ YD YPKJ WTYPDR.

# TMBP GTYYTH LDOCR KC YPT XGMKCYTZY KJ JOUJYKYOYTR NKYP M RKLLTHTCY GTYYTH KC M UMJKB JOUJYKYOYKDC BFXPTH, MCR MCF QKVTC BPMHMBYTH KC KYJ XGMKCYTZY KJ XTHXTYOMGGF BPMCQTR YD MC KRTCYKBMG GTYYTH KC YPT YTZY DL YPT BFXPTH. M BKXPTHYTZY WTJJMQT NKYP JTVTHMG HTXTYKYKDCJ DL YPT GTYYTH F, LDH KCJYMCBT, NDOGR KWXGF YD YPT BHFXYMCMGFJY YPMY F JYMCRJ KC LDH YPT GTYYTH M KL TVTHF KCJYMCBT DL YPT GTYYTH M MHT BDCVTHYTR YD YPT GTYYTH Z."""

# %%
cipher_text = ""
with open(r"..\..\cipher_text.txt") as f:
    cipher_text = f.read()

cipher_text[:500]

# %%
# Relative frequency of letters in the English language
frequency_dict = {
    'a': 8.17,  'b': 1.49,  'c': 2.78,  'd': 4.25,  'e': 12.70,
    'f': 2.23,  'g': 2.02,  'h': 6.09,  'i': 6.97,  'j': 0.15,
    'k': 0.77,  'l': 4.03,  'm': 2.41,  'n': 6.75,  'o': 7.51,
    'p': 1.93,  'q': 0.10,  'r': 5.99,  's': 6.33,  't': 9.06,
    'u': 2.76,  'v': 0.98,  'w': 2.36,  'x': 0.15,  'y': 1.97,
    'z': 0.07
}


# %%
import numpy as np
import regex as re

# %%
import matplotlib.pyplot as plt

def plot_frequency(frequency_dict):
    frequency_dict_list = list(frequency_dict.items())
    frequency_dict_list.sort(key=lambda x: x[1], reverse=True)

    x = [i[0] for i in frequency_dict_list]
    y = [i[1] for i in frequency_dict_list]

    plt.bar(x, y)
    plt.xlabel('Letter')
    plt.ylabel('Frequency (%)')
    plt.title('Relative frequency of letters')

    for i, j in zip(x, y):
        format_to_2_decimal = "{:.2f}".format(j)
        plt.text(i, j, format_to_2_decimal, ha='center', va='bottom')

# Example usage:
plot_frequency(frequency_dict)

# %% [markdown]
# Take 1000 alphabets

# %%


# %%
def clean_text(text):
    # Remove special characters and numbers
    text = re.sub(r"[^a-zA-Z\s]", "", text)

    # Remove extra whitespace
    text = "".join(text.split())

    # Convert to lowercase
    text = text.upper()

    return text    

# %%
cleaned_text = clean_text(cipher_text)
cleaned_text[:50]

# %%
mset = set(cleaned_text)
len(mset)

# %%
from collections import Counter


# %%

def get_frequencies(text):
    # Count the frequency of each letter
    c = Counter(text)
    for key in c:
        c[key] = c[key] / len(text) * 100
    return c

# %%
cipher_freq = get_frequencies(cleaned_text)
cipher_freq

# %%
eng_upper = []
for i, v in frequency_dict.items():
    eng_upper.append((i.upper(), v))

eng_upper.sort(key=lambda x: x[1], reverse=True)
eng_upper

# %%
cipher_freq

# %%

cipher_freq_arr = []
for i, v in cipher_freq.items():
    cipher_freq_arr.append((i, v))

cipher_freq_arr.sort(key=lambda x: x[1], reverse=True)
cipher_freq_arr

# %%
mapping = {}
# cipher to original mapping

for i in range(len(cipher_freq_arr)):
    mapping[cipher_freq_arr[i][0]] = eng_upper[i][0]


# %%
mapping

# %%
len(mapping)

# %%
def substitute(text, mapping):
    # Substitute each letter in the text using the mapping
    return "".join([mapping.get(c, c) for c in text])

# %%
recovered_text = substitute(cipher_text, mapping)

# %%
recovered_text

# %%
actual_key = ['M', 'U', 'B', 'R', 'T', 'L', 'Q', 'P', 'K', 'A', 'E', 'G', 'W', 'C', 'D', 'X', 'I', 'H', 'J', 'Y', 'O', 'V', 'N', 'Z', 'F', 'S']

aplhabets = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

actual_mapping = {}
for i in range(len(actual_key)):
    actual_mapping[actual_key[i]] = aplhabets[i]

# %%
attacked_cipher_mapped_to_actual = list(mapping.items())
actual_mapping_list = list(actual_mapping.items())

attacked_cipher_mapped_to_actual.sort(key=lambda x: x[0])
actual_mapping_list.sort(key=lambda x: x[0])
attacked_cipher_mapped_to_actual

# %%
actual_mapping_list

# %%
def find_how_many_correctly_matched_and_how_many_incorrectly(cipher_mapping, actual_mapping):
    correct = 0
    incorrect = 0
    
    corrects = []
    incorrects = []
    
    for k, v in cipher_mapping.items():
        if v == actual_mapping[k]:
            correct += 1
            corrects.append((k, v))
        else:
            incorrect += 1
            incorrects.append((k, v))
        
    
    
    return correct, incorrect, corrects, incorrects
    

# %%
correct, incorrect, corrects, incorrects = find_how_many_correctly_matched_and_how_many_incorrectly(mapping, actual_mapping)

# %%
print(correct)
corrects

# %%
print(incorrect)
incorrects

# %%
x = np.array(list(cipher_freq.keys()))
y = np.array(list(cipher_freq.values()))

# plot 
import matplotlib.pyplot as plt
plt.bar(x, y)
plt.xlabel('Letter')
plt.ylabel('Frequency (%)')
plt.title('Relative frequency of letters in the English language')

# annotate it
for i, j in zip(x, y):
    plt.text(i, j, str(j), ha='center', va='bottom')

# %%
plot_frequency(frequency_dict)

# %%
plot_frequency(cipher_freq)



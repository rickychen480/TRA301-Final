from AutomaticDecrypter import AutomaticDecrypter

def testSolver(text):
    key, ptext, lang = AutomaticDecrypter(text).solve()
    print(f"Ciphertext: {text}\n"
          + f"Key: {key}\n"
          + f"Possible Languages: {lang}\n"
          + f"Plaintext: {ptext}\n")

# TODO: Create CLI -> Gooey; Add substitution example
if __name__ == "__main__":


    print("---------------Testing Multilingual Vigenere Ciphers---------------")
    testSolver("migjfsikpldptczgpxucmvzeyfixdpeilcsqzxuiqxwedmftrmquniwgmwedoigdluigtugwjulxematxpx")
    testSolver("vwmdxnraqfnncsswoijwdggijxilmeusdaeaqhmsgiuocdtmjviflajovalawstwfaqovknkdjqjmtjgcgetjaiztnuoraoiahbseadziethjb")
    testSolver("iypejagkmxhyvscditcznfivzlfghkhjvpfcplavrjlxiipbrxtmbvkejg")

    print("-------------Testing Multilingual Substitution Ciphers-------------")



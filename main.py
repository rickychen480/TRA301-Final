from AutomaticDecrypter import AutomaticDecrypter


# TODO: Create CLI -> Gooey
if __name__ == "__main__":
    ctext_en = "iypejagkmxhyvscditcznfivzlfghkhjvpfcplavrjlxiipbrxtmbvkejg"
    ctext_fr = "migjfsikpldptczgpxucmvzeyfixdpeilcsqzxuiqxwedmftrmquniwgmwedoigdluigtugwjulxematxpx"

    key, ptext, lang = AutomaticDecrypter(ctext_fr).solve()
    print(f"""
    Ciphertext: {ctext_fr}
    Key: {key}
    Language: {lang}
    Plaintext: {ptext}
    """)

    key, ptext, lang = AutomaticDecrypter(ctext_en).solve()
    print(f"""
    Ciphertext: {ctext_en}
    Key: {key}
    Language: {lang}
    Plaintext: {ptext}
    """)
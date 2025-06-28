import hashlib

def hash_string(password: str, algo: str) -> str:
    algo = algo.lower()
    try:
        h = hashlib.new(algo)
        h.update(password.encode())
        return h.hexdigest()
    except:
        return None

def generate_rainbow_table(wordlist_path: str, output_path: str, algo: str = "md5"):
    try:
        with open(wordlist_path, "r", encoding="utf-8") as f:
            words = [line.strip() for line in f if line.strip()]

        with open(output_path, "w", encoding="utf-8") as out:
            for word in words:
                hashed = hash_string(word, algo)
                if hashed:
                    out.write(f"{hashed} => {word}\n")

        print(f"[✓] Rainbow table generated: {output_path}")
        print(f"[i] Algorithm: {algo} | Words: {len(words)}")

    except FileNotFoundError:
        print("[✘] Wordlist file not found.")
    except Exception as e:
        print("[✘] Error:", e)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate rainbow table from a wordlist.")
    parser.add_argument("-w", "--wordlist", type=str, default="wordlist.txt", help="Path to wordlist file")
    parser.add_argument("-o", "--output", type=str, default="rainbow_table.txt", help="Path to save rainbow table")
    parser.add_argument("-a", "--algorithm", type=str, default="md5", help="Hashing algorithm (md5, sha1, sha256, sha512)")

    args = parser.parse_args()

    generate_rainbow_table(args.wordlist, args.output, args.algorithm)

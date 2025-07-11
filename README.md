# Hashed Password Cracker

A GUI tool for cracking hashed passwords using brute-force, dictionary, and rainbow table attacks. Supports MD5, SHA1, SHA256, and SHA512 hashes.

---

## Features

- Crack single hashes or batch files of hashes
- Brute-force, dictionary, and rainbow table attack modes
- Progress bar and ETA estimation
- Summary chart of cracking results
- Detects possibly salted or unknown hashes
- Results saved to `cracked_results.txt`

---

## Requirements

- Python 3.8 or higher

### Install dependencies

```sh
pip install customtkinter matplotlib
```

---

## Usage

### Running the App

```sh
python HashedPasswordCracker/main.py
```

### Files

- `main.py` — Main GUI application
- `attacks.py` — Implements attack methods
- `utils.py` — Hash utilities and detection
- `wordlist.txt` — Wordlist for dictionary/rainbow attacks
- `rainbow_table.txt` — Precomputed rainbow table (MD5)
- `generate_rainbow_table.py` — Script to generate rainbow tables
- `hashes.txt` — Example hashes to crack

---

## How to Crack Hashes

1. **Single Hash:** Enter a hash in the input box.
2. **Batch Mode:** Click "Select Hash File" and choose a file with hashes (one per line).
3. Choose an attack method.
4. Click "Start Cracking".
5. View results and summary chart. Results are saved to `cracked_results.txt`.

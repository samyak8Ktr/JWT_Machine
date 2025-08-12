# JWT Machine

**JWT Machine** is a penetration testing utility designed to simplify the process of decoding, modifying, re-signing, and testing JSON Web Tokens (JWTs) against web applications.  
It streamlines common JWT attack vectors and saves time for security researchers who would otherwise perform these steps manually.

I am still working on the networking part of this project, particulary dealing with diffrent behavious of web applications and how they accept JWT so that part is still in development.

![JWT Machine Banner](images/interface.png)

---

## ⚠️ Warning & Ethical Use

This tool is intended **only for authorized security testing and educational purposes**.  
Unauthorized use against systems without explicit permission is **illegal** and may result in criminal prosecution.  
You are solely responsible for your actions when using JWT Machine.

**By using this tool, you agree to:**
- Only test on applications/systems you own or have permission to assess.
- Not use the tool for malicious purposes.
- Follow applicable laws and regulations in your jurisdiction.

---

## ✨ Features


- Decoding the JWT Token  
-  Manually edit the token  
- Signing / Forging the payload with own secret  
- Checking if application is not verifying the JWT signature  
- Checking for downgrade attack  
- Multiprocessed custom JWT bruteforcing to check for weak signatures used
- Sending custom web requests to the web application  

---

## 📦 Installation

1. Clone the repository:
```bash
git clone https://github.com/samyak8Ktr/JWT_Machine.git
cd jwt-machine
```

2. Install dependencies:
```bash
pip3 install -r requirements.txt
```
- **NOTE:** The code is heavily dependent on latest versions of python3 and may crash if not provided.

---

## ▶️ Usage

- Run the JWT Machine:
```bash
python3 JWT_machine.py
```

- Check the version
```bash
python3 JWT_machine.py -v
```

---

## 📜 License

MIT License — free to use, modify, and distribute, with proper attribution.

---

## 💡 Author

Developed by **Samyak Katiyar**  
GitHub: [https://github.com/samyak8Ktr](https://github.com/samyak8Ktr)

---

## Acknowledgments

- This project uses the JWT secrets wordlist from the [Wallarm jwt-secrets repository](https://github.com/wallarm/jwt-secrets), licensed under the MIT License.  

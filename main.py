import ollama
from collections import defaultdict
import os
import re
import json
import subprocess
import ast


import requests

api_ip = "10.42.0.47"

def get_response(prompt):

    response = ollama.generate(model='llama3.2:3b',
                                prompt=prompt)
    return response['response']


def get_api_call(email, password):
    # r = requests.get(api_ip,params={"email":email, "password":password})

    # data = r.json()
    cnt = 1

    temp_str = "{"
    temp_str += "email: " + email + ",\n"
    for passw in password:
        temp_str += f"password{cnt} : {passw},\n"
        cnt += 1

    temp_str += "}"

    

    prompt = f"""What can be the next contextual passoword which easy to remember based on the cintextual information
        input = {temp_str}
        
        Don;t write any extra information except the JSON output,
        predicted_password should be easy to remember and should be a little tweaked version of input passwords should be based on the input provided, returned_password should be only one password
        output format : {{"password": predicted_password}}
        """
    
    # print(prompt)
    data = (get_response(prompt))
    # print(type(data))
    try:
        data = json.loads(data)
    except:
        return data

    return data

def main():
    st = ['a']
    dict_save = open("dict.txt", "a")
    for inp in st:
        addr = "/home/harsh/Downloads/BreachCompilation/data/h/" + inp

        # Create a map of emails to passwords
        dict = defaultdict(list)

        file = open(addr, "r", encoding="latin-1")

        print(addr)
        for line in file:
            try:
                email, password = re.split(r'[ ;:\t|]', line, maxsplit=1)
                email = email.split("@")[0]
                password = password[:-1]
                dict[email].append(password)    
            except:
                print(line)
                continue
            
            

        for email in dict:
            if len(dict[email])>=3:
                dict_save.write(email + " : " + str(dict[email]) + "\n")

        
        file.close()
    dict_save.close()


def run_tar_guess(predicted_passwords,passwords, email,lst,final_res):
    
    addr = "./dodonew_PI_49775.csv"

    file = open(addr, "w")

    for password in passwords:
        file.write(password + "\n")

    file.write(email + "\n")

    file.close()

    # Run a a.out file
    a_out = subprocess.run("./a.out")

    # Read the output file
    addr = "./output.txt"
    file = open(addr, "r", encoding="latin-1")

    for line in file:
        # print(line)
        try:
            res = line.split()
            guessed_password = res[0]
            probab = res[1]
            # probab = probab[:-1]
            # print(type(guessed_password), type(probab))
            # print(guessed_password, probab)
            if guessed_password == predicted_passwords:
                print("password found with probability: ",probab)
                dct = defaultdict()
                dct["email"] = email
                dct["passwords"] = passwords
                dct["predicted_password"] = predicted_passwords
                lst.append(dct)
                final_res.write(str(dct) + "\n")
                break
        except:
            continue

    
    file.close()

    return

    
    


def compare_main_func():
    data_points_checked = 0
    dict_file = open("dict.txt", "r")
    lst = []
    final_res = open("final_res.txt", "a")
    for line in dict_file:
        email, passwords = line.split(" : ")
        # print(passwords)
        # print(type(passwords))
        passwords = ast.literal_eval(passwords)
        # print(type(passwords))
        data = ""

        cnt = 0
        while not isinstance(data, dict) and "password" not in data:
            data = get_api_call(email, passwords)
            # print(type(data))
            if cnt>5:
                print("Error in getting response")
                break
            cnt += 1

        # print(data)
        # print(type(data))
        if not isinstance(data, dict) or "password" not in data:
            continue
        predicted_passwords = str(data["password"])
        # print(predicted_passwords)
        # print(passwords)
        # print(email)
        print(predicted_passwords)
        run_tar_guess(predicted_passwords, passwords, email,lst,final_res)
        data_points_checked += 1
        print("Data points checked: ", data_points_checked)
        

        # Check 
    dict_file.close()
        

    


# def send_req():


if __name__ == "__main__":
    # main()
    compare_main_func()
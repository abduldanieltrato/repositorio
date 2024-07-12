def funcao_principal():
    x = int(input("What is x?"))
    if is_noite(x):
        print("Noite")
    else:
        print("Tarde")

def is_noite(n):
    return n % 2 == 0

funcao_principal()

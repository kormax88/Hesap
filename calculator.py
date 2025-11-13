def topla(a, b):
    return a + b

def cikar(a, b):
    return a - b

def carp(a, b):
    return a * b

def bol(a, b):
    if b == 0:
        return "Hata: Sıfıra bölme yapılamaz!"
    return a / b

def hesapla():
    print("=== Basit Hesap Makinesi ===")
    print("Yapmak istediğiniz işlemi seçin:")
    print("1. Toplama")
    print("2. Çıkarma")
    print("3. Çarpma")
    print("4. Bölme")
    print("5. Çıkış")

    while True:
        secim = input("\nSeçiminiz (1/2/3/4/5): ")

        if secim == '5':
            print("Program sonlandırıldı. 👋")
            break

        if secim not in ('1', '2', '3', '4'):
            print("Geçersiz seçim! Lütfen 1-5 arası bir değer girin.")
            continue

        try:
            sayi1 = float(input("Birinci sayıyı girin: "))
            sayi2 = float(input("İkinci sayıyı girin: "))
        except ValueError:
            print("Lütfen geçerli bir sayı girin!")
            continue

        if secim == '1':
            sonuc = topla(sayi1, sayi2)
            islem = "+"
        elif secim == '2':
            sonuc = cikar(sayi1, sayi2)
            islem = "-"
        elif secim == '3':
            sonuc = carp(sayi1, sayi2)
            islem = "*"
        elif secim == '4':
            sonuc = bol(sayi1, sayi2)
            islem = "/"

        print(f"\n{round(sayi1,2)} {islem} {round(sayi2,2)} = {sonuc}")
        print("-" * 30)

if __name__ == "__main__":
    hesapla()

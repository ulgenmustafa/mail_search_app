from search import search

while True:
    print("\n--- MAIL ARAMA ---")
    query = input("Aramak istediğin kelime: ")

    results = search(query)

    if not results:
        print("Sonuç bulunamadı\n")
        continue

    for r in results:
        print("\nDosya:", r[0])
        print("Gönderen:", r[1])
        print("Tarih:", r[2])
        print("Konu:", r[3])
        print("-" * 40)
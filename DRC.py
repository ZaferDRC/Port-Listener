import socket

MAX_DATA_SIZE = 1024 # İstemciden gelen verilerin maks miktarı
data = b''    	 	 # Boş bir byte dizisi


# "AF_INET" = Kullanılacak ağ türünü belirler (IPV4)
# "SOCK_STREAM" = Soketin türünü ve iletişim tipi (TCP)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_ip = "0.0.0.0" # Ağdaki tüm ip adresleri kullanılarak bağlantılar kabul edilebilir.
server_port = int(input("Lütfen Port Girin:"))
server_socket.bind((server_ip,server_port))  # Verilen ip ve port'u ilişkilendirip bağlantıları kabul eder.
server_socket.listen(5) # Aynı anda en fazla 5 adet bağlantı talebi kabul edilir.

while len(data) <= MAX_DATA_SIZE:
	
	# İstemciden gelen bağlantıyı kabul eder ve "client_socket" ile istemcinin ip adresini ve port numarasını client_addr olarak döndürür.
	
    client_socket, client_addr = server_socket.accept() 
    print(f"Bağlantı kabul edildi: {client_addr[0]}:{client_addr[1]}") # istemcinin ip ve port numarası ekrana yazdırıldı.
    
    chunk = client_socket.recv(MAX_DATA_SIZE) # recv gelen verileri byte cinsinden alır.
    if not chunk:
        break
        
    data += chunk
		
    print(f"Gelen Veri: {data.decode('utf-8')}")

    client_socket.close()

server_socket.close()



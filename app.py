from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import json
from difflib import get_close_matches

# Fungsi untuk memuat basis pengetahuan dari file JSON
def load_knowledge_base(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        data: dict = json.load(file)
    return data

# Fungsi untuk mencari pertanyaan terbaik yang cocok dengan input pengguna
def find_best_match(user_question: str, question: list[str]) -> str | None:
    matches: list = get_close_matches(user_question, question, n=1, cutoff=0.6)
    return matches[0] if matches else None

# Fungsi untuk mendapatkan jawaban untuk pertanyaan tertentu dari basis pengetahuan
def get_answer_for_question(question: str, knowledge_base: dict) -> str | None:
    for q in knowledge_base["question"]:
        if q["question"] == question:
            return q["answer"]

# Kelas handler untuk menangani permintaan HTTP
class MyHandler(BaseHTTPRequestHandler):
    # Fungsi untuk menangani permintaan GET
    def do_GET(self):
        # Parsing URL
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)

        # Jika permintaan mengambil data index.html
        if parsed_path.path == "/":
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            # Membaca file index.html dan mengirimkannya sebagai respons
            with open('tampilan/index.html', 'rb') as file:
                self.wfile.write(file.read())

        # Jika permintaan mengambil data dari main.py
        elif parsed_path.path == "/api":
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()

            # Mendapatkan pertanyaan dari query parameter
            user_input = query_params.get('question', [''])[0]
            
            # Memeriksa keberadaan jawaban terbaik
            knowledge_base = load_knowledge_base('knowledge_base.json')
            best_match = find_best_match(user_input, [q["question"] for q in knowledge_base["question"]])

            # Mengambil jawaban dari main.py
            if best_match:
                answer = get_answer_for_question(best_match, knowledge_base)
                response = json.dumps({"answer": answer})
            else:
                response = json.dumps({"answer": "Saya kurang mengerti dengan apa yang anda tanyakan."})

            # Mengirimkan respons
            self.wfile.write(response.encode('utf-8'))
        else:
            self.send_error(404, 'File Not Found: %s' % self.path)

# Fungsi Membuat Alamat dan Port dan Menjalankan Server
def run():
    print('Starting server...')

    # Membuat alamat dan port
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, MyHandler)
    print('Server started on port 8000...')
    print('Server Is Active')
    print('Link Acces : http://localhost:8000/')
    
    # Menjalankan server
    httpd.serve_forever()

if __name__ == '__main__':
    run()

#http://localhost:8000/
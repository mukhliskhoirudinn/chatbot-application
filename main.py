import json
from difflib import get_close_matches

# Fungsi untuk memuat basis pengetahuan dari file JSON
def load_knowledge_base(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        data: dict = json.load(file)
    return data

# Fungsi untuk menyimpan basis pengetahuan ke file JSON
def save_knowledge_base(file_path: str, data: dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

# Fungsi untuk mencari pertanyaan terbaik yang cocok dengan input pengguna
def find_best_match(user_question: str, question: list[str]) -> str | None:
    matches: list = get_close_matches(user_question, question, n=1, cutoff=0.6)
    return matches[0] if matches else None

# Fungsi untuk mendapatkan jawaban untuk pertanyaan tertentu dari basis pengetahuan
def get_answer_for_question(question: str, knowledge_base: dict) -> str | None:
    for q in knowledge_base["question"]:
        if q["question"] == question:
            return q["answer"]

# Fungsi Program learning ChatBot     
def chat_bot():
    knowledge_base: dict = load_knowledge_base('knowledge_base.json')

    while True:
        user_input: str = input('you: ')
        
        if user_input.lower() == 'quit':
            break
        
        # Mencari pertanyaan terbaik yang cocok dengan input pengguna
        best_match: str | None = find_best_match(user_input, [q["question"] for q in knowledge_base["question"]])

        if best_match:
            # Jika pertanyaan cocok, ambil jawabannya dari basis pengetahuan knowledge_base.JSON
            answer: str = get_answer_for_question(best_match, knowledge_base)
            print(f'Bot: {answer}')
        else:
            # Jika tidak ada pertanyaan yang cocok, minta pengguna untuk memberikan jawaban baru
            print('Bot: Saya kurang mengerti dengan apa yang anda tanyakan, bisa beritahu apa yang harus saya jawab?')
            new_answer: str = input('Ketik jawabannya atau ketik "skip" : ')

            if new_answer.lower() != 'skip':
                # Jika pengguna memberikan jawaban baru, tambahkan ke basis pengetahuan dan simpan
                knowledge_base["question"].append({"question": user_input, "answer": new_answer})
                save_knowledge_base('knowledge_base.json', knowledge_base)
                print('Bot : Terimakasih ^-^, Saya Mempelajari Respon Baru')

if __name__ == '__main__':
    chat_bot()

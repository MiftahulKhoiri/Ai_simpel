import json
import random

intents = [
    {
        "intent": "greeting",
        "variants": [
            "halo", "hai", "hello", "hei",
            "halo ai", "hai bot", "halo asisten",
            "hai teman", "pagi", "selamat siang", "selamat malam"
        ],
        "templates": [
            "{}",
            "{}!",
            "eh {}",
            "{} kamu",
            "{} apakah kamu ada"
        ],
        "answers": [
            "Halo, ada yang bisa saya bantu?",
            "Hai, silakan ada yang bisa saya bantu?",
            "Halo, saya siap membantu Anda.",
            "Hai, ada yang ingin Anda tanyakan?",
            "Halo, silakan sampaikan kebutuhan Anda."
        ]
    },
    {
        "intent": "identity",
        "variants": [
            "siapa kamu", "kamu siapa",
            "nama kamu siapa", "ini siapa",
            "kamu itu siapa"
        ],
        "templates": [
            "{}",
            "boleh tahu {}",
            "sebenarnya {}"
        ],
        "answers": [
            "Saya adalah asisten AI yang siap membantu Anda.",
            "Saya merupakan program AI yang dirancang untuk membantu pengguna.",
            "Saya asisten virtual berbasis kecerdasan buatan.",
            "Saya AI yang dibuat untuk menjawab pertanyaan Anda."
        ]
    },
    {
        "intent": "capability",
        "variants": [
            "kamu bisa apa",
            "apa yang bisa kamu lakukan",
            "fungsi kamu apa",
            "kamu membantu apa saja"
        ],
        "templates": [
            "{}",
            "sebenarnya {}",
            "jelaskan {}"
        ],
        "answers": [
            "Saya dapat membantu menjawab pertanyaan dan memberi informasi.",
            "Saya bisa membantu tugas sederhana dan menjawab pertanyaan umum.",
            "Saya dirancang untuk membantu percakapan dan informasi dasar.",
            "Saya dapat membantu Anda dengan berbagai pertanyaan ringan."
        ]
    },
    {
        "intent": "help",
        "variants": [
            "tolong bantu saya",
            "saya butuh bantuan",
            "bisa bantu saya",
            "saya perlu bantuan"
        ],
        "templates": [
            "{}",
            "{} sekarang",
            "tolong {}"
        ],
        "answers": [
            "Tentu, silakan jelaskan apa yang Anda butuhkan.",
            "Baik, saya siap membantu. Silakan jelaskan.",
            "Dengan senang hati, apa yang bisa saya bantu?",
            "Silakan sampaikan masalah atau pertanyaan Anda."
        ]
    },
    {
        "intent": "thanks",
        "variants": [
            "terima kasih",
            "makasih",
            "thanks",
            "terimakasih banyak"
        ],
        "templates": [
            "{}",
            "{} ya",
            "{} atas bantuannya"
        ],
        "answers": [
            "Sama-sama, senang bisa membantu.",
            "Dengan senang hati.",
            "Sama-sama, jangan ragu bertanya lagi.",
            "Senang bisa membantu Anda."
        ]
    },
    {
        "intent": "farewell",
        "variants": [
            "bye",
            "sampai jumpa",
            "dadah",
            "sampai nanti",
            "selamat tinggal"
        ],
        "templates": [
            "{}",
            "{} ya",
            "ok {}"
        ],
        "answers": [
            "Sampai jumpa, semoga harimu menyenangkan.",
            "Terima kasih, sampai jumpa kembali.",
            "Sampai bertemu lagi.",
            "Semoga hari Anda menyenangkan, sampai jumpa."
        ]
    }
]

TARGET_TOTAL = 1000
dataset = []

while sum(len(d["questions"]) for d in dataset) < TARGET_TOTAL:
    intent = random.choice(intents)
    questions = set()

    while len(questions) < 40:
        v = random.choice(intent["variants"])
        t = random.choice(intent["templates"])
        questions.add(t.format(v))

    dataset.append({
        "intent": intent["intent"],
        "questions": list(questions),
        "answers": intent["answers"]
    })

with open("dataset.json", "w", encoding="utf-8") as f:
    json.dump(dataset, f, indent=2, ensure_ascii=False)

print("Dataset natural + variasi jawaban berhasil dibuat")
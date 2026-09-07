"""
Basis Pengetahuan Medis dan Panduan Pertolongan Pertama (P3K)
Mencakup: Penyakit Kulit Gatal-Gatal, Alergi, Infeksi Jamur/Bakteri, Luka Fisik, dan Kulit Sehat.
Standar: Pedoman Dermatologi Klinis Perdoski & Kemenkes RI.
"""

from typing import Dict, Any

CONDITIONS_KNOWLEDGE_BASE: Dict[str, Dict[str, Any]] = {
    "CANTENGAN_PARONIKIA": {
        "nama_umum": "Cantengan / Radang Tepi Kuku (Ingrown Nail / Paronychia)",
        "nama_medis": "Unguis Incarnatus / Paronychia Acuta",
        "deskripsi": "Peradangan dan infeksi pada lipatan jaringan di sekitar kuku (sering pada jempol kaki), ditandai bengkak merah, nyeri berdenyut hebat, dan timbul nanah akibat sudut kuku menancap ke dalam daging.",
        "langkah_p3k": [
            "Rendam Air Hangat: Rendam kaki/tangan yang cantengan dalam air hangat dicampur garam selama 15-20 menit, 2-3 kali sehari untuk melunakkan kuku dan mengurangi bengkak.",
            "Ganjal Tepi Kuku: Selipkan secuil kapas steril kecil di bawah sudut kuku yang menusuk daging agar kuku tumbuh terangkat ke atas permukaan kulit.",
            "Oleskan Salep Antiseptik: Oleskan salep Povidone Iodine atau salep antibiotik bebas pada tepi kuku yang bengkak, lalu tutup kasa steril longgar.",
            "Gunakan Alas Kaki Terbuka: Jangan memakai sepatu sempit atau berujung lancip yang menekan jempol kaki."
        ],
        "obat_rekomendasi_bebas": [
            "Povidone Iodine salep / cairan",
            "Ibuprofen 400mg / Parasetamol 500mg (Pereda nyeri berdenyut dan radang kuku)",
            "Kasa Steril & Plester"
        ],
        "pantangan_dan_mitos": [
            "SANGAT DILARANG mencungkil, memotong paksa kuku terlalu dalam, atau memencet nanah dengan gunting kuku yang tidak steril (memperparah infeksi!).",
            "JANGAN memotong kuku dengan bentuk melengkung ke dalam; kuku harus SELALU dipotong lurus mendatar.",
            "HINDARI memakai sepatu sempit berjam-jam saat kuku masih bengkak."
        ],
        "estimasi_sembuh": "5-10 hari untuk peradangan awal; jika kuku tertancap dalam, memerlukan tindakan pencabutan kuku parsial oleh dokter.",
        "tanda_bahaya_ke_dokter": [
            "Timbul benjolan daging merah liar yang berdarah (*jaringan granulasi hipertrofik*).",
            "Nanah meluas hingga ke bawah lempeng kuku.",
            "Penderita memiliki riwayat kencing manis (Diabetes Mellitus) - Wajib segera ke dokter!"
        ]
    },
    "JAMUR_KUKU_ONIKOMIKOSIS": {
        "nama_umum": "Jamur Kuku (Fungal Nail Infection / Onychomycosis)",
        "nama_medis": "Tinea Unguium / Onychomycosis",
        "deskripsi": "Infeksi jamur dermatofita pada lempeng kuku, ditandai kuku berubah warna menjadi kuning kusam, cokelat, atau kehitaman, kuku menebal, rapuh, berkapur, dan tepi kuku mudah hancur/bergerigi.",
        "langkah_p3k": [
            "Jaga Kuku Tetap Kering: Jamur tumbuh subur di tempat lembap. Keringkan sela jari dan kuku dengan handuk bersih setelah mandi/berwudhu.",
            "Gunting Kuku Teratur: Potong kuku yang menebal secara lurus dan kikir lembut permukaan kuku yang rapuh.",
            "Gunakan Kaus Kaki Katun: Ganti kaus kaki setiap hari dan jemur sepatu di bawah sinar matahari.",
            "Jangan Berbagi Alat Kuku: Gunakan gunting kuku khusus pribadi agar tidak menularkan ke jari lain."
        ],
        "obat_rekomendasi_bebas": [
            "Cat Kuku Antijamur Amorolfine 5% / Ciclopirox (Oleskan 1-2 kali seminggu pada kuku yang terinfeksi)",
            "Salep Miconazole / Terbinafine (Untuk area kulit di sekitar kuku)"
        ],
        "pantangan_dan_mitos": [
            "JANGAN menutupi jamur kuku dengan kutek cat kuku dekoratif biasa (karena memerangkap kelembapan dan memperparah jamur).",
            "JANGAN mengikir kuku hingga lapisan kuku habis berdarah.",
            "HINDARI berjalan tanpa alas kaki di tempat umum yang lembap (seperti tepi kolam renang atau kamar mandi umum)."
        ],
        "estimasi_sembuh": "Membutuhkan kesabaran 3-6 bulan untuk kuku tangan dan 9-12 bulan untuk kuku kaki hingga kuku baru tumbuh menggantikan kuku yang rusak.",
        "tanda_bahaya_ke_dokter": [
            "Infeksi menjalar ke seluruh kuku jari tangan/kaki.",
            "Lempeng kuku terlepas dari bantalannya (*onikolisis*) disertai rasa nyeri hebat."
        ]
    },
    "HEMATOMA_KUKU_KEJEPIT": {
        "nama_umum": "Kuku Terjepit / Darah di Bawah Kuku (Subungual Hematoma)",
        "nama_medis": "Subungual Hematoma Traumatica",
        "deskripsi": "Penumpukan darah di bawah lempeng kuku akibat cedera trauma tumpul (kuku terjepit pintu, tertimpa palu, atau terinjak), membentuk bercak warna merah tua, ungu, hingga hitam pekat disertai rasa nyeri berdenyut hebat.",
        "langkah_p3k": [
            "Kompres Es Segera: Bungkus es dengan kain dan tempelkan pada kuku selama 15-20 menit untuk mengurangi pembengkakan dan pembentukan bekuan darah.",
            "Tinggikan Posisi Jari: Posisikan jari lebih tinggi dari dada untuk mengurangi tekanan darah berdenyut.",
            "Istirahatkan Jari: Hindari aktivitas menekan jari yang cedera."
        ],
        "obat_rekomendasi_bebas": [
            "Parasetamol 500mg / Asam Mefenamat (Pereda nyeri berdenyut trauma)",
            "Kasa Steril & Perban Pelindung"
        ],
        "pantangan_dan_mitos": [
            "SANGAT DILARANG melubangi kuku sendiri menggunakan peniti atau jarum yang dibakar di rumah (berisiko infeksi tulang jari *osteomielitis*!).",
            "JANGAN mencabut kuku secara paksa."
        ],
        "estimasi_sembuh": "Nyeri mereda dalam 2-3 hari. Bercak darah hitam akan hilang perlahan mengikuti pertumbuhan kuku (3-6 bulan).",
        "tanda_bahaya_ke_dokter": [
            "Bercak darah menutupi lebih dari 50% luas kuku (butuh tindakan evakuasi darah steril / trepanasi oleh dokter).",
            "Tulang jari terasa patah/retak (*fraktur falang*) atau kuku robek terangkat dari dasarnya."
        ]
    },
    "KETOMBE_SEBOROIK": {
        "nama_umum": "Ketombe Parah / Dermatitis Seboroik Kepala",
        "nama_medis": "Seborrheic Dermatitis Capitis",
        "deskripsi": "Peradangan kulit kepala kronis yang dipicu oleh jamur Malassezia dan kelebihan produksi minyak kulit kepala, menimbulkan serpihan sisik putih/kekuningan berminyak, rasa gatal, dan bercak kemerahan di kulit kepala.",
        "langkah_p3k": [
            "Gunakan Sampo Medis Khusus: Keramas menggunakan sampo anti-ketombe terapeutik (mengandung Ketoconazole, Zinc Pyrithione, atau Selenium Sulfide).",
            "Diamkan 5 Menit: Jangan langsung dibilas; biarkan busa sampo meresap ke kulit kepala selama 3-5 menit agar zat antijamur bekerja maksimal.",
            "Hindari Menggaruk Kasar: Menggaruk kulit kepala dengan kuku merusak folikel dan menyebabkan luka infeksi bernanah.",
            "Bilas Bersih: Pastikan tidak ada sisa sampo/kondisioner yang tertinggal di kulit kepala."
        ],
        "obat_rekomendasi_bebas": [
            "Sampo Ketoconazole 2% (Gunakan 2-3 kali seminggu selama 2-4 minggu)",
            "Sampo Selenium Sulfide 1% / 2.5% (Selsun)",
            "Sampo Zinc Pyrithione (ZPT)"
        ],
        "pantangan_dan_mitos": [
            "JANGAN mengoleskan minyak rambut kental atau minyak kelapa berlebihan pada kulit kepala yang sedang berketombe seboroik (karena jamur Malassezia memakan asam lemak dari minyak tersebut!).",
            "HINDARI penggunaan hair spray, gel rambut beralkohol keras, atau pewarna rambut saat kulit kepala meradang."
        ],
        "estimasi_sembuh": "Mereda dalam 2-3 minggu dengan sampo terapeutik, namun cenderung kambuh jika stres atau kebersihan kulit kepala menurun.",
        "tanda_bahaya_ke_dokter": [
            "Kulit kepala menjadi sangat merah, bengkak, dan mengeluarkan cairan bening/nanah kuning berkerak tebal.",
            "Sisik menyebar luas ke wajah, alis, cuping hidung, dan dada."
        ]
    },
    "ALOPECIA_KEBOTAKAN": {
        "nama_umum": "Kebotakan Koin / Pitak (Alopecia Areata)",
        "nama_medis": "Alopecia Areata",
        "deskripsi": "Kondisi kerontokan rambut yang terjadi secara mendadak berbentuk bulatan-bulatan koin licin pada kulit kepala, janggut, atau alis, akibat sistem kekebalan tubuh (autoimun) yang menyerang folikel rambut.",
        "langkah_p3k": [
            "Hindari Stres Berlebih: Stres fisik atau emosional sering menjadi pemicu reaktivasi autoimun alopecia.",
            "Perlakukan Rambut dengan Lembut: Gunakan sisir bergigi jarang dan jangan mengikat rambut terlalu kencang (*traction*).",
            "Lindungi Kulit Kepala: Gunakan topi atau tabir surya pada area botak yang terpapar matahari langsung.",
            "Konsultasi Dokter Kulit Segera: Terapi lini pertama (injeksi kortikosteroid intralesi) sangat efektif menumbuhkan rambut jika dimulai lebih awal!"
        ],
        "obat_rekomendasi_bebas": [
            "Lotion Minoxidil 2% atau 5% (Membantu merangsang sirkulasi darah dan folikel rambut)",
            "Suplemen Biotin & Zinc (Mendukung nutrisi pertumbuhan batang rambut)"
        ],
        "pantangan_dan_mitos": [
            "JANGAN menggosok area pitak dengan bawang putih, jahe, atau minyak rempah keras hingga kulit kepala melepuh!",
            "JANGAN mencabuti sisa-sisa rambut di sekitar lingkaran botak."
        ],
        "estimasi_sembuh": "Rambut dapat tumbuh kembali dalam 3-6 bulan (sering kali awalnya tumbuh berupa rambut halus keputihan sebelum berubah menjadi warna rambut normal).",
        "tanda_bahaya_ke_dokter": [
            "Kebotakan meluas cepat hingga mengenai seluruh kulit kepala (*Alopecia Totalis*) atau seluruh bulu tubuh (*Alopecia Universalis*)."
        ]
    },
    "KUTU_RAMBUT_PEDIKULOSIS": {
        "nama_umum": "Kutu Rambut / Ketombe Lengket (Head Lice)",
        "nama_medis": "Pediculosis Capitis",
        "deskripsi": "Infeksi parasit serangga kutu rambut (*Pediculus humanus capitis*), ditandai rasa gatal menggelitik intens di kulit kepala (terutama di belakang telinga dan tengkuk leher) dan ditemukannya bintik oval putih telur kutu (*nits*) yang melekat erat pada batang rambut.",
        "langkah_p3k": [
            "Gunakan Obat Pembasmi Kutu: Oleskan losion Permethrin 1% pada rambut dan kulit kepala yang telah dicuci bersih dan dikeringkan handuk, diamkan 10 menit lalu bilas.",
            "Gunakan Sisir Serit: Sisir rambut basah menggunakan sisir serit bergigi sangat rapat untuk menyaring kutu dewasa dan telur-telurnya.",
            "Cuci Sprei & Topi: Rendam sisir, jepit rambut, sarung bantal, dan topi dalam air panas (>55°C) selama minimal 10 menit.",
            "Ulangi Pengobatan Hari ke-7: Lakukan aplikasi kedua 7-9 hari kemudian untuk mematikan kutu baru yang baru menetas dari telur sisa."
        ],
        "obat_rekomendasi_bebas": [
            "Losion Permethrin 1% (Pedikulosisida)",
            "Sisir Serit Kutu Bergigi Rapat (Fine-toothed nit comb)"
        ],
        "pantangan_dan_mitos": [
            "SANGAT DILARANG menggunakan minyak tanah, pestisida tanaman, atau kapur ajaib di kepala (sangat beracun dan memicu iritasi luka bakar!).",
            "JANGAN bertukar sisir, helm, bando, atau handuk dengan orang lain."
        ],
        "estimasi_sembuh": "Kutu mati dalam 24 jam pengobatan; pembersihan telur tuntas dalam 7-10 hari.",
        "tanda_bahaya_ke_dokter": [
            "Kulit kepala luka berdarah dan bernanah parah akibat garukan kuku terus-menerus (*infeksi impetigo*)."
        ]
    },
    "CACAR_AIR_VARICELLA": {
        "nama_umum": "Cacar Air (Chickenpox / Varicella)",
        "nama_medis": "Varicella Zoster Infection",
        "deskripsi": "Infeksi virus Varicella Zoster yang sangat khas ditandai dengan lenting/gelembung kecil berisi cairan bening menyerupai tetesan embun di atas dasar kemerahan ('dewdrops on a rose petal'), sangat gatal, dan dapat menyebar ke dada, punggung, tangan, dan wajah.",
        "langkah_p3k": [
            "JANGAN MEMECAHKAN LENTING: Memecahkan lenting gelembung berair dapat menyebabkan infeksi bakteri sekunder dan meninggalkan bekas bopeng permanen.",
            "Oleskan Losion Calamine: Oleskan secara lembut dengan cotton bud pada bintik lenting untuk meredakan rasa gatal tanpa merusak dinding lenting.",
            "Mandi Air Suam Kuku: Mandi secara perlahan menggunakan sabun antiseptik lembut, tepuk-tepuk handuk hingga kering (jangan digosok).",
            "Gunting Kuku: Potong kuku pendek agar tidak menggores lenting saat tidur.",
            "Isolasi Mandiri: Istirahat di rumah dan hindari kontak dengan orang lain (terutama ibu hamil dan bayi) hingga semua lenting mengering menjadi keropeng."
        ],
        "obat_rekomendasi_bebas": [
            "Losion Calamine (Pereda gatal dan penyejuk lenting berair)",
            "Bedak Salicyl 2% (Taburkan tipis pada lenting yang belum pecah)",
            "Parasetamol 500mg (Pereda demam dan nyeri tubuh)",
            "Antihistamin Cetirizine 10mg (Membantu mengurangi gatal tidur malam)"
        ],
        "pantangan_dan_mitos": [
            "SANGAT DILARANG memencet, menusuk jarum, atau menggaruk lenting berair!",
            "SANGAT DILARANG memberikan obat ASPIRIN pada anak/remaja yang terkena cacar air (berisiko memicu Sindrom Reye yang fatal!).",
            "JANGAN mandi dengan air yang terlalu dingin atau digosok spons kasar.",
            "JANGAN percaya mitos bahwa cacar air tidak boleh mandi; tidak mandi justru memicu infeksi bakteri bernanah!"
        ],
        "estimasi_sembuh": "7-14 hari hingga semua lenting berair pecah alami, mengering, dan menjadi krusta/keropeng kehitaman.",
        "tanda_bahaya_ke_dokter": [
            "Lenting berubah menjadi nanah kuning kehijauan keruh dan kulit sekitar sangat bengkak merah (infeksi impetigo sekunder).",
            "Disertai sesak napas, batuk hebat, atau linglung/kejang (komplikasi pneumonia/ensefalitis).",
            "Penderita sedang hamil atau bayi di bawah usia 1 tahun (harus segera mendapat obat antivirus Asiklovir resep dokter)."
        ]
    },
    "HERPES_ZOSTER": {
        "nama_umum": "Cacar Api / Cacar Ular / Dompo (Herpes Zoster)",
        "nama_medis": "Herpes Zoster / Shingles",
        "deskripsi": "Reaktivasi virus cacar air pada saraf sensorik, ditandai lenting-lenting bergerombol berisi cairan yang tersusun mengikuti jalur saraf tubuh (hanya pada satu sisi tubuh/unilateral), disertai rasa nyeri panas terbakar atau menusuk.",
        "langkah_p3k": [
            "Jaga Lenting Tetap Utuh: Jangan digaruk atau dipecahkan.",
            "Kompres Dingin Bersih: Kompres kain basah dingin selama 15 menit untuk meredakan sensasi panas terbakar.",
            "Gunakan Pakaian Longgar: Bahan katun lembut agar tidak menimbulkan gesekan nyeri pada lenting.",
            "Segera Konsultasi Faskes: Antivirus oral (Acyclovir/Valacyclovir) paling efektif jika diminum dalam 72 jam pertama munculnya lenting!"
        ],
        "obat_rekomendasi_bebas": [
            "Parasetamol / Ibuprofen (Pereda nyeri dan sensasi berdenyut terbakar)",
            "Kompres Larutan Saline / Air Matang Dingin",
            "Kasa steril penutup lenting"
        ],
        "pantangan_dan_mitos": [
            "JANGAN dioleskan minyak panas, daun-daunan mentah, atau pasta gigi!",
            "JANGAN memecahkan gelembung lenting karena cairan mengandung virus aktif yang bisa menular.",
            "JANGAN menunda ke dokter lebih dari 3 hari (72 jam) agar saraf tidak mengalami nyeri pasca-herpes berkepanjangan."
        ],
        "estimasi_sembuh": "2-4 minggu dengan pengobatan antivirus yang tepat.",
        "tanda_bahaya_ke_dokter": [
            "Lenting muncul di area wajah dekat mata (risiko kebutaan Herpes Zoster Ophthalmicus - Segera ke IGD!).",
            "Nyeri saraf sangat hebat yang tidak berkurang dengan parasetamol."
        ]
    },
    "KULIT_NORMAL": {
        "nama_umum": "Kulit Sehat / Normal (Tidak Ditemukan Kelainan Patologis)",
        "nama_medis": "Integumentum Commune Normalis",
        "deskripsi": "Struktur kulit tampak intak, utuh, tanpa tanda infeksi aktif, luka terbuka, ataupun ruam peradangan yang signifikan.",
        "langkah_p3k": [
            "Jaga Kebersihan Kulit: Mandi teratur 2 kali sehari menggunakan sabun berbahan lembut (pH seimbang).",
            "Gunakan Pelembap: Oleskan pelembap/lotion setelah mandi untuk menjaga elastisitas dan fungsi pelindung kulit (skin barrier).",
            "Gunakan Tabir Surya: Gunakan sunscreen minimal SPF 30 saat beraktivitas di luar ruangan.",
            "Hindari Menggaruk Berlebihan: Jika terasa gatal ringan sesaat, cukup usap lembut atau kompres dingin."
        ],
        "obat_rekomendasi_bebas": [
            "Lotion Pelembap Kulit (Ceramide / Hyaluronic Acid)",
            "Sabun Mandi Lembut (Gentle Skin Cleanser)"
        ],
        "pantangan_dan_mitos": [
            "JANGAN mengoleskan salep obat keras (seperti salep kortikosteroid atau antijamur) jika kulit tidak mengalami infeksi.",
            "HINDARI mandi dengan air yang terlalu panas secara berlebihan karena dapat mengikis minyak alami kulit."
        ],
        "estimasi_sembuh": "Kondisi kulit normal dan sehat.",
        "tanda_bahaya_ke_dokter": [
            "Muncul tahi lalat baru yang membesar cepat, berubah warna, atau tepi tidak beraturan (tanda melanoma).",
            "Tiba-tiba timbul bentol kemerahan yang meluas cepat ke seluruh tubuh."
        ]
    },
    "BIDURAN_URTIKARIA": {
        "nama_umum": "Biduran / Kalikata (Hives / Urticaria)",
        "nama_medis": "Urticaria Acuta",
        "deskripsi": "Reaksi vaskular kulit yang ditandai dengan bentol-bentol kemerahan (*wheal*) menonjol berbatas tegas yang timbul mendadak dan terasa sangat gatal, sering dipicu oleh alergi makanan, udara dingin, atau stres.",
        "langkah_p3k": [
            "Hindari Pemicu Alergi: Segera hentikan kontak dengan zat yang diduga memicu alergi (makanan laut, telur, dingin, debu, obat).",
            "Kompres Dingin: Tempelkan kain basah dingin pada area bentol untuk meredakan rasa gatal dan menyempitkan pembuluh darah.",
            "Oleskan Losion Penyejuk: Oleskan Calamine lotion pada bentol untuk menenangkan rasa gatal.",
            "Gunakan Pakaian Longgar: Pilih pakaian katun yang tidak menekan kulit."
        ],
        "obat_rekomendasi_bebas": [
            "Calamine Lotion (Losion pereda gatal dan penyejuk kulit)",
            "Cetirizine 10mg / Loratadine 10mg (Antihistamin oral pereda alergi dan bentol)"
        ],
        "pantangan_dan_mitos": [
            "SANGAT DILARANG menggaruk bentol dengan kuku karena dapat memicu infeksi bakteri sekunder.",
            "JANGAN mandi dengan air panas karena panas memicu pelepasan histamin yang membuat bentol semakin meluas.",
            "JANGAN mengoleskan minyak angin/balsem panas pada area biduran."
        ],
        "estimasi_sembuh": "Bentol umumnya mereda dalam beberapa jam hingga 24 jam setelah minum antihistamin dan menghindari pemicu.",
        "tanda_bahaya_ke_dokter": [
            "Bibir, kelopak mata, atau lidah membengkak (*Angioedema*).",
            "Disertai sesak napas, mengi, suara serak, atau pusing berputar (Reaksi Syok Anafilaksis - Segera ke IGD!)."
        ]
    },
    "EKSIM_DERMATITIS": {
        "nama_umum": "Eksim / Dermatitis Kontak / Atopik",
        "nama_medis": "Dermatitis / Eczema",
        "deskripsi": "Peradangan kulit yang ditandai dengan bercak kemerahan, kulit sangat kering, bersisik, menebal (*likenifikasi*), dan gatal kronis yang sering kambuh.",
        "langkah_p3k": [
            "Perbaiki Skin Barrier: Oleskan pelembap tebal (seperti Petroleum Jelly atau krim ceramide) sesering mungkin, terutama dalam 3 menit setelah mandi.",
            "Hindari Sabun Keras: Gunakan sabun mandi tanpa pewangi (fragrance-free) dan tanpa deterjen SLS.",
            "Kompres Dingin saat Gatal: Gunakan handuk dingin untuk meredam dorongan menggaruk.",
            "Gunting Kuku: Pastikan kuku selalu pendek untuk mencegah luka garukan saat tidur."
        ],
        "obat_rekomendasi_bebas": [
            "Petroleum Jelly murni / Salep Pelembap Ceramide",
            "Hydrocortisone 1% krim (Kortikosteroid potensi ringan bebas untuk meredakan radang akut maksimal 7 hari)",
            "Cetirizine 10mg untuk mengurangi gatal malam hari"
        ],
        "pantangan_dan_mitos": [
            "JANGAN menggosok kulit eksim dengan scrub, batu apung, atau loofah.",
            "HINDARI mencuci pakaian dengan deterjen yang berbusa tajam/pewangi menyengat.",
            "JANGAN biarkan kulit dalam keadaan kering tanpa pelembap."
        ],
        "estimasi_sembuh": "Kambuhan; dapat mereda dalam 1-2 minggu dengan perawatan pelembap intensif dan salep anti-radang.",
        "tanda_bahaya_ke_dokter": [
            "Kulit mengeluarkan cairan nanah kuning berkerak (tanda infeksi bakteri impetigenisasi).",
            "Gatal mengganggu tidur dan aktivitas sehari-hari secara signifikan."
        ]
    },
    "KUDIS_SKABIES": {
        "nama_umum": "Kudis / Gudik (Scabies)",
        "nama_medis": "Scabies / Sarcoptic Acariasis",
        "deskripsi": "Infeksi kutu parasit mikro (*Sarcoptes scabiei*) pada lapisan kulit, ditandai bintik-bintik merah kecil mirip jerawat atau terowongan tipis di sela-sela jari tangan, pergelangan tangan, ketiak, atau selangkangan, dengan rasa gatal luar biasa yang memuncak di malam hari.",
        "langkah_p3k": [
            "Oleskan Obat Skabisida: Oleskan krim Permethrin 5% ke seluruh tubuh dari leher ke bawah hingga ke ujung jari kaki sebelum tidur, diamkan 8-14 jam sebelum dibilas.",
            "Cuci Semua Pakaian & Sprei: Rendam seluruh pakaian, handuk, dan sprei yang dipakai 3 hari terakhir dalam air panas (minimal 60°C) lalu setrika panas.",
            "Bungkus Barang Tak Tercuci: Masukkan kasur lipat/bantal ke dalam plastik tertutup selama minimal 72 jam agar kutu mati.",
            "Obati Seluruh Penghuni Rumah: Anggota keluarga/teman sekamar harus diobati bersamaan meskipun belum bergejala."
        ],
        "obat_rekomendasi_bebas": [
            "Permethrin 5% krim (Obat pilihan utama untuk membasmi kutu skabies)",
            "Losion Calamine untuk meredakan gatal sementara",
            "Antihistamin (Cetirizine) untuk meredakan gatal malam hari"
        ],
        "pantangan_dan_mitos": [
            "JANGAN hanya mengobati 1 orang jika ada anggota keluarga lain yang tinggal serumah (pasti akan tertular kembali!).",
            "JANGAN menggaruk bintik scabies hingga berdarah.",
            "JANGAN mengoleskan belerang mentah atau minyak tanah yang tidak higienis."
        ],
        "estimasi_sembuh": "Kutu mati setelah 1-2 kali aplikasi Permethrin, namun reaksi gatal pasca-skabies bisa bertahan 2-4 minggu.",
        "tanda_bahaya_ke_dokter": [
            "Muncul infeksi nanah meluas di sekitar bintik-bintik akibat garukan.",
            "Gejala tetap berlanjut setelah 2 minggu pasca pengobatan Permethrin."
        ]
    },
    "KURAP_KADAS": {
        "nama_umum": "Kurap / Kadas (Ringworm / Tinea Corporis)",
        "nama_medis": "Tinea Corporis / Tinea Cruris",
        "deskripsi": "Infeksi jamur dermatofita pada kulit yang khas dengan bercak kemerahan berbentuk melingkar mirip cincin, dengan bagian tepi yang lebih merah/aktif menonjol bersisik dan bagian tengah yang tampak lebih tenang (*central clearing*), terasa sangat gatal terutama saat berkeringat.",
        "langkah_p3k": [
            "Jaga Area Tetap Kering: Keringkan kulit dengan handuk bersih khusus (jangan digabung dengan bagian tubuh lain).",
            "Oleskan Salep Antijamur: Oleskan salep antijamur dari bagian luar lingkaran menuju ke tengah, lebihkan 2 cm dari batas terluar ruam.",
            "Lanjutkan Salep: Tetap oleskan salep antijamur hingga 1-2 minggu SETELAH ruam tampak hilang untuk mencegah jamur tumbuh kembali.",
            "Hindari Berbagi Pakaian: Pisahkan pakaian dan handuk dari orang lain."
        ],
        "obat_rekomendasi_bebas": [
            "Krim Miconazole 2% / Clotrimazole 1% / Terbinafine 1% (Oleskan 2 kali sehari)",
            "Sabun Antijamur Ketoconazole"
        ],
        "pantangan_dan_mitos": [
            "SANGAT DILARANG mengoleskan salep hidrokortison/steroid pada kurap! Steroid akan menyuburkan jamur dan membuat kurap meluas (*Tinea Incognito*).",
            "JANGAN menggosok dengan lengkuas atau alkohol keras yang merusak kulit."
        ],
        "estimasi_sembuh": "2-4 minggu pengobatan antijamur topikal teratur.",
        "tanda_bahaya_ke_dokter": [
            "Ruam meluas ke area kulit kepala, wajah, atau kuku.",
            "Tidak ada perbaikan setelah 2 minggu menggunakan salep antijamur bebas."
        ]
    },
    "GIGITAN_SERANGGA": {
        "nama_umum": "Gigitan Serangga / Prurigo (Insect Bite)",
        "nama_medis": "Insect Bite Reaction / Prurigo Simplex",
        "deskripsi": "Reaksi inflamasi lokal akibat gigitan nyamuk, semut api, kutu kasur (bed bugs), atau tomcat, berupa bentol merah berpusat pada titik tusukan kecil, gatal, atau rasa panas terbakar.",
        "langkah_p3k": [
            "Cuci dengan Air dan Sabun: Segera bersihkan area gigitan untuk membuang sisa air liur atau racun serangga.",
            "Kompres Es: Tempelkan kompres es yang dibalut kain selama 10 menit untuk meredakan bengkak dan gatal.",
            "Oleskan Krim Anti-Gatal: Oleskan losion calamine atau minyak telon/kayu putih jika kulit tidak lecet.",
            "Hindari Menggaruk: Menggaruk gigitan serangga sering meninggalkan bekas bintik hitam (*post-inflammatory hyperpigmentation*)."
        ],
        "obat_rekomendasi_bebas": [
            "Calamine Lotion",
            "Krim Hydrocortisone 1% jika bentol sangat meradang",
            "Minyak kayu putih / telon (hanya untuk kulit tanpa luka terbuka)"
        ],
        "pantangan_dan_mitos": [
            "JANGAN menekan atau memencet bentol serangga.",
            "JANGAN mengoleskan getah tanaman yang tidak dikenal."
        ],
        "estimasi_sembuh": "3-7 hari bentol mereda dan menghilang.",
        "tanda_bahaya_ke_dokter": [
            "Terjadi pembengkakan besar yang semakin membesar > 10 cm disertai garis merah menjalar (indikasi selulitis).",
            "Timbul lepuhan berisi nanah (misal terkena racun tomcat)."
        ]
    },
    "BIANG_KERINGAT": {
        "nama_umum": "Biang Keringat / Keringat Buntet (Prickly Heat / Miliaria)",
        "nama_medis": "Miliaria Rubra",
        "deskripsi": "Tersumbatnya saluran kelenjar keringat di bawah kulit, menimbulkan bintik-bintik merah kecil bergerombol yang terasa gatal, pedih, dan menusuk-nusuk saat cuaca panas atau berkeringat.",
        "langkah_p3k": [
            "Pindah ke Ruangan Sejuk: Beradalah di ruangan ber-AC atau dengan sirkulasi udara baik untuk menghentikan produksi keringat.",
            "Ganti Baju Basah: Segera ganti pakaian saat basah oleh keringat dengan bahan katun tipis.",
            "Mandi Air Sejuk: Mandi dengan air sejuk untuk menurunkan suhu kulit.",
            "Taburkan Bedak Salicyl: Taburkan bedak kocok atau bedak salicyl pada kulit yang sudah kering sempurna."
        ],
        "obat_rekomendasi_bebas": [
            "Bedak Salicyl 2% (Menyerap keringat dan meredakan rasa pedih gatal)",
            "Losion Calamine"
        ],
        "pantangan_dan_mitos": [
            "JANGAN mengoleskan salep atau minyak yang bertekstur kental/lengket karena akan semakin menyumbat pori kelenjar keringat.",
            "HINDARI pakaian berbahan wol atau nilon tebal."
        ],
        "estimasi_sembuh": "2-4 hari setelah berada di lingkungan sejuk dan menjaga kulit tetap kering.",
        "tanda_bahaya_ke_dokter": [
            "Bintik-bintik berubah menjadi nanah kuning kecil-kecil (*Miliaria Pustulosa*) disertai demam."
        ]
    },
    "JERAWAT_ACNE": {
        "nama_umum": "Jerawat Radang (Acne Vulgaris)",
        "nama_medis": "Acne Vulgaris",
        "deskripsi": "Penyumbatan pori-pori kulit oleh sel kulit mati dan minyak (sebum) yang terinfeksi bakteri Cutibacterium acnes, menimbulkan komedo, papul merah, atau pustul bernanah.",
        "langkah_p3k": [
            "Cuci Wajah 2x Sehari: Gunakan pembersih lembut khusus kulit berjerawat (mengandung Salicylic Acid atau Tea Tree Oil).",
            "Oleskan Obat Totol Jerawat: Totolkan obat jerawat berbahan Benzoyl Peroxide atau Salicylic Acid tepat di atas bintik jerawat.",
            "Hindari Menyentuh Wajah: Tangan kotor memindahkan bakteri baru ke pori-pori.",
            "Gunakan Tabir Surya Non-Komedogenik: Melindungi bekas jerawat agar tidak menjadi flek hitam."
        ],
        "obat_rekomendasi_bebas": [
            "Gel Benzoyl Peroxide 2.5% atau 5% (Obat totol pembasmi bakteri jerawat)",
            "Serum / Gel Salicylic Acid 2%",
            "Plester Jerawat (Acne Patch)"
        ],
        "pantangan_dan_mitos": [
            "SANGAT DILARANG memencet jerawat dengan tangan atau alat ekstraktor komedo yang tidak steril! Memicu bekas bopeng (*ice pick scar*) permanen.",
            "JANGAN mengoleskan pasta gigi (odol) pada jerawat karena menyebabkan iritasi luka bakar kimiawi."
        ],
        "estimasi_sembuh": "5-10 hari untuk jerawat papul mengempis.",
        "tanda_bahaya_ke_dokter": [
            "Muncul jerawat kistik besar (jerawat batu) yang sangat nyeri dan tidak mempan obat bebas."
        ]
    },
    "LUKA_ROBEK": {
        "nama_umum": "Luka Robek / Sayat (Laceration/Cut)",
        "nama_medis": "Vulnus Laceratum / Vulnus Scissum",
        "deskripsi": "Terputusnya kontinuitas jaringan kulit akibat benturan benda tumpul keras (jatuh dari sepeda/motor) atau sayatan benda tajam.",
        "langkah_p3k": [
            "Hentikan Pendarahan: Tekan area luka secara lembut dengan kain bersih atau kasa steril selama 5-10 menit.",
            "Bersihkan Luka: Bilas dengan air bersih mengalir (atau cairan NaCl 0.9%) untuk membersihkan pasir/debu.",
            "Disinfeksi Tepi Luka: Oleskan antiseptik Povidone Iodine di sekitar tepi luka.",
            "Tutup Luka: Rekatkan tepi luka dan tutup dengan kasa steril berpori."
        ],
        "obat_rekomendasi_bebas": [
            "Povidone Iodine 10%",
            "Larutan Saline Steril / NaCl 0.9%",
            "Kasa Steril & Plester Penutup Luka"
        ],
        "pantangan_dan_mitos": [
            "JANGAN menaburkan bubuk kopi, abu rokok, atau tanah (sumber tetanus!).",
            "JANGAN mengoleskan pasta gigi (odol), mentega, atau minyak tanah."
        ],
        "estimasi_sembuh": "7-14 hari untuk luka robek ringan/sedang.",
        "tanda_bahaya_ke_dokter": [
            "Kedalaman luka > 0.5 cm atau terlihat lapisan lemak/otot (harus dijahit sebelum 6 jam).",
            "Pendarahan tidak berhenti setelah ditekan 10 menit berturut-turut.",
            "Luka kotor terkena paku berkarat (butuh suntikan anti-tetanus)."
        ]
    },
    "LUKA_LECET": {
        "nama_umum": "Luka Lecet / Gesek (Abrasion)",
        "nama_medis": "Vulnus Excoriatio",
        "deskripsi": "Hilangnya lapisan terluar kulit (epidermis) akibat gesekan kasar dengan permukaan aspal, semen, atau lantai.",
        "langkah_p3k": [
            "Cuci dengan Air Mengalir: Bilas luka di bawah air mengalir dan sabun lembut di sekitar kulit.",
            "Keringkan Perlahan: Tepuk-tepuk dengan kasa bersih, jangan digosok.",
            "Oleskan Salep Pelembap: Oleskan tipis Petroleum Jelly atau salep antiseptik agar luka tetap lembap.",
            "Tutup Longgar: Lindungi dengan plester non-lengket jika rentan gesekan."
        ],
        "obat_rekomendasi_bebas": [
            "Petroleum Jelly murni",
            "Povidone Iodine cairan / salep",
            "Plester luka hidrokoloid"
        ],
        "pantangan_dan_mitos": [
            "JANGAN membiarkan butiran pasir/kerikil tertinggal di bawah kulit.",
            "JANGAN mengelupas koreng secara paksa.",
            "JANGAN mengoleskan alkohol 70% langsung ke luka terbuka."
        ],
        "estimasi_sembuh": "3-7 hari pembentukan lapisan kulit baru.",
        "tanda_bahaya_ke_dokter": [
            "Luka lecet sangat luas melebihi ukuran telapak tangan.",
            "Keluar cairan nanah kuning kehijauan disertai rasa panas."
        ]
    },
    "LUKA_BAKAR": {
        "nama_umum": "Luka Bakar Ringan (Minor Burn)",
        "nama_medis": "Combustio Grade I - II Superfisial",
        "deskripsi": "Kerusakan jaringan akibat paparan suhu tinggi (knalpot motor, setrika, cipratan minyak panas, air mendidih).",
        "langkah_p3k": [
            "Dinginkan Segera: Alirkan air kran bersuhu biasa selama 15-20 menit terus-menerus.",
            "Lepas Benda Menjepit: Buka cincin/jam tangan sebelum area membengkak.",
            "Oleskan Gel Pelembap: Gunakan gel lidah buaya murni atau salep luka bakar bebas.",
            "Lindungi Lepuh: Jangan pecahkan gelembung lepuh berisi cairan."
        ],
        "obat_rekomendasi_bebas": [
            "Gel Aloe Vera murni",
            "Salep Mefenamic / Bioplacenton",
            "Parasetamol untuk pereda nyeri"
        ],
        "pantangan_dan_mitos": [
            "SANGAT DILARANG mengoleskan pasta gigi (odol), kecap, mentega, atau tepung terigu!",
            "JANGAN menempelkan es batu langsung karena memicu radang dingin (*frostbite*)."
        ],
        "estimasi_sembuh": "1-2 minggu untuk luka bakar derajat 1 dan 2 superfisial.",
        "tanda_bahaya_ke_dokter": [
            "Luka bakar di area wajah, leher, kelamin, atau sendi gerak utama.",
            "Kulit tampak putih pucat atau hangus kehitaman mati rasa (derajat 3 - Segera ke IGD!)."
        ]
    },
    "PANU": {
        "nama_umum": "Panu (Tinea Versicolor / Pityriasis Versicolor)",
        "nama_medis": "Pityriasis Versicolor",
        "deskripsi": "Infeksi jamur Malassezia pada kulit, ditandai bercak putih/merah muda/cokelat bersisik halus dan gatal saat berkeringat.",
        "langkah_p3k": [
            "Jaga Kebersihan Kulit: Mandi teratur minimal 2x sehari setelah berkeringat.",
            "Keringkan Sempurna: Pastikan kulit kering sebelum berpakaian.",
            "Oleskan Salep Antijamur: Oleskan tipis merata pada bercak hingga 1-2 cm di luar batas bercak.",
            "Gunakan Pakaian Longgar: Pilih katun yang menyerap keringat."
        ],
        "obat_rekomendasi_bebas": [
            "Krim Antijamur Miconazole 2% atau Clotrimazole 1%",
            "Sampo Ketoconazole 2% / Selenium Sulfide"
        ],
        "pantangan_dan_mitos": [
            "JANGAN menggosok kulit dengan lengkuas/batu kasar hingga berdarah.",
            "JANGAN bertukar handuk atau pakaian dengan orang lain."
        ],
        "estimasi_sembuh": "2-3 minggu pengobatan rutin (pemulihan warna kulit 1-3 bulan).",
        "tanda_bahaya_ke_dokter": [
            "Bercak menyebar luas ke lebih dari 50% tubuh.",
            "Tidak membaik setelah 4 minggu pemakaian salep bebas."
        ]
    },
    "BISUL": {
        "nama_umum": "Bisul (Boil / Furuncle)",
        "nama_medis": "Furunculosis / Abses Kutan",
        "deskripsi": "Infeksi bakteri pada folikel rambut yang membentuk benjolan merah, bengkak, nyeri, dan berujung puncak nanah.",
        "langkah_p3k": [
            "Kompres Hangat: Tempelkan kain hangat selama 15-20 menit, 3-4 kali sehari.",
            "Jaga Kebersihan Tangan: Cuci tangan sebelum dan setelah menyentuh area sekitar bisul.",
            "Lindungi dengan Kasa: Tutup longgar agar tidak bergesekan dengan baju.",
            "Bilas jika Pecah: Bersihkan nanah dengan kasa steril berantiseptik saat pecah alami."
        ],
        "obat_rekomendasi_bebas": [
            "Salep Ichthyol (Salep Hitam)",
            "Kasa Steril & Plester",
            "Parasetamol / Ibuprofen untuk nyeri"
        ],
        "pantangan_dan_mitos": [
            "SANGAT DILARANG memencet atau menusuk bisul dengan jarum sendiri!",
            "HINDARI menyentuh bisul di area segitiga wajah (antara hidung dan bibir)."
        ],
        "estimasi_sembuh": "7-14 hari hingga mengempis atau pecah alami.",
        "tanda_bahaya_ke_dokter": [
            "Bisul di wajah dekat hidung/mata atau muncul beberapa mata bisul (karunkel).",
            "Disertai demam tinggi atau pasien mengidap diabetes."
        ]
    },
    "LUKA_TUSUK_PUNCTURE": {
        "nama_umum": "Luka Tusuk Benda Runcing / Paku (Puncture Wound)",
        "nama_medis": "Vulnus Punctum",
        "deskripsi": "Luka yang disebabkan oleh penetrasi benda runcing tajam (paku berkarat, duri ikan/tanaman, jarum suntik, kawat, pecahan kaca lancip) yang menembus jaringan dalam. Lubang luar kecil namun risiko tinggi infeksi anaerobik!",
        "langkah_p3k": [
            "Bilas Air Mengalir & Sabun Antiseptik: Alirkan air bersih mengalir dan sabun selama 5-10 menit untuk membuang kotoran yang terbawa masuk.",
            "Tekan Ringan Sekitar Luka: Biarkan sedikit darah mengalir keluar bersama kotoran, jangan ditekan terlalu keras.",
            "Disinfeksi dengan Povidone Iodine: Oleskan antiseptik iodin di permukaan lubang tusukan.",
            "TUTUP LONGGAR: JANGAN menutup luka tusuk dengan plester kedap udara (karena bakteri tetanus Clostridium tetani bersifat anaerob dan berkembang biak di tempat tanpa oksigen!).",
            "JANGAN Mencabut Benda Sendiri jika Masih Tertancap Dalam: Jika paku/pisau masih menancap dalam, stabilkan posisi benda dan segera ke IGD untuk pencabutan steril."
        ],
        "obat_rekomendasi_bebas": [
            "Povidone Iodine 10%",
            "Kasa Steril Longgar & Plester",
            "Parasetamol 500mg untuk pereda nyeri"
        ],
        "pantangan_dan_mitos": [
            "SANGAT DILARANG menutup luka tusuk dengan plester kedap udara tanpa sirkulasi oksigen (memicu tetanus fatal!).",
            "SANGAT DILARANG menaburkan bubuk kopi, minyak rem, abu rokok, atau tanah kotor!",
            "JANGAN mencabut paksa benda asing berukuran besar yang menancap dalam tanpa pengawasan tim medis."
        ],
        "estimasi_sembuh": "7-14 hari jika steril; pemantauan gejala tetanus selama 3-21 hari.",
        "tanda_bahaya_ke_dokter": [
            "Tertusuk benda kotor/berkarat/tanah (WAJIB suntik Serum Anti-Tetanus ATS / Vaksin TT dalam <48 jam!).",
            "Timbul rasa kaku pada rahang (trismus/lockjaw), kejang otot leher, atau demam tinggi.",
            "Benda asing (pecahan jarum/karat) tertinggal di dalam jaringan."
        ]
    },
    "LUKA_GIGITAN_HEWAN": {
        "nama_umum": "Luka Gigitan / Cakaran Hewan (Animal Bite / Rabies Risk)",
        "nama_medis": "Vulnus Morsum (Animal Bite)",
        "deskripsi": "Luka robekan atau tusukan gigi/cakar hewan berdarah panas (anjing, kucing, kera, kelelawar) yang berisiko fatal menularkan virus Rabies (Hydrophobia) atau infeksi bakteri anaerobik mulut hewan.",
        "langkah_p3k": [
            "CUCI DENGAN AIR MENGALIR DAN DETERJEN/SABUN MINIMAL 15 MENIT: Ini adalah protokol mutlak Kemenkes RI dan WHO! Deterjen/sabun mampu merusak selubung lemak (lipid envelope) virus rabies sehingga virus mati sebelum masuk ke saraf.",
            "Bilas dengan Antiseptik: Beri Povidone Iodine 10% atau alkohol 70% setelah dicuci sabun.",
            "JANGAN MENJAHIT LUKA: Luka gigitan hewan TIDAK BOLEH dijahit rapat kecuali darurat pendarahan arteri (agar virus tidak terperangkap di dalam jaringan).",
            "SEGERA KE FASKES / RABIES CENTER: Dapatkan suntikan Vaksin Anti Rabies (VAR) dan Serum Anti Rabies (SAR) sesegera mungkin!",
            "Amankan dan Observasi Hewan: Karantina hewan penggigit selama 10-14 hari untuk melihat tanda rabies (hewan mati, takut air, agresif, liur berlebih)."
        ],
        "obat_rekomendasi_bebas": [
            "Sabun antiseptik / deterjen mandi batangan",
            "Povidone Iodine 10%",
            "Kasa steril pelindung longgar"
        ],
        "pantangan_dan_mitos": [
            "SANGAT DILARANG menunda ke rumah sakit / faskes! Rabies memiliki tingkat kematian 99.9% jika gejala saraf sudah muncul!",
            "JANGAN mengoleskan cabai, getah, atau darah hewan yang menggigit pada luka (mitos berbahaya!).",
            "JANGAN membalut luka secara kedap udara."
        ],
        "estimasi_sembuh": "Luka fisik sembuh 7-14 hari; proteksi rabies memerlukan rangkaian vaksinasi VAR hari ke-0, 3, 7, dan 21.",
        "tanda_bahaya_ke_dokter": [
            "Semua gigitan anjing, kucing liar, monyet liar, atau kelelawar WAJIB segera ke IGD/Puskesmas Rabies Center!",
            "Luka gigitan berlokasi di area risiko tinggi (wajah, leher, ujung jari yang padat serabut saraf)."
        ]
    },
    "LUKA_BAKAR_BERAT_DERAJAT_3": {
        "nama_umum": "Luka Bakar Berat Derajat 3 (Full Thickness Burn)",
        "nama_medis": "Combustio Grade III (Full Thickness)",
        "deskripsi": "Kerusakan parah yang membakar seluruh ketebalan lapisan kulit (epidermis, dermis, dan jaringan lemak/otot di bawahnya), ditandai kulit tampak putih lilin pucat atau hangus gosong kehitaman (eschar), kaku mengeras, dan seringkali tidak terasa sakit karena ujung saraf sensorik telah terbakar hancur.",
        "langkah_p3k": [
            "HENTIKAN SUMBER PANAS: Padamkan api, matikan arus listrik, atau lepaskan pakaian yang terbakar jika tidak menempel pada kulit.",
            "TUTUP DENGAN KAIN STERIL KERING: Tutup area luka bakar dengan kain kasa steril atau kain katun bersih yang kering (JANGAN basahi dengan air dingin jika luka bakar luas karena memicu hipotermia!).",
            "Tinggikan Area yang Terbakar: Posisikan di atas dada jika memungkinkan untuk mengurangi pembengkakan.",
            "SEGERA HUBUNGI AMBULANS / IGD 119: Pasien membutuhkan cairan infus resusitasi (Formula Parkland) untuk mencegah syok hipovolemik."
        ],
        "obat_rekomendasi_bebas": [
            "Kasa steril kering penutup sementara",
            "Selimut hangat pelindung hipotermia"
        ],
        "pantangan_dan_mitos": [
            "SANGAT DILARANG mengoleskan odol/pasta gigi, kecap, mentega, tepung, atau minyak goreng!",
            "JANGAN merendam luka bakar luas dengan air es dingin (memicu syok hipotermia fatal).",
            "JANGAN mengelupas pakaian yang menempel rekat di kulit yang hangus terbakar."
        ],
        "estimasi_sembuh": "Memerlukan penanganan bedah rekonstruksi/cangkok kulit (skin graft) selama berbulan-bulan di rumah sakit.",
        "tanda_bahaya_ke_dokter": [
            "Luka bakar derajat 3 adalah DARURAT MERAH IGD MUTLAK!",
            "Luka bakar di area wajah, leher (risiko jalan napas bengkak), kelamin, atau sendi gerak utama."
        ]
    },
    "LUKA_MEMAR_KONTUSIO": {
        "nama_umum": "Luka Memar / Lebam Tumpul (Bruise / Contusion)",
        "nama_medis": "Vulnus Contusum / Hematoma Kutis",
        "deskripsi": "Cedera jaringan lunak akibat benturan benda tumpul (terantuk, terbentur meja, terpukul, terinjak) yang menyebabkan pembuluh darah kapiler di bawah kulit pecah tanpa adanya robekan kulit terbuka, menimbulkan bercak warna ungu kebiruan/merah tua dan pembengkakan nyeri.",
        "langkah_p3k": [
            "Protokol R.I.C.E (Rest, Ice, Compression, Elevation):",
            "1. Rest (Istirahat): Hindari menggerakkan atau membebani area yang cedera.",
            "2. Ice (Kompres Dingin): Kompres es dibalut handuk selama 15-20 menit setiap 2-3 jam pada 48 jam pertama untuk menghentikan pendarahan kapiler internal.",
            "3. Compression (Balut Tekan): Balut lembut dengan perban elastis (jangan terlalu kencang) untuk menekan pembengkakan.",
            "4. Elevation (Tinggikan): Posisikan anggota tubuh yang memar lebih tinggi dari posisi jantung.",
            "Kompres Hangat Setelah 48 Jam: Setelah 2 hari pertama berlalu, ganti ke kompres hangat untuk melancarkan sirkulasi darah dan menyerap sisa bekuan darah."
        ],
        "obat_rekomendasi_bebas": [
            "Gel Heparin Sodium (Thrombophob gel)",
            "Parasetamol 500mg untuk pereda nyeri",
            "Perban elastis pelindung"
        ],
        "pantangan_dan_mitos": [
            "SANGAT DILARANG mengurut atau memijat keras area memar pada 48 jam pertama (dapat merobek pembuluh darah lebih lebar dan memperparah pendarahan dalam!).",
            "JANGAN kompres air panas pada 24-48 jam pertama."
        ],
        "estimasi_sembuh": "1-2 minggu (warna memar memudar dari ungu/biru -> hijau -> kuning kecokelatan -> pulih).",
        "tanda_bahaya_ke_dokter": [
            "Memar membesar sangat cepat disertai nyeri luar biasa ekstrem (sindrom kompartemen).",
            "Memar di area kepala disertai pusing muntah, atau di area perut akibat benturan keras (risiko pendarahan organ dalam)."
        ]
    },
    "LUKA_TEKAN_DEKUBITUS": {
        "nama_umum": "Luka Tekan / Borok Dekubitus (Bedsore / Pressure Injury)",
        "nama_medis": "Decubitus Ulcer / Pressure Injury",
        "deskripsi": "Kerusakan kulit dan jaringan di bawahnya akibat penekanan berkepanjangan pada bagian tubuh dengan tonjolan tulang (tumit, bokong sakrum, pinggul, siku) pada pasien tirah baring lama, stroke, atau lansia, ditandai kemerahan menetap hingga borok terbuka bernanah.",
        "langkah_p3k": [
            "Ubah Posisi Tubuh Tiap 2 Jam: Miringkan pasien ke kiri dan kanan bergantian secara terjadwal untuk membebaskan titik tekanan tulang.",
            "Gunakan Kasur Anti-Dekubitus: Gunakan kasur angin bertekanan dinamis (air mattress bubble) untuk mendistribusikan tekanan tubuh.",
            "Cuci Luka dengan Cairan NaCl 0.9%: Bersihkan kotoran dan eksudat secara lembut menggunakan larutan saline steril (jangan gunakan alkohol pekat di dasar luka!).",
            "Gunakan Balutan Lembap Modern (Moist Wound Healing): Gunakan perban hidrokoloid, hidrogel, atau foam dressing untuk merangsang tumbuhnya jaringan granulasi merah sehat.",
            "Jaga Kulit Tetap Kering dari Ompol/Keringat: Ganti popok dewasa sesering mungkin agar kulit tidak mengalami maserasi."
        ],
        "obat_rekomendasi_bebas": [
            "Cairan Infus Saline NaCl 0.9%",
            "Salep Hydrogel / Madu Medis Perawatan Luka",
            "Balutan Foam Dressing / Hidrokoloid"
        ],
        "pantangan_dan_mitos": [
            "JANGAN memijat atau menggosok area tulang yang memerah (mempercepat robeknya jaringan bawah kulit).",
            "JANGAN membiarkan luka mengering mengeras terbuka tanpa balutan lembap (memperlambat pertumbuhan jaringan baru).",
            "HINDARI bantal donat berbentuk cincin berongga karena justru memotong sirkulasi darah di sekelilingnya."
        ],
        "estimasi_sembuh": "2-4 minggu untuk stadium 1-2; berbulan-bulan untuk stadium 3-4 dengan perawatan luka modern.",
        "tanda_bahaya_ke_dokter": [
            "Luka bertambah dalam hingga terlihat otot, tendon, atau tulang putih (Stadium 4).",
            "Mengeluarkan nanah berbau sangat busuk, demam tinggi, atau pasien menggigil (tanda sepsis sistemik)."
        ]
    },
    "LUKA_SAYAT_IRIS": {
        "nama_umum": "Luka Sayat / Iris Benda Tajam (Cut / Incised Wound)",
        "nama_medis": "Vulnus Scissum / Incisivum",
        "deskripsi": "Terputusnya lapisan kulit akibat irisan benda tajam tipis bertepi rata (pisau dapur, silet, cutter, pecahan beling datar, atau kertas kaku), ditandai tepi luka yang rapi dan pendarahan kapiler/vena yang mudah keluar.",
        "langkah_p3k": [
            "Hentikan Pendarahan Segera: Tekan langsung di atas luka menggunakan kain bersih atau kasa steril selama 3-5 menit tanpa diangkat-angkat.",
            "Bilas dengan Air Mengalir: Bersihkan darah dan kotoran dengan air mengalir atau cairan infus NaCl 0.9%.",
            "Disinfeksi Tepi Sayatan: Oleskan antiseptik Povidone Iodine di sekitar kulit tepi sayatan.",
            "Rapatkan Tepi Luka: Rekatkan kedua tepi luka yang terbelah dan kunci menggunakan plester luka (butterfly bandage) atau plester strip.",
            "Tutup Kasa Steril: Lindungi dari debu dan kuman."
        ],
        "obat_rekomendasi_bebas": [
            "Plester luka strip / butterfly",
            "Povidone Iodine 10%",
            "Kasa steril & micropore"
        ],
        "pantangan_dan_mitos": [
            "JANGAN menaburkan bubuk kopi, bedak, atau abu dapur pada sayatan.",
            "JANGAN membuka-buka kasa tekan sebelum 5 menit (mengganggu proses pembekuan darah alami)."
        ],
        "estimasi_sembuh": "5-8 hari tepi luka menyatu rapat.",
        "tanda_bahaya_ke_dokter": [
            "Panjang sayatan > 2 cm atau menganga lebar (membutuhkan jahitan dokter agar sembuh rapi tanpa bekas parut).",
            "Pendarahan memancar deras (indikasi cedera pembuluh darah arteri).",
            "Mati rasa atau jari tidak bisa ditekuk (indikasi putusnya tendon/saraf motorik)."
        ]
    }
}

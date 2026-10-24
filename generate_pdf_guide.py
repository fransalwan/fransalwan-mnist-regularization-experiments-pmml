import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, KeepTogether, PageBreak, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        
        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(54, 800, "PMML Assignment 2: Replikasi MNIST & Eksperimen Regularisasi")
            self.drawRightString(541, 800, "Frans Alwan Purba | MKA FMIPA UGM")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(54, 794, 541, 794)

        # Footer
        page_str = f"Halaman {self._pageNumber} dari {page_count}"
        self.drawString(54, 35, "Dokumen Persiapan Kelas & Diskusi Presentasi")
        self.drawRightString(541, 35, page_str)
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(54, 45, 541, 45)
        self.restoreState()

def build_pdf(filename="Class_Preparation_Guide_PMML_Assignment2.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom styles
    primary_color = colors.HexColor("#1E3A8A")   # Navy
    secondary_color = colors.HexColor("#0284C7") # Blue
    text_color = colors.HexColor("#1E293B")      # Dark slate
    accent_bg = colors.HexColor("#F8FAFC")

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=primary_color,
        spaceAfter=4
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=15,
        textColor=secondary_color,
        spaceAfter=12
    )

    h1_style = ParagraphStyle(
        'SectionH1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=primary_color,
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'SectionH2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        textColor=secondary_color,
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=text_color,
        spaceAfter=5
    )

    bullet_style = ParagraphStyle(
        'BulletText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=text_color,
        leftIndent=12,
        spaceAfter=3
    )

    qa_q_style = ParagraphStyle(
        'QAQuestion',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#0F172A"),
        spaceBefore=4,
        spaceAfter=2,
        keepWithNext=True
    )

    qa_a_style = ParagraphStyle(
        'QAAnswer',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12.5,
        textColor=colors.HexColor("#334155"),
        spaceAfter=6
    )

    code_style = ParagraphStyle(
        'CodeSnippet',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8,
        leading=10.5,
        textColor=colors.HexColor("#0F172A")
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=colors.white,
        alignment=1
    )

    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=10.5,
        textColor=text_color
    )

    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10.5,
        textColor=text_color
    )

    story = []

    # 1. Header Banner / Cover Information
    story.append(Paragraph("PANDUAN PERSIAPAN KELAS & PRESENTASI", title_style))
    story.append(Paragraph("Mata Kuliah: Pembelajaran Mesin Mendalam Lanjut (PMML) | MKA FMIPA UGM", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=primary_color, spaceBefore=0, spaceAfter=8))

    # Meta Table
    meta_data = [
        [Paragraph("<b>Nama Mahasiswa:</b> Frans Alwan Purba", body_style), Paragraph("<b>Dosen Pengampu:</b> Dr. Afiahayati, S.Kom., M.Cs.", body_style)],
        [Paragraph("<b>NIM:</b> 25/563545/PPA/07116", body_style), Paragraph("<b>Topik:</b> Replikasi MNIST & Eksperimen Regularisasi", body_style)],
        [Paragraph("<b>Framework:</b> TensorFlow 2.21 / Keras 3.15", body_style), Paragraph("<b>Repositori:</b> github.com/fransalwan/mnist-regularization-experiments-pmml", body_style)]
    ]
    meta_table = Table(meta_data, colWidths=[240, 247])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F1F5F9")),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 10))

    # 2. Objektif & Konteks Tugas
    story.append(Paragraph("1. Objektif & Latar Belakang Tugas", h1_style))
    story.append(Paragraph(
        "Tugas Assignment 2 bertujuan untuk memvalidasi pemahaman mahasiswa mengenai konsep <i>Learning Strategy</i> dan teknik pencegahan <i>overfitting</i> pada Deep Neural Network. Eksperimen diawali dengan mereplikasi model dasar (Slide 20–23) berupa Artificial Neural Network (Feedforward MLP) untuk klasifikasi digit MNIST, lalu mengevaluasi secara komparatif lima skenario regularisasi: L1, L2, Dropout, Early Stopping, dan kombinasi L1 + Dropout.",
        body_style
    ))

    # 3. Teori Dasar & Formulasi Matematis
    story.append(Paragraph("2. Landasan Teori & Formulasi Matematis", h1_style))
    
    story.append(Paragraph("A. Mengapa Overfitting Terjadi?", h2_style))
    story.append(Paragraph(
        "Overfitting terjadi ketika model memiliki kapasitas parameter yang berlebih dibandingkan kompleksitas pola intrinsik data. Model menghafal <i>noise</i> dan artefak spesifik pada training set, yang ditandai dengan penurunan kontinu pada training loss namun diikuti saturasi atau peningkatan pada validation loss (gap generalisasi melebar).",
        body_style
    ))

    story.append(Paragraph("B. Komparasi Empat Pendekatan Regularisasi", h2_style))
    
    p_l1 = (
        "<b>1. Regularisasi L1 (Lasso Penalty):</b><br/>"
        "Menambahkan suku penalti nilai absolut bobot pada fungsi objektif:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<b>J(W) = L_CE(y, y_hat) + &lambda; &Sigma; |w_ij|</b><br/>"
        "Mekanisme turunan menghasilkan gradien konstan &plusmn;&lambda;. Hal ini memaksa bobot fitur yang tidak signifikan (seperti piksel latar belakang MNIST yang bernilai 0) menjadi <b>tepat nol (sparsity)</b>. L1 berfungsi sekaligus sebagai seleksi fitur terintegrasi."
    )
    story.append(Paragraph(p_l1, bullet_style))

    p_l2 = (
        "<b>2. Regularisasi L2 (Ridge / Weight Decay):</b><br/>"
        "Menambahkan suku penalti kuadrat nilai bobot:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<b>J(W) = L_CE(y, y_hat) + &lambda; &Sigma; (w_ij)&sup2;</b><br/>"
        "Mekanisme update gradien mendegradasi bobot secara proporsional: <b>w &larr; (1 - 2&eta;&lambda;)w - &eta;&nabla;L</b>. Mencegah bobot ekstrem, meredam ketergantungan pada piksel tunggal, dan menjaga permukaan loss tetap mulus tanpa membuat bobot tepat nol."
    )
    story.append(Paragraph(p_l2, bullet_style))

    p_drop = (
        "<b>3. Dropout (Stochastic Regularization):</b><br/>"
        "Secara acak menonaktifkan neuron pada lapisan tersembunyi dengan probabilitas <i>p = 0.25</i> pada setiap mini-batch iterasi. Memutus ketergantungan ko-adaptasi (<i>co-adaptation</i>) antar neuron, memaksa setiap unit mempelajari representasi yang mandiri dan tangguh. Bertindak sebagai aproksimasi <i>ensemble learning</i> dari ribuan sub-jaringan."
    )
    story.append(Paragraph(p_drop, bullet_style))

    p_es = (
        "<b>4. Early Stopping (Regularisasi Komputasional):</b><br/>"
        "Menghentikan proses iterasi pelatihan secara otomatis ketika <i>validation loss</i> berhenti menurun selama <i>patience = 3</i> epoch. Opsi <code>restore_best_weights = True</code> menjamin model menyimpan parameter pada titik optimum global, menghemat biaya komputasi dan mencegah over-training."
    )
    story.append(Paragraph(p_es, bullet_style))

    story.append(Spacer(1, 6))

    # 4. Arsitektur Teknis
    story.append(Paragraph("3. Arsitektur Teknis & Parameter Jaringan", h1_style))
    story.append(Paragraph(
        "Arsitektur dirancang konsisten di seluruh skenario: <b>Flatten(28&times;28 &rarr; 784) &rarr; Dense(64, ReLU) &rarr; [Regularizer] &rarr; Dense(10, Softmax)</b>.",
        body_style
    ))

    arch_data = [
        [Paragraph("Layer", table_header_style), Paragraph("Tipe Layer", table_header_style), Paragraph("Dimensi Output", table_header_style), Paragraph("Parameter", table_header_style), Paragraph("Keterangan", table_header_style)],
        [Paragraph("1", table_cell_bold), Paragraph("Flatten", table_cell_style), Paragraph("(None, 784)", table_cell_style), Paragraph("0", table_cell_style), Paragraph("Meratakan matriks citra 28&times;28", table_cell_style)],
        [Paragraph("2", table_cell_bold), Paragraph("Dense (Hidden)", table_cell_style), Paragraph("(None, 64)", table_cell_style), Paragraph("50,240", table_cell_style), Paragraph("784 &times; 64 bobot + 64 bias (ReLU)", table_cell_style)],
        [Paragraph("3", table_cell_bold), Paragraph("Dropout", table_cell_style), Paragraph("(None, 64)", table_cell_style), Paragraph("0", table_cell_style), Paragraph("Hanya aktif saat Skenario 2(c) & 2(e)", table_cell_style)],
        [Paragraph("4", table_cell_bold), Paragraph("Dense (Output)", table_cell_style), Paragraph("(None, 10)", table_cell_style), Paragraph("650", table_cell_style), Paragraph("64 &times; 10 bobot + 10 bias (Softmax)", table_cell_style)],
        [Paragraph("Total", table_cell_bold), Paragraph("Trainable Parameters", table_cell_bold), Paragraph("-", table_cell_style), Paragraph("<b>50,890</b>", table_cell_bold), Paragraph("Kapasitas bobot konstan di semua skenario", table_cell_style)]
    ]
    arch_table = Table(arch_data, colWidths=[30, 95, 80, 65, 217])
    arch_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_color),
        ('ALIGN', (0,0), (-1,0), 'CENTER'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-2), [colors.white, colors.HexColor("#F8FAFC")]),
        ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(arch_table)

    story.append(Spacer(1, 10))

    # 5. Tabel Hasil Eksperimen
    story.append(Paragraph("4. Rekapitulasi Hasil Eksperimen Empiris", h1_style))
    story.append(Paragraph(
        "Hasil pengujian evaluasi pada test set MNIST (10.000 citra uji) setelah pelatihan dengan random seed 42:",
        body_style
    ))

    res_data = [
        [Paragraph("No", table_header_style), Paragraph("Skenario Pengujian", table_header_style), Paragraph("Metode Regularisasi", table_header_style), Paragraph("Hyperparameter", table_header_style), Paragraph("Test Loss", table_header_style), Paragraph("Test Acc", table_header_style), Paragraph("&Delta; Acc", table_header_style), Paragraph("Status / Catatan", table_header_style)],
        [Paragraph("0", table_cell_bold), Paragraph("Baseline", table_cell_style), Paragraph("Tanpa Regularisasi", table_cell_style), Paragraph("-", table_cell_style), Paragraph("0.0919", table_cell_style), Paragraph("97.13%", table_cell_style), Paragraph("Acuan", table_cell_style), Paragraph("Slide 20-23, rentan overfit iterasi lanjut", table_cell_style)],
        [Paragraph("1", table_cell_bold), Paragraph("Scenario 2(a)", table_cell_style), Paragraph("L1 Regularization", table_cell_style), Paragraph("&lambda; = 10<sup>-4</sup>", table_cell_style), Paragraph("0.1728", table_cell_style), Paragraph("97.28%", table_cell_style), Paragraph("+0.15%", table_cell_bold), Paragraph("Akurasi naik berkat sparsity fitur", table_cell_style)],
        [Paragraph("2", table_cell_bold), Paragraph("Scenario 2(b)", table_cell_style), Paragraph("L2 Regularization", table_cell_style), Paragraph("&lambda; = 10<sup>-3</sup>", table_cell_style), Paragraph("0.1568", table_cell_style), Paragraph("97.06%", table_cell_style), Paragraph("-0.07%", table_cell_style), Paragraph("Weight decay meredam bobot ekstrem", table_cell_style)],
        [Paragraph("3", table_cell_bold), Paragraph("Scenario 2(c)", table_cell_bold), Paragraph("Dropout", table_cell_bold), Paragraph("p = 0.25 (25%)", table_cell_bold), Paragraph("<b>0.0918</b>", table_cell_bold), Paragraph("<b>97.34%</b>", table_cell_bold), Paragraph("<b>+0.21%</b>", table_cell_bold), Paragraph("<b>Performa Terbaik (Loss & Acc)</b>", table_cell_bold)],
        [Paragraph("4", table_cell_bold), Paragraph("Scenario 2(d)", table_cell_style), Paragraph("Early Stopping", table_cell_style), Paragraph("patience = 3", table_cell_style), Paragraph("0.0965", table_cell_style), Paragraph("97.07%", table_cell_style), Paragraph("-0.06%", table_cell_style), Paragraph("Stop di Ep. 15, bobot Ep. 12 direstorasi", table_cell_style)],
        [Paragraph("5", table_cell_bold), Paragraph("Scenario 2(e)", table_cell_style), Paragraph("L1 + Dropout", table_cell_style), Paragraph("&lambda;=10<sup>-4</sup>, p=0.25", table_cell_style), Paragraph("0.1881", table_cell_style), Paragraph("97.17%", table_cell_style), Paragraph("+0.04%", table_cell_style), Paragraph("Proteksi ganda (analitik + stokastik)", table_cell_style)]
    ]
    res_table = Table(res_data, colWidths=[20, 75, 85, 65, 48, 50, 42, 102])
    res_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_color),
        ('ALIGN', (0,0), (-1,0), 'CENTER'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('BACKGROUND', (0,4), (-1,4), colors.HexColor("#DCFCE7")), # Highlight best
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(res_table)
    story.append(Spacer(1, 8))

    # Visual Plot
    plot_path = "plots/comparison_val_loss.png"
    if os.path.exists(plot_path):
        story.append(Paragraph("<b>Grafik Perbandingan Validation Loss Seluruh Skenario:</b>", h2_style))
        img = Image(plot_path, width=440, height=220)
        story.append(img)
        story.append(Spacer(1, 8))

    # 6. Jawaban Pertanyaan Kritis Dosen
    story.append(Paragraph("5. Bank Jawaban Kritis untuk Tanya Jawab (Q&A)", h1_style))

    q1 = "<b>T: Kenapa Test Loss L1 (0.1728) dan L2 (0.1568) lebih tinggi dari Baseline (0.0919), padahal akurasinya kompetitif?</b>"
    a1 = "<b>Jawab:</b> Pada Keras/TensorFlow, nilai loss yang dilaporkan saat evaluasi regularizer adalah <i>Total Loss</i> yang mencakup suku penalti: <b>J_total = L_CE + &lambda;&Omega;(W)</b>. Penalti L1/L2 menambahkan offset skalar positif pada total loss. Loss yang tampak lebih besar bukan berarti model salah mengklasifikasi, melainkan refleksi dari nilai penalti bobot. Buktinya, metrik akurasi L1 justru meningkat (+0.15%) dibanding baseline."
    story.append(Paragraph(q1, qa_q_style))
    story.append(Paragraph(a1, qa_a_style))

    q2 = "<b>T: Mengapa Dropout menghasilkan performa akurasi tertinggi (97.34%) pada tugas ini?</b>"
    a2 = "<b>Jawab:</b> Citra MNIST memiliki korelasi spasial antar piksel. MLP standar rentan mengalami <i>co-adaptation</i> (sejumlah neuron hanya aktif secara bersamaan mengoreksi error neuron lain). Dengan menonaktifkan 25% neuron secara acak di setiap iterasi, jaringan dipaksa belajar representasi fitur yang terdistribusi dan independen. Saat evaluasi/pengujian, seluruh neuron aktif secara simultan layaknya model <i>ensemble</i>."
    story.append(Paragraph(q2, qa_q_style))
    story.append(Paragraph(a2, qa_a_style))

    q3 = "<b>T: Mengapa pada Early Stopping pelatihan berhenti di Epoch 15 tetapi bobot Epoch 12 yang disimpan?</b>"
    a3 = "<b>Jawab:</b> Parameter <code>patience = 3</code> memberikan toleransi 3 epoch berturut-turut tanpa perbaikan <i>validation loss</i>. Val loss terendah tercapai pada Epoch 12. Karena pada Epoch 13, 14, dan 15 val loss tidak menurun, callback menghentikan pelatihan di Epoch 15. Fitur <code>restore_best_weights = True</code> mengembalikan bobot ke kondisi optimum Epoch 12, menghemat 25% komputasi dan membuang bobot yang mulai overfit."
    story.append(Paragraph(q3, qa_q_style))
    story.append(Paragraph(a3, qa_a_style))

    q4 = "<b>T: Apakah penambahan Dropout atau L1/L2 menambah beban memori parameter model?</b>"
    a4 = "<b>Jawab:</b> Tidak sama sekali. Total trainable parameter tetap konsisten di <b>50,890 parameter</b> di seluruh model. L1/L2 hanya memodifikasi fungsi loss dan turunan gradien, sementara Dropout hanya menerapkan mask biner stokastik pada forward pass tanpa memiliki matriks bobot atau bias tersendiri."
    story.append(Paragraph(q4, qa_q_style))
    story.append(Paragraph(a4, qa_a_style))

    story.append(Spacer(1, 6))

    # 7. Panduan Alur Presentasi PPTX
    story.append(Paragraph("6. Panduan Alur Presentasi Slide-by-Slide (8 Slide)", h1_style))
    
    ppt_flow = [
        "<b>Slide 1 (Judul):</b> Sapa dosen & rekan, sebutkan identitas (Frans Alwan Purba, MKA UGM), judul tugas mengenai strategi regularisasi pada MNIST.",
        "<b>Slide 2 (Repositori & Setup):</b> Tunjukkan repositori GitHub, notebook interaktif, penggunaan random seed 42 untuk jaminan reproduktifitas.",
        "<b>Slide 3 (Skenario 2a - L1):</b> Bahas konsep Lasso & sparsity. Tekankan eliminasi piksel non-esensial yang mendongkrak akurasi hingga 97.28%.",
        "<b>Slide 4 (Skenario 2b - L2):</b> Bahas Ridge & weight decay. Tekankan fungsi penghalusan bobot ekstrem dan kestabilan gradien dengan akurasi 97.06%.",
        "<b>Slide 5 (Skenario 2c - Dropout):</b> Sorot ini sebagai <b>Champion Model</b> (Akurasi 97.34%, Loss 0.0918). Jelaskan konsep pemutusan ko-adaptasi neuron.",
        "<b>Slide 6 (Skenario 2d - Early Stopping):</b> Tekankan efisiensi komputasi: hemat 25% epoch (berhenti di Epoch 15 dan restore Epoch 12) dengan akurasi 97.07%.",
        "<b>Slide 7 (Skenario 2e - Kombinasi L1 + Dropout):</b> Jelaskan sinergi penalti matematis + stokastik arsitektural (akurasi stabil 97.17%).",
        "<b>Slide 8 (Kesimpulan & Rekomendasi):</b> Berikan kesimpulan praktis: kombinasi Dropout dan Early Stopping adalah strategi paling ideal untuk MLP klasifikasi citra sederhana."
    ]
    for step in ppt_flow:
        story.append(Paragraph(f"&bull; {step}", bullet_style))

    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#CBD5E1"), spaceBefore=4, spaceAfter=8))
    story.append(Paragraph("<i>Dokumen dibuat secara otomatis untuk bahan acuan resmi tugas PMML MKA FMIPA UGM.</i>", ParagraphStyle('Footnote', fontName='Helvetica-Oblique', fontSize=7.5, textColor=colors.HexColor("#64748B"), alignment=1)))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF successfully generated: {filename}")

if __name__ == "__main__":
    build_pdf()

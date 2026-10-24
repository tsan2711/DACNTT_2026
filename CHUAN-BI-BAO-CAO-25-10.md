# Chuẩn bị báo cáo 25/10/2026

Deck: `BaoCaoCuoiKy_25-10_52300057_52300006_v2.pptx` (16 slide, có speaker notes)
Demo: `.venv/bin/python tools/demo_verifier.py` (CPU, ~10 giây)
Thời lượng mục tiêu: 15–20 phút + hỏi đáp.

---

## PHẦN A — KIẾN THỨC CẦN NẮM

### A1. Dự án trong 1 câu
> Người ta nói model AI nhỏ có thể **tự giỏi toán lên** bằng cách học lại từ bài làm của chính nó.
> Nhóm kiểm tra lời đó ở model 1,5B và thấy: **không, nó không giỏi lên.**

Đây là **kết quả âm tính** (negative result). Kết quả âm tính có giá trị nếu đo cẩn thận.

### A2. Câu chuyện học sinh – giáo viên
- **Học sinh** = model **Qwen2.5-1.5B-Instruct** (nhỏ).
- **Giáo viên** = máy chấm **`math-verify`**. Chỉ nhìn **đáp án cuối**, không đọc lời giải.
- Mỗi vòng **GVT** (Generate → Verify → Select → Train):
  1. Học sinh làm bài, mỗi đề làm nhiều lần.
  2. Giáo viên so đáp án với sách.
  3. Giữ bài đúng, bỏ bài sai.
  4. Học sinh ôn lại chính những bài được giữ.
  5. Lặp lại 5 vòng.
- Gọi là "tự cải thiện" vì **không cần người chấm tay**.

**Câu hỏi nghiên cứu:** sau nhiều vòng, học sinh **giỏi toán thật**, hay chỉ **học viết cho vừa ý giáo viên**?

### A3. Thuật ngữ bắt buộc thuộc
| Từ | Nghĩa |
|---|---|
| **pass@1** | Làm mỗi đề 1 lần → % đề đúng |
| **pass@k** | Làm mỗi đề k lần (k=8) → % đề có **ít nhất 1 lần** đúng. k là số lần làm lại, **không phải** số cách giải |
| **Held-out exam** | 150 đề để riêng, model **không bao giờ học**. Thi trên đây mới là điểm thật |
| **LoRA** | Chỉ chỉnh một phần nhỏ model → train nhẹ, chạy được trên GPU Kaggle |
| **Learning rate (lr)** | Tốc độ học. Nhóm thử 4 mức: 1e-5 → 5e-4 |
| **Seed** | Hạt giống ngẫu nhiên. Chạy lại nhiều seed để chắc kết quả không do may rủi |
| **Đối chứng (control)** | Chạy phiên bản "bỏ đi một thứ" để xem thứ đó có tác dụng không |
| **MATH-500 / GSM8K** | Bộ đề toán khó / toán đố tiểu học |

### A4. Bốn phát hiện chính
1. **Model không giỏi lên.** 4 learning rate, nhiều seed, 2 bộ đề. Không lần nào có mức tăng đáng tin. Khoảng tin cậy loại trừ mức tăng > 2,2 điểm độ chính xác.
   Ví dụ Run A: pass@1 32% → ~29%, pass@8 gần như đứng yên.
2. **Học nhanh quá thì tệ đi.** Ở lr cao nhất (5e-4), độ chính xác giảm ở mọi lần chạy. Hai lý do:
   - Bài làm xong thì sai nhiều hơn (kém 5–11 điểm so với model gốc trên cùng đề).
   - Model viết dài hơn, bị cắt ở giới hạn 512 token nhiều hơn.
3. **Lệch định dạng làm máy chấm loại nhầm bài đúng** (phần demo).
   - Đáp án sách: `\frac43`. Model viết: `\boxed{\frac{4}{3}}`. Cùng là 4/3 nhưng bị chấm **SAI**.
   - Loại nhầm **15,5–18,4%** bài đúng → **cứ ~6 bài đúng thì vứt 1**.
   - Chuẩn hoá định dạng rồi chấm lại: điểm tuyệt đối cao hơn 4,7–8 điểm, nhưng **vẫn không tiến bộ**. Kết luận giữ nguyên.
4. **Hai đối chứng không tạo khác biệt.**
   - Vá lỗi `\dfrac`: lỗi này chỉ xuất hiện ở ~0,5% bài, quá hiếm để ảnh hưởng.
   - Bỏ hẳn bước lọc (học cả bài sai): không khác rõ.
   - → Bước "chấm và lọc", trái tim của GVT, **không thấy tác dụng** ở quy mô này.

### A5. Điểm trung thực (nói ra để được tin)
- Thiết kế đầu tiên (gộp 2 bộ đề, chấm trên chính đề đã học) cho thấy model **sụp mạnh**. Làm lại cẩn thận (tách riêng, thi đề để riêng) thì **không lặp lại** → nhóm thu hẹp kết luận theo dữ liệu.
- **Giới hạn:** model nhỏ, ít seed, GPU hạn chế. Câu hỏi "model có học kiểu viết của giáo viên không" **chưa trả lời được**.

### A6. So với các bài báo khác (đã tra arXiv ngày 24/10/2026)

**Bài gốc, báo cáo có cải thiện → khác nhóm mình, nhưng họ dùng model lớn:**
| Bài | Nội dung | Vì sao khác |
|---|---|---|
| **STaR** — Zelikman và cộng sự, NeurIPS 2022, arXiv:2203.14465 | Tự sinh lời giải rồi học lại, model tiến bộ | Chính bài thừa nhận model ban đầu phải **đủ lớn** để có năng lực suy luận |
| **ReST-EM** — Singh và cộng sự (Google DeepMind), arXiv:2312.06585 | Self-training trên MATH vượt fine-tune bằng dữ liệu người | Dùng PaLM 2 (rất lớn); kết quả **tốt lên theo kích thước model** |

**Bài kiểm chứng gần đây → giống nhóm mình:**
| Bài | Nội dung | Giống ở đâu |
|---|---|---|
| **Yue và cộng sự**, NeurIPS 2025, arXiv:2504.13837 | RL **không tạo năng lực mới**, chỉ giúp đúng sớm hơn; pass@k lớn thì model gốc bằng hoặc hơn | pass@k của mình đứng yên |
| **Phantom Gains** — Xu và cộng sự, 08/2026, arXiv:2608.20290 | Self-training Qwen3-8B: nhiều "tiến bộ" là **ảo** khi có đối chứng; self-training còn làm hỏng đề vốn giải được | Mình cũng dùng đối chứng + đề để riêng, và thấy điểm giảm |

**Về máy chấm:**
| Bài | Nội dung | So sánh |
|---|---|---|
| **TinyV** — Xu và cộng sự, ICML 2025, arXiv:2505.14625 | >38% bài trên Big-Math bị verifier chấm nhầm là sai; sửa thì RL tốt hơn tới 10% | Cùng hiện tượng (mình đo 15,5–18,4%), nhưng ở mình sửa xong **kết luận không đổi** |

⚠️ Chỉ trích các số ở bảng trên (38%, 10%). Mới đọc tóm tắt, chưa mở bảng đầy đủ của từng bài.

---

## PHẦN B — BÁO CÁO THẾ NÀO (theo từng slide)

| Slide | Nói gì | Thời gian |
|---|---|---|
| 1–2 Bìa, mục lục | Chào thầy, giới thiệu nhóm, đề tài | 0:30 |
| 3 Đề tài | Kể chuyện **học sinh – giáo viên** (A2). Kết bằng câu hỏi "giỏi thật hay học chữ?" | 2:00 |
| 4 Cách đo | pass@1, pass@k, **đề để riêng** (A3). Nhấn: k là số lần làm lại | 1:30 |
| 5 Máy chấm | 2 loại lệch định dạng: `\dfrac` hiếm (<1%), `\boxed` phổ biến (15,5–18,4%). Nói là **lệch định dạng**, không nói ai gây ra | 1:30 |
| 6 Thiết kế | Model 1,5B, LoRA, 5 vòng, 4 lr, 2 bộ đề, đối chứng | 1:00 |
| 7–8 Kết quả 1, 2 | Phát hiện ① và ② (A4) | 3:00 |
| 9 Đối chứng | Phát hiện ④ | 1:30 |
| 10 Phát hiện | Phát hiện ③: 1/6 bài đúng bị vứt; chấm lại, kết luận vẫn giữ | 1:30 |
| 11 Demo | Chạy demo (xem Phần C) | 1:30 |
| 12 Trả lời | Trả lời câu hỏi nghiên cứu: **không giỏi lên** | 1:30 |
| 13 So sánh | Bảng 5 bài báo, nói đoạn so sánh (xem dưới) | 1:00 |
| 14 Giới hạn | A5 | 1:00 |
| 15 Việc tiếp theo | Model lớn hơn, nhiều seed hơn, đo kiểu viết tốt hơn | 0:45 |
| 16 Cảm ơn | Mời thầy đặt câu hỏi | — |

**Đoạn so sánh bài khác (nói ở slide 13, ~30 giây):**
> "Các bài gốc như STaR và ReST-EM báo cáo cải thiện, nhưng họ dùng model lớn. Các nghiên cứu kiểm chứng gần đây, như Yue và cộng sự ở NeurIPS 2025 và Phantom Gains năm 2026, đều thấy self-training không mở rộng năng lực thật. Kết quả của nhóm ở model 1,5B nhất quán với các nghiên cứu này. Về máy chấm, TinyV cũng ghi nhận verifier loại nhầm bài đúng, hơn 38% trên bộ của họ."

### Câu chốt để thầy nhớ
> "Vòng tự học trông có vẻ hợp lý, nhưng ở model nhỏ, tín hiệu 'đáp án cuối có được chấm đúng không' **không đủ** để dạy model giỏi toán hơn."

---

## PHẦN C — DEMO

```bash
.venv/bin/python tools/demo_verifier.py
```
Nhấn Enter để qua từng phần:
1. **Ví dụ tay:** cùng 4/3 → máy chấm gốc SAI, đã chuẩn hoá ĐÚNG.
2. **3 bài thật** của model bị chấm nhầm.
3. **Bảng tổng:** 15,5–18,4% bài đúng bị loại nhầm.

Muốn chấm trực tiếp: thêm `--live 200` (khoảng 10 giây).

**Lời dẫn:**
> "Để chấm, máy phải so đáp án model với đáp án sách. Hai bên viết khác định dạng: sách viết trần, model bọc trong `\boxed{}`. Cùng là 4/3 nhưng máy chấm sai. Lỗi không báo gì cả, âm thầm xảy ra: cứ 6 bài đúng thì 1 bài bị vứt khỏi tập học. Nhóm đã chuẩn hoá định dạng và chấm lại toàn bộ: model vẫn không tiến bộ."

**Nếu thầy hỏi thẳng "lệch định dạng do đâu?"** → trả lời thật: *"Do cách lưu đáp án gốc trong pipeline, nhóm phát hiện khi tự kiểm lại và đã sửa, chấm lại toàn bộ."* (Paper đã ghi rõ, đừng né.)

---

## PHẦN D — CÂU HỎI DỄ GẶP

| Câu hỏi | Trả lời |
|---|---|
| Kết quả âm tính thì đóng góp gì? | Kiểm một tuyên bố phổ biến ở model nhỏ và thấy không đứng; tìm ra một nguồn sai lệch của verifier mà người khác cũng có thể gặp; kết quả khớp với các nghiên cứu kiểm chứng gần đây. |
| Sao không dùng model lớn? | Giới hạn GPU Kaggle. Đề tài nhắm đúng model nhỏ. STaR cũng nói phương pháp cần model đủ lớn, nên kiểm ở model nhỏ là có ý nghĩa. |
| Có chắc không phải do train sai? | 4 learning rate, nhiều seed, 3 đối chứng, thi trên đề để riêng. |
| Sao không sửa máy chấm cho tốt? | Đề tài là **đo** tuyên bố, không phải sửa máy chấm. Sửa máy chấm là hướng của TinyV. |
| pass@k tăng = nhiều cách giải? | Không. k chỉ là số lần làm lại cùng đề. |
| Khác gì Yue và cộng sự? | Họ dùng RL, model lớn hơn. Mình dùng vòng lọc + SFT (học có giám sát) thuần, model 1,5B. Cùng hình dạng kết quả. |
| Khoảng tin cậy có chắc không? | Chưa tính phương sai giữa các seed train, nên chỉ giới hạn hiệu ứng một cách lỏng. Đã ghi trong giới hạn. |

---

## PHẦN E — VIỆC LÀM TỐI NAY
- [ ] Đọc A2 + A4 đến khi kể được bằng lời của mình
- [ ] Đọc A6, thuộc tên 5 bài (STaR, ReST-EM, Yue, Phantom Gains, TinyV)
- [ ] Chạy demo 1 lần trên máy mang đi báo cáo
- [ ] Tập nói 1 lượt với đồng hồ (< 20 phút)
- [ ] Đọc Phần D, tự trả lời to từng câu

Nguồn (tra 24/10/2026):
- https://arxiv.org/abs/2203.14465
- https://arxiv.org/abs/2312.06585
- https://arxiv.org/abs/2504.13837
- https://arxiv.org/abs/2608.20290
- https://arxiv.org/abs/2505.14625

# Kịch bản thuyết trình — báo cáo 25/10/2026

Đi kèm `BaoCaoNhanh_25-10_52300057_52300006.pptx` (11 slide) và `paper_revised.pdf` (33 trang).
Tổng khoảng **12 phút** + hỏi đáp. Đọc to thử ít nhất một lần trước khi vào.

**Bối cảnh:** lần báo cáo trước (13/9) nhóm đã trình bày đề tài, thiết kế gộp, và việc giả thuyết bị bác bỏ ở
learning rate 1e-5. Hôm nay: **ôn phần cũ thật ngắn (slide 2–3), dồn thời gian cho phần mới (slide 4–9).**

**Ba điều cần nhớ khi nói:**
1. Câu mở đầu và câu kết luận **giống nhau**: *không thấy model giỏi lên.*
2. Mỗi kết quả nói kèm **chỗ nằm trong paper** ("Bảng 4 của paper"). Thầy thấy nhóm nắm chắc tài liệu.
3. Nói chậm ở **slide 6** (phát hiện) và **slide 8** (kết luận). Dừng 2 giây cho thầy nhìn.

---

## Chuẩn bị trước khi vào phòng
- [ ] Deck nhanh mở ở chế độ trình chiếu.
- [ ] `paper_revised.pdf` mở ở cửa sổ thứ hai, sẵn trang 1.
- [ ] Terminal ở thư mục gốc repo, gõ sẵn: `.venv/bin/python 25-10-2026/demo_verifier.py`
- [ ] `demo_output.txt` để dự phòng nếu máy lỗi.
- [ ] Deck đầy đủ `BaoCaoDayDu_*.pptx` (hoặc bản v2 ở gốc repo) để mở khi bị hỏi sâu.

## Bản đồ paper (để chỉ khi thầy hỏi)

| Paper | Nội dung | Trang |
|---|---|---|
| Abstract | Toàn bộ kết luận | 1 |
| §1 Introduction | Câu hỏi nghiên cứu | 1 |
| §2 Related Work | STaR, ReST-EM, Yue, TinyV, Phantom Gains | 2 |
| §3.2 The Verifier | Lỗi `\dfrac`, lỗi `\boxed` 15,5–18,4% | 3 |
| §3.3 + Bảng 1 | Hai thiết kế, danh sách mọi lần chạy | 4–5 |
| §4.1 + Bảng 2 | Thiết kế gộp: cú sụp 50 → 18,6% | 6 |
| §4.2 + Hình 1, Bảng 3 | Làm lại cô lập: không sụp | 6–8 |
| §4.3 | Vá `\dfrac` không đo được tác dụng | 7 |
| §4.4 + Bảng 4, 5 | 4 learning rate, khoảng tin cậy (≤ +2,2 điểm) | 7–9 |
| Bảng 6 | Đối chứng: vá, bỏ lọc, train trên gold | 10 |
| §4.5 + Bảng 7 | Vì sao tụt | 9–11 |
| §5.1 | Trả lời câu hỏi đề tài | 10 |
| §6, §7 | Giới hạn, kết luận | 11–12 |
| Tài liệu tham khảo | | 12–13 |
| Phụ lục A–K | Bản đầy đủ: B verifier (15), G learning rate (22), H anatomy (25), J giới hạn (31), K hướng tiếp | 13–33 |

---

Lời nói dưới đây sinh từ `tools/make_quick_pptx.py`, giống hệt phần ghi chú (speaker notes) trong deck. Mỗi đoạn đọc theo thứ tự chữ trên slide; dòng nghiêng là chỗ trong paper, cũng in ở chân slide.

<!-- SLIDES:BEGIN -->

## Slide 1 — Bìa

> Em chào thầy. Nhóm em gồm Sang và Duy Anh. Đề tài: tự học có làm model nhỏ giỏi toán hơn không?
>
> Lần trước nhóm đã báo cáo phần đầu. Hôm nay em trình bày phần làm tiếp, đã viết thành paper.
>
> Nói trước câu trả lời: không thấy model giỏi lên.

---

## Slide 2 — 01 · Câu hỏi
*Trong paper: §1 Introduction (tr. 1) · §3.4 các thước đo (tr. 4)*

> Nhắc lại ý tưởng: model tự làm bài, máy tự chấm, bài nào đúng thì giữ lại cho model học. Lặp vài vòng.
>
> Nhưng máy chấm chỉ nhìn đáp số cuối, không đọc lời giải. Nên câu hỏi là: model giỏi toán thật, hay chỉ học cách ghi đáp số cho vừa ý máy chấm?
>
> Nhóm chấm trên 150 đề mà model chưa từng học (mục 1 của paper).

**Nếu bị hỏi:** 4 thước đo chốt TRƯỚC khi chạy: pass@1, pass@k, kiểu chữ, số đề thêm/mất. pass@k: làm k lần, ít nhất 1 lần đúng; k là số lần làm lại, không phải số cách giải.

---

## Slide 3 — 02 · Cách làm
*Trong paper: §3.3 + Bảng 1 (tr. 4–5) · §4.1–4.2, Bảng 2–3 (tr. 6–8)*

> Để chắc không bỏ sót, nhóm thử nhiều cách: 4 tốc độ học, mỗi cách chạy 2–3 lần, thêm 3 phép đối chứng.
>
> Khung dưới là chuyện lần trước: cách làm đầu tiên cho thấy model tụt mạnh, nhưng làm lại cẩn thận thì không tụt như vậy nữa (Bảng 1 và mục 4 của paper).

**Nếu bị hỏi:** Thiết kế gộp P khác thiết kế cô lập I ở nhiều điểm cùng lúc, trong đó P train nhiều bước hơn khoảng 4,5 lần mỗi vòng. Nên nhóm không kết luận nguyên nhân cú sụp.

---

## Slide 4 — 03 · Kết quả 1
*Trong paper: §4.4, Bảng 4–5 (tr. 7–9) · §4.5, Bảng 7 (tr. 9–11)*

> Kết quả 1: không tốc độ học nào làm model giỏi lên. Trên biểu đồ, mọi cột đều đi xuống.
>
> Học chậm thì gần như không đổi, học nhanh thì còn tệ đi. Mức tăng lớn nhất có thể chỉ khoảng 2 điểm (Bảng 4 của paper).

**Nếu bị hỏi:** Cận 2,2 điểm là cận lỏng: tính trên độ chính xác mẫu (chọn sau khi chạy) và không tính nhiễu giữa các lần train (chạy lặp cùng cấu hình lệch 3,2 điểm). 'lr càng cao càng tụt' mới rõ ở 1 seed. Lý do tụt (mục 4.5): lời giải viết xong sai nhiều hơn, và viết dài hơn nên bị cắt ở 512 token.

---

## Slide 5 — 04 · Kết quả 2
*Trong paper: Bảng 6 (tr. 10) · §4.3 (tr. 7)*

> Kết quả 2: nhóm thử sửa máy chấm, và thử bỏ hẳn máy chấm. Cả hai đều không tạo khác biệt rõ: lần chạy này tốt hơn, lần khác lại kém hơn.
>
> Lý do: lỗi được sửa quá hiếm, chỉ ảnh hưởng vài bài (Bảng 6 của paper).

**Nếu bị hỏi:** Bản vá \dfrac chỉ đổi 0–4 bài trong tập học. Bỏ lọc train gấp 3–4 lần số bước nên cũng không phải đối chứng sạch. Học lời giải mẫu của người thì tụt mạnh nhất.

---

## Slide 6 — 05 · Phát hiện
*Trong paper: §3.2 (tr. 3) · Phụ lục B (tr. 15)*

> Phát hiện quan trọng: máy chấm gạch nhầm khoảng 1/6 số bài làm đúng.
>
> Lý do đơn giản: đáp án trong sách và đáp án model viết khác cách trình bày, dù cùng một số. Ví dụ cùng là bốn phần ba, nhưng viết khác kiểu là máy chấm sai.
>
> Nhóm sửa lỗi này rồi chấm lại: model vẫn không giỏi lên. Kết luận giữ nguyên (mục 3.2 của paper).

**Nếu bị hỏi:** Cụ thể: đáp án gốc lưu trơn (\frac43), model bọc trong \boxed{}. Loại nhầm 15,5–18,4% bài đúng; kéo pass@1 tuyệt đối thấp 4,7–8,0 điểm. Nếu hỏi lệch do đâu: do cách lưu đáp án gốc trong pipeline, nhóm tự kiểm lại thì phát hiện, đã chấm lại toàn bộ; paper có ghi.

---

## Slide 7 — Demo
*Tái hiện số trong §3.2 và Phụ lục B của paper*

> Em xin chạy demo. Phần 1: cùng một đáp số, máy chấm gốc nói SAI, sửa rồi thì nói ĐÚNG.
>
> Phần 2: vài bài thật của model bị chấm nhầm.
>
> Phần 3: tính trên toàn bộ, khoảng 1/6 bài đúng bị gạch, đúng như trong paper.

**Nếu bị hỏi:** Chạy ở thư mục gốc repo, chỉ cần CPU. Nếu lỗi: mở 25-10-2026/demo_output.txt. Phần 4 (--live) dao động theo cỡ mẫu; số để trích là bảng phần 3.

---

## Slide 8 — 06 · Kết luận
*Trong paper: §5.1 (tr. 10)*

> Trả lời câu hỏi đề tài.
>
> Model có giỏi toán hơn không? Không thấy.
>
> Có học cách ghi đáp số cho vừa ý máy chấm không? Chưa đủ dữ liệu để kết luận.
>
> Tóm lại: với model nhỏ, vòng tự học này không làm model giỏi lên (mục 5.1 của paper).

**Nếu bị hỏi:** Dấu hiệu chốt trước cần pass@1 tăng, mà pass@1 không tăng, nên không kết luận được. Điểm yếu tự nhận: luật đọc kết quả chỉ một chiều.

---

## Slide 9 — 07 · So sánh
*Trong paper: §2 Related Work (tr. 2)*

> Kết quả này có khác người khác không? Các bài báo cáo tiến bộ đều dùng model lớn. Các nghiên cứu kiểm chứng gần đây thì thấy giống nhóm: vòng tự học không làm model giỏi hơn thật.
>
> Các bài này đều trích trong mục 2 của paper.

**Nếu bị hỏi:** Tra arXiv 24/10/2026: STaR 2203.14465, ReST-EM 2312.06585, Yue 2504.13837, Phantom Gains 2608.20290 (gần nhóm nhất), TinyV 2505.14625. Chỉ trích số TinyV: >38% false negative, tăng tới 10%.

---

## Slide 10 — 08 · Giới hạn & tiếp theo
*Trong paper: §6 Limitations (tr. 11) · Phụ lục J (tr. 31), K*

> Giới hạn: chạy ít lần, chỉ một model và một máy chấm.
>
> Việc tiếp theo quan trọng nhất: train lại với máy chấm đã sửa lỗi (mục 6 của paper).

**Nếu bị hỏi:** Bên phải còn: tách nguyên nhân cú sụp thiết kế gộp, đối chứng dương, giới hạn token lớn hơn 512. Bản vá \boxed đổi ~1/5 tập học, gấp 34–49 lần bản vá \dfrac.

---

## Slide 11 — Cảm ơn

> Chi tiết đầy đủ nằm trong paper. Em cảm ơn thầy đã lắng nghe, mời thầy đặt câu hỏi.

<!-- SLIDES:END -->

---

## Hỏi đáp — câu trả lời mẫu

| Thầy hỏi | Trả lời | Chỉ vào paper |
|---|---|---|
| Kết quả âm tính thì đóng góp gì? | Kiểm một tuyên bố phổ biến ở model nhỏ và thấy nó không đứng; tìm ra một nguồn sai lệch của máy chấm mà người khác cũng có thể gặp; kết quả khớp các nghiên cứu kiểm chứng gần đây. | §5, §2 |
| Sao không dùng model lớn hơn? | Giới hạn GPU Kaggle. Đề tài nhắm đúng model nhỏ, và các bài báo cáo tiến bộ đều dùng model lớn, nên kiểm ở model nhỏ là có ý nghĩa. | §6 |
| Có chắc không phải do train sai? | 4 learning rate, nhiều seed, 3 đối chứng, chấm trên đề thi tách riêng. | Bảng 4, 6 |
| Sao không sửa máy chấm cho tốt? | Đề tài là **đo** tuyên bố, không phải sửa máy chấm; sửa máy chấm là hướng của TinyV. | §2 |
| pass@k là gì, tăng có nghĩa là nhiều cách giải không? | Làm k lần, có ít nhất 1 lần đúng. k là số lần làm lại cùng đề, không phải số cách giải. | §3.4 |
| Cú sụp lần trước (50 → 18,6%) đâu rồi? | Thiết kế gộp chấm trên chính đề đã học và train nhiều hơn khoảng 4,5 lần mỗi vòng. Làm lại cô lập thì không lặp lại, nên nhóm không kết luận "model sụp". Nguyên nhân chưa tách được. | §4.1–4.2, Bảng 2–3 |
| Khoảng tin cậy có chắc không? | Chưa tính phương sai giữa các seed train, nên chỉ giới hạn hiệu ứng một cách lỏng. Đã ghi trong giới hạn. | §6, Phụ lục C |
| Khác gì Yue và cộng sự? | Họ dùng RL trên model lớn hơn; nhóm dùng lọc + SFT thuần trên model 1,5B. Cùng hình dạng kết quả. | §2 |

**Không biết thì nói thật:** "Dạ nhóm chưa đo điều đó, đây là một giới hạn." Tốt hơn đoán.

### Slide 8: "Tại sao lại *chưa rõ*?"

Luật chốt **trước khi chạy**: chỉ kết luận "model học cách ghi đáp số cho vừa ý máy chấm" khi đủ 3 dấu hiệu:
(1) pass@1 **tăng**, (2) pass@k **đứng yên**, (3) kiểu viết **tụ về một khuôn**. pass@1 không tăng mà còn giảm → dấu
hiệu 1 không xuất hiện → luật không "bật" được, nên không kết luận có hay không.

*Ví dụ:* muốn biết học sinh có chép bài không, thầy nhìn dấu hiệu "điểm tăng vọt mà hỏi miệng không hiểu". Học kỳ này
điểm em đó **giảm** — thầy không kết luận được gì về chuyện chép bài.

> Dạ, nhóm em chốt từ trước: chỉ kết luận khi điểm làm 1 lần **tăng** mà năng lực thật không đổi. Điểm không tăng mà
> còn giảm, nên dấu hiệu đó không xuất hiện. Không thấy dấu hiệu không có nghĩa là không có, nên nhóm ghi "chưa rõ".

| Hỏi tiếp | Trả lời |
|---|---|
| Sao không nhìn kiểu viết là biết? | Tỉ lệ đáp án đóng khung có đổi, nhưng giải thích được theo cả hai cách: bắt chước máy chấm, hoặc chỉ trôi dần khi học. |
| Vậy luật có vấn đề? | Dạ đúng, luật chỉ đo được một chiều (khi điểm tăng). Nhóm nhận ra sau khi chạy và đã ghi trong paper. |
| Muốn trả lời thì làm gì? | Cần thí nghiệm có điểm tăng (model lớn hơn), hoặc đối chứng dương: cố tình làm máy chấm ưu ái một kiểu viết rồi xem có đo ra không. |

---

## Demo: đọc kết quả thế nào

Lệnh: `.venv/bin/python 25-10-2026/demo_verifier.py --live 200`

**Ý nghĩa chung:** máy chấm **đã vá** làm y hệt máy gốc, chỉ thêm một bước: đưa đáp án sách về **cùng cách trình
bày** với đáp án model trước khi so. Bài nào máy vá nhận mà máy gốc gạch = bài **đúng nhưng bị chấm oan**.

**Phần 1 — ví dụ tay.** Sách ghi 4/3 trơn, model ghi 4/3 trong "hộp đáp án". Máy gốc SAI, máy vá ĐÚNG.
> Cùng là 4/3, chỉ khác cách trình bày mà bị chấm sai.

**Phần 2 — ví dụ thật.** 3 bài thật model làm ở vòng 0 (chưa học gì): xác suất 33/100, khoảng (3/5; 8/3], căn 51.
Model làm đúng cả ba, máy gốc gạch cả ba.
> Đây không phải ví dụ em tự đặt ra, mà là bài thật model làm đúng nhưng bị gạch.

**Phần 3 — bảng tổng** ⭐ số để trích dẫn.

| Cột | Nghĩa |
|---|---|
| `run` | Lần chạy (bảng dưới) |
| `vòng` | Vòng tự học; vòng 0 = model gốc chưa học |
| `gốc nhận` | Số bài máy gốc chấm đúng |
| `vá nhận` | Số bài máy vá chấm đúng (gần với số bài đúng thật) |
| `bị loại nhầm` | (vá − gốc) / vá = tỉ lệ bài đúng bị gạch oan |

| Tên run | Là gì | Lời giải mỗi vòng |
|---|---|---|
| `a-math500-lr-fixed` | MATH-500, tốc độ học 5e-4, lần chạy 1, 3 vòng | 500 đề × 4 = 2.000 |
| `a-math500-lr-fixed-seed2` | Cùng cấu hình, lần chạy 2 | 2.000 |
| `qwen15b-math500-a` | Run A gốc, tốc độ học 1e-5, 5 vòng | 500 đề × **8** = 4.000 |

- Dòng đầu: vòng 0 có **787** bài đúng thật, máy gốc chỉ nhận **642** → **145 bài đúng bị vứt** (18,4%).
- **15,5–18,4% ở mọi run, mọi vòng** → lỗi có mặt suốt quá trình, không phải tình cờ. Model mất ~1/6 dữ liệu tốt
  mỗi vòng.
- Cột "vá nhận" giảm qua các vòng (787 → 708 → 566) → model làm đúng ít đi, khớp kết luận "học nhanh thì tệ đi".
- 2 run đầu mỗi đề 4 lời giải, `qwen15b-math500-a` mỗi đề 8 lời giải (nên số gấp đôi). "500 đề" là toàn bộ
  MATH-500, gồm cả phần để học và 150 đề thi.

**Phần 4 — kết quả chính: model có giỏi lên không** ⭐ phần quan trọng nhất của demo.
Thanh dài = điểm pass@1 trên 150 đề thi model không được học, mỗi █ = 2,5 điểm, lần chạy 1 (khớp Bảng 3, 4, 6).

| Cấu hình | Vòng 0 → vòng cuối | Đọc là |
|---|---|---|
| tốc độ học 1e-5 (Run A, 5 vòng) | 32,0 → 29,3 (−2,7) | gần như đứng yên |
| 1e-4 | 33,3 → 34,0 (+0,7) | đứng yên |
| 2e-4 | 33,3 → 31,3 (−2,0) | đứng yên |
| 5e-4 | 33,3 → 23,3 (−10,0) | **tụt rõ** |
| không lọc, 5e-4 | 33,3 → 27,3 (−6,0) | tụt |
| học lời giải mẫu, 5e-4 | 33,3 → 15,3 (−18,0) | tụt mạnh nhất |

> Đây là kết quả chính. Không cấu hình nào giỏi lên. Học chậm thì đứng yên, học nhanh thì tụt. Thanh nào lệch dưới
> khoảng 7 điểm là nằm trong sai số của 150 đề.

Nếu hỏi "+0,7 là có tăng?": 0,7 điểm trên 150 đề là chưa tới 1 đề, khoảng tin cậy từ −6,7 tới +8,0 (Bảng 5).

**Phần 5 — cùng một đề, trước và sau khi học** (lần chạy lr 5e-4, model gốc so với vòng 2). Hai đề model gốc làm
đúng cả 4 lần, model sau 2 vòng sai cả 4 lần. Mỗi đề minh họa một lý do tụt (mục 4.5):

| Đề | Model gốc | Sau 2 vòng | Lý do |
|---|---|---|---|
| Viết 3/20 dưới dạng số thập phân | chia gọn, ra 0,15 | viết một dãy số nhân đôi vô nghĩa (20,48; 40,96; 81,92...) tới hết giới hạn, **không có đáp số** | viết lan man, bị cắt |
| Số nhỏ nhất bằng 2 lần nghịch đảo của nó trừ 1 | giải phương trình, ra −2 | viết xong, lập luận lan man "chỉ số nguyên dương mới hợp", ra **1** | làm xong mà sai |

> Đây là cùng một đề. Model gốc làm gọn và đúng. Sau 2 vòng tự học: đề thứ nhất nó viết lan man đến hết giấy, đề
> thứ hai nó viết xong nhưng lập luận sai. Đó chính là hai lý do model tụt điểm.

Lưu ý: đây là 2 ví dụ được **chọn** để minh họa (trong 6 đề có kiểu "đúng 4/4 → sai 4/4"), không phải mẫu ngẫu
nhiên; số chung là ở phần 4. Hai đề thuộc MATH-500, chưa kiểm là thuộc phần học hay phần thi.

**Phần 6 — chấm trực tiếp 200 bài ngẫu nhiên** (khi chạy `--live 200`). Ví dụ `gốc nhận 64, vá nhận 80` → 16/80 =
20%. Lệch so với 15,5–18,4% là bình thường: mẫu nhỏ (chỉ 80 bài đúng), chạy lại có thể ra ~13–20%.
> Chấm ngay tại chỗ trên mẫu nhỏ ra khoảng 20%, cùng mức với bảng tổng. Số chính thức là 15,5–18,4%.

**Câu chốt demo:**
> Máy chấm gạch oan khoảng 1/6 số bài đúng, ở mọi lần chạy, mọi vòng. Nhưng kể cả bỏ qua lỗi đó, model vẫn không
> giỏi lên: học chậm thì đứng yên, học nhanh thì viết lan man và giải sai.

**Thời gian:** phần 1–3 khoảng 1 phút, phần 4–5 khoảng 2 phút. Gấp thì bỏ phần 2 và phần 6.

---

## Hỏi về fine-tuning model

**Cấu hình (paper §3.4, tr. 4) — thuộc để trả lời nhanh:**

| Thông số | Giá trị | Nói đơn giản |
|---|---|---|
| Model | Qwen2.5-1.5B-Instruct | Model nhỏ 1,5 tỷ tham số, đã được dạy làm theo lệnh |
| Cách train | LoRA SFT (TRL `SFTTrainer`) | Học có giám sát, chỉ chỉnh thêm một phần nhỏ |
| LoRA | rank 16, alpha 32, trên `q_proj` và `v_proj` | Gắn "miếng vá" nhỏ vào 2 ma trận của lớp attention |
| Mỗi vòng | adapter **mới**, train lại **từ model gốc** | Không cộng dồn qua các vòng (giống ReST-EM) |
| Dữ liệu học | mọi lời giải được máy chấm nhận | Không tự chọn tay |
| Epoch / batch | 1 epoch, batch 2 | Số bước train = nửa số bài được giữ |
| Optimizer | AdamW, giảm tốc độ học tuyến tính, không warmup | Mặc định phổ biến |
| Tốc độ học | 1e-5 (mặc định ban đầu), sau thử 1e-4, 2e-4, 5e-4 | |
| Độ dài | tối đa 512 token cả khi sinh lẫn khi train | |
| Sinh lời giải | nhiệt độ 0,8, top-p 0,8, top-k 20; k = 4 hoặc 8 lần mỗi đề | |
| Máy | 1 GPU T4 trên Kaggle, fp16 | Miễn phí, giới hạn 12 giờ/phiên |

| Thầy hỏi | Trả lời |
|---|---|
| LoRA là gì, sao không fine-tune toàn bộ? | LoRA giữ nguyên model gốc, chỉ học thêm hai ma trận nhỏ gắn vào. Số tham số học ít hơn rất nhiều nên vừa GPU T4 miễn phí. Fine-tune toàn bộ 1,5B không vừa bộ nhớ và dễ làm hỏng model hơn. |
| Có thể LoRA quá yếu nên model mới không học được? | Dạ, ở tốc độ học 1e-5 model gần như không đổi, nên nhóm tăng lên tới 5e-4. Ở đó model **thay đổi rõ** (tụt), tức là LoRA đủ mạnh để làm thay đổi model; chỉ là thay đổi theo chiều xấu. Đây cũng là một giới hạn nhóm ghi lại: chưa thử rank lớn hơn hay full fine-tune. |
| Sao mỗi vòng train lại từ model gốc mà không train tiếp? | Để mỗi vòng chỉ khác nhau ở **dữ liệu được chọn**, không cộng dồn lỗi qua các vòng. ReST-EM cũng làm vậy. Đổi lại, kết quả chưa nói gì về kiểu train cộng dồn. |
| Tốc độ học 1e-5 có phải quá nhỏ? | Dạ, đó là mặc định chưa tinh chỉnh. Nhóm nhận ra nên đã thử thêm 3 mức lớn hơn; không mức nào làm model giỏi lên (Bảng 4). |
| Sao chỉ 1 epoch? | Để không học thuộc tập nhỏ. Hệ quả: lần chạy nào giữ được nhiều bài thì train nhiều bước hơn, nên các đối chứng có lượng train khác nhau. Paper ghi là giới hạn. |
| Sao loss tính cả phần đề bài? | Đó là mặc định của thư viện lúc chạy. Ảnh hưởng chưa đo; nếu làm lại sẽ chỉ tính loss trên lời giải. |
| 512 token có đủ không? | Không hoàn toàn: model gốc đã có 41–48% lời giải chạm giới hạn ở lr 5e-4. Nhóm kiểm thêm với giới hạn dài hơn: khoảng cách giữa model đã học và model gốc **không thu hẹp**, nên giới hạn token không giải thích hết việc tụt (Phụ lục H). |
| Khác gì RL (như GRPO, PPO)? | RL học từ điểm thưởng ngay trong lúc sinh. Nhóm dùng cách đơn giản hơn: lọc bài đúng rồi học có giám sát (SFT). Kết quả chỉ nói về cách này, không về RL. |
| Model tụt vì sao? | Hai phần (mục 4.5): (1) lời giải viết xong sai nhiều hơn, tụt 5,5–10,6 điểm so với model gốc trên cùng đề; (2) bị cắt ở 512 token nhiều hơn. Phần bị cắt chiếm 12–30% mức tụt ở lần chạy 1, 52–72% ở lần chạy 2. Ở tốc độ học 1e-4 và 2e-4 thì toàn bộ là do (1). |
| Có overfitting không? | Chấm trên 150 đề model chưa từng học nên đo được khả năng tổng quát. Ở đề chưa học, điểm không tăng; với lr cao thì giảm. |
| Train trên lời giải gold của người sao lại tụt mạnh nhất? | Lời giải model viết ngắn đi hơn một nửa, và độ đúng của các bài viết xong cũng tụt mạnh (mục 4.5). Lời giải mẫu của người viết ngắn, bỏ bước, khác kiểu model tự viết. Kim và cộng sự thấy hiện tượng gần giống (ngắn đi, kém đi), nhưng họ làm self-distillation, không phải SFT thường, nên chỉ là tương tự lỏng (§2). |

## Số cần thuộc
1,5B · 150 đề thi · 4 learning rate · 2–3 seed · 3 đối chứng · tăng tối đa ≤ 2,2 điểm ·
loại nhầm 15,5–18,4% (~1/6) · thiết kế gộp 50 → 18,6% · paper 12 trang thân bài + phụ lục A–K.

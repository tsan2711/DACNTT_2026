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

## Số cần thuộc
1,5B · 150 đề thi · 4 learning rate · 2–3 seed · 3 đối chứng · tăng tối đa ≤ 2,2 điểm ·
loại nhầm 15,5–18,4% (~1/6) · thiết kế gộp 50 → 18,6% · paper 12 trang thân bài + phụ lục A–K.

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

> Dạ em chào thầy. Nhóm em gồm Nguyễn Tấn Sang và Trần Duy Anh. Đề tài như trên slide: tự học có làm model nhỏ giỏi toán hơn không?
>
> Lần báo cáo trước (13/9), nhóm em đã thấy giả thuyết ban đầu không đứng, nhưng mới thử ở một learning rate. Hôm nay em trình bày phần làm tiếp, và toàn bộ đã được viết thành paper.
>
> Câu trả lời ngắn, như dòng dưới tiêu đề: không thấy tiến bộ nào đo được. Thí nghiệm dùng model Qwen2.5 1,5B, fine-tune LoRA, máy chấm math-verify, trên hai bộ đề MATH-500 và GSM8K.

---

## Slide 2 — 01 · Câu hỏi
*Trong paper: §1 Introduction (tr. 1) · §3.4 các thước đo (tr. 4)*

> Đầu tiên em nhắc lại câu hỏi. Ba ô trên slide là vòng lặp: (1) model làm mỗi đề nhiều lần, (2) máy chấm chỉ so đáp án cuối, không đọc lời giải, (3) model học lại trên các lời giải được nhận. Lặp 3 đến 5 vòng; đây là vòng lặp của STaR, ReST, RFT.
>
> Vì máy chấm chỉ nhìn đáp án cuối nên mới có câu hỏi trong khung: sau nhiều vòng, model giỏi toán thật, hay chỉ học cách viết mà máy chấm chịu nhận?
>
> Dòng cuối là cách đo: chấm trên 150 đề thi riêng model không được học, với 4 thước đo chốt trước khi chạy: pass@1, pass@k, kiểu chữ \boxed, và số đề thêm/mất. Phần này là mục 1 và 3.4 của paper.

**Nếu bị hỏi:** 4 thước đo được chốt TRƯỚC khi chạy. pass@k: làm k lần, ít nhất 1 lần đúng; k là số lần làm lại, không phải số cách giải.

---

## Slide 3 — 02 · Cách làm
*Trong paper: §3.3 + Bảng 1 (tr. 4–5) · §4.1–4.2, Bảng 2–3 (tr. 6–8)*

> Để không bỏ sót tiến bộ nếu có, nhóm thử đủ nhiều cấu hình, là bốn con số trên slide: 4 learning rate từ 1e-5 đến 5e-4; 2 đến 3 seed mỗi cấu hình; 3 đối chứng là vá máy chấm, bỏ lọc, và học lời giải gốc; và 150 đề thi tách riêng có khoảng tin cậy bootstrap. Danh sách các lần chạy là Bảng 1 của paper.
>
> Khung dưới là phần thầy đã nghe lần trước: thiết kế đầu tiên trộn 2 bộ dữ liệu và chấm trên chính tập train thì model tụt từ 50 xuống 18,6%. Làm lại cho sạch thì cú sụp đó không lặp lại. Đây là mục 4.1 và 4.2 của paper.

**Nếu bị hỏi:** Thiết kế gộp P khác thiết kế cô lập I ở nhiều điểm cùng lúc, trong đó P train nhiều bước hơn khoảng 4,5 lần mỗi vòng. Nên nhóm không kết luận nguyên nhân cú sụp.

---

## Slide 4 — 03 · Kết quả 1
*Trong paper: §4.4, Bảng 4–5 (tr. 7–9) · §4.5, Bảng 7 (tr. 9–11)*

> Kết quả thứ nhất, như tiêu đề: không learning rate nào làm model giỏi lên. Biểu đồ là thay đổi độ chính xác sau 2 vòng trên MATH-500; mọi cột đều âm.
>
> Ba con số bên phải: 0 lần chạy nào tăng pass@1 hay pass@k một cách chắc chắn; mức tăng lớn nhất mà dữ liệu còn cho phép chỉ khoảng 2,2 điểm; và ở learning rate cao, model tụt rõ, vì lời giải viết xong kém chính xác hơn.
>
> Số chi tiết ở Bảng 4 và khoảng tin cậy ở Bảng 5; phân tích vì sao tụt ở mục 4.5, Bảng 7.

**Nếu bị hỏi:** Cận 2,2 điểm là cận lỏng: tính trên độ chính xác mẫu (chọn sau khi chạy) và không tính nhiễu giữa các lần train (chạy lặp cùng cấu hình lệch 3,2 điểm). 'lr càng cao càng tụt' mới rõ ở 1 seed.

---

## Slide 5 — 04 · Kết quả 2
*Trong paper: Bảng 6 (tr. 10) · §4.3 (tr. 7)*

> Kết quả thứ hai: sửa máy chấm hay bỏ máy chấm đều không tạo khác biệt rõ. Bảng là pass@1 ở vòng 2, learning rate 5e-4; model gốc là 33,3 ở seed 1 và 31,3 ở seed 2.
>
> Dòng đầu, máy chấm gốc, là mốc. Vá \dfrac và không lọc đều đổi chiều theo seed: seed này cao hơn mốc, seed kia thấp hơn. Học lời giải mẫu của người thì tụt mạnh nhất.
>
> Vì sao bản vá vô tác dụng: nó chỉ đổi 0 đến 4 bài trong tập học, quá nhỏ để đo ra. Bài học là đếm tần suất lỗi trước khi xây thí nghiệm. Bảng này là Bảng 6 của paper.

**Nếu bị hỏi:** Bỏ lọc train gấp 3–4 lần số bước nên cũng không phải đối chứng sạch. Học lời giải mẫu: model chuyển hẳn sang kiểu viết của lời giải mẫu và tụt mạnh.

---

## Slide 6 — 05 · Phát hiện
*Trong paper: §3.2 (tr. 3) · Phụ lục B (tr. 15)*

> Phát hiện quan trọng nhất: máy chấm loại nhầm khoảng 1/6 lời giải đúng. Nguyên nhân như dòng dưới tiêu đề: đáp án gốc lưu không có \boxed, còn model lại viết \boxed.
>
> Biểu đồ bên trái: ở mỗi vòng 0, 1, 2, cột xanh là số lời giải bản vá nhận, cột đỏ là số máy chấm gốc nhận; khoảng chênh là 15,5 đến 18,4%, con số lớn bên phải, ở mọi vòng.
>
> Ví dụ ngay dưới: đáp án gốc là \frac43, model viết \boxed{\frac{4}{3}}. Cùng là 4/3 nhưng bị chấm sai.
>
> Nhóm chấm lại khi không còn lỗi này: model vẫn tụt, kết luận giữ nguyên. Lỗi này ở mục 3.2, phần kiểm tra đầy đủ ở phụ lục B. Em xin demo ngay.

**Nếu bị hỏi:** Lỗi có trong mọi thí nghiệm, cả hai nhánh, nên không làm sai phép so sánh, nhưng kéo pass@1 tuyệt đối thấp 4,7–8,0 điểm. Sửa lỗi này làm tập học lớn thêm ~1/5 (440 → 542). Nếu hỏi lệch do đâu: do cách lưu đáp án gốc trong pipeline, nhóm tự kiểm lại thì phát hiện, đã chấm lại toàn bộ; paper có ghi.

---

## Slide 7 — Demo
*Tái hiện số trong §3.2 và Phụ lục B của paper*

> Chạy lệnh ở cuối slide trong terminal, Enter để qua từng phần.
>
> Phần 1, ví dụ tay: cùng đáp án 4/3, máy chấm gốc SAI, bản vá ĐÚNG.
>
> Phần 2, ví dụ thật: 3 lời giải thật của model bị loại nhầm, đọc đề và đáp án.
>
> Phần 3, bảng tổng: 15,5 đến 18,4% trên 500 đề, mọi vòng, đúng con số trong paper.
>
> Phần 4, chấm trực tiếp lời giải ngẫu nhiên ngay trên máy.

**Nếu bị hỏi:** Chạy ở thư mục gốc repo, chỉ cần CPU. Nếu lỗi: mở 25-10-2026/demo_output.txt. Phần 4 dao động theo cỡ mẫu; số để trích là bảng phần 3.

---

## Slide 8 — 06 · Kết luận
*Trong paper: §5.1 (tr. 10)*

> Trả lời câu hỏi đề tài, hai ô trên slide.
>
> Model có giỏi toán hơn không? Không thấy. Ở cả 4 learning rate, không lần chạy nào tăng chắc chắn; learning rate cao thì còn tụt.
>
> Có học cách viết của máy chấm không? Chưa rõ. Dấu hiệu nhóm chốt trước cần pass@1 tăng, mà pass@1 không tăng, nên không kết luận được.
>
> Tóm lại, như dòng cuối: ở quy mô 1,5B, LoRA, một máy chấm theo luật, vòng lặp tự học không cho thấy tiến bộ. Đây là mục 5.1 của paper.

**Nếu bị hỏi:** Điểm yếu tự nhận: luật đọc kết quả chỉ một chiều, nhóm nhận ra sau khi chạy.

---

## Slide 9 — 07 · So sánh
*Trong paper: §2 Related Work (tr. 2)*

> Kết quả này có lạc lõng không? Bảng so với 5 bài, đều trích ở mục 2 của paper.
>
> Hai dòng KHÁC: STaR đề xuất vòng lặp này; ReST-EM có tiến bộ nhưng giảm dần sau vòng đầu, và dùng model lớn.
>
> Hai dòng GIỐNG: Yue và cộng sự ở NeurIPS 2025 thấy RL tăng pass@1 nhưng ở pass@k lớn thì model gốc thắng; Phantom Gains 2026 thấy khi có đối chứng, nhiều tiến bộ hoá ra là ảo. Đây là bài gần nhóm nhất.
>
> Dòng cuối, TinyV, ghi nhận cùng hiện tượng máy chấm loại nhầm lời giải đúng.
>
> Kết luận ở khung dưới: bài báo cáo tiến bộ dùng model lớn; ở 1,5B nhóm thấy như các bài kiểm chứng.

**Nếu bị hỏi:** Tra arXiv 24/10/2026: STaR 2203.14465, ReST-EM 2312.06585, Yue 2504.13837, Phantom Gains 2608.20290, TinyV 2505.14625. Chỉ trích số TinyV: >38% false negative, tăng tới 10%.

---

## Slide 10 — 08 · Giới hạn & tiếp theo
*Trong paper: §6 Limitations (tr. 11) · Phụ lục J (tr. 31), K*

> Cột trái là giới hạn: ít seed, 2–3 mỗi cấu hình; một model, một máy chấm, không phải RL; một số thước đo thêm sau khi chạy; và lỗi \boxed chưa được vá khi train.
>
> Cột phải là việc tiếp theo: train lại với bản vá \boxed và nhiều seed; tách nguyên nhân cú sụp của thiết kế gộp; làm đối chứng dương để biết thiết kế đo được hiệu ứng cỡ nào; và thử giới hạn token lớn hơn 512.
>
> Mục 6 của paper tóm tắt, phụ lục J liệt kê đầy đủ, phụ lục K là hướng tiếp theo.

**Nếu bị hỏi:** Bản vá \boxed là thí nghiệm máy chấm có tác động thật: đổi ~1/5 tập học, gấp 34–49 lần bản vá \dfrac. Cần cố định số bước train khi so sánh.

---

## Slide 11 — Cảm ơn

> Kết quả đầy đủ nằm trong paper, đường dẫn ở cuối slide; chi tiết ở phụ lục A đến K. Nhóm em xin cảm ơn thầy đã lắng nghe, mời thầy đặt câu hỏi.

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

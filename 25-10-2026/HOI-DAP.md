# Hỏi đáp dự phòng (chỉ mở khi thầy hỏi)

## Bảng 5: vì sao cần, phương pháp gì?

Nguồn: §3.4 "Uncertainty", phụ lục C (trang 18), `experiments/viec3/bootstrap_ci.py`.

- **Bảng 4 và Bảng 5 khác nhau ở đâu:** Bảng 4 là ước lượng điểm trên một bộ 150 đề. Bảng 5 là khoảng tin
  cậy 95% cho mức thay đổi, tính cho mọi run. Mọi kết luận trong paper dựa trên Bảng 5.
- **Phương pháp:** bootstrap ghép cặp ở mức đề.
  - Lấy mẫu có hoàn lại 150 đề, làm 10.000 lần.
  - Mỗi lần tính hiệu "vòng cuối − vòng 0" trên cùng các đề đã bốc.
  - Khoảng 95% là phân vị 2,5 và 97,5 của các hiệu đó.
- **Vì sao ghép cặp:** hai vòng chấm trên cùng một bộ đề, nên phải loại phương sai do đề này khó hơn đề kia.
- **Vì sao lấy mẫu lại theo đề:** 4 lời giải của cùng một đề tương quan với nhau. Nếu lấy mẫu lại từng lời
  giải thì phương sai bị đánh giá thấp.
- **Vì sao khoảng của pass@1 rộng:** mỗi đề chỉ có một lần rút, đúng hoặc sai. Ví dụ dòng 1e-4 seed 1:
  - pass@1: +0,7 [−6,7; +8,0];
  - độ chính xác mẫu: −1,5 [−5,3; +2,2].
- **Giới hạn:**
  - Khoảng tin cậy không tính phương sai giữa các lần train: chạy lặp cùng cấu hình đã lệch 3,2 điểm.
  - Không hiệu chỉnh đa so sánh (bảng có 76 khoảng). Vì vậy chỉ kết luận theo mẫu hình lặp lại qua nhiều
    run và seed.
- **Thước đo chốt trước:** pass@1 là thước đo chốt trước, và không có khoảng pass@1 nào nằm hẳn trên 0. Độ
  chính xác mẫu được chọn sau khi chạy, chỉ dùng để đặt cận trên: mức tăng, nếu có, không quá khoảng 2,2
  điểm.

## Bài này đóng góp gì? Sao không dùng RL, có bài RL còn hay hơn?

Nguồn: §1 "Contributions", §2, phụ lục A mục "Positioning". Số liệu bài RL đối chiếu với abstract và bản HTML
trên arXiv ngày 29/10/2026.

**Câu trả lời ngắn:** Bài em không đề xuất phương pháp tốt hơn RL. Em kiểm tra công thức self-training bằng SFT
(kiểu STaR/RFT), loại rẻ và hay dùng nhất, với cách đo chặt. Ở 1.5B nó không cho cải thiện đo được.

**Đóng góp, so với hai bài gần nhất** (Xu et al. *Phantom Gains*, Qwen3-8B; Egashira et al., lỗi verifier
trong RLVR, bài toán số học tổng hợp):

- Đo lỗi verifier ngay trong vòng lặp: lỗi lưu đáp án gold làm verifier từ chối 15,5–18,4% lời giải đúng (khoảng
  1/6). Các bài khác thường giả định một tỉ lệ nhiễu cố định.
- Chấm trên đề tách riêng, mọi so sánh đều có khoảng tin cậy bootstrap theo đề (Bảng 5).
- Tách "giải xong nhưng sai" khỏi "hết token": ở learning rate cao nhất, lời giải chạy xong kém hơn 5,5–10,6 điểm.
- Báo cả kết quả không lặp lại được (cú sụt ở thiết kế gộp), coi đó là bài học thiết kế thí nghiệm.
- **Không nhận** "verifier lệch + đối chứng vá" là đóng góp: phần vá chỉ đổi 0–4 ví dụ, quá yếu (paper đã ghi).

**Các bài RL trên model nhỏ có gain lớn:**

| Bài | Model | Kết quả |
|---|---|---|
| Wang et al., 1-shot RLVR (arXiv 2504.20571, NeurIPS 2025) | Qwen2.5-**Math**-1.5B | MATH500: 36,0% → 73,6% với 1 ví dụ |
| Dang & Ngo, Open-RS (arXiv 2503.16219) | DeepSeek-R1-Distill-Qwen-1.5B | AMC23: 63% → 80%; 7.000 mẫu, 4×A40, 24 giờ, $42 |
| Zeng et al., SimpleRL-Zoo (arXiv 2503.18892) | 10 model, gồm Qwen2.5 0.5B–32B | GRPO, reward theo luật |

**Vì sao không so trực tiếp được:**

1. **Model nền khác.** Gain lớn nhất nằm ở model chuyên toán (Qwen2.5-Math) hoặc distill từ R1. Model của mình là
   Qwen2.5-1.5B-Instruct bản thường.
2. **RL có thể chỉ khơi lại cái có sẵn.** Shao et al., *Spurious Rewards* (arXiv 2506.10947): với Qwen2.5-Math-7B,
   reward ngẫu nhiên vẫn tăng MATH-500 21,4 điểm, gần bằng 29,1 điểm khi dùng reward đúng. Với Qwen2.5 bản thường,
   reward sai hoặc chỉ chấm định dạng vẫn tăng MATH-500, chỉ reward ngẫu nhiên là không. Với Llama3 và OLMo2 thì
   reward giả thường không giúp. Model nhỏ hưởng lợi ít hơn từ reward ngẫu nhiên. Ý chính: gain RL trên Qwen chưa
   chắc là model học thêm toán.
3. **Cơ chế khác.** RL học online và bị phạt cả khi sai (advantage của GRPO). SFT của mình chỉ học từ mẫu được
   chấp nhận, mỗi vòng học lại từ model gốc. Chu et al. (arXiv 2501.17161, ICML 2025) cho thấy SFT tổng quát hoá kém
   hơn RL, nhưng trên game bài và bài toán điều hướng, không phải toán.
4. **Khớp bức tranh chung.** Yue et al. (đã cite): RL tăng pass@1 nhưng ở pass@k lớn model gốc vẫn thắng, tức RL
   khuếch đại chứ không mở rộng năng lực. Ở 1.5B, SFT tự sinh còn không khuếch đại được.

**Đề xuất mới: bộ kiểm toán cho vòng GVT với verifier lệch** (rút ra từ dữ liệu đã có, không cần chạy thêm; cả
bốn phần đều định nghĩa sau khi chạy, phải nói rõ là post hoc):

1. **Kiểm định "model có học theo verifier không", dùng được cả khi accuracy giảm.** Luật chốt trước chỉ bật được khi
   pass@1 tăng (§5.1), nên không trả lời được nhánh hai của câu hỏi. Đề xuất: mỗi vòng, chấm lại mẫu của chính vòng
   lặp bằng verifier đã sửa, rồi tính tỉ lệ lời giải đúng bị verifier gốc từ chối, tách theo từng loại lỗi. Nếu
   model học né cái verifier từ chối thì tỉ lệ này phải giảm qua các vòng, bất kể accuracy lên hay xuống. Dữ liệu
   của mình: lỗi lưu gold từ chối khoảng 1/6 số lời giải đúng (15,5–18,4%) ở **mọi** vòng, không giảm dần, nên với
   loại lỗi này model không thích nghi (§3.2, phụ lục B). Trong những gì đã đọc, *Phantom Gains*, Egashira và TinyV không dùng tỉ lệ này qua các vòng để kiểm tra
   model có thích nghi không. Paper: §5.3.
2. **Phân rã độ giảm accuracy** thành phần do lời giải chạy xong mà sai và phần do số lời giải hết token tăng. Ở lr
   5e-4, phần hết token chiếm 12–30% (seed 1) và 52–72% (seed 2) (bảng phân rã, §4.5). *Phantom Gains* chỉ cảnh
   báo cap token có thể làm đọc nhầm kết quả, không đưa ra cách phân rã.
3. **Kiểm tra "liều" của đối chứng trước khi chạy:** đếm xem phần vá verifier đổi bao nhiêu ví dụ train. Bài mình
   vá lỗi `\dfrac` chỉ đổi 0–4 ví dụ, trong khi lỗi lưu gold (không được vá) đổi khoảng 100 (440 → 542).
4. **Ghép liều khi so thiết kế gộp với thiết kế tách:** thiết kế gộp train nhiều hơn khoảng 4,5 lần mỗi vòng, nên
   không biết cú sụt do gộp hay do liều.

Câu nói gọn: "Ngoài kết quả âm, bài đề xuất một cách kiểm tra trực tiếp xem model có học theo máy chấm không: theo
dõi tỉ lệ lời giải đúng bị máy chấm từ chối qua các vòng, trên chính mẫu của vòng lặp. Cách này dùng được cả khi
độ chính xác giảm, chỗ mà luật cũ bó tay."

Giới hạn khi nói: mới kiểm được một loại lỗi; loại lỗi lớn đó chạy y nguyên trong mọi run, chưa có đối chứng ghép
liều; "chưa thấy bài nào làm" chỉ đúng với danh sách đã khảo sát (đến 10/2026).

**Nếu bị hỏi "sao không thử RL":** ngoài phạm vi câu hỏi nghiên cứu (kiểm tra vòng GVT bằng SFT), và GPU Kaggle
miễn phí không đủ cho RL online. Related Work hiện chưa cite các bài RL trên model nhỏ; nhận đây là thiếu sót sẽ bổ
sung.

## Tra nhanh

| Câu hỏi | Mở |
|---|---|
| Cấu hình từng run | Bảng 1 · trang 5 |
| Chấm lại sau khi sửa lỗi `\boxed` | Phụ lục B · trang 15–17 |
| Kết quả ở learning rate 1e-5 | Hình 1 · trang 7 |
| Chi tiết lần chạy 1024 token và lần chạy lặp | Phụ lục H · trang 25–28 |
| Đóng góp, so với bài khác | Phụ lục A, mục "Positioning" |
| Demo lỗi máy chấm | `.venv/bin/python 25-10-2026/demo_verifier.py --live 200` |

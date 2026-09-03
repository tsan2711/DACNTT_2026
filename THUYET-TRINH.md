# Kịch bản nói chuyện với thầy — cập nhật sau khi có cả 2 cỡ model (2026-09-03)

Bản này có đủ **0.5B lẫn 1.5B**, cùng cấu hình — hiện tượng lặp lại ở cả
hai, và 1.5B còn mạnh hơn hẳn. Đây là điểm thuyết phục nhất: không phải
1 lần chạy ngẫu nhiên, mà 2 cỡ model độc lập cùng cho một chiều kết quả.
Nói khoảng 2-3 phút, đọc to thử trước khi trình bày.

---

## Kịch bản (đọc/nói)

Dạ đề tài của em là: cho một máy giải toán nhỏ tự học nhiều vòng, dùng một
máy chấm tự động để lọc bài đúng rồi dạy lại chính nó — không cần người
chấm tay. Người ta gọi cách này là tự-cải-thiện.

**Vấn đề em nghi ngờ:** máy chấm đó không đọc cách làm bài, chỉ so đáp án
cuối với sách — và nó chấm sai có quy luật, hay gạch nhầm bài **đúng** chỉ
vì viết khác kiểu sách, ví dụ sách ghi `1/2`, máy viết `\dfrac{1}{2}` thay vì
`\frac{1}{2}` là bị gạch, dù giá trị giống hệt. Em đo thật trên 400 đáp án:
có kiểu viết bị gạch **100%** dù đúng giá trị. Câu hỏi của em: cái lệch đó
lặp qua nhiều vòng tự học có làm máy chỉ giỏi **viết đúng kiểu máy chấm ưa**
thay vì giỏi toán thật không?

Em đã tra 29 bài báo để chắc chưa ai làm đúng hướng này — có bài đo máy chấm
lệch nhưng chỉ 1 vòng, có bài chạy nhiều vòng nhưng máy chấm của họ hoàn hảo,
không lệch như của em. Chưa bài nào ghép cả ba: máy chấm lệch-vì-chữ, lặp
nhiều vòng, và đo xem chữ viết có hội tụ theo thời gian không.

**Trước khi chạy, em dự đoán 2 khả năng:** hoặc máy giỏi thật (đo bằng 2 số:
làm 1 lần đúng bao nhiêu %, và cho làm lại 8 lần thì cả hai số cùng tăng),
hoặc máy chỉ học viết chữ (số đầu tăng, số sau đứng yên hoặc giảm).

**Kết quả thật** sau khi chạy đủ 500 đề, 5 vòng, cả 2 cỡ model trên Kaggle —
**cả hai số đều giảm ở cả hai model**, không phải khả năng nào em dự đoán
ban đầu (dự đoán chỉ có: cùng tăng = giỏi thật, hoặc pass@1 tăng/pass@8 đứng
= học viết chữ). Số thật:

| Model | Làm 1 lần đúng (pass@1) | Cho làm lại 8 lần (pass@8) |
|---|---|---|
| 0.5B | 31% → 27% (giảm 12%) | 60% → 55% (giảm 9%) |
| 1.5B | 50% → **19%** (giảm 63%) | 73% → **49%** (giảm 33%) |

Model to hơn — 1.5B, gấp 3 lần tham số — **sụp mạnh hơn hẳn**, không ổn định
hơn như trực giác thường nghĩ. Xu hướng giảm rất đều, tăng tốc dần qua từng
vòng, không có vòng nào tăng lại — khó coi là nhiễu. Đi kèm là chữ viết đổi
mạnh (`\boxed{}` giảm hơn nửa ở 1.5B), và số bài "giữ để ôn" mỗi vòng cũng
sụp theo (ở 1.5B: 3962→1566, mất gần 60%).

Em hiểu đây là bằng chứng máy chấm lệch làm hại thật sự cả pipeline tự-train
— mạnh hơn hẳn em nghĩ ban đầu, và có 2 cỡ model độc lập cùng xác nhận một
chiều, không phải trùng hợp của riêng 1 lần chạy.

---

## Nếu thầy hỏi thêm

- **"Sao không đoán ra kết quả này từ đầu?"** — Vì hai bài gần nhất trong 29
  bài khảo sát (ReST-EM, và một bài đo đúng cặp số này) đều không dùng máy
  chấm lệch-vì-chữ như của em, nên không có tiền lệ để đoán trước hình dạng
  này.
- **"Có chắc không phải nhiễu ngẫu nhiên?"** — Cả 2 model đều giảm đều đặn,
  không lên xuống thất thường (0.5B: 4/4 vòng giảm; 1.5B: 5/5 vòng giảm,
  càng về sau càng nhanh), mẫu đủ lớn (500 đề × 2 bộ mỗi model). Vẫn còn 1
  giới hạn thật: mỗi cỡ model chỉ chạy 1 lần (chưa lặp lại nhiều seed để đo
  phương sai), và dùng tập test (chưa tách train/test riêng).
- **"Vì sao model to hơn lại sụp nặng hơn?"** — Giả thuyết cơ chế (chưa
  chứng minh chắc): mỗi vòng train một adapter mới từ base, chỉ trên đúng
  tập bài verifier chấm đúng ở vòng trước — tập đó co hẹp dần qua mỗi vòng
  (ở 1.5B mất gần 60% sau 5 vòng). Model to hơn có thể học/khớp nhanh hơn
  vào đúng tập hẹp-lệch đó (overfit nhanh hơn với cùng 1 epoch), nên sụp
  nhanh hơn — cần đọc thêm để xác nhận, chưa chắc 100%.
- **"Bước tiếp theo?"** — Viết vào bài báo với đúng 2 giới hạn đã nêu, đối
  chiếu rõ với ReST-EM và Teacher-Free Self-Training để chỉ ra góc này họ
  chưa đo tới.

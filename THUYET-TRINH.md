# Kịch bản nói chuyện với thầy — cập nhật sau bộ 3 thí nghiệm cô lập A/B/C (2026-09-09)

Bản trước (2026-09-03) kể chuyện "máy chấm lệch làm sụp năng lực, 2 cỡ model
cùng xác nhận". **Bản đó đã sai** — không phải sai số liệu, mà sai ở chỗ
thiết kế thí nghiệm không đủ sạch để kết luận như vậy. Bản này kể đúng
những gì đã đo được, kể cả phần bác bỏ chính giả thuyết ban đầu.

Nói khoảng 3-4 phút. Đọc to thử trước khi trình bày. **Điểm quan trọng nhất
khi nói:** không né chuyện dự đoán sai — đó là phần làm bài mạnh lên, không
phải chỗ để giấu.

---

## Kịch bản (đọc/nói)

Dạ đề tài của em là: cho một máy giải toán nhỏ tự học nhiều vòng, dùng một
máy chấm tự động để lọc bài đúng rồi dạy lại chính nó — không cần người
chấm tay. Người ta gọi cách này là tự-cải-thiện.

**Giả thuyết ban đầu của em:** máy chấm đó không đọc cách làm, chỉ so đáp án
cuối với sách — và nó chấm sai **có quy luật**, hay gạch nhầm bài đúng chỉ vì
viết khác kiểu, ví dụ viết `\dfrac{1}{2}` thay vì `\frac{1}{2}` là bị gạch
dù giá trị y hệt. Em đo thật: kiểu viết đó bị gạch **100%**, và tỉ lệ gạch
nhầm bài đúng là 7.8% trên MATH-500, 0% trên GSM8K. Em dự đoán: cái lệch đó
lặp qua nhiều vòng sẽ làm model sụp năng lực dần, và sụp trên MATH-500 chứ
không sụp trên GSM8K.

**Lần chạy đầu trông như xác nhận giả thuyết rất mạnh.** Em chạy 5 vòng trên
2 bộ đề gộp chung, 2 cỡ model. Model 1.5B: làm-1-lần-đúng rớt từ 50% xuống
19%, cho-làm-8-lần rớt từ 73% xuống 49%. Sụp rất sâu, rất đều. Nếu dừng ở
đây thì em đã có một bài báo "đẹp".

**Nhưng em kiểm tra lại thiết kế và thấy nó không trả lời được câu hỏi của
chính nó.** Có hai lỗ hổng. Thứ nhất, em gộp 2 bộ đề vào **một** bộ nhớ học
chung mỗi vòng — mà trong đó GSM8K chiếm tới 69%, nên điểm của MATH-500
thực chất bị ảnh hưởng bởi chuyện xảy ra bên GSM8K, không tách ra được. Thứ
hai, em chấm điểm trên đúng những đề đã dùng để chọn bài dạy — nên "sụp" có
thể chỉ là hết thuộc bài, không phải mất năng lực thật.

**Em làm lại thí nghiệm cho sạch:** mỗi bộ đề chạy riêng, bộ nhớ riêng, và
tách 30% đề ra làm đề thi mà máy **chưa từng** được học. Rồi em thêm đúng
một thí nghiệm đối chứng mà thiết kế cũ không có: chạy lại y hệt, chỉ **vá**
đúng chỗ máy chấm bị lệch — nếu giả thuyết của em đúng, bản vá phải khá hơn
rõ rệt.

**Kết quả: giả thuyết của em không đứng vững.**

| Lần chạy | Làm 1 lần đúng (vòng 0→4) | Làm 8 lần đúng (vòng 0→4) |
|---|---|---|
| A — MATH-500, máy chấm gốc | 32.0% → 29.3% | 57.3% → 56.0% |
| B — MATH-500, **máy chấm đã vá** | 32.0% → 28.7% | 57.3% → 53.3% |
| C — GSM8K, máy chấm gốc | 66.7% → 54.0% | 92.7% → 90.0% |

Ba điều đọc ra từ bảng này. Một: **cú sụp biến mất** — cột "làm 8 lần" gần
như đứng yên ở cả ba, thay vì rớt 22–26 điểm như lần chạy gộp. Hai: **vá máy
chấm không đổi gì cả** — A và B gần như trùng nhau, chênh 0.6 điểm tức là
đúng 1 đề trên 150 đề. Đây là đối chứng sạch nhất trong cả đề tài, chỉ khác
đúng 1 biến, nên nó bác bỏ trực tiếp giả thuyết ban đầu của em. Ba: GSM8K
vẫn còn rơi 12.7 điểm ở cột làm-1-lần nhưng cột làm-8-lần không đổi — tức là
model không quên cách giải, chỉ kém ổn định ở lần trả lời đầu.

**Vậy em kết luận gì.** Cái sụp nặng em thấy lúc đầu **chủ yếu là hiện vật
của cách đo**, không phải bằng chứng máy chấm lệch gây hại. Đóng góp của bài
vì thế thu hẹp lại, nhưng vẫn là đóng góp thật: em chỉ ra được rằng **gộp
nhiều bộ đề vào một lần train, cộng với chấm trên chính đề đã học, đủ để tạo
ra một hiện tượng "sụp" giả** trong loại thí nghiệm này — mà thiết kế đó lại
đang khá phổ biến. Nói cách khác, bài chuyển từ "phát hiện một cơ chế gây
hại" sang "cảnh báo một cái bẫy phương pháp".

**Em đã chạy lặp lại lần A với seed khác để kiểm tra**, và nó xác nhận: cột
làm-8-lần vẫn phẳng y nguyên (58.7% → 58.7%), cột làm-1-lần vẫn rơi ~3 điểm
rồi đứng. Hai lần chạy độc lập cùng một hình dạng.

**Lần lặp đó còn cho em một con số em không ngờ tới.** Vòng 0 là model gốc,
chưa học gì cả — hai seed lẽ ra phải đo ra cùng một điểm. Nhưng seed này ra
32.0%, seed kia ra 36.7%, chênh **4.7 điểm**, chỉ vì bốc trúng 150 đề thi
khác nhau. Nghĩa là **riêng việc đổi tập đề đã tạo ra chênh lệch lớn hơn
toàn bộ hiệu ứng em đang đo**. Cái này quan trọng: nó cho em một thước đo để
biết một khác biệt phải lớn cỡ nào mới đáng tin — và chênh lệch giữa A với B
(0.6 điểm) thì nhỏ hơn thước đo đó nhiều lần.

**Em nói thẳng phần chưa chắc:** lần B mới chạy 1 seed, nên kết luận "vá
không có tác dụng" cần thêm một cặp seed nữa mới chốt hẳn. Đó là lần chạy kế
tiếp của em.

---

## Nếu thầy hỏi thêm

- **"Vậy đề tài còn giá trị không, hay phải làm lại từ đầu?"** — Dạ còn, và
  không phải làm lại. Câu hỏi nghiên cứu giữ nguyên, hạ tầng code giữ
  nguyên, dữ liệu đã chạy đều dùng được. Cái đổi là **kết luận** và **phạm
  vi tuyên bố**. Một kết quả phủ định đo bằng đối chứng sạch vẫn là kết quả
  đăng được — và thực tế nó khó bị vặn hơn kết quả khẳng định, vì hội đồng
  không nghi được là em chỉnh số cho khớp giả thuyết.

- **"Sao không phát hiện lỗ hổng đó ngay từ đầu?"** — Dạ đúng là lẽ ra nên
  thấy sớm hơn. Em phát hiện khi tách điểm theo từng bộ đề và thấy GSM8K —
  bộ mà máy chấm gần như không lệch — lại sụp mạnh hơn MATH-500. Chi tiết đó
  ngược hẳn giả thuyết, và chính nó dẫn em đi kiểm tra lại thiết kế.

- **"Có chắc kết luận bác bỏ này đúng không?"** — Dạ chưa chắc hoàn toàn.
  A và B trùng nhau trên **một** seed thì phù hợp với việc bản vá không có
  tác dụng, nhưng chưa loại trừ được một tác dụng nhỏ bị nhiễu che. Đó là lý
  do việc kế tiếp của em là chạy lặp seed, trước khi viết con số cuối vào
  bài.

- **"Ba lần chạy mới khác lần cũ ở nhiều thứ cùng lúc, sao so được?"** — Dạ
  đúng, đổi 3 thứ cùng lúc: bỏ gộp bộ đề, thêm đề thi riêng, và giảm số đề
  mỗi lần chạy. Nên em **không** dùng phép so cũ-mới để kết luận nhân quả.
  Kết luận bác bỏ của em chỉ dựa trên so sánh **nội bộ** giữa A và B — hai
  lần chạy giống hệt nhau, khác đúng một biến.

- **"Còn chỗ GSM8K rơi 12.7 điểm thì sao?"** — Dạ đó là câu hỏi mở duy nhất
  còn lại. Nó rơi gần hết ở vòng cuối, trên đề thi 150 đề, một seed — chưa
  đủ để phân biệt tín hiệu thật với nhiễu. Em ghi nó vào bài như một quan sát
  cần kiểm chứng, không ghi như một phát hiện.

- **"Bước tiếp theo?"** — Dạ ba việc: chạy lặp seed cho A và B để chốt kết
  luận bác bỏ; chạy thêm một thí nghiệm "không lọc" (train trên toàn bộ bài
  làm, không qua máy chấm) để tách hẳn ảnh hưởng của khâu lọc; rồi mới viết
  số cuối vào bài báo. Bản thảo bài báo em đã viết lại theo hướng mới rồi,
  chỉ chờ số từ seed lặp để khoá bảng kết quả.

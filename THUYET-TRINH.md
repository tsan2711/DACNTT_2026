# Kịch bản nói — báo cáo tuần 1 đến tuần 3 (12/9/2026)

Đi kèm `BaoCaoTienDo_Tuan1-3_52300057_52300006.pptx`, 18 slide.
Tổng khoảng **15–17 phút**. Đọc to thử ít nhất một lần trước khi vào.

**Lưu ý về cách xưng hô:** slide viết ở giọng trung tính, không có "em" hay
"thầy" — vì slide là để cả phòng đọc. Còn lời nói thì vẫn xưng "em" bình
thường, và mở đầu chào cả thầy lẫn các bạn.

**Ba điều cần nhớ khi nói:**
1. Đây là bài kể chuyện "em tưởng đúng, hoá ra sai". Đừng né chỗ sai —
   nói thẳng thì thành điểm mạnh, nói vòng thì kiểu gì cũng bị hỏi tới.
2. Chỗ quan trọng nhất là **slide 11** (hai đường chồng lên nhau). Nói chậm
   lại ở đó, dừng 2 giây cho mọi người nhìn hình.
3. Số nào cũng nói kèm ý nghĩa. Đừng đọc "hai mươi hai phẩy bốn điểm" trống
   không, mà nói "tụt hơn hai mươi điểm, tức là mất gần một phần ba".

---

## Slide 1 — Bìa  ·  ~20 giây

> Dạ em chào thầy, chào các bạn. Hôm nay em báo cáo ba tuần đầu của đề tài.
>
> Em xin nói trước kết quả chính cho dễ theo dõi: em có một giả
> thuyết, em chạy thí nghiệm và ban đầu tưởng là đúng. Nhưng sau đó em phát
> hiện cách đo của mình có lỗi. Em đo lại cho đúng, thì kết quả ngược lại.
> Giả thuyết của em sai.

*Đừng vội chuyển slide. Để câu cuối lắng một nhịp.*

---

## Slide 2 — Nội dung  ·  ~15 giây

> Phần trình bày đi theo thứ tự này: bối cảnh đề tài, lỗi của máy chấm, kết
> quả hai tuần đầu, vấn đề trong thiết kế, và cuối cùng là thí nghiệm làm lại.

---

## Slide 3 — Đề tài  ·  ~60 giây

> Dạ đề tài của em thế này. Muốn model giải toán giỏi hơn thì bình thường
> phải có người ngồi soạn lời giải mẫu cho nó học. Việc đó rất tốn công.
>
> Nên người ta nghĩ ra cách khác: cho model tự làm bài. Rồi dùng một máy chấm
> tự động, chọn ra những bài nó làm đúng. Lấy đúng mấy bài đó dạy lại cho
> chính nó. Làm đi làm lại nhiều vòng. Người ta gọi cách này là tự học.
>
> Nhưng cả cách làm này dựa trên một niềm tin: **máy chấm phải chấm đúng**.
> Nếu máy chấm sai, model sẽ học nhầm mà không ai biết.
>
> Và máy chấm em dùng thì có sai. Sai theo một quy luật cố định. Nên câu hỏi
> của em là: sau nhiều vòng như vậy, model có bị dở đi không?

---

## Slide 4 — Một vòng chạy  ·  ~50 giây

> Một vòng gồm ba bước. Model tự làm mỗi đề tám lần, ra tám lời giải khác
> nhau. Máy chấm lấy đáp án cuối so với đáp án trong sách, sai thì bỏ. Còn
> lại bao nhiêu thì đem dạy lại cho model. Xong một vòng, lặp lại năm lần.
>
> Chỗ này quan trọng: mỗi vòng em dạy lại **từ model gốc**, chỉ bằng bài của
> vòng trước. Nên nếu máy chấm bỏ sót một kiểu bài nào đó, thì vòng sau model
> càng ít gặp kiểu đó. Vòng sau nữa lại càng ít hơn. Nó dồn lại.
>
> Còn hai con số em dùng để đo. **pass@1** là cho model làm một lần, đúng bao
> nhiêu phần trăm. **pass@8** là cho làm tám lần, chỉ cần một lần đúng là
> tính đúng — cái này đo xem model còn giải nổi bài hay không.

*Nhấn chữ "còn giải nổi bài hay không". Cả bài sau này xoay quanh pass@8.*

---

## Slide 5 — Máy chấm sai ở đâu  ·  ~50 giây

> Đây là chỗ máy chấm sai. Giả sử đáp án đúng của bài là một nửa.
>
> Model viết `\frac{1}{2}` thì máy chấm nhận. Nhưng model viết `\dfrac{1}{2}`
> thì máy chấm gạch. Mọi người nhìn cột giữa — hai cách viết đó **hiện ra y hệt
> nhau**, cùng là một phần hai. Chỉ khác cách gõ thôi.
>
> Em thử 146 lần thì gạch cả 146 lần, không trượt lần nào.
>
> Lý do là máy chấm không đọc cách giải. Nó chỉ lấy đáp án cuối rồi so chữ.
>
> Em có kiểm tra tay 128 bài **model làm đúng**, thì máy gạch oan 10 bài, tức
> khoảng bảy phẩy tám phần trăm. Riêng bộ GSM8K thì không gạch oan bài nào,
> vì đáp án bộ đó toàn số nguyên, không có phân số.
>
> Em xin nhấn một chỗ dễ nhầm: bảy phẩy tám phần trăm này là **tỉ lệ máy chấm
> sai**, không phải tỉ lệ model làm sai. Máy chấm sạch không làm điểm model
> cao lên — nó chỉ làm cho điểm đo được trở nên đáng tin thôi.

*Nếu có người hỏi ngay "sao không sửa máy chấm đi" — trả lời: "Dạ có sửa,
đó là thí nghiệm ở slide 11 ạ." Rồi đi tiếp, đừng nhảy cóc.*

---

## Slide 6 — Tuần 1  ·  ~40 giây

> Tuần 1 em chạy thử với model nhỏ, Qwen 0.5B, 500 đề mỗi bộ, năm vòng, trên
> GPU của Kaggle.
>
> Kết quả là cả hai con số đều tụt. pass@1 từ 31 xuống 27. pass@8 từ 60 xuống
> gần 55.
>
> Em thấy vậy là khớp với điều mình nghĩ: máy chấm gạch nhầm bài đúng, model
> học thiếu, nên dở đi. Nhưng model này nhỏ, mức tụt cũng ít, nên em chưa dám
> chắc. Tuần 2 em chạy lại với model to gấp ba.

---

## Slide 7 — Tuần 2  ·  ~60 giây

> Model 1.5B thì tụt mạnh hơn hẳn. pass@1 từ 50 xuống còn 18. pass@8 từ 72
> xuống 48 — tức là mất hai mươi bốn điểm, gần một phần ba.
>
> Vòng nào cũng tụt, không vòng nào gượng lại. Đến đây em gần như tin chắc là
> giả thuyết của mình đúng rồi.
>
> Ở đây em xin giải thích con số vòng 0. Vòng 0 là model gốc, chưa học gì cả.
> 69,6% trên GSM8K là năng lực thật của nó — ba mươi phần trăm còn lại nó làm
> sai thật, và máy chấm gạch là gạch đúng. Máy chấm sạch không có nghĩa điểm
> phải là một trăm phần trăm.
>
> Và vì máy chấm ở GSM8K không gạch oan, nên cú tụt từ 69,6 xuống 26,6 là
> **tụt thật**, không phải sai số đo.
>
> Nhưng có một chỗ em thấy lạ. Mọi người nhìn hai dòng dưới: em tách số ra theo
> từng bộ đề, thì **GSM8K lại tụt nhiều nhất** — hai mươi lăm điểm.
>
> Mà GSM8K chính là bộ mà máy chấm gần như không gạch nhầm bài nào. Theo giả
> thuyết của em thì bộ đó phải đứng yên mới đúng.
>
> Chi tiết này làm em quay lại soi thiết kế thí nghiệm.

*Đây là bản lề của cả bài. Nói chậm đoạn "mà GSM8K chính là bộ...", và nhìn
xuống phòng một nhịp — đây là lúc người nghe phải thấy có gì đó sai.*

---

## Slide 8 — Hai lỗi  ·  ~70 giây

> Soi lại thì em thấy cách đo của mình có hai lỗi.
>
> **Lỗi thứ nhất.** Em gộp hai bộ đề lại rồi dạy chung một lần. Mọi người nhìn
> dòng cuối bảng: trong đống bài đem đi dạy mỗi vòng, GSM8K chiếm gần 70%,
> vòng nào cũng vậy.
>
> Nghĩa là khi em đo điểm của MATH-500, thật ra model đó học chủ yếu từ
> GSM8K. Hai bộ dính vào nhau. Em không tách được "tại máy chấm sai" với
> "tại lây từ bộ kia".
>
> **Lỗi thứ hai.** Em chấm điểm trên chính những đề đã dùng để chọn bài dạy.
> Nên điểm tụt có thể chỉ là model quên bài cũ, chứ chưa chắc là nó dở đi
> thật.
>
> Hai lỗi này cộng lại thì thí nghiệm của em không trả lời được câu hỏi của
> chính nó.

---

## Slide 9 — Đo lại  ·  ~50 giây

> Nên em làm lại. Năm lần chạy mới, sửa cả hai lỗi.
>
> Mỗi lần chỉ chạy một bộ đề thôi, không gộp nữa. Và em giữ riêng 30% số đề
> làm đề thi, model chưa từng được học mấy đề đó.
>
> Mọi người để ý hai dòng in đậm. Lần chạy A và lần chạy B **giống hệt nhau**, chỉ
> khác đúng một chỗ: ở B em đã sửa lỗi của máy chấm.
>
> Nếu giả thuyết của em đúng, thì B phải khá hơn A rõ rệt. Đây là phép thử
> trực tiếp, và thiết kế cũ của em không làm được phép thử này.
>
> Tổng cộng khoảng 25 giờ GPU, chia nhiều phiên vì Kaggle giới hạn 12 tiếng
> một lần.

---

## Slide 10 — Kết quả  ·  ~60 giây

> Đây là kết quả. Trục đứng là pass@8, tức là model còn giải nổi bài không.
>
> Hai đường màu cam là cách đo cũ. Mọi người thấy nó lao xuống, mất hai mươi hai
> đến hai mươi sáu điểm.
>
> Ba đường còn lại là cách đo mới. Gần như nằm ngang. Không tụt.
>
> Nghĩa là cú tụt mà em báo cáo ở tuần 1 và tuần 2 — nó đến từ **cách em đo**,
> chứ không phải từ máy chấm.

*Chỉ tay vào hai đường cam trước, rồi mới chỉ ba đường phẳng. Dừng 2 giây.*

---

## Slide 11 — Thí nghiệm quan trọng nhất  ·  ~70 giây

> Còn đây là thí nghiệm quan trọng nhất của em.
>
> Đường xanh là máy chấm để nguyên. Đường cam là máy chấm **đã sửa**. Mọi thứ
> khác giống hệt nhau.
>
> Hai đường nằm chồng lên nhau. Ở lần chạy thứ hai, từ vòng 2 trở
> đi, hai con số **giống hệt nhau**, không lệch một chữ số nào.
>
> Em sửa đúng cái lỗi mà cả đề tài cho là nguyên nhân. Sửa xong, điểm không
> nhúc nhích.
>
> Đề thi có 150 đề, nên mỗi đề đáng khoảng 0,67 điểm. A với B chênh nhau
> nhiều nhất là 0,6 điểm — tức là đúng một đề.
>
> Đây là bằng chứng mạnh nhất cho thấy em đã nghĩ sai.

*Nói câu cuối chậm và rõ. Đừng xin lỗi, đừng rào đón — chỉ nói sự việc.*

---

## Slide 12 — Vì sao (slide nền đen)  ·  ~70 giây

> Em có tìm ra được lý do vì sao sửa mà không ăn thua.
>
> Đúng là gặp cách viết đó thì máy chấm gạch 100%, không trượt lần nào. Nghe
> rất nặng.
>
> **Nhưng** trong bốn nghìn bài model làm mỗi vòng, chỉ có 22 bài viết theo
> kiểu đó thôi. Tức là nửa phần trăm. Còn bộ GSM8K thì không có bài nào.
>
> Nhân hai con số lại: phần bài bị gạch oan mỗi vòng chỉ là nửa phần trăm.
> Quá ít để làm tụt hai mươi điểm.
>
> Em còn đo được trực tiếp nữa. Ở vòng 0 model chưa học gì cả, nên lần chạy A
> và B làm ra y hệt một bộ bài. Khác nhau chỉ là máy chấm nào chấm thôi. Sửa
> máy chấm xong thì kết quả đổi đúng một đề trên 150 đề.
>
> Bài học em rút ra, và em nghĩ cái này dùng được cho người khác: một lỗi
> nặng tới đâu cũng chỉ hại được đúng bằng số lần nó thật sự xảy ra.

*Slide này nền đen, khác hẳn mấy slide kia. Tận dụng: đứng yên, nói chậm.*

---

## Slide 13 — Phạm vi đề tài  ·  ~50 giây

> Vậy đề tài đi tiếp thế nào.
>
> Cái bên trái em bỏ. Giả thuyết ban đầu, em đã tự kiểm tra bằng thí nghiệm
> đối chứng, chạy hai lần cho chắc. Không đúng.
>
> Cái bên phải em giữ. Gộp nhiều bộ đề dạy chung, rồi chấm trên chính đề đã
> học, sẽ tạo ra một cú tụt giả. Cái này em có số liệu.
>
> Kèm thêm một lưu ý cho người làm sau: muốn biết một lỗi máy chấm có hại
> không, thì phải đếm xem nó xảy ra bao nhiêu lần, chứ không chỉ nhìn nó nặng
> cỡ nào.
>
> Kết luận này nhỏ hơn cái em định làm lúc đầu. Nhưng cái bẫy em vấp phải thì
> nhiều người cũng đang vấp, nên em nghĩ vẫn đáng viết ra.

---

## Slide 14 — Bài học rút ra  ·  ~80 giây

> Từ ba tuần vừa rồi em rút ra một quy luật, và bảng này là bằng chứng cho
> nó. Em xin nói trước: **cả hai cột số giữa đều là số đề tài đã đo**, không
> phải em ước lượng.
>
> Cột thứ hai là model thật sự viết kiểu đó bao nhiêu phần trăm số bài — đếm
> trên bốn nghìn lời giải mỗi vòng. Cột thứ ba là máy chấm gạch kiểu đó bao
> nhiêu phần trăm — cái này em đo bằng cách ép máy chấm trên đáp án viết lại.
>
> Cột cuối là nhân hai cột lại. Đó mới là thiệt hại thật.
>
> Giờ mọi người nhìn dòng in đậm. `\dfrac` — cái em đem ra thử suốt ba tuần
> — bị gạch **100%**, nặng nhất bảng. Nhưng model chỉ viết kiểu đó ở **nửa
> phần trăm** số bài. Nhân lại còn 0,55%.
>
> Nói thẳng ra là em đã chọn đúng cái ô cho hiệu ứng nhỏ nhất trong cả bảng.
> Không phải em đo sai, mà là chọn nhầm chỗ để đo.
>
> Và mọi người để ý dòng thứ hai: `\boxed`. Model viết kiểu đó ở hơn một nửa
> số bài, mà máy chấm cũng gạch khoảng hai mươi phần trăm. Nhân lại là khoảng
> mười phần trăm — gấp gần hai mươi lần cái em đã thử.
>
> Vùng đó thì chưa ai đo, kể cả đề tài này.

*Đây là slide nặng nhất về số. Đi từng cột một, đừng đọc cả bảng một lượt.
Dừng lại ở dòng in đậm.*

---

## Slide 15 — Đề tài tiếp theo  ·  ~70 giây

> Nên đề tài tiếp theo của em là đi đo cái ngưỡng đó.
>
> Cách làm rất gọn: giữ nguyên toàn bộ vòng lặp, chỉ đổi chỗ máy chấm bị lệch
> thôi. Mỗi lần chạy cho một điểm trên trục tần suất.
>
> Và điểm đầu tiên thì em đã có sẵn rồi — chính là ba tuần vừa rồi, ở tần
> suất nửa phần trăm, không thấy ảnh hưởng gì.
>
> Điểm thứ hai em sẽ bắt máy chấm gạch cách viết `\boxed`, phổ biến gấp
> khoảng **chín mươi lần**. Chỉ tốn một lần chạy, khoảng năm tiếng GPU.
>
> Điểm hay của thí nghiệm này là **ngã nào cũng ra kết quả dùng được**. Nếu
> model tụt điểm thì quy luật kia được chứng minh bằng thực nghiệm, và đề tài
> có một con số cụ thể để cảnh báo người dùng: lỗi máy chấm phải phổ biến tới
> mức nào thì mới đáng lo.
>
> Còn nếu vẫn không tụt, thì kết luận là lỗi máy chấm không phải thứ đáng lo
> trong tự học — cũng là một câu trả lời rõ ràng.
>
> Toàn bộ code và dữ liệu cũ em dùng lại được hết, chỉ cần thêm một tuỳ chọn
> cho máy chấm thôi.

*Đây là slide bán đề tài mới. Nhấn hai chỗ: "chín mươi lần" và "ngã nào cũng
ra kết quả dùng được". Nói dứt khoát, đừng rào đón.*

---

## Slide 16 — Chỗ còn chưa chắc  ·  ~50 giây

> Em xin nói một chỗ em còn chưa chắc.
>
> Cả bảy lần chạy, điểm đều tụt khoảng ba điểm ngay ở vòng 1 rồi đứng yên.
> Nhưng mấy bài báo lớn về tự học thì đều báo là model **khá lên**. Em chưa
> giải thích được vì sao của em ngược lại.
>
> Có một khả năng đơn giản mà em chưa loại trừ được: model này vốn đã được
> tinh chỉnh rất kỹ rồi. Em dạy thêm một chút nữa, có thể chỉ làm nó lệch
> khỏi trạng thái tốt sẵn có — bất kể em dạy nó bằng gì.
>
> Nên em sẽ thử dạy bằng lời giải mẫu của sách, thay vì bài model tự làm.
> Nếu khá lên thì vòng lặp không sao. Còn nếu cũng tụt thì cú tụt là do việc
> dạy thêm, không liên quan tự học, và em phải sửa kết luận lần nữa.
>
> Code em viết xong rồi, đang chờ tới lượt GPU.

---

## Slide 17 — Chỗ còn yếu  ·  ~40 giây

> Em xin nói trước mấy chỗ còn yếu.
>
> Đề thi chỉ có 150 đề, nên mỗi đề đáng 0,67 điểm. Chỉ cần đổi cách bốc đề
> thi thôi là điểm vòng 0 đã lệch 4,7 điểm — nhiều hơn cả cái em đang đo.
>
> Mỗi cấu hình em mới chạy được hai lần, riêng lần C thì mới một lần.
>
> Và lần chạy mới khác lần cũ tới ba chỗ. Nên em chỉ dám kết luận dựa trên so
> sánh A với B thôi, vì hai lần đó chỉ khác nhau đúng một chỗ.

---

## Slide 18 — Tóm tắt  ·  ~30 giây

> Tóm lại ba tuần vừa rồi: em chạy bảy lần, khoảng 40 giờ GPU. Em dựng một
> thí nghiệm để kiểm tra giả thuyết của chính mình, và nó cho thấy em sai. Lý
> do em cũng tìm ra được.
>
> Đề tài chuyển sang cảnh báo về cách đo. Nhỏ hơn, nhưng em chắc chắn.
>
> Sắp tới em chạy thí nghiệm điều khiển tần suất lỗi, để tìm cái ngưỡng đó,
> rồi viết lại bài báo.
>
> Em cảm ơn thầy và các bạn đã theo dõi. Rất mong nhận được góp ý ạ.

---

# Câu hỏi có thể bị hỏi — xếp theo slide

Cách dùng: đọc lướt toàn bộ một lần trước khi vào. Ba câu ở mục **Khó nhất**
cuối file thì học thuộc ý, vì đó là mấy câu có thể làm hỏng buổi bảo vệ.

Nguyên tắc chung khi trả lời: **câu nào chưa biết thì nói chưa biết**, kèm
cách sẽ kiểm tra. Đừng chế số. Cả bài này mạnh ở chỗ trung thực, bịa một câu
là mất sạch.

---

## Slide 1 — Bìa

**"Báo cáo một kết quả sai, vậy đề tài coi như thất bại à?"**
> Dạ em nghĩ ngược lại ạ. Nếu em không tự tìm ra lỗi này thì em đã viết một
> bài báo với kết luận sai. Tới lúc người khác phát hiện thì nặng hơn nhiều.
> Còn tự phát hiện và tự sửa thì đó là quy trình nghiên cứu chạy đúng.

**"Vậy ba tuần vừa rồi có phí không?"**
> Dạ không ạ. Code, dữ liệu, và cả bảy lần chạy vẫn dùng lại được hết. Cái
> thay đổi là kết luận, chứ không phải công sức.

---

## Slide 3 — Đề tài

**"Tự học khác gì fine-tuning bình thường?"**
> Dạ fine-tuning bình thường thì dữ liệu dạy là do người soạn. Còn tự học thì
> dữ liệu dạy là do chính model sinh ra, rồi lọc bằng máy chấm. Không cần
> người viết lời giải, nên rẻ hơn rất nhiều — nhưng đổi lại là phải tin vào
> máy chấm.

**"Sao không thuê người chấm cho chính xác?"**
> Dạ vì mỗi vòng model sinh bốn nghìn lời giải, năm vòng là hai mươi nghìn.
> Chấm tay hết thì không khả thi ạ. Với lại nếu có người chấm thì đã không
> cần tự học, cứ đưa lời giải mẫu cho nó học là xong.

**"Hướng này đã có ai làm chưa?"**
> Dạ có mấy nhánh riêng lẻ ạ. Có bài đo máy chấm sai bao nhiêu, nhưng chỉ đo
> một vòng. Có bài chạy tự học nhiều vòng, nhưng máy chấm của họ chuẩn nên
> không có vấn đề này. Chưa bài nào ghép cả hai: máy chấm có lỗi đã đo được,
> chạy nhiều vòng, và theo dõi xem chuyện gì xảy ra.

---

## Slide 4 — Một vòng chạy

**"Sao mỗi vòng lại dạy lại từ model gốc, không dạy tiếp lên model cũ?"**
> Dạ em làm theo đúng cách mấy bài chuẩn trong lĩnh vực này làm ạ. Lý do là
> nếu dạy chồng lên nhau thì không biết model dở đi vì dữ liệu xấu hay vì bị
> dạy quá nhiều lần. Dạy lại từ gốc thì mỗi vòng là một phép đo độc lập.

**"Sao lại chọn k bằng 8?"**
> Dạ vì giới hạn GPU ạ. Bài chuẩn trong lĩnh vực dùng k bằng 32, nhưng em
> chạy trên Kaggle miễn phí nên k bằng 8 là mức em kham được. Đây cũng là một
> hạn chế em có ghi trong bài.

**"pass@8 có ý nghĩa thực tế gì? Người dùng đâu có cho model làm 8 lần."**
> Dạ đúng là người dùng chỉ hỏi một lần ạ. pass@8 không phải để đo trải
> nghiệm người dùng, mà để phân biệt **hai kiểu hỏng khác nhau**. Nếu pass@8
> cũng tụt thì model thật sự mất năng lực giải bài. Còn nếu pass@8 giữ nguyên
> mà chỉ pass@1 tụt, thì model vẫn biết giải, chỉ là kém ổn định hơn. Hai
> chuyện đó cần cách chữa khác nhau.

**"Năm vòng đã đủ chưa?"**
> Dạ chưa chắc ạ. Em không biết qua vòng năm thì đường cong còn tụt tiếp,
> đứng lại, hay gượng lên. Đây là hạn chế thật, em có ghi trong bài báo.

---

## Slide 5 — Máy chấm sai ở đâu

**"Máy chấm không sai trên GSM8K, sao vòng 0 không phải 100%?"**
> Dạ hai cái đó khác nhau ạ. Máy chấm không sai nghĩa là nó không gạch oan
> bài model làm đúng. Còn 69,6% là **model giải được bao nhiêu** — ba mươi
> phần trăm còn lại model làm sai thật, máy chấm gạch là gạch đúng. Máy chấm
> sạch không đẩy điểm lên, nó chỉ làm cho con số 69,6% đó đáng tin thôi ạ.

**"Sao không dùng một model khác làm máy chấm cho chuẩn hơn?"**
> Dạ có hướng đó ạ, đã có bài làm rồi. Nhưng nó tốn tiền và chậm hơn nhiều,
> và bản thân model chấm cũng có lỗi riêng của nó. Em chọn máy chấm theo luật
> vì đó là cái đang được dùng phổ biến nhất, nên lỗi của nó mới đáng đo.

**"Kiểm tra tay có 128 bài, mẫu nhỏ vậy có tin được không?"**
> Dạ 128 bài là em kiểm tra từng bài một nên chắc chắn về mặt chất lượng, còn
> về số lượng thì đúng là nhỏ ạ. Nhưng con số 7,8% này chỉ dùng để mô tả bối
> cảnh thôi. Kết luận chính của em không dựa vào nó, mà dựa vào thí nghiệm
> đối chứng ở slide 11.

**"math-verify là thư viện nhiều người dùng, sao lại có lỗi đơn giản vậy?"**
> Dạ vì nó phải chuẩn hoá rất nhiều kiểu viết khác nhau, không thể phủ hết
> được ạ. Đây không phải lỗi ẩu, mà là giới hạn cố hữu của cách chấm bằng so
> chuỗi. Có bài báo khác đo độc lập cũng ra khoảng mười bốn phần trăm gạch
> oan, cùng cỡ với con số của em.

---

## Slide 6 — Tuần 1

**"Tụt ba tới năm điểm thì có phải nhiễu không?"**
> Dạ đúng ạ, và đây là chỗ em phải tự nhận. Bây giờ em biết riêng việc đổi
> cách bốc đề thi đã làm điểm lệch 4,7 điểm rồi, tức là cú tụt ở tuần 1 nằm
> gọn trong vùng nhiễu. Lúc đó em chưa đo được cái ngưỡng nhiễu này nên chưa
> biết. Đó cũng là một bài học về thứ tự làm việc.

**"Sao chỉ lấy 500 đề mỗi bộ?"**
> Dạ vì mỗi vòng phải sinh 500 nhân 8 là bốn nghìn lời giải, năm vòng là hai
> mươi nghìn. Với GPU miễn phí thì một lần chạy đã mất năm tiếng rồi ạ.

---

## Slide 7 — Tuần 2

**"Vậy GSM8K tụt mạnh là do đâu?"**
> Dạ vì máy chấm ở GSM8K sạch nên cú tụt đó là tụt thật, model dở đi thật ạ.
> Và nó cũng không giải thích được bằng chuyện chấm trên đề đã học — vì nếu
> model thuộc bài thì điểm phải tăng chứ không rơi xuống dưới cả điểm ban
> đầu. Khi em chạy GSM8K riêng một mình thì nó chỉ tụt 12,7 điểm và pass@8
> đứng yên. Nghĩa là khoảng 27 điểm còn lại đến từ việc **gộp hai bộ đề dạy
> chung**. Cái sai của em là quy nó cho máy chấm, chứ hiện tượng thì có thật.

**"Vì sao model to lại tụt nặng hơn? Trực giác là ngược lại chứ."**
> Dạ em cũng thấy ngược ạ. Giả thuyết của em, chưa chứng minh, là model to
> khớp vào tập dữ liệu nhanh hơn — cùng một epoch nhưng nó học sâu hơn vào
> cái tập đã bị lọc hẹp, nên lệch nhanh hơn. Nhưng em chưa đo trực tiếp nên
> chưa dám khẳng định.

**"Có chắc không phải lỗi code không?"**
> Dạ em có kiểm tra mấy chỗ dễ sai nhất. Dữ liệu đem dạy có đúng định dạng
> như lúc model sinh bài. Model có nạp đúng adapter sau mỗi vòng. Và quan
> trọng nhất là khi đo lại bằng thiết kế sạch thì cú tụt biến mất — nếu là
> lỗi code thì nó phải còn nguyên ở cả hai thiết kế.

---

## Slide 8 — Hai lỗi

**"Sao ban đầu lại thiết kế gộp hai bộ đề?"**
> Dạ vì em muốn có nhiều đề hơn trong một lần chạy cho tiết kiệm GPU ạ. Lúc
> đó em nghĩ hai bộ đề độc lập nhau nên gộp lại không sao. Em không nghĩ tới
> chuyện chỉ có một adapter chung học cả hai.

**"Tỉ lệ 69% ổn định suốt năm vòng, ổn định thế thì sao lại là vấn đề?"**
> Dạ ổn định chỉ loại được một giả thuyết thôi ạ — là giả thuyết "tỉ lệ trôi
> dần nên gây nhiễu". Nhưng nó không loại được vấn đề chính: một adapter duy
> nhất học 69% từ GSM8K rồi được đem đi chấm trên MATH-500. Hai bộ vẫn dính
> vào nhau, chỉ là dính đều đặn.

**"Chấm trên đề đã dùng để chọn bài dạy thì sai ở chỗ nào? Model có được xem
đáp án đâu."**
> Dạ model không xem đáp án, nhưng nó được dạy bằng chính lời giải của nó cho
> đúng mấy đề đó ạ. Nên điểm của nó trên mấy đề đó phản ánh cả chuyện "nhớ
> bài" lẫn "biết giải", không tách ra được.

---

## Slide 9 — Đo lại

**"Sao lại giữ 30% làm đề thi, không phải 20% hay 50%?"**
> Dạ 30% là mức thông dụng ạ. Giữ nhiều quá thì còn ít đề để dạy, giữ ít quá
> thì đề thi nhỏ, đo không ổn định. Em không thử nhiều mức khác nhau.

**"Sao không sửa từng lỗi một để biết lỗi nào mới là thủ phạm?"**
> Dạ đúng ra nên làm vậy ạ, và đây là một thiếu sót thật. Em sửa cả hai cùng
> lúc nên không tách được đóng góp của từng lỗi. Chính vì thế kết luận bác bỏ
> của em **không dựa** vào phép so cũ với mới, mà chỉ dựa vào so A với B —
> hai lần chạy đó chỉ khác nhau đúng một biến.

**"Sao không chạy nhiều seed hơn?"**
> Dạ mỗi lần chạy mất khoảng năm tiếng GPU, mà Kaggle giới hạn mười hai tiếng
> một phiên và có hạn mức tuần ạ. Em ưu tiên chạy hai seed cho cặp A và B
> trước, vì đó là chỗ kết luận chính nằm.

---

## Slide 10 — Kết quả

**"Đổi ba thứ cùng lúc thì sao so sánh cũ với mới được?"**
> Dạ em không dùng phép so đó để kết luận ạ. Em chỉ dùng nó để mô tả: thiết
> kế cũ ra thế này, thiết kế mới ra thế kia. Còn kết luận bác bỏ thì hoàn
> toàn dựa vào so A với B, nằm trong cùng một thiết kế, khác nhau đúng một
> biến.

**"pass@8 phẳng nhưng pass@1 vẫn tụt, vậy vẫn có hại chứ?"**
> Dạ vâng, vẫn có hại ạ, nhưng là kiểu hại khác. Model không mất năng lực
> giải bài, nó chỉ kém ổn định ở lần trả lời đầu. Riêng bộ GSM8K tụt 12,7
> điểm thì vượt ngưỡng nhiễu, nên em coi đó là hiện tượng thật — nhưng mới
> chạy một lần nên chưa dám khẳng định.

---

## Slide 11 — Thí nghiệm đối chứng

**"Có chắc phần code sửa máy chấm chạy đúng không?"**
> Dạ có ba chỗ xác nhận ạ. Một là file cấu hình của lần chạy ghi rõ chế độ vá
> đang bật. Hai là ở seed 1, vòng 0 hai bên ra khác nhau — 36,7 với 37,3 —
> mà vòng 0 thì hai bên sinh ra y hệt một bộ bài, nên khác biệt đó **chính
> là** tác dụng của bản vá. Ba là nếu bản vá không chạy thì hai bên phải
> giống nhau tuyệt đối ở mọi vòng, mà thực tế pass@8 vẫn khác nhau.

**"Hai đường trùng khít vậy, có phải chạy nhầm cùng một cấu hình hai lần
không?"**
> Dạ không ạ, và cái khác biệt nhỏ xíu ở vòng 0 lại chính là bằng chứng. Nếu
> là cùng một cấu hình thì vòng 0 phải giống hệt. Nó khác nhau đúng một đề —
> đó là bản vá có tác dụng, nhưng tác dụng chỉ bằng một đề trên 150.

**"Chênh 0,6 điểm, sao biết đó là nhiễu chứ không phải hiệu ứng nhỏ?"**
> Dạ em không khẳng định nó bằng không ạ. Em nói là nó **nhỏ hơn ngưỡng đo
> được của thiết lập này**. Đề thi 150 đề thì một đề đã là 0,67 điểm, nên
> 0,6 điểm nằm dưới mức phân giải. Muốn nói chắc nó bằng không thì phải tăng
> số đề thi hoặc chạy thêm seed.

---

## Slide 12 — Vì sao

**"0,55% là đếm trên toàn bộ lời giải hay chỉ riêng đáp án cuối?"**
> Dạ em đếm số lần cách viết đó xuất hiện **ở bất kỳ đâu** trong lời giải ạ.
> Mà máy chấm thì chỉ đọc đáp án cuối. Nên con số thật sự ảnh hưởng tới máy
> chấm còn **nhỏ hơn** 0,55%. Nghĩa là ước lượng của em đang thiên về phía
> nhiều, mà vẫn quá ít để gây hại.

**"Nếu cách viết đó hiếm vậy, sao ban đầu lại chọn nó để nghiên cứu?"**
> Dạ vì em đo mức nặng trước mà quên đo tần suất ạ. Em thấy nó bị gạch 100%
> nên nghĩ là nghiêm trọng. Đúng ra phải đếm xem nó xuất hiện bao nhiêu lần
> đã. Đó chính là bài học em rút ra, và em nghĩ nó dùng được cho người khác.

---

## Slide 13 — Phạm vi đề tài

**"Kết quả âm tính thì đăng được không?"**
> Dạ em nghĩ được ạ. Vì em không chỉ nói "không đúng", mà đo được **vì sao**
> không đúng — nặng 100% nhưng chỉ xảy ra ở nửa phần trăm số bài. Và cái bẫy
> thiết kế em vấp phải thì khá phổ biến trong mấy bài cùng hướng.

**"Đóng góp còn lại có đủ cho một bài báo không?"**
> Dạ em nghĩ đủ cho mức hội thảo ạ. Bài có ba thứ: một cảnh báo về thiết kế
> đo có số liệu chứng minh, một quy tắc đọc lại các con số lỗi máy chấm mà
> những bài khác công bố, và một thí nghiệm đối chứng sạch. Em không dám nói
> nó là đóng góp lớn, nhưng nó là đóng góp thật và kiểm chứng lại được.

---

## Slide 14 — Bài học rút ra

**"Con số 20% gạch của \boxed lấy ở đâu ra?"**
> Dạ từ phép thử ép máy chấm ạ: em lấy đáp án chuẩn, viết lại theo kiểu
> boxed, rồi bắt máy chấm chấm lại chính đáp án đó. Khoảng 20% bị gạch.

**"Nếu \boxed gây thiệt hại tới 10% thì sao thực tế không thấy model tụt?"**
> Dạ câu này đúng và em phải nói rõ ạ. Con số 20% kia là từ phép thử **ép**,
> không phải tỉ lệ tự nhiên khi model viết bài. Tỉ lệ gạch oan thật đo trên
> bài model làm là 7,8% tính chung. Nên cột "thiệt hại thực tế" ở dòng
> \boxed là **ước lượng trên**, không phải số đã đo. Và chính vì vậy thí
> nghiệm tiếp theo của em phải **chủ động ép** máy chấm gạch, chứ không thể
> ngồi chờ tỉ lệ tự nhiên.

**"Sao \frac bị gạch 0% mà \dfrac bị gạch 100%? Cùng là phân số mà."**
> Dạ vì máy chấm dùng một bộ luật phân tích cú pháp, và bộ luật đó biết lệnh
> `\frac` nhưng không biết lệnh `\dfrac` ạ. Gặp lệnh lạ thì nó không phân
> tích được nên coi như sai. Không phải nó so sánh giá trị.

---

## Slide 15 — Đề tài tiếp theo

**"Ép máy chấm gạch \boxed là tự tạo ra lỗi giả. Thực tế làm gì có máy chấm
tệ tới mức đó?"**
> Dạ đúng là không có máy chấm nào tệ như vậy ạ. Nhưng mục đích của em không
> phải mô phỏng một máy chấm có thật, mà là **điều khiển một biến để đo quan
> hệ**. Giống như trong y học người ta tăng liều để tìm ngưỡng, chứ không ai
> uống liều đó thật. Khi đã biết quan hệ giữa tần suất lỗi và mức hại, thì áp
> ngược lại được cho bất kỳ máy chấm thật nào: chỉ cần đếm tần suất lỗi của
> nó là biết có đáng lo không.

**"Đề tài mới có khác đề tài cũ nhiều quá không?"**
> Dạ không ạ, vẫn cùng một câu hỏi gốc: lỗi máy chấm ảnh hưởng thế nào tới tự
> học. Chỉ khác là trước em hỏi "có ảnh hưởng không", giờ em hỏi "ảnh hưởng
> từ mức nào". Toàn bộ code và dữ liệu cũ vẫn dùng lại được.

**"Nếu ép tới 51% mà vẫn không tụt thì sao?"**
> Dạ thì đó cũng là kết luận rõ ràng ạ: lỗi máy chấm không phải thứ đáng lo
> trong tự học, kể cả khi nó phổ biến. Lúc đó câu hỏi chuyển sang chỗ khác —
> vì phải có cái gì đó làm model tụt, mà không phải máy chấm.

---

## Slide 16 — Chỗ còn chưa chắc

**"Nếu thí nghiệm dạy-bằng-lời-giải-mẫu cũng tụt thì đề tài còn lại gì?"**
> Dạ thì em phải sửa kết luận lần nữa ạ, và em nói trước điều đó hôm nay chứ
> không giấu. Nhưng kể cả trường hợp xấu đó, hai thứ vẫn còn nguyên: cảnh báo
> về thiết kế gộp bộ đề, và quy tắc mức-nặng nhân tần-suất. Hai cái đó không
> phụ thuộc vào kết quả thí nghiệm này.

**"Sao không thử model chưa qua tinh chỉnh, cho sạch?"**
> Dạ đó đúng là cách kiểm tra tốt ạ, em có nghĩ tới. Nhưng model chưa tinh
> chỉnh thì điểm khởi đầu rất thấp, có khi không đủ bài đúng để dạy vòng
> tiếp theo. Em để việc đó vào phần mở rộng nếu còn GPU.

---

## Slide 17 — Hạn chế

**"Nhiễu tới 4,7 điểm mà kết luận lại dựa trên chênh lệch 0,6 điểm — có mâu
thuẫn không?"**
> Dạ không mâu thuẫn ạ, vì hai con số đó đo hai thứ khác nhau. 4,7 điểm là
> chênh lệch giữa **hai bộ đề thi khác nhau** — đổi seed thì bốc 150 đề khác.
> Còn A với B ở cùng một seed thì dùng **chung một bộ đề thi**, nên phép so
> của chúng không dính cái phương sai đó. Con số 4,7 chỉ để cảnh báo khi so
> điểm tuyệt đối giữa các lần chạy khác seed thôi ạ.

**"Sao không tăng số đề thi lên cho đỡ nhiễu?"**
> Dạ tăng đề thi thì phải giảm đề dạy, vì tổng có 500 đề. Hoặc tăng tổng số
> đề thì tốn GPU gấp đôi. Với hạn mức hiện tại thì em chưa làm được, nhưng
> đây là việc nên làm nếu xin được thêm GPU.

---

## Slide 18 — Tóm tắt

**"Kế hoạch thời gian còn lại thế nào?"**
> Dạ việc chờ GPU là chính ạ. Hai lần chạy nữa, mỗi lần khoảng năm tiếng.
> Phần viết bài báo thì em đã viết lại phần lớn rồi, chỉ chờ số cuối để chốt
> bảng kết quả.

**"Sao chỉ chạy model 1.5B, không chạy to hơn?"**
> Dạ vì Kaggle miễn phí giới hạn mười hai tiếng một phiên ạ. Một lần chạy
> 1.5B đã mất khoảng năm tiếng. Model to hơn thì không đủ giờ.

---

# Ba câu khó nhất — học thuộc ý

**1. "Em có chắc kết luận bác bỏ này đúng không?"**
> Dạ chắc ở phần A với B, vì em chạy hai seed khác nhau, lần nào hai đường
> cũng chồng lên nhau, và ở seed thứ hai thì từ vòng 2 trở đi con số giống
> hệt nhau. Còn phần so sánh thiết kế cũ với thiết kế mới thì em **không** dám
> chắc hoàn toàn, vì đổi ba thứ cùng lúc. Em chỉ kết luận trong phạm vi A
> với B thôi ạ.

**2. "Sao không phát hiện lỗi thiết kế sớm hơn?"**
> Dạ lẽ ra nên thấy sớm hơn ạ. Em phát hiện nhờ tách số theo từng bộ đề, thấy
> GSM8K tụt nhiều nhất — mà đó lại là bộ máy chấm không sai. Chi tiết đó
> ngược hẳn giả thuyết nên em mới quay lại soi thiết kế. Bài học là em đã
> nhìn số gộp quá lâu trước khi tách ra.

**3. "Vậy rốt cuộc cái gì làm model tụt điểm?"**
> Dạ em trả lời được một phần ạ. Chắc chắn **không phải** máy chấm lệch —
> cái đó em đã kiểm tra bằng đối chứng. Chắc chắn **có phần** do gộp hai bộ
> đề dạy chung, vì bỏ gộp đi thì mất khoảng 27 điểm thiệt hại trên GSM8K.
> Còn phần tụt nhẹ còn lại thì em **chưa biết**, và đó đúng là thí nghiệm em
> đang chạy dở. Em không muốn đoán khi chưa có số ạ.

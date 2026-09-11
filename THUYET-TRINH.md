# Kịch bản nói — báo cáo tuần 1 đến tuần 3 (12/9/2026)

Đi kèm `BaoCaoTienDo_Tuan1-3_52300057_52300006.pptx`, 16 slide.
Tổng khoảng **13–15 phút**. Đọc to thử ít nhất một lần trước khi vào.

**Ba điều cần nhớ khi nói:**
1. Đây là bài kể chuyện "em tưởng đúng, hoá ra sai". Đừng né chỗ sai —
   nói thẳng thì thành điểm mạnh, nói vòng thì thầy sẽ hỏi tới.
2. Chỗ quan trọng nhất là **slide 11** (hai đường chồng lên nhau). Nói chậm
   lại ở đó, dừng 2 giây cho thầy nhìn hình.
3. Số nào cũng nói kèm ý nghĩa. Đừng đọc "hai mươi hai phẩy bốn điểm" trống
   không, mà nói "tụt hơn hai mươi điểm, tức là mất gần một phần ba".

---

## Slide 1 — Bìa  ·  ~20 giây

> Dạ em chào thầy. Hôm nay em báo cáo ba tuần đầu của đề tài.
>
> Em xin nói trước kết quả chính luôn cho thầy dễ theo dõi: em có một giả
> thuyết, em chạy thí nghiệm và ban đầu tưởng là đúng. Nhưng sau đó em phát
> hiện cách đo của mình có lỗi. Em đo lại cho đúng, thì kết quả ngược lại.
> Giả thuyết của em sai.

*Đừng vội chuyển slide. Để câu cuối lắng một nhịp.*

---

## Slide 2 — Nội dung  ·  ~15 giây

> Em sẽ đi theo thứ tự này: đề tài là gì, máy chấm sai chỗ nào, rồi hai lần
> chạy đầu, chỗ em thấy không ổn, và cuối cùng là em đo lại ra sao.

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
> thì máy chấm gạch. Thầy nhìn cột giữa — hai cách viết đó **hiện ra y hệt
> nhau**, cùng là một phần hai. Chỉ khác cách gõ thôi.
>
> Em thử 146 lần thì gạch cả 146 lần, không trượt lần nào.
>
> Lý do là máy chấm không đọc cách giải. Nó chỉ lấy đáp án cuối rồi so chữ.
>
> Em có kiểm tra tay 128 bài làm đúng, thì máy gạch nhầm 10 bài, tức khoảng
> bảy phẩy tám phần trăm. Riêng bộ GSM8K thì không gạch nhầm bài nào, vì đáp
> án bộ đó toàn số nguyên, không có phân số.

*Nếu thầy hỏi ngay "sao không sửa máy chấm đi" — trả lời: "Dạ em có sửa,
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
> Nhưng có một chỗ em thấy lạ. Thầy nhìn hai dòng dưới: em tách số ra theo
> từng bộ đề, thì **GSM8K lại tụt nhiều nhất** — hai mươi lăm điểm.
>
> Mà GSM8K chính là bộ mà máy chấm gần như không gạch nhầm bài nào. Theo giả
> thuyết của em thì bộ đó phải đứng yên mới đúng.
>
> Chi tiết này làm em quay lại soi thiết kế thí nghiệm.

*Đây là bản lề của cả bài. Nói chậm đoạn "mà GSM8K chính là bộ...".*

---

## Slide 8 — Hai lỗi  ·  ~70 giây

> Soi lại thì em thấy cách đo của mình có hai lỗi.
>
> **Lỗi thứ nhất.** Em gộp hai bộ đề lại rồi dạy chung một lần. Thầy nhìn
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
> Thầy để ý hai dòng in đậm. Lần chạy A và lần chạy B **giống hệt nhau**, chỉ
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
> Hai đường màu cam là cách đo cũ. Thầy thấy nó lao xuống, mất hai mươi hai
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
> Thầy thấy hai đường nằm chồng lên nhau. Ở lần chạy thứ hai, từ vòng 2 trở
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

## Slide 13 — Đề tài đi tiếp  ·  ~50 giây

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

## Slide 14 — Chỗ còn chưa chắc  ·  ~50 giây

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

## Slide 15 — Chỗ còn yếu  ·  ~40 giây

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

## Slide 16 — Tóm tắt  ·  ~30 giây

> Tóm lại ba tuần vừa rồi: em chạy bảy lần, khoảng 40 giờ GPU. Em dựng một
> thí nghiệm để kiểm tra giả thuyết của chính mình, và nó cho thấy em sai. Lý
> do em cũng tìm ra được.
>
> Đề tài chuyển sang cảnh báo về cách đo. Nhỏ hơn, nhưng em chắc chắn.
>
> Sắp tới em chạy nốt thí nghiệm phân định, rồi viết lại bài báo.
>
> Em cảm ơn thầy. Mong thầy góp ý giúp em ạ.

---

# Nếu thầy hỏi thêm

**"Vậy ba tuần vừa rồi có phí không?"**
> Dạ không ạ. Toàn bộ code, dữ liệu, và mấy lần chạy vẫn dùng được. Cái đổi
> là kết luận. Với lại nếu em không tự tìm ra lỗi này thì em đã viết một bài
> báo sai, tới lúc hội đồng phát hiện thì nặng hơn nhiều ạ.

**"Sao không phát hiện sớm hơn?"**
> Dạ đúng là lẽ ra nên thấy sớm hơn. Em phát hiện nhờ tách số ra theo từng bộ
> đề, thấy GSM8K tụt nhiều nhất mà bộ đó máy chấm không sai. Chi tiết đó
> ngược hẳn giả thuyết nên em mới đi soi lại thiết kế.

**"Kết quả âm tính thì đăng được không?"**
> Dạ em nghĩ được ạ. Vì em không chỉ nói "không đúng", mà đo được **vì sao**
> không đúng — lỗi nặng 100% nhưng chỉ xảy ra ở nửa phần trăm số bài. Và cái
> bẫy thiết kế em vấp phải thì khá phổ biến trong mấy bài cùng hướng.

**"Em có chắc kết luận bác bỏ này đúng không?"**
> Dạ chắc ở phần A với B, vì em chạy hai lần seed khác nhau, lần nào hai
> đường cũng chồng lên nhau. Còn phần so sánh cách đo cũ với cách đo mới thì
> em chưa dám chắc hoàn toàn, vì đổi ba thứ cùng lúc.

**"Bước tiếp theo cụ thể là gì?"**
> Dạ ba việc ạ. Một là chạy thí nghiệm dạy bằng lời giải mẫu, để biết cú tụt
> là do tự học hay do việc dạy thêm. Hai là chạy lặp thêm cho lần chạy C.
> Ba là viết lại bài báo — em viết lại phần lớn rồi, chờ số cuối để chốt bảng
> kết quả.

**"Sao chỉ chạy model 1.5B, không chạy to hơn?"**
> Dạ vì em chạy trên Kaggle miễn phí, mỗi phiên tối đa 12 tiếng. Một lần chạy
> 1.5B đã mất khoảng 5 tiếng rồi ạ. Model to hơn thì không đủ giờ.

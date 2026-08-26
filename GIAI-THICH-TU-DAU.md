# Đề tài của bạn là gì — giải thích từ số 0, cho dân kỹ thuật phần mềm

File này viết cho người **biết code nhưng chưa từng làm ML/AI**. Mọi khái niệm
sẽ ví với thứ bạn đã quen (hàm, test, CI/CD, patch/diff) trước khi dùng từ
chuyên ngành. Lần này viết **kỹ hơn phần nền** — không chỉ ví von mà giải
thích cơ chế thật bên trong (weights là gì, train làm gì thật sự, generate
sinh chữ kiểu gì, verifier chấm ra sao), kèm **ví dụ chạy tay có số thật**,
và **câu hỏi tự kiểm tra** ở cuối để bạn tự chắc là đã hiểu đúng, không còn lủng.

Đọc theo thứ tự từ đầu, đừng nhảy cóc — phần 2 dựa vào phần 1, phần 3 dựa
vào phần 2.

---

## 1. Nền tảng: model thật sự là gì, train thật sự làm gì

### 1.1 Model là một hàm, nhưng "hàm" ở đây nghĩa chính xác là gì

Một model như Qwen2.5-0.5B-Instruct là một hàm toán học khổng lồ:

```
output_text = f(input_text)
```

Nhưng bên trong `f` không có `if/else` do người viết. Nó là một chuỗi các
**phép nhân ma trận** (matrix multiplication) nối tiếp nhau. "0.5B" nghĩa là
có khoảng **500 triệu con số** (gọi là *tham số*, *weights*) nằm rải trong
các ma trận đó. Chạy model = đưa input qua từng lớp ma trận, mỗi lớp nhân
input với một đống con số rồi cộng lại, ra output của lớp đó, đưa tiếp lớp
sau — giống một pipeline hàm lồng nhau `f = f_n(...f_2(f_1(x)))`, mỗi
`f_i` là một phép nhân ma trận + một hàm phi tuyến nhỏ (để không rút gọn
được thành 1 phép nhân duy nhất).

**Điểm quan trọng nhất cần nhớ:** những con số đó (weights) **không được
lập trình tay**. Chúng do một quá trình gọi là *train* tự động dò ra. Việc
của model không phải "hiểu nghĩa" theo cách người hiểu — nó là một hàm số
được luyện để với input dạng này, ra output dạng kia, dựa trên hàng tỷ ví dụ
đã thấy lúc train (bởi người khác, gọi là *base model*, bạn không tự train
từ đầu — xem mục 1.4).

### 1.2 Input/output không phải là chữ trực tiếp — mà là *token*

Model không đọc từng ký tự hay từng từ tiếng Việt/Anh theo nghĩa thường.
Chữ được cắt thành các mảnh nhỏ gọi là **token** (có thể là cả từ, nửa từ,
hoặc vài ký tự — do một bảng từ điển cố định quyết định, gọi là *tokenizer*).
Ví dụ (minh hoạ, không phải cắt thật): `"12 quả táo"` có thể thành các token
`["12", " quả", " táo"]`. Mỗi token được ánh xạ thành một số nguyên (ID), rồi
số đó được đưa vào model.

Model sinh chữ theo kiểu **từng token một, tự hồi quy** (*autoregressive*):

```
đưa vào: [token1, token2, ..., tokenN]
model dự đoán: xác suất của MỌI token có thể đứng kế tiếp
                (ví dụ 50000 khả năng, mỗi khả năng một xác suất)
chọn 1 token trong đó (cách chọn — xem mục 1.3)
nối token vừa chọn vào cuối chuỗi, lặp lại bước trên
dừng khi model tự sinh ra token "kết thúc" hoặc chạm giới hạn độ dài
```

Nói cách khác: model **không viết cả câu trả lời cùng lúc**. Nó đoán từng
mảnh một, dựa trên tất cả những gì đã đoán trước đó — giống việc gõ auto-
complete trên điện thoại, nhưng chọn từ tiếp theo dựa trên xác suất do model
tính, không phải theo tần suất từ điển đơn giản.

### 1.3 Vì sao chạy model 2 lần trên cùng 1 đề có thể ra 2 kết quả khác nhau

Ở bước "chọn 1 token trong đó" ở trên, có 2 cách:

- **Chọn xác suất cao nhất mỗi lần** (*greedy*, hoặc temperature = 0) → luôn ra
  đúng 1 kết quả cố định, chạy lại bao nhiêu lần cũng giống hệt.
- **Chọn ngẫu nhiên có trọng số theo xác suất** (temperature > 0, ví dụ 0.8) →
  token có xác suất cao thì dễ được chọn hơn, nhưng không chắc chắn — chạy
  lại nhiều lần sẽ ra nhiều câu trả lời khác nhau, dù cùng 1 đề bài.

**Đây là lý do vì sao khái niệm "làm bài k lần" (mục 7) có ý nghĩa**: nếu
model chạy với temperature > 0, cho nó làm k lần trên cùng 1 đề sẽ ra k bài
làm khác nhau (khác cách viết, có khi khác luôn kết quả đúng/sai) — giống
chạy lại một hàm có yếu tố ngẫu nhiên (như `random.choice` có trọng số) nhiều
lần để xem tỉ lệ ra kết quả đúng là bao nhiêu.

### 1.4 Train (huấn luyện) thật sự làm gì — cơ chế, không chỉ ví von

Trước hết, phân biệt 2 việc khác nhau hay bị lẫn:

- **Pretrain** (train từ đầu): tốn hàng triệu đô, cần hàng nghìn GPU, dùng
  hàng nghìn tỷ token văn bản. Đây là việc các công ty lớn (Alibaba/Qwen team,
  OpenAI, Google...) đã làm sẵn. **bạn không làm bước này.**
- **Fine-tuning** (huấn luyện thêm): lấy model đã pretrain sẵn (gọi là *base
  model*), rồi chỉnh thêm một ít trên dữ liệu riêng. Đây là việc bạn làm (mục
  1.5, LoRA).

Cơ chế train, dù pretrain hay fine-tune, đều dựa trên vòng lặp sau — đây là
phần hay bị hiểu mơ hồ nhất, nên viết kỹ:

```
1. Đưa 1 ví dụ vào model: (đề bài, câu trả lời ĐÚNG mong muốn)
2. Model chạy, ra một dự đoán (xác suất cho mỗi token tiếp theo)
3. So dự đoán đó với câu trả lời ĐÚNG → tính ra một con số gọi là LOSS
   (loss càng lớn = model dự đoán càng lệch xa câu trả lời đúng)
4. Tính xem MỖI con số trong 500 triệu weight cần tăng hay giảm bao nhiêu
   để loss ở bước 3 giảm xuống — phép tính này gọi là GRADIENT
   (đạo hàm riêng của loss theo từng weight — không cần bạn tự tính tay,
   thư viện làm tự động, gọi là backpropagation)
5. Chỉnh từng weight một chút theo hướng gradient chỉ (gọi là 1 "bước" train)
6. Lặp lại với ví dụ tiếp theo, hàng nghìn/triệu lần
```

**Ví dụ tối giản hoá cực nhỏ để nắm ý tưởng** (không phải cách model thật
hoạt động, nhưng đúng ý tưởng gradient descent):

Giả sử có hàm `f(x) = w * x`, muốn `f(2) = 6` nhưng chưa biết `w`.

```
Bắt đầu:  w = 1        → f(2) = 2      (đúng ra phải là 6, sai 4)
Bước 1:   tăng w lên một chút theo hướng làm f(2) gần 6 hơn
          w = 1.4      → f(2) = 2.8    (sai còn 3.2)
Bước 2:   w = 1.9       → f(2) = 3.8   (sai còn 2.2)
...
Sau nhiều bước: w hội tụ về 3           → f(2) = 6  (đúng)
```

Train model thật giống hệt ý tưởng này, chỉ khác: không phải 1 số `w`, mà
500 triệu số cùng lúc; không phải 1 ví dụ, mà hàng triệu ví dụ; và bước
"tăng/giảm một chút" (gọi là *learning rate*) phải chọn cẩn thận — quá lớn
thì `w` nhảy loạn không hội tụ, quá nhỏ thì train rất lâu.

**Vậy "model học giỏi hơn" nghĩa chính xác là gì?** Nghĩa là: sau train,
với các đề bài **giống dạng** đã train, model có xu hướng sinh ra câu trả
lời gần với câu trả lời đúng hơn — vì các weight đã được chỉnh để giảm loss
trên đúng kiểu ví dụ đó. Nó **không** đảm bảo model hiểu bản chất toán học —
đây chính là gốc rễ câu hỏi nghiên cứu ở mục 3.

### 1.5 LoRA — vì sao không train lại cả 500 triệu số

Train lại toàn bộ 500 triệu (hoặc 1.5 tỷ với model lớn hơn) số rất tốn — cần
nhiều bộ nhớ GPU để lưu gradient cho từng số. **LoRA** (Low-Rank Adaptation)
là một mẹo:

- Giữ nguyên toàn bộ weight gốc `W` (không đụng vào, đóng băng — *frozen*).
- Với một vài lớp quan trọng, thêm **2 ma trận nhỏ** `A` và `B`, sao cho lúc
  chạy, weight hiệu dụng là `W + A×B`.
- **Chỉ train `A` và `B`** — kích thước nhỏ hơn `W` rất nhiều lần (ví dụ
  `W` là ma trận 1000×1000 = 1 triệu số, còn `A` là 1000×16 và `B` là
  16×1000, cộng lại chỉ 32 nghìn số — con số 16 này gọi là *rank*, viết tắt
  `r`, càng nhỏ càng rẻ nhưng học được ít hơn).

Ví như: `W` là một thư viện lớn không đụng vào (đóng gói, immutable), còn
`A×B` là một lớp decorator/monkey-patch nhỏ đè lên, chỉ patch đúng phần cần
sửa. Rẻ hơn nhiều, chạy được trên GPU yếu (T4 trên Kaggle), và **mỗi vòng
train lại một adapter `A,B` MỚI từ đầu** trên base model gốc (không cộng dồn
qua các vòng) — điều này quan trọng để hiểu đúng cách đo ở mục 7: mỗi vòng
là một lần fine-tune độc lập từ base, không phải fine-tune-lên-fine-tune.

### 1.6 Verifier (máy chấm) hoạt động đúng 3 bước, không phải 1 bước "so y chang"

`math-verify` (thư viện dùng trong đề) làm đúng 3 bước:

```
1. PARSE (trích xuất): tìm và lôi ra đáp án cuối cùng trong bài làm
   (ví dụ tìm trong \boxed{...}, hoặc câu cuối "Vậy đáp án là ...")
   → nếu không tìm ra được gì hợp lệ: coi là parse_empty (lỗi, tính là sai)

2. NORMALIZE (chuẩn hoá): biến đáp án vừa lôi ra và đáp án sách về
   MỘT DẠNG chung để so sánh công bằng hơn — ví dụ hiểu \frac{1}{2}
   và \dfrac{1}{2} là cùng 1 dạng biểu thức toán (dùng thư viện kiểu
   SymPy để "hiểu" biểu thức, không chỉ so chuỗi ký tự thô)

3. COMPARE (so sánh): sau khi chuẩn hoá, so 2 giá trị có bằng nhau không
   → trả True/False
```

**Bug nằm ở bước 1 và 2, không phải bước 3.** Bước 3 (so sánh 2 giá trị đã
chuẩn hoá) gần như luôn đúng. Nhưng bước 1 (không lôi ra được đáp án nếu
viết theo cách lạ) và bước 2 (chuẩn hoá không nhận diện được mọi cách viết
tương đương, ví dụ 1 vài lệnh LaTeX hiếm) là chỗ gây lỗi — kết quả là verifier
**từ chối một bài làm đúng giá trị**, gọi là **false negative (FN)**. Ngược
lại — verifier chấp nhận một bài làm sai — gọi là **false positive (FP)**.
Đo thật trên repo: `math-verify` gần như không có FP, nhưng có FN thật (mục 3).

### 1.7 Reward — chỉ là con số 0/1 từ verifier, dùng để quyết định "giữ lại hay bỏ"

Trong đề này, *reward* đơn giản chỉ là kết quả của verifier: 1 nếu đúng, 0
nếu sai. Reward này **không** được dùng để tính gradient trực tiếp kiểu RL
(đề đã quyết định dùng SFT, không dùng GRPO — xem mục 9 phần "Từ điển"). Nó
chỉ dùng để **lọc** — bài nào reward = 1 thì được giữ lại làm dữ liệu train
cho vòng sau, bài reward = 0 thì bỏ.

---

## 2. Đề tài là gì — ráp các mảnh ở mục 1 lại thành 1 vòng lặp

Giờ ráp lại: một **vòng** (round) trong đề tài này làm đúng các bước sau,
mỗi bước dùng đúng cơ chế đã giải thích ở mục 1:

```
Vòng N:
  (1) GENERATE — với mỗi bài toán, model sinh k lời giải khác nhau
      (dùng cơ chế autoregressive + sampling ở mục 1.2–1.3, k lần độc lập)
       ↓
  (2) VERIFY — với mỗi lời giải, verifier chạy 3 bước ở mục 1.6,
      trả về đúng/sai cho từng lời giải
       ↓
  (3) SELECT — giữ lại các cặp (đề bài, lời giải) mà verifier bảo ĐÚNG
       ↓
  (4) TRAIN — dùng đúng các cặp vừa giữ làm dữ liệu, train một adapter
      LoRA MỚI (mục 1.5) từ base model, theo cơ chế gradient descent
      ở mục 1.4
       ↓
Vòng N+1: model bây giờ dùng adapter mới train ở vòng N, lặp lại (1)-(4)
```

Đây gọi là **self-improving** (tự cải thiện): không cần người ngồi chấm tay
— verifier tự động làm việc chọn lọc đó, rồi model tự học lại từ chính lời
giải nó vừa được chấm đúng. Ý tưởng nghe hợp lý: mỗi vòng chỉ học từ bài
"đúng", nên càng lặp càng giỏi.

**Đề tài của bạn:** *"tin verifier chấm tự động 100% chính xác đó có thật sự
đúng không — và nếu không, hậu quả tích luỹ qua nhiều vòng là gì?"*

### Ví dụ chạy tay — 1 vòng, có số/chữ thật (đơn giản hoá để dễ theo dõi)

Đề bài: *"Lan có 3 túi kẹo, mỗi túi 4 viên. Lan cho bạn 2 viên. Hỏi Lan còn
bao nhiêu viên kẹo?"* — đáp án sách (gold): `10`.

**(1) GENERATE, k = 4** — model sinh 4 lời giải (temperature > 0 nên khác nhau):

| # | Model viết | Đáp án cuối model đưa ra |
|---|---|---|
| 1 | "3×4=12, 12−2=10. Vậy Lan còn \boxed{10} viên." | `10` |
| 2 | "3 túi 4 viên là 12 viên, trừ 2 còn lại **mười** viên." | `"mười"` (chữ, không phải số) |
| 3 | "3×4−2=10.0" | `10.0` |
| 4 | "3×4=12, 12+2=14. Vậy còn \boxed{14} viên." | `14` (sai phép tính) |

**(2) VERIFY** — verifier chạy PARSE → NORMALIZE → COMPARE với gold `10`:

| # | Parse ra được? | Chuẩn hoá về | So với gold `10` | Kết quả |
|---|---|---|---|---|
| 1 | Có (`10`) | `10` | bằng | **Đúng** |
| 2 | Có thể KHÔNG parse ra được số từ chữ `"mười"` | — | — | **Sai (FN — thực ra đúng giá trị!)** |
| 3 | Có (`10.0`) | `10` (chuẩn hoá bỏ số 0 thừa) | bằng | **Đúng** |
| 4 | Có (`14`) | `14` | khác | **Sai (đúng là sai thật)** |

**(3) SELECT** — giữ lại lời giải #1 và #3 (verifier bảo đúng). Lời giải #2
— dù giá trị đúng — **bị loại vì cách viết**, đây chính là hiện tượng ở
mục 3. Lời giải #4 bị loại đúng (nó sai thật).

**(4) TRAIN** — model được fine-tune (LoRA) trên 2 ví dụ vừa giữ (#1, #3) —
cả hai đều thuộc kiểu viết "số Ả Rập + có `\boxed{}`". Không có ví dụ nào
dạy model rằng viết `"mười"` cũng được chấp nhận, vì ví dụ đó đã bị loại
ngay từ vòng này. Lặp lại qua nhiều vòng, model ngày càng ít có lý do viết
theo những kiểu bị loại — đây là mầm mống của câu hỏi nghiên cứu.

---

## 3. Vấn đề bạn nghi ngờ — và vì sao nó giống một bug quen thuộc

Từ ví dụ trên: `math-verify` **không đọc cách làm bài**, chỉ lôi đáp án cuối
rồi so — giống một bài test chỉ `assertEqual` giá trị cuối, không kiểm logic
bên trong. Và bước lôi/chuẩn hoá đó (mục 1.6) **không hoàn hảo**.

Đo thật trên 400 đáp án đúng, viết lại theo nhiều kiểu (Việc 1, xem mục 8):
một số kiểu viết **bị gạch 100% dù đáp án đúng giá trị** (ví dụ toàn bộ các
cách viết dùng lệnh LaTeX `\dfrac`/`\tfrac` thay vì `\frac`). Đây không phải
verifier "chấm sai lung tung" — nó chấm sai **có quy luật**: những bài viết
đúng nhưng "khác văn phong sách" bị loại một cách hệ thống.

**Hậu quả nghi ngờ, ví như bug CI quen thuộc:** nếu test suite của bạn có
một lỗi hệ thống — chỉ pass code viết theo đúng 1 style nhất định, dù logic
đúng hay sai không quan trọng bằng style — thì sau nhiều vòng "chỉ giữ code
pass test, rồi tự động refactor theo code đã pass" (đúng cơ chế bước
SELECT→TRAIN ở mục 2), codebase sẽ dần dần **chỉ còn đúng 1 style đó**,
không phải vì logic tốt hơn, mà vì test chỉ chấp nhận style đó. Nhìn báo cáo
CI thấy "tỷ lệ pass tăng dần qua các release" — tưởng chất lượng tăng, thật
ra chỉ đang hội tụ về style mà test ưa.

**Câu hỏi nghiên cứu, viết lại một câu:**

> Sau nhiều vòng lặp generate → verify → select → train, model đang thật sự
> **giỏi giải toán hơn**, hay chỉ đang học **viết đáp án đúng kiểu verifier
> thích** — và có cách nào phát hiện chuyện đó từ bên trong vòng lặp không?

**Đang focus vào đúng câu hỏi này** — không phải câu rộng hơn ("SLM có tự
cải thiện được qua GVT không", câu đó nhiều người đã trả lời "có" rồi, xem
mục 6). Phần hẹp — verifier lệch-vì-chữ tích lũy qua nhiều vòng — mới là
phần chưa ai đo.

---

## 4. Toàn cảnh: đường đi từ đầu tới cuối, đang đứng ở đâu

Cả dự án (không chỉ vòng lặp GVT ở mục 2) đi qua các chặng sau, theo đúng thứ tự:

```
A. Đọc hiểu đề, dựng khung khái niệm (GVT là gì, đo bằng gì)          ✅ Xong
        ↓
B. Khảo sát tài liệu rộng — tìm xem "khoảng trống" có thật không       ✅ Xong (29 bài, tra lại qua
        ↓                                                                  Semantic Scholar 2026-08-24)
C. Thu hẹp câu hỏi thành 1 câu đo được cụ thể (mục 3)                  ✅ Xong
        ↓
D. Xây công cụ đo NỀN TẢNG trước khi chạy vòng lặp thật:
   - Việc 1: verifier có thật sự chấm sai vì văn phong không?          ✅ Xong
   - Việc 2: bug đó có xảy ra trên bài model THẬT viết không?          ✅ Xong
        ↓
E. Xây code cho vòng lặp thật (generate→verify→select→train),
   2 nhánh: Mac (thử nhỏ, không phải số thật) + Kaggle (GPU, số thật)  ✅ Code xong
        ↓
F. Chạy thử trên Kaggle ở quy mô NHỎ (vài chục bài, 1-2 vòng)          ✅ Xong (2026-08-26 — 20 bài
   để bắt lỗi kỹ thuật (thư viện đổi version, code chưa test thật)         GSM8K, 2 vòng, chạy sạch)
        ↓
   ────────────────  ĐANG ĐỨNG Ở ĐÂY  ────────────────
        ↓
G. Chạy đủ quy mô thật (500 bài, 5 vòng, 2 cỡ model 0.5B/1.5B)         ⬜ Chưa làm — BƯỚC KẾ TIẾP
   → đây là bước duy nhất tạo ra SỐ LIỆU THẬT cho bài báo
        ↓
H. Đọc bảng số (pass@1, pass@k, văn phong) — xác nhận hay bác bỏ       ⬜ Chưa làm
   nghi ngờ ở mục 3
        ↓
I. Viết bài báo, so sánh rõ với 2 bài gần nhất (ReST-EM,               ⬜ Chưa làm
   Teacher-Free Self-Training — xem mục 6)
        ↓
J. Nộp — cần biết yêu cầu thầy trước (deadline, định dạng)             ⬜ Chưa hỏi, xem CAU-HOI-THAY.md
```

**Lưu ý quan trọng về chữ "Xong" ở A–E:** "Xong" ở đây nghĩa là **đã chạy
xong và có số/code**, KHÔNG có nghĩa là "bạn đã thuộc lòng, giải thích vo
được". Nếu đọc xong mục 1–3 vẫn còn chỗ mơ hồ, đó là bình thường — dùng
mục 12 (tự kiểm tra) để lộ ra đúng chỗ còn hổng, rồi quay lại đọc kỹ đoạn
tương ứng, đừng chỉ tin vào chữ "✅ Xong" trong bảng.

**Tóm một câu vị trí hiện tại:** hạ tầng đo (A–E) đã xong toàn bộ, kể cả code
chạy thật trên Kaggle — nhưng **chưa bấm nút chạy lần nào**, nên chưa có một
con số thật nào để đưa vào bài báo. Việc tiếp theo bắt buộc là chạy, không
phải viết thêm code hay đọc thêm bài.

---

## 5. Cách giải quyết này tác động gì — so với không có nó

Nếu **không** đo tách riêng pass@1 / pass@k / văn phong (tức là chỉ làm như
đa số bài GVT/self-training vẫn làm — chỉ nhìn pass@1 tăng là kết luận "model
giỏi hơn"):

| Không có phát hiện này | Có phát hiện này (phần bạn thêm vào) |
|---|---|
| Chỉ nhìn pass@1 tăng qua các vòng → kết luận "model tự cải thiện thành công" | Nhìn thêm pass@k + văn phong → phân biệt được "giỏi thật" (pass@k cũng tăng, văn phong đa dạng) với "học viết đúng kiểu verifier thích" (pass@1 tăng nhưng pass@k đứng, văn phong tụ về 1 kiểu) |
| Sai lệch của verifier âm thầm tích lũy qua nhiều vòng, không ai phát hiện vì không ai đo lại bằng gold data mỗi vòng | Phát hiện được **ngay trong vòng lặp**, không cần thêm nhãn người mỗi vòng (chỉ cần đo pass@k + văn phong, hai thứ tự sinh ra từ chính quá trình generate) |
| Rủi ro: công bố "model tự cải thiện qua self-training" nhưng cải thiện đó chỉ là ảo — model không thật sự giỏi hơn, chỉ giỏi "lách" đúng cách verifier chấm | Biết rõ giới hạn thật của các pipeline kiểu GVT khi verifier không hoàn hảo — mà trong thực tế, verifier luật (rule-based) như `math-verify` **luôn** không hoàn hảo (xem Việc 1, 2) |
| Cách đo bị coi là chỉ đúng cho đúng 1 thí nghiệm | Cách đo (bộ 3 con số) tổng quát hoá được cho **bất kỳ** pipeline self-training nào dùng verifier luật, không riêng đề toán này |

Nói ngắn: nếu không làm phần này, một pipeline GVT có thể "báo cáo thành
công" (số pass@1 đẹp) trong khi thực chất không cải thiện khả năng giải toán
— và không ai biết, vì không ai đo pass@k + văn phong song song. Phần đóng
góp của bạn là **cách phát hiện sớm** hiện tượng đó, dùng được ngay trong lúc
train, không cần chờ đánh giá cuối cùng bằng tập test riêng.

---

## 6. Vì sao đáng làm — đã có ai làm chưa

Đã khảo sát 29 bài báo liên quan (xem `papers/KHAO-SAT.md` — mỗi bài đều tra
lại thật qua arXiv/Semantic Scholar, không đoán từ trí nhớ; đã tra chéo lại
lần 2 qua Semantic Scholar ngày 2026-08-24, khớp 100%). Kết luận:

- **Có người đã chỉ ra** verifier tự động hay chấm sai (giống bug ở mục 3) — nhưng họ chỉ đo trong **một vòng** train, không lặp nhiều vòng. (`From Accuracy to Robustness`, arXiv 2505.22203)
- **Có người đã chạy đúng vòng lặp nhiều lần** (gọi là ReST-EM, arXiv 2312.06585, giống hệt sơ đồ ở mục 2) trên đúng bộ đề toán này — nhưng họ không hề để ý tới việc verifier có thể chỉ chấp nhận một kiểu viết, không đo xem cách viết của model có "hội tụ" theo thời gian không.
- **Có người đo hiện tượng gần giống** ("model học xong tệ hơn khi thử nhiều lần" — tương tự nghi ngờ ở mục 3, đo đúng cặp pass@8/pass@64 qua nhiều vòng) nhưng trên verifier **hoàn hảo** (không có bug chấm-sai-vì-văn-phong). (`Teacher-Free Self-Training Amplifies but Does Not Compound`, arXiv 2606.07856)

**Chưa ai ghép đủ 3 mảnh:** (verifier có bug chấm-sai-vì-văn-phong) + (lặp
nhiều vòng, không phải 1 lần) + (đo xem văn phong đầu ra có hội tụ theo thời
gian không). Đó là phần bạn làm.

Hai bài trên (ReST-EM, Teacher-Free Self-Training) là **hai bài gần nhất**,
đọc kỹ hai bài này trước khi viết bài báo để biết chính xác cần nói khác họ
chỗ nào (xem bước 2 ở mục 9).

---

## 7. Đo bằng cách nào — 3 con số, có ví dụ số thật

Với mỗi bài toán, cho model làm **k lần** (ví dụ k=8, giống chạy lại cùng
một test 8 lần vì nó hơi flaky — lý do vì sao chạy lại ra khác nhau, xem
mục 1.3).

| Con số | Ý nghĩa | Ví như |
|---|---|---|
| **pass@1** | Làm 1 lần, verifier chấp nhận bao nhiêu % | Chạy test đúng 1 lần, tỉ lệ pass ngay lần đầu |
| **pass@k** | Làm k lần, **ít nhất 1 lần** verifier chấp nhận | Cho retry k lần, tỉ lệ có ít nhất 1 lần pass |
| **Văn phong đầu ra** | Đếm model hay dùng kiểu viết nào (`\boxed{}`, phân số, thập phân...) qua từng vòng | Đếm style code (tabs vs spaces, kiểu đặt tên biến...) qua từng release |

### Ví dụ số thật, tính tay

Giả sử có 5 bài toán, mỗi bài cho model làm k=4 lần, bảng đúng(1)/sai(0):

| Bài | Lần 1 | Lần 2 | Lần 3 | Lần 4 | Có ít nhất 1 đúng? |
|---|---|---|---|---|---|
| 1 | 1 | 0 | 1 | 0 | Có |
| 2 | 0 | 0 | 0 | 0 | Không |
| 3 | 1 | 1 | 1 | 1 | Có |
| 4 | 0 | 1 | 0 | 0 | Có |
| 5 | 0 | 0 | 0 | 1 | Có |

- **pass@1** (chỉ tính Lần 1 của mỗi bài): đúng ở bài 1, 3 → `2/5 = 40%`
- **pass@4** (= pass@k với k=4, tính "có ít nhất 1 đúng"): đúng ở bài 1,3,4,5 → `4/5 = 80%`

Nhận xét: pass@k luôn ≥ pass@1 (càng cho thử nhiều càng dễ trúng ít nhất 1
lần). Điều đáng quan tâm không phải bản thân 2 số này, mà là **chúng đổi
thế nào qua nhiều vòng train**:

**Cách đọc kết quả (bảng chân lý rút gọn):**

| pass@1 | pass@k | Văn phong | Kết luận |
|---|---|---|---|
| Tăng | Tăng | Đa dạng | Có thể đang giỏi thật (chưa chắc, cần xem thêm) |
| Tăng | Đứng/giảm | Tụ về 1 kiểu | **Manh mối mạnh: đang học viết chữ, không học toán** |
| Tăng | — | Chưa tụ | Chưa đủ bằng chứng, có thể chỉ ổn định hơn |

`pass@k` giống việc bạn cho code chạy lại nhiều lần: nếu chỉ pass thêm khi
chạy 1 lần đầu tiên nhưng cho retry thoải mái thì tỉ lệ pass không đổi —
nghĩa là code không "học được gì mới", chỉ đang **chắc chắn hơn ở đúng 1
cách làm cũ**, không mở rộng khả năng.

---

## 8. Trạng thái hiện tại trong repo (tính tới 2026-08-26)

| Việc | Trạng thái |
|---|---|
| Việc 1 — đo verifier chấm sai kiểu viết nào (200 GSM8K + 200 MATH) | **Xong**, có bảng số |
| Việc 2 — đo trên bài model thật đã viết sẵn (không phải bạn tự đặt) | **Xong** — GSM8K gần như không sai, MATH sai oan ~7.8% |
| Việc 3 — code cho vòng lặp thật (generate→verify→select→train) | Code xong, **đã xác nhận chạy sạch thật trên Kaggle** (2026-08-26, 20 bài GSM8K, 2 vòng — xem `experiments/viec3/KAGGLE.md`), gặp 3 lỗi lệch version thư viện và đã sửa cả 3 |
| Khảo sát bài báo (29 bài, xác nhận "chưa ai làm") | **Xong**, xác nhận lại 2 lần (WebSearch/WebFetch + Semantic Scholar), xem `papers/KHAO-SAT.md` |
| Chạy Kaggle quy mô nhỏ (bắt lỗi) | **Xong** (2026-08-26) |
| Chạy Kaggle full lấy số paper (500 bài, 5 vòng, 2 cỡ model) | **Chưa làm — bước kế tiếp** |
| Viết bài báo | **Chưa bắt đầu** |
| Hỏi thầy về hạn nộp / yêu cầu | **Chưa điền** — xem `CAU-HOI-THAY.md` |

---

## 9. Việc cần làm tiếp, theo thứ tự — và tại sao đúng thứ tự này

1. **Điền `CAU-HOI-THAY.md`** (hạn nộp, có bắt buộc phải mới hay được reproduce, sản phẩm nộp là gì, Kaggle có được tính không).
   *Tại sao trước tiên:* mọi bước sau (viết bài kiểu gì, cần bao nhiêu số, deadline chạy Kaggle) đều phụ thuộc câu trả lời của thầy. Hỏi trước để không tốn công làm sai hướng — chi phí hỏi gần như 0, chi phí làm sai hướng rất cao.

2. **Đọc kỹ 2 bài đụng gần nhất**: ReST-EM (2312.06585) và Teacher-Free Self-Training Amplifies but Does Not Compound (2606.07856).
   *Tại sao:* lần trước thầy nói hướng trình bày "chưa đúng" — rủi ro lớn nhất là không phân biệt rõ được với 2 bài này khi bị hỏi trực tiếp "khác gì bài X". Đọc kỹ để trả lời chính xác, không chung chung.

3. ~~Chạy thử trên Kaggle ở quy mô nhỏ trước~~ — **Xong (2026-08-26)**: 20 bài GSM8K, 2 vòng, chạy sạch sau khi sửa 3 lỗi lệch phiên bản thư viện (chi tiết `experiments/viec3/KAGGLE.md`).

4. **Chạy đủ quy mô thật** (500 bài, 5 vòng, 2 cỡ model 0.5B và 1.5B, GSM8K+MATH) — dùng đúng lệnh Ô 3 trong `experiments/viec3/KAGGLE.md`.
   *Tại sao:* đây là bước DUY NHẤT tạo ra số liệu thật. Không có bước này, mọi phần khác (bảng mục 7, kết luận mục 5) chỉ là giả thuyết, chưa kiểm chứng được.

5. **Viết bài báo** dựa trên số đo được, đối chiếu rõ với ReST-EM và Teacher-Free Self-Training.
   *Tại sao đặt cuối:* chỉ viết được sau khi có số thật (bước 4) và biết chính xác cần nói khác gì 2 bài kia (bước 2) — viết trước khi có số là viết theo giả thuyết, dễ phải sửa lại toàn bộ.

**Việc còn treo song song, chưa cần chặn tiến độ:** vẫn chưa chốt có thêm một
hướng mở rộng nào (ví dụ: phát hiện lệch mà không cần gold label giữa vòng,
hoặc so sánh mức độ lệch giữa model 0.5B và 1.5B) — quyết định này có thể để
sau khi có số thật từ bước 4, lúc đó sẽ rõ hướng nào đáng làm thêm hơn.

---

## 10. Từ điển tra nhanh

| Chữ hay gặp | Nghĩa | Không phải |
|---|---|---|
| SLM | Small Language Model — model nhỏ (0.5B, 1.5B tham số) | Không phải "model nhỏ về mặt code", là ít tham số hơn model to (7B, 70B...) |
| Token | Mảnh chữ nhỏ (cả từ/nửa từ) model thực sự xử lý, xem mục 1.2 | Không phải 1 ký tự, không phải luôn là 1 từ |
| Weight / tham số | 1 con số bên trong model, được train tự động dò ra (mục 1.1) | Không phải code người viết tay |
| Loss | Con số đo model dự đoán sai bao nhiêu so với đáp án đúng lúc train (mục 1.4) | Không phải điểm số cuối cùng của model khi dùng thật |
| Gradient descent | Cách tự động chỉnh weight để loss giảm dần (mục 1.4) | Không phải thuật toán tìm kiếm brute-force |
| Gold | Đáp án đúng trong sách/dataset | Không phải bài model tự viết |
| FN (false negative) | Verifier gạch nhầm — bài đúng mà bảo sai | Ngược với FP |
| FP (false positive) | Verifier khen nhầm — bài sai mà bảo đúng | `math-verify` gần như không mắc lỗi này, chỉ mắc FN |
| GRPO | Một thuật toán RL để train model theo reward — đề này **không dùng** GRPO (xem quyết định trong `HUONG-DAN.md`), dùng SFT (học đơn giản hơn) | — |
| SFT | Supervised Fine-Tuning — cách train đơn giản nhất: đưa đúng (đề, lời giải đúng) rồi dạy model lặp lại kiểu đó | Không phải RL — không cần công thức reward phức tạp |
| RLVR | Reinforcement Learning with Verifiable Rewards — nhóm kỹ thuật dùng verifier tự động làm reward để train bằng RL | Đề bạn liên quan tới nhóm này nhưng dùng SFT, không phải RL thuần |
| k | Số lần cho model làm lại cùng 1 đề (không phải số dạng đề khác nhau) | — |
| Temperature | Con số điều khiển model chọn token ngẫu nhiên hay luôn chọn xác suất cao nhất (mục 1.3) | Không liên quan tới nhiệt độ phần cứng |

---

## 11. Nếu vẫn rối, chỉ nhớ 3 dòng

1. Có máy giải toán (model) và máy chấm tự động (verifier) — máy chấm có bug: hay chấm sai bài đúng vì viết khác kiểu sách.
2. Người ta lặp vòng: máy giải → máy chấm giữ bài đúng → dạy lại máy giải bằng đúng bài đó → lặp — tưởng máy ngày càng giỏi toán.
3. Bạn đo: cái bug chấm sai đó lặp nhiều vòng có làm máy giải chỉ giỏi "viết đúng kiểu máy chấm thích" thay vì giỏi toán thật không — và đây là góc **chưa ai đo** (đã tra 29 bài để chắc). Hạ tầng đo xong hết rồi, **chỉ còn thiếu bước bấm nút chạy trên Kaggle để lấy số thật**.

---

## 12. Tự kiểm tra — trả lời được hết thì coi như hết lủng

Trả lời (nói to hoặc viết ra) trước khi xem đáp án bên dưới mỗi câu.

**Câu 1.** Model 0.5B nghĩa là gì — "0.5B" đếm cái gì?
> *Đáp:* Đếm số **weight** (tham số) bên trong model — khoảng 500 triệu con số, không liên quan tới "0.5 tỷ dòng code" hay dung lượng ổ đĩa.

**Câu 2.** Vì sao cho model làm cùng 1 đề 2 lần có thể ra 2 câu trả lời khác nhau?
> *Đáp:* Vì model sinh từng token bằng cách **lấy mẫu ngẫu nhiên có trọng số** theo xác suất (temperature > 0), không phải luôn chọn token xác suất cao nhất — xem mục 1.3.

**Câu 3.** "Train" model nghĩa chính xác là làm gì với các con số bên trong nó?
> *Đáp:* Tính loss (model sai bao nhiêu so với đáp án đúng), rồi dùng gradient để biết mỗi weight cần tăng/giảm bao nhiêu để loss giảm, rồi chỉnh weight một chút theo hướng đó — lặp lại nhiều lần (mục 1.4). Không phải "nhồi dữ liệu vào cho model nhớ".

**Câu 4.** LoRA tiết kiệm ở chỗ nào so với train lại toàn bộ model?
> *Đáp:* Giữ nguyên (đóng băng) weight gốc `W`, chỉ train 2 ma trận nhỏ `A`, `B` (số lượng tham số ít hơn `W` rất nhiều) rồi cộng `W + A×B` lúc chạy — mục 1.5.

**Câu 5.** Verifier `math-verify` có đúng 3 bước, kể tên và bug nằm ở bước nào?
> *Đáp:* PARSE (lôi đáp án ra) → NORMALIZE (chuẩn hoá về 1 dạng) → COMPARE (so sánh). Bug (gây FN) nằm ở bước PARSE và NORMALIZE, không phải bước COMPARE — mục 1.6.

**Câu 6.** FN và FP khác nhau ở đâu — verifier trong đề mắc lỗi nào nhiều hơn?
> *Đáp:* FN = verifier từ chối một bài **đúng thật** (chấm sai theo hướng khắt khe). FP = verifier chấp nhận một bài **sai thật**. `math-verify` gần như không có FP, nhưng có FN thật (đo được ở Việc 1, 2).

**Câu 7.** pass@1 và pass@k khác nhau ở đâu — pass@k luôn ≥ hay ≤ pass@1?
> *Đáp:* pass@1 = đúng ngay lần thử đầu tiên. pass@k = đúng ít nhất 1 trong k lần thử. pass@k luôn **≥** pass@1 (thử nhiều lần dễ trúng hơn thử 1 lần) — mục 7.

**Câu 8.** Nếu pass@1 tăng qua các vòng nhưng pass@k đứng yên và văn phong tụ về 1 kiểu, kết luận gì?
> *Đáp:* Manh mối mạnh cho thấy model đang học "viết đúng kiểu verifier thích" chứ không phải học giỏi toán hơn thật sự — vì nếu giỏi thật, pass@k (khả năng ra được đáp án đúng khi có nhiều cơ hội thử) cũng phải tăng theo — mục 7.

**Câu 9.** Vì sao mỗi vòng train lại LoRA "từ base model", không phải "từ adapter vòng trước"?
> *Đáp:* Để mỗi vòng là một fine-tune độc lập, chỉ chịu ảnh hưởng của đúng dữ liệu được chọn ở vòng đó — giữ đúng thiết kế thí nghiệm, tránh hiệu ứng cộng dồn không kiểm soát được giữa các vòng làm khó tách bạch nguyên nhân (mục 1.5).

**Câu 10.** Đề tài này khác câu hỏi rộng "SLM có tự cải thiện qua GVT được không" ở chỗ nào?
> *Đáp:* Câu rộng đã được nhiều bài trả lời "có" rồi (STaR, ReST-EM...). Đề tài của bạn hẹp hơn: giả sử GVT chạy được, thì việc verifier lệch-vì-chữ có làm cho sự "cải thiện" đó là ảo (chỉ học văn phong) hay không — và đo bằng cách nào để phát hiện ngay trong vòng lặp, không cần nhãn người thêm (mục 3, 5).

Nếu có câu nào trả lời còn ấp úng — quay lại đọc đúng mục được trích trong
đáp án, đừng đọc lại từ đầu cả file.

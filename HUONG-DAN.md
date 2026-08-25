# Hướng dẫn repo — cho người chưa biết lập trình

Mỗi khái niệm: **ví dụ trước**, rồi mới “là gì / làm gì / vì sao / cách khác”.

- `TOI-HIEU.md` = đề tài.
- File này = hiểu từng thứ bằng ví dụ.

Đổi code hoặc chạy thí nghiệm → sửa **Đã làm / chưa làm** và **Nhật ký**.

**Bài mẫu dùng xuyên file** (nhớ 2 bài này là đủ):

- **Bài táo:** sách ghi đáp án `10`. (3 hộp × 4 quả − 2 = 10.)
- **Bài nửa:** sách ghi `1/2`.

---

# Phần A — Chuyện

## A1. Hai nhân vật

**Ví dụ.** Học sinh viết:

```
3 × 4 = 12
12 − 2 = 10
\boxed{10}
```

Cô **không đọc** hai dòng phép. Chỉ lấy `10` trong khung, so với sách `10`. Chịu.

Nếu học sinh làm đúng phép nhưng khoanh `10.0` hoặc viết dài `The answer is 10`, cô có thể gạch — tùy máy chấm.

**Là gì.** Học sinh = model (viết bài). Cô = `math-verify` (chỉ so chỗ khoanh với sách).

## A2. Vòng GVT

**Ví dụ một khóa.**

1. Generate: học sinh nộp 8 bài (cùng đề táo, chữ khác nhau).
2. Verify: cô chịu 3 bài khoanh `10`, gạch 5 bài (sai toán hoặc chữ cô không ưa).
3. Select: chỉ giữ 3 bài chịu.
4. Train: học sinh ôn 3 bài đó.
5. Khóa sau: hay khoanh đúng kiểu cô hơn.

Người ta gọi đó là tự tiến bộ, không cần người chấm bài mới.

## A3. Câu paper

**Ví dụ.** Sau 5 khóa, lần nộp đầu cô cho 70 điểm (trước 40).

- Làm bài khá hơn = đề táo **trước không làm được**, giờ làm được (bước đúng).
- Hợp cô hơn = vẫn chỉ những đề cũ, nhưng lần đầu hay viết `\boxed{10}` đúng kiểu cô.

Paper lấy số để xem nghi nhánh nào. Không thay cô.

## A4. Tuần này = việc 1

**Ví dụ.** Không gọi học sinh. Lấy sách `1/2`, tự viết `\dfrac{1}{2}`, đưa cô. Nếu gạch → phạt chữ (vì ta biết số đúng).

Làm vậy hàng trăm đáp án × nhiều kiểu chữ → bảng. MATH ít gạch vì chữ → đề yếu, dừng.

Bảng đủ 200+200 (2026-08-16): MATH **có** gạch vì chữ (`\dfrac` 146/146 `parse_empty`). **Đi việc 2.** Số nằm `results/viec1/`, quyết định `results/viec1/decision.md`. Smoke 20 bài cũ: `results/viec1/smoke-limit20/`.

---

# Phần B

Mục lục: [B1 cô](#b1-math-verify) · [B2 parse](#b2-parse-và-verify) · [B3 preset](#b3-preset) · [B4 gold](#b4-gold) · [B5 model](#b5-model) · [B6 bộ đề](#b6-gsm8k-và-math-500) · [B7 chữ](#b7-latex-và-kiểu-khoanh) · [B8 nhãn](#b8-gạch-nhầm) · [B9 python](#b9-python) · [B10 file](#b10-jsonl-cli-manifest) · [B11 gvt](#b11-gvt) · [B12 pass](#b12-pass1-passk) · [B13 test](#b13-test-và-stub)

---

## B1. math-verify

**Ví dụ.** Trên máy có chương trình đã cài, không cửa sổ. Ta đưa:

- chữ 1 (sách): `1/2`
- chữ 2 (ta viết): `0.5`

Người biết cùng một nửa. Chương trình trả chịu hoặc gạch (hoặc “không đọc được”).

Đưa `\dfrac{1}{2}` — trên 20 bài GSM8K thử, cô **không đọc được** → gạch cả 20. Không phải 20 bài sai toán.

**Là gì.** Máy chấm tự động. Tên gói `math-verify` 0.9.0 trong `.venv`. Không chat, không viết bài, không phải học sinh.

**Làm gì.** Lôi số khỏi câu → đổi sang dạng so được → so với sách.

**Vì sao.** Vòng GVT ngoài đời dùng đúng máy này. Đề đo máy đó, không chế máy mới.

**Cách khác — ví dụ cùng `1/2` vs `0.5`**

| Cách | Kết quả ví dụ | Ta? |
|------|----------------|-----|
| `math-verify` | Có thể chịu hoặc gạch — **đó là số ta đo** | Có |
| So khớp chữ | `"1/2"=="0.5"` → sai ngay | Không |
| Người | “Cùng một nửa, cho điểm” | Việc 2, không train |
| ChatGPT chấm | Có thể cho điểm, lần sau khác | Không |
| TinyV (sửa cô) | Cô mới ít gạch `\dfrac` | Cấm — đổi đề |
| Tự so SymPy | Mình viết máy chấm khác | Lệch đề |

https://github.com/huggingface/Math-Verify

---

## B2. Parse và verify

Hai bước **của cùng một máy chấm**. Không phải hai máy.

Giống cô chấm: **(1) tìm chỗ khoanh trên tờ** rồi **(2) so với sách**.  
Parse = bước 1. Verify = bước 2.

### Parse — tìm chỗ khoanh

Cô **không đọc hiểu** bài. Cô **soi tờ**, tìm cụm chữ trông giống đáp án, theo thứ tự ưu tiên (từ trên xuống, cái nào có thì lấy, hết thì thử cái dưới).

Tờ bài táo:

```
3 hộp, mỗi hộp 4 quả: 3 × 4 = 12
Ăn 2 quả: 12 − 2 = 10
```

Trên tờ có nhiều số: `3`, `4`, `12`, `2`, `10`. Cô phải **chọn một**. Cách chọn (giản lược, đúng tinh thần `math-verify`):

| Ưu tiên | Cô tìm gì trên tờ | Ví dụ lôi ra |
|---------|-------------------|--------------|
| 1 | Có `\boxed{...}` không? | `\boxed{10}` → lấy `10` |
| 2 | Có câu neo không? “The answer is…”, “final answer” | `The answer is 10` → lấy `10` |
| 3 | Có toán trong `$...$` hoặc `\frac{...}` không? | `$\frac{1}{2}$` → lấy một nửa |
| 4 | Không có mốc trên → hay lấy **số / công thức gần cuối tờ** | Dòng cuối `12 − 2 = 10` → hay lấy `10` |

**Ví dụ A — có khung, dễ.**

```
... 12 − 2 = 10
\boxed{10}
```

Cô thấy khung → lấy `10`. Các số `3`, `4`, `12` bị bỏ. Đây là lý do người ta bắt model viết `\boxed{}`.

**Ví dụ B — có câu neo.**

```
... 12 − 2 = 10
The answer is 10
```

Cô thấy “The answer is” → lấy `10`.

**Ví dụ C — không khung, không câu.**

```
3 × 4 = 12
12 − 2 = 10
```

Cô không thấy mốc → hay lấy số **cuối**. May thì `10`. Không may (bài dài, số cuối không phải đáp án) → lôi nhầm. Bài giảng gọi lỗi này: **lôi nhầm số**. Khác lỗi “viết `\dfrac` không đọc được”.

**Ví dụ D — việc 1 (tờ rất ngắn).**

Việc 1 không đưa cả trang lời. Chỉ đưa **một chuỗi ta viết sẵn**, ví dụ `0.5` hoặc `\dfrac{1}{2}`.

- `0.5` → không cần tìm trong bài dài; cả tờ chỉ có `0.5` → parse ra một nửa (nếu cô hiểu thập phân).
- `\dfrac{1}{2}` → cô **tìm thấy** cụm LaTeX đó nhưng **không hiểu lệnh** `\dfrac` → coi như không lôi ra được → `parse_empty`.

“Tìm chỗ khoanh” gồm hai việc nhỏ: **chọn cụm chữ nào trên tờ**, rồi **đọc cụm đó thành số**. Fail việc 2 cũng gọi là parse thất bại.

**Ví dụ 1 — tìm được.** `The answer is \frac{1}{2}` → chọn cụm sau câu neo, đọc được một nửa.

**Ví dụ 2 — không đọc được cụm.** `\dfrac{1}{2}` → có cụm, không đọc được lệnh → `parse_empty`. Chưa so sách.

### Verify — so với sách

Chỉ chạy khi **cả sách lẫn bài đều parse được**.

**Ví dụ 3 — chịu.**  
Sách parse ra: một nửa. Bài `0.5` parse ra: một nửa. Verify: cùng giá trị → chịu.

**Ví dụ 4 — gạch vì không bằng.**  
Sách: `10`. Bài: `11`. Cả hai đọc được. Verify: khác nhau → gạch, nhãn `compare_false`.

**Ví dụ 5 — không tới bước so.**  
Bài `\dfrac{1}{2}` parse rỗng. Verify **không chạy**. Đã gạch ở parse.

### Một đường

```
sách "1/2"  --parse-->  (một nửa)
bài  "0.5"  --parse-->  (một nửa)
                         \  /
                       verify → chịu
```

```
sách "1/2"     --parse-->  (một nửa)
bài  "\dfrac{1/2}" --parse-->  (rỗng)  → dừng, gạch parse_empty
```

**Vì sao tách hai bước.** Cùng là gạch, lý do khác:

| Gạch lúc | Ví dụ | Nghĩa |
|----------|--------|--------|
| Parse | `\dfrac` | Cô không đọc được chữ |
| Verify | `1/3` vs `0.33` | Cô đọc được, bảo không bằng |

Việc 1 cần tách hai cái đó. Chỉ ghi “sai” thì không biết cô phạt chữ hay phạt giá trị.

**Thứ tự.** Luôn so `verify(sách, bài)`. Đổi chỗ hai đối số có thể ra khác.

**Cách khác.** So nguyên câu `"The answer is 1/2"` với `"1/2"` → luôn gạch, dù số đúng — vì không có bước parse (lôi số ra).

---

## B3. Preset

Preset = **bộ cài đặt có sẵn** trên cùng máy `math-verify` (như camera: Chân dung / Ban đêm). Hai bộ:

- **`default`** = lúc mới cài máy, **rộng** hơn.
- **`reward`** = bộ tác giả máy khuyên khi điểm cô dùng để **dạy máy**, **chặt** hơn. Tên “reward” = thưởng trong tài liệu, không phải cô khác.

Công tắc chỉ đổi lúc đọc **tờ học sinh**. Sách luôn đọc `default`.

---

### Vì sao máy chấm có hai bộ (không phải ta bịa)

Người viết `math-verify` tách hai việc khác nhau:

**1. Chấm để biết học sinh giỏi toán không** (`default`)  
Muốn rộng: `\frac`, `$...$`, câu chữ… vẫn lôi được số. Chữ hơi xấu thì **sửa giúp**.  
Nếu keo quá, điểm thấp vì **chữ**, tưởng học sinh dốt toán.

**2. Chấm để chọn bài được ôn / làm điểm thưởng lúc train** (`reward`)  
Nếu rộng, học sinh viết lung tung vẫn được “đúng” → ôn toàn bài chữ bẩn → càng viết bẩn.  
Nên chặt: ưu tiên `\boxed{}`, **không** sửa giúp LaTeX xấu. Học sinh muốn được ôn thì phải viết đúng kiểu máy ưa.

Cùng một tờ có thể: default chịu, reward gạch. Đó là chủ ý, không phải lỗi.

---

### Vì sao **việc 1 của ta** chạy cả hai

Việc 3 (GVT) lọc bài được ôn bằng bộ **chặt** (`reward`) — đúng lúc “dạy máy”.

Nếu việc 1 **chỉ default:** bảng mô tả cô buổi kiểm tra rộng. Học sinh thực ra ôn với cô chặt. Số việc 1 **không khớp** việc 3.

Nếu việc 1 **chỉ reward:** biết cô lúc học, **không biết** cô rộng gạch ít hơn bao nhiêu. Paper cần: “phạt chữ là do máy vốn vậy, hay chỉ lúc bật chế độ dạy?” Hai cột trả lời được.

Nên mỗi kiểu chữ trên bảng = **hai hàng**. Không chọn một rồi bỏ cái kia.

**Ví dụ đọc bảng.** Kiểu `\dfrac`: cả hai 20/20 gạch → máy **vốn** không đọc lệnh đó, không phải chỉ nút chặt.  
Nếu sau này MATH: default 2% gạch, reward 12% → lúc dạy máy phạt chữ **nặng hơn** lúc chấm thường — đúng chỗ đề nghi “hợp cô lúc ôn”.

Trên 20 bài GSM8K dễ, hai bộ có thể ra giống. Vẫn chạy đủ hai. Đừng kết luận “như nhau” trước khi có MATH.

---

## B4. Gold

**Ví dụ GSM8K.** File gốc một bài:

```
Natalia ... #### 18
```

Gold việc 1 = `18` (sau `####`). Bỏ hết lời.

**Ví dụ việc 1.** Gold `18` → ta tạo `18.0`, `\boxed{18}`… đưa cô. Không gọi học sinh.

**Ví dụ nếu dùng bài model.** Model viết phép sai ra `17` nhưng `\boxed{17}` đẹp. Cô gạch. Không biết vì sai toán hay vì chữ. Gold `18` đổi thành `18.0` thì biết: nếu gạch là vì chữ.

**Là gì.** Đáp án cuối sách. Prediction việc 1 = gold đổi chữ.

**Cách khác.** Bài model (việc 2). Bịa 5 số (chỉ đủ test ống).

---

## B5. Model

**Ví dụ việc 3 (Mac).** Đưa đề táo. Qwen 0.5B in ra một bài (thường ngắn, hay sai). Đó là generate. Cô chấm; bài chịu thì ôn LoRA. Mac chỉ thử ống, không lấy số paper.

**Ví dụ việc 1.** Không có bước này. Chỉ có sách + đổi chữ + cô.

**Là gì.** Chương trình viết chữ. SLM = nhỏ (Qwen). LLM = lớn (GPT). Việc 1 không chạy; việc 3 mới gọi.

**Cách khác.** GPT-4 (không phải đề). Người viết (không self-improve).

---

## B6. GSM8K và MATH-500

**Ví dụ GSM8K.** “Natalia bán kẹp… còn bao nhiêu?” Đáp án `18`. Ít phân số → ít bẫy `\dfrac`. Smoke 20 bài: hầu hết kiểu 0% gạch, trừ `\dfrac`/`\tfrac`.

**Ví dụ MATH-500.** Đáp án sách `\dfrac{1}{2}` hoặc `\sqrt{2}`. Cùng giá trị viết `\frac{1}{2}` / `0.5` dễ làm cô lệch. **Bảng MATH mới quyết định đề sống.**

**Là gì.** Hai tủ đề có sẵn, có đáp án sách. Không phải tệp mình nhồi để học thuộc.

**Vì sao hai bộ.** GSM8K = đối chứng dễ. MATH = chỗ đề sống/chết. Paper toán hay dùng họ này.

**Cách khác.** Chỉ GSM8K → dễ tưởng đề chết. AIME → lệch checklist. Tự soạn 10 đề → không ai tin.

**Tải.** Ta dùng link JSONL (`urllib`). Không cài thêm `datasets`. Ví dụ: lần đầu chạy, máy tải `gsm8k_test.jsonl` vào `data/gold/`, lần sau dùng file đó.

---

## B7. Kiểu khoanh (variant) — và LaTeX / `\boxed{}`

Việc 1: lấy **một gold**, **copy thành nhiều chuỗi chữ khác nhau**, mỗi chuỗi đưa cô một lần.

Gold bài vịt = `18`. Ta không gọi model. Ta tự viết:

```
18
18.0
\boxed{18}
$18$
The answer is 18
```

Cùng là mười tám. Cô chịu hay gạch **từng chuỗi** — đó là B7.

**Variant / kiểu khoanh** = một cách copy đó. List cố định (mục 6 bài giảng), không phải MATH-500 tạo ra.

**LaTeX** = cách **gõ toán** trên máy. Giấy vẽ phân số; máy gõ `\frac{1}{2}`.  
`\dfrac` / `\tfrac` = **cùng một nửa**, lệnh khác. Người coi như nhau; cô có thể chỉ đọc được `\frac` → gạch `\dfrac`.

**`\boxed{18}`** = gõ cho ra số trong **hộp** (khoanh đáp án). Đã nói ở preset.

Gold `18` **không** đổi thành `0.5` (không cùng số) → hàng thập phân `0/0`, bỏ, không tính.

Gold `1/2` mới đổi được `0.5`, `\frac{1}{2}`, `\dfrac{1}{2}`…

Hổng (list không hết format): `VIEC-SAU.md` mục 1. Không sửa bằng LLM tuần này.

---

## B8. Gạch nhầm và nhãn

**Ví dụ gạch nhầm.** Sách `1/2`, ta viết `\dfrac{1}{2}` (đúng toán). Cô gạch vì không đọc được. Đó là false negative.

**Ví dụ khen nhầm (hiếm).** Sách `10`, bài `11`, cô chịu. Việc 1 không tập trung.

**Ví dụ đọc bảng smoke.** Hàng `dfrac | 20/20 | parse_empty`: 20 lần đưa `\dfrac{...}`, 20 lần cô không lôi ra toán.

| Nhãn | Ví dụ |
|------|--------|
| `ok` | Sách `10`, bài `\boxed{10}`, cô chịu |
| `parse_empty` | Bài `\dfrac{1}{2}`, cô không hiểu lệnh |
| `timeout` | Công thức quá dài, cô nghĩ quá 5 giây |
| `compare_false` | Sách `1/3`, bài `0.33`, cô đọc được nhưng bảo không bằng |
| `—` | Không lần nào gạch, hoặc `n=0` |

---

## B9. Python

**Ví dụ.** File `run.py` = tờ hướng dẫn. Gõ lệnh thì máy làm 20 bài × nhiều kiểu chữ, không bấm từng ô Excel.

**Ví dụ `.venv`.** Hộp đồ riêng. Cài cô vào hộp này. Máy khác / project khác không lẫn. Mở Terminal, gõ `.venv/bin/python ...` = dùng hộp đó.

**Ví dụ import.** `run.py` nói: “mượn `load_gold` từ code mình, mượn `parse` từ cô”. Không tải internet mỗi lần (trừ lần đầu lấy file đề).

**Ví dụ stdlib.** `json` đọc một dòng đề. `urllib` tải file lần đầu. `csv` ra Excel. Không cần pandas cho bảng nhỏ.

**Ví dụ hai gói pip.** `math-verify` = cô. `pytest` = bấm thử ống nước. Không cài wandb (bảng điểm cloud) — việc 1 không cần.

---

## B10. JSONL, CLI, manifest

**Ví dụ JSONL.** File `gsm8k_test.jsonl`, mỗi dòng một bài, dạng `{"answer": "... #### 18"}`. Dòng 1 = bài 1, dòng 2 = bài 2.

**Ví dụ CLI.**

```bash
.venv/bin/python -m experiments.viec1.run --dataset gsm8k --limit 20
```

Nghĩa: dùng hộp `.venv`, chạy việc 1, chỉ GSM8K, 20 bài. Không mở web.

**Ví dụ manifest.** `results/viec1/manifest.json` ghi: ngày 2026-08-16, n=200, cô 0.9.0, antlr 4.13.2. Bảng smoke cũ (n=20) để riêng ở `smoke-limit20/`. Tháng sau cài cô 0.10, số không trộn.

---

## B11. Ba chữ của đề lớn (việc 3 đã chạy ống)

**GVT** = 4 bước ở A2: học sinh viết → cô chấm → giữ bài chịu → ôn → lặp.  
Tên đề tài. Việc 3 đã cắm đủ bốn bước trong `src/dacntt/gvt/`. Việc 1–2 chỉ soi cô.

**Reasoning** = mấy dòng **làm bài**, không phải chỗ khoanh.

```
3 × 4 = 12      ← reasoning (cô không đọc)
12 − 2 = 10     ← reasoning (cô không đọc)
\boxed{10}      ← chỗ khoanh (cô chỉ nhìn cái này)
```

Người ta khoe GVT làm reasoning khá hơn. Cô không đọc reasoning. Đó là gốc đề.

**Human annotation** = **người** ngồi ghi đúng/sai cho từng bài máy mới viết.  
GVT khoe: không cần người đó — cô máy chấm thay.  
(Sách `#### 18` vẫn do người làm từ trước = tủ đề, không phải chấm bài mới.)

SFT trên Mac = ôn bài cô giữ (LoRA ngắn, mlx-lm). SFT trên Kaggle = cùng vòng, cùng cách chọn bài, đổi sang transformers+peft+TRL (không phải GRPO). Không sửa cô.

---

## B12. pass@1, pass@k

**Ví dụ.** Một đề táo. Cho học sinh làm 8 lần (chữ/lời hơi khác).

Lần: đúng, sai, đúng, sai, sai, sai, sai, sai → 2/8 lần cô chịu.

- pass@1: chỉ lấy lần 1. Lần 1 đúng → đề này đạt pass@1.
- pass@8: trong 8 lần có ít nhất một lần đúng → đạt pass@8.

**Không phải** 8 dạng đề khác nhau. **Không phải** 8 cách giải.

**Ví dụ hợp cô.** Trước: 8 lần 3 kiểu chữ đúng. Sau: 8 lần gần như luôn `\boxed{10}` — lần 1 hay đúng (pass@1 tăng), 8 lần không thêm đề mới (pass@8 đứng).

Việc 3 ghi hai số này mỗi vòng, cộng đếm chữ. Mac toy: xem `results/viec3/`. Số paper: Kaggle.

---

## B13. Test và stub

**Ví dụ test.** `test_variants.py`: đưa gold `1/2`, bắt `rewrite_dfrac` ra đúng chuỗi `\dfrac{1}{2}`. Gãy = ống đổi chữ hỏng, chưa nói cô.

Không viết test “cô phải gạch 0.5” — đó là kết quả thí nghiệm trên bảng.

**Ví dụ stub (cũ).** Trước việc 3, `gvt/generate.py` báo “chưa xây”. Nay đã có `ScriptedGenerate` (dry) và `MlxGenerate` (Qwen trên Mac).

---

# Phần C — Quyết định (kèm ví dụ)

| Chọn | Ví dụ “nếu chọn khác” |
|------|------------------------|
| Cô `math-verify` | So chữ: `1/2` vs `0.5` luôn sai — không còn đề “cô lệch chữ” |
| Gold đổi chữ | Dùng bài model sai `17`: không biết gạch vì toán hay chữ |
| GSM8K + MATH | Chỉ 20 GSM8K: tưởng đề chết, bỏ sót MATH |
| default và reward | Chỉ default: việc 3 dùng cô keo, số không khớp |
| Sách trước | Đổi chỗ verify: có thể ra bảng khác, không so được |
| Mac ≠ paper | Lấy pass@* 8 đề Qwen 0.5B trên Mac viết như SOTA: sai đề |

---

# Phần D — Ống nước

Việc 1: `experiments/viec1/run.py`. Việc 2: `experiments/viec2/run.py`. Việc 3: `experiments/viec3/run.py`.

**Ví dụ một vòng việc 1 (1 đáp án, 1 kiểu chữ, 1 preset):**

1. `gold/`: lấy `1/2`
2. `variants/`: đổi thành `\dfrac{1}{2}`
3. `verify/`: cô default → gạch, nhãn `parse_empty`
4. Cộng vào hàng `math500 | dfrac | default`

Lặp hết bài × hết kiểu × hai preset → `results/viec1/table.md`.

**Ví dụ một vòng việc 2 (1 bài model, 1 preset):**

1. Tải lời model có sẵn (không gọi Qwen tại chỗ)
2. Cô chấm cả bài
3. Đọc sách + chỗ khoanh: đúng thật không? (`read.py`, thay đọc tay)
4. Đúng mà cô gạch → FN; tách lôi nhầm số / viết không nhận

**Ví dụ một vòng việc 3 (1 đề, k=4, preset reward lúc dạy):**

1. Generate: học sinh nộp 4 bài cùng đề táo
2. Verify: cô `reward` chịu 2, gạch 2 (sai toán hoặc chữ)
3. Select: giữ 2 bài chịu
4. Train: ôn LoRA 2 bài đó — mlx-lm (Mac) hoặc transformers+peft+TRL SFT (Kaggle)
5. Đo: pass@1, pass@k, đếm `\boxed` / `\dfrac` / thập phân; nếu rẻ thì A/B/C

Dry không gọi Qwen: tự viết 4 chữ từ sách, cô chấm thật. mlx gọi Qwen 0.5B.

| Khúc | File |
|------|------|
| Sách | `src/dacntt/gold/sources.py` `load.py` `extract.py` |
| Chữ | `variants/registry.py` `rewrite.py` |
| Cô | `verify/presets.py` `adapter.py` |
| Đọc chỗ khoanh | `src/dacntt/read.py` |
| Bảng việc 1 | `report/table.py` `manifest.py` |
| Việc 2 | `experiments/viec2/run.py` `traces.py` |
| Việc 3 vòng | `gvt/generate.py` `select.py` `train.py` `loop.py` `measure.py` |
| Việc 3 CLI | `experiments/viec3/run.py` |
| Việc 3 Kaggle | `experiments/viec3/KAGGLE.md` |
| Test | `tests/test_variants.py` `test_verify_adapter.py` `test_read.py` `test_gvt.py` |

---

# Phần E — Lệnh

```bash
.venv/bin/python -m experiments.viec1.run --dataset gsm8k --limit 20
.venv/bin/python -m experiments.viec1.run --dataset both --n 200 --presets default,reward
.venv/bin/python -m experiments.viec2.run --n 200 --presets reward,default
.venv/bin/python -m experiments.viec3.run --mode dry --n 100 --rounds 2 --k 4
.venv/bin/python -m experiments.viec3.run --mode mlx --n 8 --rounds 2 --k 4 --max-tokens 48 --lora-iters 8
.venv/bin/pytest tests -q
```

**Ví dụ đọc hàng việc 1 (bảng 200):** `math500 | LaTeX khác lệnh (dfrac) | default | 146/146 | 100% | parse_empty`  
= 146 đáp án sách đổi được thành `\dfrac{...}`, cô không đọc được cả 146.

**Ví dụ đọc hàng việc 2:** `math500 | reward | 10 / 128 | 7.8% | lôi nhầm 8, viết không nhận 2`  
= 128 bài model đúng thật; cô gạch 10. Tám lần vì bài dài lôi nhầm số; hai lần vì chữ (`\left` / `6+9i`).

- GSM8K việc 1 ~0% gạch vì chữ thường (trừ `\dfrac`/`\tfrac`) → bình thường.
- MATH việc 1 vài–100% tùy kiểu, không chỉ lôi nhầm số → **đã đi việc 2**.
- Việc 2 GSM8K FN 0%; MATH FN 7.8% (cùng `reward` và `default`).
- Việc 3 Mac: ống GVT chạy; dry 100 đề chọn bài thật; mlx 8 đề Qwen 0.5B. **Không** phải số paper. Kaggle: `experiments/viec3/KAGGLE.md`.

---

# Phần F — Đã / chưa

**Đã:** đề; ống việc 1; cô 0.9.0; bảng 200 GSM8K + 200 MATH; việc 2 FN (GSM8K 0%, MATH 7.8%); **ống việc 3** (generate / select / train + pass@* / chữ); dry 100 đề; mlx toy 8 đề.

**Chưa:** số paper trên Kaggle (T4, 0.5B rồi 1.5B, SFT qua transformers+peft+TRL, k=8); hỏi thầy.  
Chỗ hổng list chữ: [`VIEC-SAU.md`](VIEC-SAU.md) — việc 2 đã thấy format thật (`\left`, số phức, bài dài). Vẫn không nhét LLM vào `rewrite.py`.

---

# Nhật ký

### 2026-08-16 — Việc 3: ống GVT + dry 100 đề + mlx toy

- Bốn bước nằm `src/dacntt/gvt/`: học sinh viết, cô chấm, giữ bài chịu, ôn LoRA (Mac) / GRPO (Kaggle, chưa chạy).
- Select lúc dạy = `reward`. Exam ghi `reward` và `default`.
- Dry (không Qwen): 100 GSM8K × 4 chữ × 2 vòng. Cô gạch `\dfrac`, giữ 300/400. pass@1 100% vì lần đầu luôn `\boxed{gold}` — chứng minh ống, không phải model giỏi. `results/viec3/`.
- mlx: Qwen 2.5 0.5B 4bit, 8 đề GSM8K, k=4, 2 vòng, max 48 token, LoRA vài bước (~8 phút). pass@1 **0%** cả hai vòng; pass@4 **12.5%** đứng; chữ gần như không `\boxed`. A/B/C = 0. `results/viec3/mlx-toy/`. Không lấy số paper.
- Paper: `experiments/viec3/KAGGLE.md` (T4, 0.5B rồi 1.5B, k=8, GRPO).
- Lệnh dry: `.venv/bin/python -m experiments.viec3.run --mode dry --n 100 --rounds 2 --k 4`.

### 2026-08-23 — Kaggle: đổi GRPO → SFT, code thật thay pseudocode

- Quyết định lại: nhánh Kaggle dùng **SFT** (khớp thiết kế select→train sẵn có), không dùng GRPO. GRPO tự sinh rollout + `reward_fn` trong lúc train, không khớp bước `select_batch` tách rời đã có trong `loop.py`.
- Thêm `HfLoraSftTrain` (`gvt/train.py`) và `HfGenerate` (`gvt/generate.py`): transformers + peft + TRL `SFTTrainer`, cùng ngữ nghĩa với `MlxLoraTrain`/`MlxGenerate` (mỗi vòng LoRA mới từ base, chỉ train trên bài vòng đó được giữ).
- `experiments/viec3/run.py` có `--mode hf`: một lệnh CLI y hệt đường Mac, không còn phải chép tay pseudocode notebook trong `KAGGLE.md`.
- Chưa chạy được trên máy này (không có torch/CUDA) — chưa test thật. Sẽ lộ lỗi version TRL/transformers lần đầu chạy trên Kaggle; sửa thẳng trong `train.py`/`generate.py`, không vá trong notebook.

### 2026-08-16 — Việc 2: bài model thật, FN MATH 7.8%

- Tải lời có sẵn, không gọi Qwen: GSM8K `qwen3.5-397b-a17b` (200 dòng accepted), MATH-500 `Qwen2.5-7B-Instruct` (200 đề, một lần / đề).
- “Đọc tay” = so sách với chỗ khoanh (`read.py`).
- GSM8K: 0/200 gạch nhầm (câu neo `The answer is …`, khớp việc 1).
- MATH: 10/128 = **7.8%** FN, cả `reward` lẫn `default`. 8 lôi nhầm số, 2 viết không nhận (`\left` vs ngoặc thường; `6+9i` vs `6 + 9i`).
- File: `results/viec2/table.md` `doc.md` `manifest.json`. Lệnh: `.venv/bin/python -m experiments.viec2.run --n 200 --presets reward,default`.

### 2026-08-16 — Việc 1 đủ 200+200: đi việc 2

- Lệnh: `.venv/bin/python -m experiments.viec1.run --dataset both --n 200 --presets default,reward`.
- GSM8K: chữ thường 0/200; `\dfrac`/`\tfrac` 200/200 `parse_empty`.
- MATH: `\dfrac`/`\tfrac` **146/146 (100%)** `parse_empty`; thập phân `0.50` 13/22; hộp 41/200; gold nguyên văn 24/200 cô không đọc (`p-q`, `\text{…}`, `\sqrt{51}`, `\dfrac` sẵn trong sách…).
- Không phải “chỉ lôi nhầm số” → **đi việc 2**. Chi tiết: `results/viec1/decision.md`. Smoke 20 bài cũ: `results/viec1/smoke-limit20/`.

### 2026-08-16 — B11 rút: GVT / reasoning / người chấm — việc 1 chưa chạy

### 2026-08-16 — Tạo VIEC-SAU.md

- Mục 1: list kiểu chữ ta nghĩ ra, không cover hết; cover thực tế = việc 2, không tối ưu rewrite bằng model.

### 2026-08-16 — B7 rút: cùng gold, copy nhiều chữ đưa cô

### 2026-08-16 — B3: vì sao có default và reward, vì sao việc 1 chạy cả hai

### 2026-08-16 — B3 rút thành công tắc hai vị trí

### 2026-08-16 — B3: preset = hai nấc keo cùng một cô

### 2026-08-16 — Parse: cô soi tờ theo mốc boxed / câu neo / số cuối

### 2026-08-16 — B2 viết lại: parse = tìm khoanh, verify = so sách

### 2026-08-16 — Thêm ví dụ cho mọi khái niệm

- Hai bài mẫu xuyên file: táo (`10`) và nửa (`1/2`).
- Mỗi mục B mở bằng ví dụ trước định nghĩa.

### 2026-08-16 — B1 khối “nếu vẫn tối”

### 2026-08-16 — Khuôn là gì / làm gì / vì sao / cách khác

### 2026-08-16 — Khung việc 1, smoke 20 GSM8K

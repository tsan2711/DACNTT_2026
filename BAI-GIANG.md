# Đề bài là gì, và bạn cần làm gì

Sản phẩm cuối: **một bài báo**. Không phải app, không phải model để bán.

Nếu chỉ đọc được một phần: đọc **mục 1 và mục 2**. Xong là đã hiểu đề. Phần còn lại là chi tiết, đọc khi làm.

---

# 1. Đề bài — nói thường

Có một **máy giải toán** (model).  
Có một **máy chấm** (math-verify): nó không đọc bài làm, chỉ so đáp án với sách.

Người ta làm vòng này nhiều lần:

```
máy giải toán làm bài
        ↓
máy chấm: đúng thì giữ, sai thì bỏ
        ↓
lấy những bài “đúng” dạy lại máy giải toán
        ↓
lặp lại
```

Người ta tưởng vòng này dạy máy **giỏi toán hơn**.

Nhưng máy chấm hay **gạch bài đúng** chỉ vì viết khác sách:

- sách `1/2`, máy viết `0.5` → có thể bị gạch
- sách `\frac{1}{2}`, máy viết `\dfrac{1}{2}` → có thể bị gạch

Gạch nhầm khoảng 1/10 bài đúng. Gần như không khen nhầm.  
Nó tưởng đo “đúng đáp án không”. Thực ra đang phạt **cách viết**.

**Đề bài của bạn:**

> Cho máy giải toán nhỏ học nhiều vòng với máy chấm đó.  
> Nó đang giỏi toán hơn, hay chỉ học **viết đúng kiểu máy chấm ưa**?

Bạn **không sửa** máy chấm.  
Bạn **đo** xem chuyện đó có xảy ra không.

Giống: giáo viên keo, chỉ thích một kiểu chữ. Học sinh học nhiều khóa. Chúng giỏi toán, hay chỉ học chữ?

---

# 2. Bạn cần làm gì

Ba việc, **theo thứ tự**. Việc 1 chưa xong thì chưa làm việc 2.

## Việc 1 — tuần này (máy đang có, không cần GPU mạnh)

Hỏi: máy chấm đang gạch những kiểu viết nào?

1. Cài math-verify.
2. Lấy đáp án đúng trong sách (khoảng 200 bài dễ GSM8K + 200 bài khó MATH).
3. Tự viết lại mỗi đáp án theo nhiều kiểu: `1/2`, `0.5`, `\boxed{}`, `\dfrac`…
4. Cho máy chấm. Kiểu nào bị gạch = máy chấm lệch.
5. Ghi thành **một bảng**: kiểu viết / bị gạch không / vì sao.

**Xong việc 1 khi:** có bảng đó.

- Bảng cho thấy bài khó hay bị gạch vì cách viết → đề tài còn đất, làm việc 2.
- Bảng gần như không bị gạch vì cách viết → đề tài yếu, **dừng**, đừng train.

Chưa train. Chưa tải model lớn. Chỉ chấm đáp án sách.

## Việc 2 — sau khi có bảng (vẫn chưa train nhiều)

Lấy lời giải **máy giải toán thật** (tải có sẵn trên mạng).  
Cho máy chấm. Những câu máy bảo sai — **mình đọc tay**: thực ra đúng hay sai.

Ra số: trong các bài đúng, máy gạch nhầm bao nhiêu phần trăm.  
Làm trên bài dễ rồi bài khó. Bảng bài khó mới là móng bài báo.

## Việc 3 — sau đó (Kaggle, GPU)

Mới cho máy giải toán học nhiều vòng. Mỗi vòng ghi:

- làm một lần đã đúng hơn chưa? (**pass@1**)
- cho làm nhiều lần, vẫn còn nhiều cách đúng không? (**pass@k**)
- chữ viết có ngày càng giống một kiểu không?

Nếu pass@1 tăng mà pass@k đứng/giảm, **và** chữ viết tụ về một kiểu → đề bài được trả lời: đang học chữ, không học toán.

Máy Mac chỉ dùng để thử code (100 bài, 2 vòng). Số liệu paper lấy trên Kaggle.

---

# 3. Việc hôm nay / tuần này (checklist)

Làm từ trên xuống. Chưa xong dòng trên thì chưa làm dòng dưới.

- [ ] Đọc lại mục 1 đến khi nói được đề bài bằng một câu, không nhìn tài liệu.
- [ ] Hỏi trường: nộp khi nào? Chỉ cần làm lại thí nghiệm cũ, hay phải có cái mới?
- [ ] Cài `math-verify` (xem mục 8 nếu cần lệnh).
- [ ] Tải bộ đáp án GSM8K và MATH-500 (chỉ đáp án, chưa cần model).
- [ ] Viết list ~10 kiểu viết sẽ thử (mục 6 có sẵn list).
- [ ] Chạy máy chấm trên các kiểu đó. Ra bảng.
- [ ] Quyết định: đi tiếp hay dừng.

**Không làm tuần này:** train model, cài vLLM, dựng GRPO, tải Qwen 1.5B, viết framework.

---

# 4. Một câu chuyện để khỏi rối

Học sinh làm đúng `1/2`.  
Giáo viên chỉ chấp nhận `0.5`. Gạch.  
Bài đó không được đưa vào buổi ôn.  

Học sinh khác viết `0.5`. Được khen. Được ôn đi ôn lại.

Sau 5 khóa: cả lớp viết `0.5`. Điểm giáo viên tăng.  
Hỏi lại bằng cách khác, hoặc cho làm nhiều lần — lớp không giỏi hơn, chỉ đồng phục chữ.

Bạn đo: giáo viên đang gạch kiểu chữ nào (việc 1–2), rồi xem lớp có đồng phục chữ sau nhiều khóa không (việc 3).

---

# 5. Đề bài không phải gì

| Không phải | Vì |
|------------|-----|
| Làm model giải toán điểm cao | Đó là bài của người khác (Open-R1, TinyZero) |
| Sửa máy chấm cho ít gạch nhầm | Đó là bài TinyV |
| Viết app / website | Sản phẩm là bài báo |
| Chứng minh model nhỏ thành GPT-4 | Máy chấm chỉ **chọn**, không **tạo** năng lực mới |

---

# 6. Chi tiết việc 1 — bảng lệch máy chấm

Đọc khi bắt tay làm việc 1.

**Khóa dụng cụ** (ghi vào một file, để số sau này so được):

- version `math-verify`
- version `antlr4`
- dùng config mặc định hay config “reward” (config reward chặt hơn, gạch nhiều hơn)

**List kiểu viết nên thử** (với mỗi đáp án sách):

| Kiểu | Ví dụ nếu sách là `1/2` |
|------|-------------------------|
| Số trần | `1/2` |
| Thập phân | `0.5` , `0.50` |
| LaTeX thường | `\frac{1}{2}` |
| LaTeX khác lệnh | `\dfrac{1}{2}` , `\tfrac{1}{2}` |
| Có hộp | `\boxed{1/2}` |
| Có dấu đô la | `$1/2$` |
| Có câu | `The answer is 1/2` |
| Có ẩn | `x = 1/2` |
| Có đơn vị | `1/2 apples` |
| Số nguyên tương đương | `18` vs `18.0` (với bài GSM8K) |

Chạy: `parse(sách)` rồi `parse(kiểu viết)` rồi `verify(sách, kiểu viết)`.  
`False` = gạch nhầm (vì ta biết giá trị đúng).

Ghi bảng:

| Bộ bài | Kiểu viết | Số lần gạch / tổng | Lý do đoán (lôi sai số / không hiểu latex / so không ra) |
|--------|-----------|---------------------|----------------------------------------------------------|

**Cách đọc bảng:**

- GSM8K (bài dễ, đáp án số nguyên) gần 0% gạch vì cách viết → bình thường, đừng tuyên bố đề tài chết.
- MATH (bài khó, phân số / latex) vài phần trăm đến ~10% gạch vì cách viết → đề tài còn đất.
- MATH cũng gần 0%, chỉ gạch vì lôi nhầm số trong bài dài → đề tài yếu (chỉ lỗi “tìm số”), dừng.

---

# 7. Sau này mới cần — việc 3 đo gì

Đọc khi việc 1–2 xong.

Với mỗi đề, cho máy làm **k lần** (ví dụ 8 lần):

- **pass@1** = làm một lần đã đúng chưa. (thi một phát)
- **pass@k** = trong k lần, có ít nhất một lần đúng. (cho thi lại)

| Nếu giỏi toán hơn | Nếu chỉ học chữ máy chấm |
|-------------------|---------------------------|
| Cả hai số tăng | pass@1 tăng, pass@k đứng hoặc giảm |

Đồng thời đếm chữ viết mỗi vòng: bao nhiêu `\boxed{}`, bao nhiêu phân số, bao nhiêu thập phân…

**Kết luận mạnh:** pass@1 tăng **và** chữ viết ngày càng giống nhau. Một mình một thứ thì chưa đủ.

---

# 7b. Kết quả thật — lần chạy đầu tiên (n=500, Kaggle, 2026-08-27)

**Dự đoán trước khi chạy** (đúng bảng ở mục 7): hoặc cả hai số cùng tăng (giỏi
thật), hoặc pass@1 tăng còn pass@k đứng/giảm (chỉ học chữ). Hai kịch bản đó
là tất cả những gì đoán trước.

**Số thật ra được** (Qwen2.5-0.5B, GSM8K+MATH-500, 500 đề/bộ, k=8, 5 vòng):

| Vòng | pass@1 | pass@8 |
|---|---|---|
| 0 | 31.1% | 60.5% |
| 1 | 31.9% | 58.9% |
| 2 | 29.9% | 56.1% |
| 3 | 28.9% | 55.5% |
| 4 | 27.4% | 54.9% |

**Cả hai số cùng GIẢM** — không khớp kịch bản nào đã đoán trước. Đây là kịch
bản thứ 3, chưa lường tới: máy **tệ đi thật** qua mỗi vòng, không phải chỉ
"học viết chữ đẹp che giấu việc không giỏi thêm".

Đi kèm: chữ viết vẫn đổi thật (`\boxed{}` giảm 5880→5513 lần trên 8000 lần
viết, kiểu `\frac`/gán biến tăng dần) — nên phần "chữ hội tụ" trong giả
thuyết vẫn đúng, chỉ là đi cùng cả hai số cùng giảm, không phải chỉ pass@1
tăng. Bảng thêm/mất đề (A/C) xác nhận cùng chiều: mất đề nhiều hơn thêm đề ở
cả 4/4 vòng.

**Vì sao vẫn đáng viết vào bài báo, không phải kết quả "hỏng":** đây là bằng
chứng máy chấm lệch làm hại pipeline tự-train — chỉ là hại theo kiểu mạnh
hơn dự đoán ban đầu (tệ đi thẳng, không phải chỉ giả vờ giỏi). Số bài "giữ
để ôn" mỗi vòng cũng giảm dần (2533→2123) — gợi ý cơ chế: tập ví dụ "đúng"
bị verifier lọc ra ngày càng hẹp/lệch, vòng sau học từ tập đó nên tệ hơn —
gần giống hiện tượng "model collapse" (mục 9 dưới, nhóm bài Shumailov) nhưng
xảy ra trên dữ liệu ĐÃ LỌC qua verifier lệch, không phải toàn bộ dữ liệu tự
sinh như bài gốc đó — đây chính là khác biệt cần nhấn khi trình bày.

**Chưa kết luận chắc lúc viết đoạn trên:** mới 1 lần chạy, 1 cỡ model (0.5B).
Đã chạy thêm 1.5B — xem mục 7c ngay dưới.

---

# 7c. Kết quả thật — 1.5B, cùng lệnh (n=500, Kaggle, 2026-09-02)

**Chạy y hệt cấu hình 0.5B** (500 đề/bộ, k=8, 5 vòng), chỉ đổi model sang
`Qwen2.5-1.5B-Instruct`. Mục đích: xem hiện tượng "cả hai số cùng giảm" ở
mục 7b có lặp lại ở cỡ model khác không.

| Vòng | pass@1 | pass@8 | Giữ/ôn |
|---|---|---|---|
| 0 | 50.0% | 72.6% | 3962 |
| 1 | 46.2% | 71.5% | 3730 |
| 2 | 44.5% | 70.2% | 3395 |
| 3 | 32.4% | 63.6% | 2638 |
| 4 | 18.6% | 48.6% | 1566 |

**Lặp lại — và mạnh hơn nhiều.** So sánh trực tiếp với 0.5B (vòng 0 → vòng 4):

| | pass@1 | pass@8 |
|---|---|---|
| 0.5B | 31.1%→27.4% (giảm 12%) | 60.5%→54.9% (giảm 9%) |
| 1.5B | 50.0%→**18.6%** (giảm 63%) | 72.6%→**48.6%** (giảm 33%) |

Model to hơn (1.5B, gấp 3 lần tham số) **sụp mạnh hơn hẳn** model nhỏ, không
phải ổn định hơn như có thể đoán theo trực giác thường ("model to hơn thì
chắc chắn hơn"). Xu hướng giảm ở 1.5B rất đều, tăng tốc dần (mức giảm mỗi
vòng: −3.8, −1.7, −12.1, −13.8 điểm pass@1) — 5/5 vòng đều giảm, không có
vòng nào tăng lại, khó coi là nhiễu ngẫu nhiên. Số bài giữ để ôn cũng sụp
theo (3962→1566, mất gần 60%), và bảng A/C ở 2 vòng cuối lệch hẳn về phía
mất đề (117 mất/51 thêm ở vòng 3; 194 mất/44 thêm ở vòng 4) — đúng dạng sụp
tăng tốc, không phải trôi dạt đều đều.

Văn phong cũng đổi mạnh hơn hẳn 0.5B: `\boxed{}` giảm hơn nửa (5608→2693
trên 8000 lần viết), `$...$` tăng hơn gấp đôi (1453→3406), `\dfrac` tăng 10
lần (24→241).

**Đọc kết quả:** hiện tượng "verifier lệch làm pipeline tự-train sụp qua
nhiều vòng" giờ có 2 cỡ model xác nhận cùng chiều, không phải trùng hợp của
riêng 1 model. Đây đủ vững để đưa vào bài báo làm phát hiện chính — mạnh
hơn cả giả thuyết ban đầu (dự đoán ở mục 7 chỉ tính tới "học viết chữ đẹp",
không tính tới khả năng sụp thật, và càng không tính tới việc model to hơn
lại sụp nặng hơn).

**Còn thiếu để chắc chắn hoàn toàn:** đây vẫn chỉ 1 lần chạy/cỡ model (không
lặp lại nhiều seed để đo phương sai), và cả 2 lần đều dùng `--dataset both`
trên tập test (chưa tách train/test riêng — xem giới hạn đã ghi trong
`experiments/viec3/KAGGLE.md`). Đủ để viết vào bài báo kèm đúng 2 giới hạn
này, không đủ để tuyên bố tuyệt đối.

---

# 8. Máy và phần mềm (đã chốt)

| Việc | Dùng gì |
|------|---------|
| Việc 1–2 | Máy đang có, CPU, `math-verify` |
| Thử code vòng lặp | Mac, 100 bài, 2 vòng, Qwen 0.5B, `mlx-lm`. Không lấy số paper |
| Việc 3 lấy số | Kaggle (GPU T4), Qwen 0.5B rồi 1.5B, LoRA SFT qua transformers + peft + TRL (không phải GRPO) |

Cài việc 1:

```bash
pip install 'math-verify[antlr4_13_2]'
```

Dùng:

```python
from math_verify import parse, verify

sach = parse("1/2")
viet = parse("0.5")
print(verify(sach, viet))  # True hoặc False
```

Không cài thêm repo khác trừ khi được yêu cầu.

---

# 9. Năm bài người khác đã viết (đọc sau khi thuộc đề)

| Bài | Họ làm | Bạn khác chỗ nào |
|-----|--------|------------------|
| [TinyV](https://arxiv.org/abs/2505.14625) | Máy chấm gạch nhầm → hại học. Họ **sửa** máy chấm. Một lần học. | Bạn **không sửa**. Bạn lặp nhiều vòng và đo. |
| [Imperfect verifiers](https://arxiv.org/abs/2510.00915) | Máy chấm nhiễu. Họ sửa công thức học. | Bạn coi máy gạch theo **cách viết**, không phải nhiễu lung tung. |
| [Limit of RLVR](https://arxiv.org/abs/2504.13837) | Học xong: thi một phát điểm tăng, cho thi nhiều lần thì model gốc thắng. | Bạn dùng đúng cách đo đó, thêm: có phải vì **kiểu chữ** không. |
| [STaR](https://arxiv.org/abs/2203.14465) | Vòng làm bài → lọc đúng → dạy lại. | Họ tin máy chấm sạch. Bạn không tin. |
| [Spurious Rewards](https://arxiv.org/abs/2506.10947) | Thưởng bừa, thậm chí chỉ thưởng có `\boxed{}`, điểm vẫn tăng. | Họ phá thưởng cố ý. Bạn để máy chấm “sạch” nhưng lệch chữ. |

---

# 10. Thuật ngữ (tra khi gặp)

| Chữ trong tài liệu khác | Nghĩa |
|-------------------------|--------|
| Verifier | Máy chấm |
| Gold | Đáp án sách |
| FN / false negative | Gạch nhầm (đúng mà bảo sai) |
| FP / false positive | Khen nhầm (sai mà bảo đúng) |
| GSM8K | Bộ bài toán dễ, đáp án gần như số nguyên |
| MATH / MATH-500 | Bộ bài khó hơn, nhiều phân số và LaTeX |
| pass@1 | Thi một phát |
| pass@k | Cho thi k lần, trúng một lần là được |
| SFT / RLVR / LoRA | Cách dạy lại máy ở việc 3 (SFT trên bài được chọn, không phải RL trực tiếp). Việc 1 chưa cần |

---

# 11. Máy chấm làm gì bên trong (đọc khi làm bảng việc 1)

Repo: https://github.com/huggingface/Math-Verify

Ba bước: **lôi đáp án** → **đổi sang dạng so được** → **so với sách**.

Hay gạch vì:

1. Lôi nhầm số trong bài dài (lấy số cuối, không phải đáp án).
2. Không hiểu kiểu latex lạ (`\dfrac` khác `\frac`).
3. `0.33` không được coi bằng `1/3` (thiếu chữ số).
4. Sách viết `(1,2)`, máy viết `1 < x < 2` — cùng nghĩa, máy gạch.
5. Timeout hoặc không đọc được → tính sai.

Khi ghi bảng việc 1, tách: **lôi nhầm số** khác **viết đúng nhưng máy không nhận**. Đề tài sống ở loại thứ hai.

`verify(sách, bài)` không đối xứng: đổi chỗ hai đối số có thể ra kết quả khác. Luôn để sách là đối số đầu.

Hai chế độ chấm: mặc định rộng hơn; chế độ “reward” (khi dạy máy) chặt hơn. Phải ghi rõ đang dùng cái nào.

---

# 12. Khi lại không hiểu, chỉ nhớ 4 dòng

1. Máy chấm hay gạch bài đúng vì **cách viết**.
2. Người ta vẫn dùng máy đó để dạy máy giải toán nhiều vòng.
3. **Đề bài:** sau nhiều vòng, máy giải toán giỏi toán hay chỉ giỏi viết chữ máy chấm ưa?
4. **Việc của bạn tuần này:** đo máy chấm đang gạch những kiểu viết nào. Chưa dạy máy.

# Nội dung nhập lên trang đề tài ELIT

> Soạn 2026-09-04. Vấn đề nghiên cứu đã chốt (xem `TOI-HIEU.md`), đã tra lại
> "có bài nào làm đúng cái mình đưa ra chưa" (xem `papers/KHAO-SAT.md`,
> cập nhật 2026-09-04). Kết luận tra: **chưa có bài trùng**. Dưới đây là
> phần chữ để dán vào ELIT.

---

## 1. Tên đề tài

**Tiếng Việt:** Verifier lệch-vì-văn-phong gây sụp năng lực trong tự-huấn-luyện
lặp vòng ở model suy luận nhỏ.

**Tiếng Anh:** When the Grader Has a Style: Format-Biased Verifiers Cause
Capability Collapse in Iterative Self-Training of Small Reasoning Models.

**Sản phẩm:** một bài báo nghiên cứu (không phải phần mềm/ứng dụng, không phải
model thương mại).

---

## 2. Bài toán nghiên cứu (đã chốt)

### 2.1. Bối cảnh

Một họ phương pháp phổ biến để cải thiện model ngôn ngữ nhỏ (SLM) trên toán
suy luận **không cần người gán nhãn** là vòng lặp **Generate–Verify–Train (GVT)**
— nền của STaR, ReST/ReST-EM, RFT:

```
generate  — SLM tự sinh k lời giải cho mỗi đề
verify    — verifier tự động (ở đây: math-verify) so đáp án cuối với đáp án sách
select    — giữ lời giải được verifier chấm "đúng", bỏ phần còn lại
train     — huấn luyện lại chính SLM trên tập được giữ
          — lặp nhiều vòng
```

"Self-improving" = không có người gán nhãn cho lời giải mới; verifier đóng vai
"giáo viên". Toàn bộ họ này dựa trên một **giả định ngầm**: verifier phân biệt
đúng/sai một cách đáng tin cậy.

### 2.2. Vấn đề

Verifier luật (rule-based) cho toán — như `math-verify` — chỉ trích đáp án cuối
rồi so sau khi chuẩn hoá; nó **không đọc lời giải**, và bước chuẩn hoá không phủ
hết mọi cách viết tương đương. Hệ quả: nó **gạch nhầm** (false negative) những
lời giải **đúng** nhưng viết theo kiểu nó không nhận. Quan trọng: độ lệch này
**có hướng** — gần như không bao giờ khen nhầm (false positive ≈ 0), chỉ gạch
nhầm theo đúng một chiều.

### 2.3. Câu hỏi nghiên cứu

> Khi một verifier lệch-có-hướng như vậy được dùng làm bộ lọc trong vòng GVT và
> **lặp lại nhiều vòng** (không phải một lần), hậu quả là gì? Cụ thể: SLM đang
> cải thiện năng lực suy luận thật, hay chỉ học **viết đúng kiểu verifier ưa**,
> hay tệ hơn — **sụp năng lực**?

Cách đo: **không sửa verifier** (đó là hướng của TinyV). Giữ nguyên verifier
lệch sẵn, chạy vòng GVT nhiều lần, và đo:

- **pass@1** (làm 1 lần đúng bao nhiêu đề) và **pass@k** (làm k lần, ít nhất 1
  lần đúng) qua từng vòng — tách "ổn định hơn" khỏi "giải được thêm đề";
- **hội tụ văn phong** đầu ra qua từng vòng (11 nhãn: `\boxed`, `\dfrac`, `$...$`,
  câu văn, số thập phân…);
- **bảng A/B/C**: mỗi vòng có bao nhiêu đề *mới* giải được (A), *ổn định hơn* (B),
  *mất đi* (C).

---

## 3. Đã có bài báo nào làm đúng việc này chưa? (kết quả tra)

Đã khảo sát **32 bài** (29 bài đợt 2026-08-23/24 + 3 bài tra lại 2026-09-04),
xác nhận từng bài qua WebSearch/WebFetch trực tiếp trang arXiv (tên, mã arXiv,
ngày). Chi tiết đầy đủ: `papers/KHAO-SAT.md`.

**Kết luận: chưa có bài nào ghép đủ 3 mảnh của đề tài:**

1. verifier luật **lệch-vì-định-dạng thật** (không phải nhiễu giả lập tỉ lệ cố định),
2. **nhiều vòng** SFT self-training liên tiếp,
3. đo **cả năng lực** (pass@1/pass@k) **lẫn hội tụ văn phong** cùng lúc.

Các bài đụng gần nhất và chỗ khác:

| Bài | Họ làm | Khác đề tài này |
|---|---|---|
| Teacher-Free Self-Training Amplifies but Does Not Compound (arXiv 2606.07856) | Nhiều vòng self-training, đo đúng cặp pass@k | Verifier của họ **so chuỗi tuyệt đối, không lệch**; không đo văn phong |
| From Accuracy to Robustness (arXiv 2505.22203) | Đo recall verifier luật toán (~86%, tức ~14% FN) | Chỉ **RLVR 1 vòng**; không theo dõi lệch tích luỹ qua vòng; không đo văn phong |
| Imperfect Verifiers (arXiv 2510.00915) | Framework nhiễu ρ₀/ρ₁; *tự nêu* "nhiễu phụ thuộc định dạng" | Chủ động **giả định tỉ lệ nhiễu cố định**; chỉ **1 vòng RL** |
| TinyV (arXiv 2505.14625) | Đo FN verifier luật (~38%), **sửa** verifier bằng LLM phụ | Chỉ 1 lần đánh giá; hướng ngược (sửa, không phải đo hậu quả khi giữ nguyên) |
| ReST-EM (arXiv 2312.06585) | Chạy đúng khung GVT nhiều vòng trên MATH | Không đặc tả/không đo lệch verifier; tự ghi nhận 1 lần regression (APPS) nhưng **không điều tra nguyên nhân** |
| Delay, Plateau, or Collapse (arXiv 2605.02909) | Phân loại lỗi verifier trong RLVR; "FN chỉ làm chậm, không sụp" | **RLVR 1 vòng** + verifier mô phỏng; cơ chế "tập huấn luyện co hẹp qua từng vòng" của đề tài này chỉ xuất hiện ở chế độ multi-round SFT mà họ không xét — phải trả lời rõ trong Related Work |

Không bài nào trong 32 bài phủ định câu hỏi của đề tài. Đề tài "còn đất".

---

## 4. Mô tả những gì đã làm

### Việc 1 — Dò xem `math-verify` gạch nhầm ở đâu (XONG)

Chạy `math-verify 0.9.0` (antlr 4.13.2), 2 preset `default`/`reward`, trên
200 GSM8K + 200 MATH-500.

- GSM8K: gần như **không** gạch vì cách viết thường (0/200), trừ lệnh LaTeX lạ.
- MATH-500: `\dfrac`/`\tfrac` bị gạch **146/146 (100%)** dù đáp án đúng giá trị
  (`parse_empty` — verifier không đọc được lệnh); thập phân thừa số 0 (`0.50`)
  gạch 13/22 (59%); lời giải có `$`/hộp gạch ~20%.
- Hai preset ra số gần trùng → phạt-vì-chữ là của verifier, không phải riêng
  nút `reward`.
- Kết luận: có "đất" thật — **viết đúng nhưng verifier không nhận**, tập trung
  ở `\dfrac`/`\tfrac` và thập phân thừa số 0.

Kết quả: `results/viec1/` (`table.md`, `decision.md`).

### Việc 2 — Đo tỉ lệ gạch nhầm trên bài model thật (XONG)

Lấy lời giải **đúng thật** do model sinh (GSM8K: traces teacher công khai;
MATH-500: rollouts Qwen2.5-7B công khai), đọc tay so đáp án sách với chỗ verifier
khoanh.

- **Gạch nhầm 7.8% trên MATH-500** (10/128), **0% trên GSM8K** (0/200). Hai
  preset ra cùng số.
- Trong 10 ca FN: 8 ca verifier lôi nhầm số trong bài dài, 2 ca viết đúng mà
  verifier không nhận (`\left( ... \right)` vs `( ... )`; `6+9i` vs `6 + 9i`).
- Số này độc lập, **cùng chiều** với "From Accuracy to Robustness" (~14% FN) →
  lệch verifier không phải hiện tượng hiếm.

Kết quả: `results/viec2/` (`doc.md`, `table.md`, `fn_samples.md`).

### Việc 3 — Chạy vòng GVT 5 vòng và đo (XONG — số thật trên Kaggle T4)

Vòng GVT: generate (k=8 mẫu/đề) → verify (`math-verify`) → select (preset
`reward`) → train (LoRA r=16, alpha=32, SFT 1 epoch, **adapter mới từ base mỗi
vòng, không cộng dồn**) → lặp 5 vòng. 2 cỡ model: Qwen2.5-0.5B-Instruct và
1.5B-Instruct. 2 bộ đề: GSM8K + MATH-500 (500 đề/bộ).

**Kết quả chính — cả pass@1 lẫn pass@8 đều GIẢM đơn điệu qua các vòng:**

| Model | Vòng 0 | Vòng 4 | Δ |
|---|---|---|---|
| 0.5B pass@1 | 31.1% | 27.4% | −12% |
| 0.5B pass@8 | 60.5% | 54.9% | −9% |
| 1.5B pass@1 | 50.0% | 18.6% | **−63%** |
| 1.5B pass@8 | 72.6% | 48.6% | **−33%** |

- **Không khớp** cả 2 kịch bản dự đoán ban đầu ("giỏi đều lên" / "chỉ học lệch
  văn phong, năng lực đứng yên") → hậu quả là **sụp năng lực thật**.
- **Phản trực giác:** model 1.5B (gấp 3 lần tham số) sụp **nặng hơn hẳn** model
  0.5B.
- Tập mẫu được verifier chấp nhận **co hẹp dần**: 1.5B mất **60%** số mẫu qua 5
  vòng (3962 → 1566).
- Văn phong hội tụ: 1.5B dùng `\boxed{}` giảm hơn nửa (5608 → 2693 lần/vòng),
  `$...$` tăng hơn gấp đôi.
- Bảng A/B/C (1.5B): số đề *mất* (C) vượt số đề *mới giải được* (A) ở cả 4/4
  vòng, khoảng cách nới rộng mạnh 2 vòng cuối (C = 117 rồi 194) → sụp tăng tốc.

**Cơ chế đề xuất:** vòng lặp tự-siết qua tập huấn luyện co hẹp — mỗi vòng học
lại từ base chỉ trên tập verifier chấp nhận ở vòng trước; tập đó vừa nhỏ dần vừa
lệch về một kiểu viết; sai lệch **cộng dồn** thay vì tự triệt tiêu. Họ hàng gần
với "model collapse" nhưng xảy ra **ngay cả khi đã lọc qua verifier** tưởng-là-
đáng-tin.

Kết quả: `results/viec3/qwen05b-n500/table.md`, `results/viec3/qwen15b-n500/table.md`;
code: `src/dacntt/gvt/`, `experiments/viec3/run.py`.

### Bản thảo bài báo (XONG phần không cần thầy)

`papers/DRAFT.md` — đã viết đủ: Tiêu đề, Abstract, Introduction, Related Work
(đọc bản đầy đủ 4 bài gần nhất, không chỉ abstract), Method, Results (2 biểu đồ),
Discussion, Limitations, Conclusion, References (8 bài trích dẫn thật).

**Còn chờ thầy:** (1) ngôn ngữ nộp (Việt/Anh) và format trích dẫn (APA/IEEE…);
(2) đọc soát toàn bài lần cuối.

---

## 5. Sản phẩm và hướng hoàn thiện

**Sản phẩm:** một bài báo nghiên cứu (bản thảo đã có ở `papers/DRAFT.md`).

**Việc còn lại:** (1) lặp lại thí nghiệm nhiều seed để đo phương sai; (2) tách
train/test riêng (hiện `select` và `exam` cùng dùng tập test); (3) thử cỡ model
thứ ba (>1.5B) xem xu hướng "to hơn sụp nặng hơn" có tiếp tục; (4) chốt ngôn ngữ
+ format theo yêu cầu thầy rồi dịch/định dạng lại.

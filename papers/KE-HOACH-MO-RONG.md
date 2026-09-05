# Kế hoạch mở rộng — từ "2 lần chạy Kaggle" lên số liệu đứng vững trước hội đồng

> **Cập nhật 2026-09-04 (sau phản biện mô phỏng "hội đồng chấm"):** điểm ước
> tính ~7.6/10 *có điều kiện* — đúng nếu hoàn thành Giai đoạn 0–3. Phản biện
> chỉ ra thêm 2 lỗ hổng chưa có trong bản kế hoạch đầu: (1) phát hiện phụ ấn
> tượng nhất bài — "model to sụp nặng hơn" — vẫn chỉ là giả thuyết chưa đo
> trực tiếp; (2) ablation "không lọc" đang bị xếp *tuỳ chọn* trong khi nó là
> bằng chứng trung tâm để tách cơ chế của đề tài khỏi model collapse cổ điển.
> Đã thêm Giai đoạn 4 và 5 mới để vá hai chỗ này, đánh số lại các giai đoạn
> mở rộng cũ.

> **Cập nhật 2026-09-05 — Giai đoạn 0.2 và Giai đoạn 5 đã chạy thật (không
> cần GPU mới, tìm lại được `generations.jsonl` gốc từ Kaggle output của cả
> 2 lần chạy cũ):**
>
> **1. Tách pass@1/pass@k theo GSM8K vs MATH-500 — kết quả không ủng hộ rõ
> câu chuyện "verifier lệch gây sụp":**
>
> | | GSM8K pass@1 | MATH-500 pass@1 | GSM8K pass@8 | MATH-500 pass@8 |
> |---|---|---|---|---|
> | 0.5B | −18.9% | **+5.6% (tăng!)** | −10.6% | −6.8% |
> | 1.5B | −61.8% | −65.1% | −28.0% | −41.6% |
>
> Ở 0.5B, MATH-500 (verifier lệch) hầu như không đổi trong khi GSM8K (verifier
> sạch) sụp nhiều hơn — **ngược hướng** dự đoán. Ở 1.5B cả hai cùng sụp nặng,
> không tách bạch rõ theo verifier-bias. Đã kiểm tra thêm: tỉ lệ GSM8K/MATH-500
> trong tập được giữ để train mỗi vòng **ổn định ~68–70% suốt 5 vòng ở cả 2
> model** — loại được giả thuyết "nhiễu chéo do pool đổi tỉ lệ dataset".
> Nguyên nhân thật của mẫu hình này **vẫn chưa rõ**.
>
> **2. Đa dạng đáp án trước khi lọc qua verifier — ngược với giả thuyết ban
> đầu:** model không hội tụ vào 1 đáp án qua các vòng, mà **ngày càng phân
> tán hơn** (1.5B: 24.8% → 1.7% số đề có cả 8 lần ra cùng 1 đáp án). Đây là
> bằng chứng sụp năng lực thật, nhưng đòi hỏi viết lại Discussion §5.1 —
> không phải "hội tụ vào 1 kiểu trả lời" mà là "style hội tụ, nội dung đáp
> án phân tán". Xem `results/viec3/mechanism.md` và `results/viec3/*/by_dataset.md`.
>
> **Hệ quả cho ưu tiên:** Giai đoạn 0.2 (rẻ, đã làm) hoá ra **không đủ** để
> kết luận verifier-bias là nguyên nhân — kết quả mơ hồ/mâu thuẫn giữa 2
> model. Điều này **nâng Giai đoạn 1 (đối chứng verifier thật, kiểm soát
> đúng 1 biến) lên mức khẩn cấp nhất** trong toàn kế hoạch — hiện là thí
> nghiệm duy nhất còn khả năng trả lời được câu hỏi trung tâm của bài.

> **Cập nhật 2026-09-05, phần 2 — thiết kế lại Giai đoạn 1–2 sau khi thấy
> nhiễm chéo giữa 2 bộ đề.** Phát hiện ở bản cập nhật ngay trên (GSM8K sụp
> nhiều hơn MATH-500 ở 0.5B — ngược dự đoán) hoá ra có lý do kỹ thuật rõ:
> mọi lần chạy trước dùng `--dataset both`, tức **một adapter LoRA chung**
> train mỗi vòng trên **tập gộp cả hai bộ đề đã lọc**. Vì vậy hiệu năng trên
> GSM8K bị ảnh hưởng bởi đúng những gì xảy ra với phần MATH-500 trong cùng
> tập train (và ngược lại) — không có cách nào tách bạch "verifier lệch gây
> sụp" khỏi "nhiễm chéo giữa hai domain" từ số liệu đó.
>
> **Hướng nghiên cứu không đổi, nhưng thiết kế thí nghiệm đổi:** thay vì tiếp
> tục chạy `--dataset both` (đã có sẵn 2 lần, dùng làm số tham chiếu/pooled),
> **các lần chạy Track B tiếp theo chạy CÔ LẬP từng bộ đề riêng**
> (`--dataset gsm8k` hoặc `--dataset math500`, không gộp). Đây không phải
> đổi hướng — đây là sửa đúng lỗ hổng vừa lộ ra, và **thiết kế mới còn rẻ
> hơn thiết kế cũ**: mỗi lần chạy cô lập chỉ có n=500 (so với n=1000 gộp
> cả hai) → generate/train nhanh hơn khoảng một nửa. 3 lần chạy cô lập tốn
> tổng GPU-giờ **thấp hơn** 2 lần chạy gộp như kế hoạch cũ, mà lại tách bạch
> được đúng biến cần đo. Xem thiết kế mới ở Giai đoạn 1 (đã viết lại hoàn
> toàn) và Giai đoạn 2 bên dưới.
>
> **Vì sao đây là tin tốt cho sức thuyết phục của bài, không phải tin xấu:**
> nếu GSM8K cô lập (verifier gần sạch, không còn nhiễm MATH-500) vẫn sụp
> nặng, đó là bằng chứng đóng góp của bài **rộng hơn** dự kiến ban đầu —
> không chỉ "verifier lệch-vì-format gây sụp", mà "bản thân vòng lặp SFT
> nhiều vòng trên tập tự-lọc-co-hẹp đủ gây sụp năng lực, bất kể verifier có
> lệch hay không" — một claim tổng quát hơn, áp dụng cho cả họ phương pháp
> GVT/STaR/ReST-EM, không chỉ trường hợp verifier lệch. Nếu ngược lại (GSM8K
> cô lập ổn định, chỉ MATH-500 cô lập mới sụp), giả thuyết hẹp ban đầu được
> xác nhận sạch, không còn nghi ngờ gì về nhiễm chéo. **Cả hai kết quả đều
> làm bài mạnh hơn** — kết quả duy nhất làm bài yếu đi là không chạy thí
> nghiệm này và tiếp tục dùng số liệu gộp có nhiễm chéo.

Soạn 2026-09-04, sau khi tự đánh giá bài hiện tại (`papers/DRAFT.md`,
`papers/latex/paper.tex`) là **mỏng**: mỗi cấu hình model × bộ đề chỉ chạy
**1 lần**, không seed, `select`/`exam` dùng chung tập test, 2 bộ đề gộp
thành 1 số pass@1/pass@8, không giữ log sinh gốc (`generations.jsonl`) của
2 lần chạy thật trên Kaggle. Số liệu là thật, nhưng **không ai — kể cả
chính mình sau này — kiểm chứng lại được**. Đó là lý do "trông ảo".

Nguyên tắc xếp thứ tự: làm trước việc **rẻ** (không tốn GPU, hoặc tốn ít)
mà **tăng độ tin cậy nhiều**; để sau việc tốn GPU nhiều mà chỉ tăng thêm
diện phủ.

---



## Hiểu lầm cần tránh: KHÔNG lấy dataset của 4 bài đối trọng để chạy lại

4 bài dùng để "xoáy vào" khi lập luận (Teacher-Free Self-Training 2606.07856,
Delay/Plateau/Collapse 2605.02909, From Accuracy to Robustness 2505.22203,
ReST-EM 2312.06585) **không phải nguồn dữ liệu để tải về chạy qua pipeline
của mình**:

- Teacher-Free Self-Training: domain FlashFill (sinh chương trình), không
phải toán, không có file dataset chuẩn — tái lập tốn ngang một đề tài phụ,
không liên quan câu hỏi của bài (hiện tượng lệch-vì-format chỉ xảy ra ở
toán có LaTeX/phân số).
- Delay, Plateau, or Collapse: verifier **mô phỏng** (tự chỉnh tỉ lệ lỗi giả
lập) trên số học tổng hợp — không phải dataset thật, và pipeline của họ là
RLVR 1 vòng, khác kiến trúc SFT nhiều vòng của bài này.
- From Accuracy to Robustness: dùng toán thật nhưng verifier/harness cụ thể
không chắc tái lập đúng được — dùng số họ **công bố** (recall ~86%) để đối
chiếu là đủ, không cần chạy lại.
- ReST-EM: dùng MATH (cùng nguồn Hendrycks MATH mà MATH-500 của bài này cũng
lấy từ đó) — **không cần lấy về**, bài này đã ở cùng benchmark rồi.

Bằng chứng thực nghiệm thật sự ("chạy train và đo để so sánh") không đến từ
việc tái lập domain của 4 bài kia — mà đến từ **thí nghiệm đối chứng ở Giai
đoạn 1 bên dưới, chạy trên đúng dữ liệu của bài này** (MATH-500/GSM8K, chỉ
đổi verifier gốc ↔ verifier đã vá). Thí nghiệm đó tái tạo lại bên trong một
bài đúng cái đối lập mà Teacher-Free Self-Training gợi ý (verifier sạch →
chỉ khuếch đại; verifier lệch → sụp thật), nhưng có kiểm soát biến thật, thay
vì so sánh khập khiễng giữa hai domain khác nhau. 4 bài kia dùng làm **điểm
neo lập luận trong Related Work/Discussion**, không phải nguồn dữ liệu.

---



## Vấn đề lớn nhất, chưa ai nói tới: bài chưa có nhóm đối chứng

Bài hiện tại chứng minh: chạy GVT với `math-verify` (verifier lệch) → sụp.
Nhưng **chưa chứng minh** chính cái lệch gây ra sụp, chứ không phải bản
thân việc "mỗi vòng train lại từ base trên tập ngày càng hẹp" tự nó đã đủ
gây sụp, bất kể verifier tốt hay xấu. Đây là lỗ hổng nhân quả — không phải
lỗi trình bày, mà là lỗi lập luận khoa học. Nếu hội đồng hỏi "sao biết là
tại verifier lệch, không phải tại chính cơ chế lặp vòng?", hiện bài
**không có câu trả lời bằng số liệu**.

Kế hoạch dưới đây ưu tiên vá đúng chỗ này trước.

---



## Giai đoạn 0 — Sửa hạ tầng, không tốn GPU (làm ngay tuần này)

1. **Giữ lại log sinh gốc.** Từ nay, mọi lần chạy `experiments/viec3/run.py`
  phải lưu `generations.jsonl` (mỗi dòng có `dataset`, `round`, `problem_id`,
   lời giải, kết quả verify) về máy/Drive, không chỉ giữ bảng gộp
   `table.md`. Không có file này thì không việc nào ở Giai đoạn 1–3 làm lại
   được nếu cần soát.
2. **Kiểm tra 2 lần chạy cũ có còn log gốc không** (trên Kaggle output, notebook
  version history, hoặc bất cứ đâu đã tải về). Nếu còn: tách ngay pass@1/pass@8
   theo **từng bộ đề riêng** (GSM8K vs MATH-500) thay vì số gộp — đây là việc
   **giá trị cao nhất, chi phí gần bằng 0**, vì code đã gắn nhãn `dataset` cho
   từng bản ghi (`experiments/viec3/run.py:279`), chỉ cần lọc lại, không cần
   chạy GPU. Nếu GSM8K (verifier gần sạch, FN≈0%) sụp ít hơn hẳn MATH-500
   (verifier lệch, FN≈7.8%) trong cùng vòng lặp — đó là bằng chứng nhân quả
   trực tiếp, lấy từ dữ liệu đã có.
3. **Cố định và ghi lại seed** cho mọi lần chạy tới (`--seed` nếu code đã hỗ
  trợ, nếu chưa thì thêm — xem `experiments/viec3/run.py`), cùng đúng phiên
   bản thư viện (`math-verify`, `transformers`, `peft`, `trl`) vào mỗi
   `manifest.json`. Đây là thứ hội đồng hỏi đầu tiên khi nghi ngờ số liệu:
   "chạy lại có ra số y hệt không?"

Nếu (2) tách được số theo bộ đề và cho kết quả đúng hướng, bài đã **mạnh hơn
hẳn** mà chưa tốn một GPU-giờ nào của Giai đoạn 1.

1. **Sanity-check vòng 0 với số Qwen công bố chính thức** (không tốn GPU —
  đã có số vòng 0, chỉ cần tra và so). Đã tra (2026-09-04, blog chính thức
   Qwen2.5-LLM):

  | Model         | GSM8K công bố | MATH công bố | TB ước lượng | Vòng 0 của bạn (gộp) |
  | ------------- | ------------- | ------------ | ------------ | -------------------- |
  | 0.5B-Instruct | 49.6%         | 34.4%        | ~42.0%       | 31.1%                |
  | 1.5B-Instruct | 73.2%         | 55.2%        | ~64.2%       | 50.0%                |

   Đúng chiều (1.5B > 0.5B, đúng tỉ lệ tương đối) nhưng **thấp hơn công bố
   10–14 điểm** ở cả hai model — cần làm rõ trước khi coi số vòng 0 là mốc
   sạch để so sánh các vòng sau. Nghi vấn hàng đầu: pass@1 ở đây tính trên
   **1 mẫu sampling ngẫu nhiên** (để còn tính pass@8), không phải greedy
   decoding như benchmark chính thức thường dùng; và `max_tokens=512` có
   thể cắt cụt lời giải MATH-500 dài. Cần: (a) ghi rõ trong Method đây là
   sampling-based pass@1, không phải greedy — không so trực tiếp bằng số
   với bảng Qwen mà chỉ dùng để kiểm tra thứ hạng/độ lớn hợp lý; (b) thử lại
   với `max_tokens` cao hơn cho một mẫu nhỏ MATH-500 để loại trừ khả năng
   cắt cụt là nguyên nhân chính của khoảng lệch.

---



## Giai đoạn 1 — Ba lần chạy cô lập từng bộ đề (ưu tiên cao nhất, cần GPU)

**Thiết kế cũ (đã bỏ):** chạy đối chứng verifier trên `--dataset both` (gộp
GSM8K+MATH-500). Bỏ vì phát hiện 2026-09-05: `--dataset both` khiến một
adapter chung train mỗi vòng trên tập gộp đã lọc — nhiễm chéo giữa hai
domain, không tách được "tại verifier lệch" khỏi "tại lây từ bộ kia". Xem
khối cập nhật đầu file.

**Thiết kế mới — cô lập hoàn toàn, 3 lần chạy, đều `--holdout-frac 0.3`
(gộp luôn việc tách train/test của Giai đoạn 2 cũ vào đây, không tốn thêm
lượt chạy riêng):**

| Chạy | `--dataset` | `--patch-verifier` | Trả lời câu hỏi gì |
|---|---|---|---|
| **A** | `math500` | không | MATH-500 một mình (không lẫn GSM8K), verifier gốc — có sụp không, sụp bao nhiêu khi không còn nhiễm chéo? Đây cũng là **số headline MATH-500 mới**, đã tách train/test. |
| **B** | `math500` | **có** | Y hệt A, chỉ đổi verifier (vá `\dfrac`/`\tfrac`) — **control thật**, đúng một biến khác A. So sánh A vs B trả lời trực tiếp "verifier lệch có phải nguyên nhân". |
| **C** | `gsm8k` | không | GSM8K một mình (không lẫn MATH-500), verifier gốc — verifier ở đây gần như không lệch (FN≈0%). Nếu C vẫn sụp nặng ngang A, đó là bằng chứng cơ chế **không đặc thù cho verifier lệch** — sụp xảy ra ngay cả khi verifier gần sạch, miễn còn vòng lặp SFT trên tập tự-lọc-co-hẹp. |

**Vì sao không cần chạy patch-verifier trên GSM8K:** `\dfrac`/`\tfrac` gần
như không xuất hiện trong lời giải GSM8K (đáp án nguyên, không cần phân số
LaTeX) — vá verifier ở đó gần như không đổi gì, tốn 1 lượt chạy mà không ra
thêm thông tin.

**Đọc kết quả theo bảng quyết định:**

| A (MATH500 gốc) | B (MATH500 vá) | C (GSM8K gốc) | Kết luận |
|---|---|---|---|
| Sụp | Đỡ sụp rõ rệt | Không sụp | Giả thuyết hẹp ban đầu **đúng sạch** — verifier lệch là nguyên nhân chính, hết nghi ngờ nhiễm chéo. |
| Sụp | Đỡ sụp rõ rệt | **Cũng sụp** | Cả hai đều đúng một phần: verifier lệch làm nặng thêm (A vs B khác nhau), nhưng có một cơ chế nền khác cũng gây sụp độc lập với verifier (C sụp dù verifier sạch). Claim cần nới rộng. |
| Sụp | **Sụp tương tự A** | Sụp | Verifier lệch **không phải** nguyên nhân chính — đổi hướng đóng góp sang "vòng lặp SFT nhiều vòng trên tập tự-lọc-co-hẹp tự nó đủ gây sụp, bất kể verifier" — claim **rộng hơn**, áp dụng cho cả họ GVT/STaR/ReST-EM. |

Không có ô nào trong bảng trên là "hỏng đề tài" — ô nào cũng cho một câu
chuyện viết được, chỉ khác mức độ rộng/hẹp của claim chính.

**Chi phí ước tính:** 3 lần chạy, mỗi lần n=500 (một bộ đề, không gộp) — mỗi
lần ước tính **nhẹ hơn khoảng một nửa** so với 1 lần chạy `--dataset both`
cũ (n=1000). Tổng 3 lần cô lập ước tính **thấp hơn hoặc tương đương** 2 lần
chạy gộp của thiết kế cũ (Giai đoạn 1 + 2 cũ cộng lại), mà tách bạch được
đúng biến, không nhiễm chéo, và có luôn train/test split.

**Lưu ý:** cả 3 lần đều mới chạy 1 seed — kết luận nhân quả vẫn sơ bộ cho tới
khi có Giai đoạn 3 (lặp seed) trên đúng cấu hình được chọn làm headline sau
khi thấy A/B/C ra sao.

---

---



## Giai đoạn 2 — Lặp seed cho cấu hình headline (bắt buộc, chi phí thấp)

Chờ kết quả A/B/C ở Giai đoạn 1 trước khi chọn đúng cấu hình cần lặp seed —
nhiều khả năng là run A hoặc B trên MATH-500 (nơi câu chuyện chính — verifier
lệch — xảy ra), vì đó sẽ là con số headline chính của bài dù kết luận rơi
vào ô nào trong bảng quyết định ở Giai đoạn 1. Chạy thêm **2 seed nữa** cho
đúng cấu hình đó (1.5B, `--dataset math500`, cùng `--holdout-frac`), báo cáo
trung bình ± độ lệch chuẩn qua 3 seed thay vì một đường cong đơn.

**Chi phí ước tính:** 2 lần chạy, mỗi lần n=500 (một bộ đề) — rẻ hơn ước
tính cũ vì không còn chạy `--dataset both`.

---

## Giai đoạn 3 — Ablation "không lọc" (nâng lên gần-bắt buộc sau phản biện)

Bản kế hoạch đầu xếp việc này vào mục tuỳ chọn (4.1 cũ). Phản biện chỉ ra đây
là **bằng chứng trung tâm**, không phải mở rộng cho đẹp: nó là thứ duy nhất
tách được cơ chế của đề tài (co hẹp + lệch qua lọc verifier) khỏi model
collapse cổ điển (co hẹp do train trên toàn bộ phân phối tự sinh, không lọc)
— hiện mục 5.1 Discussion chỉ *lập luận bằng chữ* cho sự khác biệt này, chưa
có số.

**Thiết kế:** chạy đúng vòng GVT, giữ nguyên mọi thứ, nhưng bỏ bước `select`
— train trên **toàn bộ** k=8 lời giải mỗi vòng, không lọc qua verifier.

**Đọc kết quả:**

- Nếu "không lọc" sụp **nặng hơn hẳn** "lọc qua verifier lệch" → lọc bằng
verifier lệch vẫn tốt hơn không lọc gì, dù không tốt bằng verifier sạch —
củng cố khung "mức độ lệch quyết định mức độ sụp", một phổ chứ không phải
nhị phân.
- Nếu "không lọc" sụp **tương đương hoặc nhẹ hơn** "lọc qua verifier lệch" →
phát hiện phản trực giác mạnh hơn cả bài chính: lọc bằng một verifier lệch
còn *tệ hơn* không lọc gì — vì lọc tạo ảo giác "đã chọn được cái tốt" trong
khi thực chất đang cô đặc dần vào đúng kiểu verifier ưa. Đáng để là một
phát hiện độc lập trong Results, không chỉ Discussion.

**Chi phí ước tính:** 1 lần chạy (bước `generate` có thể tái dùng từ Giai
đoạn 1 nếu cùng cấu hình dataset/model, chỉ cần chạy lại `select`+`train`+`exam`
với `--no-filter`).

---

## Giai đoạn 4 — Cơ chế "model to sụp nặng hơn" (đã làm được một nửa, không cần GPU thêm)

Đây là phát hiện phụ ấn tượng nhất bài nhưng ban đầu **hoàn toàn chưa kiểm
chứng trực tiếp** — mục 5.2 Discussion chỉ đưa giả thuyết "model to fit
nhanh và chặt hơn vào tập hẹp" rồi tự thừa nhận "chưa chứng minh trực tiếp".

**Cập nhật 2026-09-05 — phần 1 đã xong, dùng lại log gốc tìm được từ Kaggle:**

- ✅ **Độ đa dạng đáp án trước khi lọc qua verifier** — đã chạy
  (`experiments/viec3/analyze_mechanism.py`, kết quả ở
  `results/viec3/mechanism.md`). Phát hiện: **ngược** giả thuyết ban đầu —
  model không hội tụ vào 1 đáp án mà ngày càng phân tán hơn (1.5B: 24.8%→
  1.7% số đề có cả 8 lần ra cùng 1 đáp án). Đã đưa vào `paper.tex` §4.5 +
  sửa Discussion §5.1 (bản nháp, chờ chốt sau khi có A/B/C).
- ⬜ **Train loss theo từng vòng** — chưa đo được, vì log này
  (`train_logs/round_*.json`) là tính năng mới thêm 2026-09-04, 2 lần chạy
  cũ không có. Sẽ tự động có từ Giai đoạn 1 (A/B/C) trở đi — không tốn GPU
  riêng, chỉ cần `python -m experiments.viec3.analyze_mechanism` sau khi có
  log của A/B/C.

**Chi phí ước tính:** ~0 GPU-giờ thêm — phần diversity đã dùng lại được data
cũ, phần train-loss ăn theo Giai đoạn 1.

---

## Giai đoạn 5 — Mở rộng diện phủ (làm nếu còn ngân sách/thời gian, không bắt buộc)

Xếp theo giá trị giảm dần:

1. **Thêm 1 cỡ model thứ ba** (ví dụ Qwen2.5-3B-Instruct, 4-bit nếu cần vừa
  T4) — kiểm tra xu hướng "to hơn sụp nặng hơn" có tiếp tục hay có điểm đảo
   chiều. Chi phí cao nhất trong danh sách (model to hơn = train/generate
   chậm hơn nhiều trên T4).
2. **Chạy dài hơn 5 vòng** (8–10 vòng) cho riêng 1.5B — xem đường cong có
  chững lại/hồi phục hay tiếp tục giảm. Rẻ nếu tận dụng checkpoint sẵn có
   (chạy tiếp từ vòng 4, không chạy lại từ đầu).
3. **Một họ model khác ngoài Qwen** (ví dụ Llama hoặc Gemma cỡ nhỏ) — phản
  biện chỉ ra bài chỉ đo trên 1 họ model, không biết hiện tượng có đặc thù
   riêng của Qwen không. Chi phí cao (harness sinh/prompt template phải làm
   lại cho model khác) — chỉ làm nếu còn nhiều thời gian, nếu không thì ghi
   thẳng vào Limitations thay vì bỏ qua.

---



## Định vị đúng khi viết — đừng để phản biện overclaim thay bạn

Ngay cả sau khi làm hết Giai đoạn 0–4, bài vẫn chỉ đo trên: 1 họ model
(Qwen), 1 verifier (`math-verify`), 1 phương pháp train (LoRA SFT, không so
với RL/GRPO — nhánh self-improve phổ biến nhất hiện nay). Khi viết
Conclusion/Abstract, tránh câu kiểu "chúng tôi chứng minh verifier lệch luôn
gây sụp năng lực" (quá rộng) — dùng đúng phạm vi đã đo: "trong phạm vi
self-training bằng SFT-lọc trên model Qwen2.5 cỡ nhỏ với verifier luật cho
toán, chúng tôi đo được...". Một giới hạn được tự nhận đúng phạm vi trước
khi hội đồng hỏi luôn mạnh hơn một câu kết luận rộng bị vặn lại thành điểm
yếu.

---



## Tổng ngân sách GPU ước tính (Kaggle T4, free tier ~30h/tuần)


| Giai đoạn | Số lần chạy (n=500, cô lập từng bộ) | Bắt buộc? |
| --- | --- | --- |
| 0 | 0 (chỉ xử lý log có sẵn — **đã xong**) | **Có** |
| 1 (A/B/C — cô lập từng bộ + đối chứng verifier) | 3 | **Có** — vá cả lỗ hổng nhân quả lẫn nhiễm chéo |
| 2 (2 seed cho cấu hình headline) | 2 | **Có** |
| 3 (ablation không lọc) | 1 | **Nên làm** |
| 4 (đo cơ chế overfit) | 0 — diversity **đã xong**, loss ăn theo GĐ 1 | **Nên làm** — phần rẻ đã xong |
| 5.1 (model thứ 3) | 1–2 | Tuỳ thời gian còn lại |
| 5.2 (chạy dài hơn) | ~0.5 (chạy tiếp) | Tuỳ thời gian còn lại |
| 5.3 (họ model khác) | 2+ | Chỉ nếu dư thời gian nhiều |

Tổng tối thiểu (0–4): **6 lần chạy** n=500 (cô lập, không gộp) — nhiều hơn
số lượt (5→6) nhưng mỗi lượt chỉ bằng một nửa quy mô `--dataset both` cũ, nên
**tổng GPU-giờ ước tính thấp hơn hoặc tương đương** kế hoạch trước, và tách
bạch được đúng biến thay vì để nhiễm chéo. Đây là phần **quyết định độ đứng
vững** của claim chính, không phải phần mở rộng cho đẹp.

---



## Nếu hết thời gian trước ngày báo cáo: làm gì trước

Thứ tự không thể bỏ, theo đúng mức độ "hội đồng sẽ hỏi trước":

1. Giai đoạn 0 — **đã xong** (log gốc tìm lại được, đã phân tích).
2. Giai đoạn 1, chạy A trước (MATH-500 cô lập, verifier gốc) — nếu chỉ chạy
  được **một** thí nghiệm nữa trước hạn, chạy cái này trước, vì nó vừa là số
   headline mới vừa là mốc so sánh cho B và C.
3. Giai đoạn 1, chạy C (GSM8K cô lập) — nếu chạy được thí nghiệm thứ hai,
  chạy cái này trước B. C trả lời câu hỏi lớn hơn ("có phải verifier lệch
   là nguyên nhân, hay do chính cơ chế lặp vòng") — quan trọng hơn B (vốn chỉ
   kiểm tra 1 chỗ vá cụ thể) nếu phải chọn.
4. Giai đoạn 1, chạy B (MATH-500 cô lập, verifier vá) — hoàn thiện bộ 3, cho
  phép so sánh A vs B đúng nghĩa control.
5. Giai đoạn 2 (seed) — nếu còn GPU cho một việc nữa, làm việc này, vì số
  headline đứng một mình (1 seed) quá mỏng manh.
6. Giai đoạn 3 (ablation không lọc) — nếu còn một lượt chạy nữa.
7. Giai đoạn 4 (đo cơ chế overfit) — phần diversity **đã xong**; phần loss tự
  có khi chạy xong Giai đoạn 1, không cần lượt chạy riêng.
8. Còn lại (Giai đoạn 5), nếu không kịp: **nói thẳng trong phần Limitations**
  rằng đây là giới hạn đã biết, có kế hoạch cụ thể — và dùng đúng cách
   "Định vị đúng khi viết" ở trên để không bị vặn thành điểm yếu bị giấu.


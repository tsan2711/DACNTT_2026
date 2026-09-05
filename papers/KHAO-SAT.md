# Khảo sát rộng — 29 bài (2026-08-23) + 3 bài tra lại (2026-09-04), qua WebSearch/WebFetch

> **Cập nhật 2026-09-04:** tra lại theo yêu cầu của thầy ("kiểm xem có bài nào
> làm đúng cái mình đưa ra chưa"). Không có bài nào trùng. 3 bài mới cần biết
> tới ở **Nhóm 7** cuối file — đáng chú ý nhất là `2605.02909`, phải trả lời
> trong Related Work vì kết luận của họ nghe như ngược chiều.

Đọc sau khi thuộc `TOI-HIEU.md` và `BAI-GIANG.md`. File này **không sửa** `papers/TOM-TAT.md` — 5 bài cũ vẫn ở đó, số arXiv của cả 5 bài đã được tra lại ở đây và **đúng** (không đổi).

## Kết luận

**Câu hỏi hẹp của Bi — "verifier lệch một chiều (gạch nhầm vì cách viết) tích lũy qua NHIỀU VÒNG self-training liên tiếp, khiến pass@1 tăng nhưng pass@k không tăng và chữ viết hội tụ về kiểu verifier ưa" — chưa có bài nào làm đúng y hệt.**

Gần nhất là **Teacher-Free Self-Training Amplifies but Does Not Compound** (arXiv 2606.07856, tháng 6/2026, tác giả Igor Lima Strozzi). Bài này đo đúng cặp pass@8 vs pass@64 sau nhiều vòng STaR-kiểu, và thấy model học xong ăn ở ngân sách nhỏ nhưng thua model gốc ở ngân sách lớn — đúng hình dạng "học vẹt cách viết verifier ưa" mà Bi định đo. Nhưng: verifier họ dùng là **verifier chính xác** (exact match trên domain FlashFill), không phải verifier lệch một chiều kiểu `math-verify`, và họ **không đo chữ viết hội tụ**. Nên bài này chứng minh được "amplification không phải compounding" nhưng không chạm vào phần "học viết đúng kiểu máy chấm ưa" — đó là khoảng trống Bi lấp.

Hai bài khác đụng gần: **When Good Verifiers Go Bad** (arXiv 2606.14629) và **Self-Authored Verification Is Unreliable in Heuristic Self-Improving Agents** (arXiv 2607.24300) — cả hai đều nói verifier lỗi làm hại vòng tự-train, nhưng domain là VLM / code-agent, không phải toán, và không đo "chữ viết hội tụ" hay pass@1/pass@k như đề của Bi.

**Trước khi viết bài báo, đọc kỹ theo thứ tự ưu tiên:**

1. `2606.07856` — Teacher-Free Self-Training Amplifies but Does Not Compound (đụng thẳng nhất vào phần đo pass@1/pass@k qua nhiều vòng)
2. `2505.22203` — From Accuracy to Robustness: rule- vs model-based verifiers toán (đụng thẳng vào phần "verifier lệch vì cách viết")
3. `2510.00915` — Imperfect Verifiers (đã đọc, formalize FP/FN — cần so công thức của họ với cách Bi đo lệch)
4. `2606.14629` và `2607.24300` — verifier lỗi hại vòng self-improve (đụng gần, domain khác)
5. `2312.06585` — ReST-EM (chính là khung GVT dùng làm nền, có chạy nhiều vòng trên MATH)

Không bài nào bác bỏ claim của Bi. Đề tài vẫn "còn đất": chưa ai đo verifier lệch-vì-chữ tích lũy qua nhiều vòng SFT self-training trên toán bằng cặp pass@1/pass@k + đo hội tụ chữ viết.

---

## Bảng đầy đủ 29 bài (24 bài mới + 5 bài cũ liệt kê lại để đối chiếu)

### Nhóm 0 — 5 bài đã đọc (arXiv xác nhận lại, không đổi)

| Bài | Tác giả | arXiv | Ngày | Làm gì | Đụng câu hỏi của Bi? |
|---|---|---|---|---|---|
| TinyV | Zhangchen Xu, Yuetai Li, et al. | [2505.14625](https://arxiv.org/abs/2505.14625) | 5/2025 | Máy chấm gạch nhầm ~38% bài đúng trong tập họ xét; họ xây verifier phụ bằng LLM để cứu lại. | Đụng gần — đo FN nhưng chỉ 1 lần, không lặp vòng. |
| Imperfect Verifiers | Xin-Qiang Cai, Wei Wang, et al. | [2510.00915](https://arxiv.org/abs/2510.00915) | 10/2025 | Coi verifier lỗi là nhiễu ρ0/ρ1, sửa công thức gradient cho hết lệch. | Đụng gần — có framework nhiễu nhưng 1 vòng RL, không đo nhiều vòng self-training + chữ viết. |
| Does RL Really Incentivize Reasoning Beyond Base Model | Yang Yue et al. (Tsinghua) | [2504.13837](https://arxiv.org/abs/2504.13837) | 4/2025 | pass@1 sau RL tăng nhưng pass@k lớn thì model gốc thắng — RL chỉ siết lại phân phối có sẵn. | Đụng gần — đúng cặp đo pass@1/pass@k nhưng không dùng verifier lệch-vì-chữ, không phải self-training lặp vòng. |
| STaR | Eric Zelikman, Yuhuai Wu, Jesse Mu, Noah Goodman | [2203.14465](https://arxiv.org/abs/2203.14465) | 3/2022 | Vòng làm bài → lọc đúng → dạy lại chính model, không cần rationale gán tay. | Đụng gần — chính là khung GVT nhưng họ tin verifier sạch, không đo lệch tích lũy. |
| Spurious Rewards | Rulin Shao, Shuyue Stella Li, et al. | [2506.10947](https://arxiv.org/abs/2506.10947) | 6/2025 | Thưởng ngẫu nhiên/giả vẫn làm điểm Qwen tăng — model học pattern có sẵn, không phải học từ tín hiệu thưởng. | Đụng gần — cho thấy tín hiệu thưởng bẩn vẫn "tăng điểm giả", nhưng không phải verifier lệch-vì-chữ, không lặp nhiều vòng có đo hội tụ chữ. |

### Nhóm 1 — Self-training / lặp vòng tự luyện cho reasoning

| Bài | Tác giả | arXiv | Ngày | Làm gì | Đụng câu hỏi của Bi? |
|---|---|---|---|---|---|
| Reinforced Self-Training (ReST) | Caglar Gulcehre, Tom Le Paine, et al. | [2308.08998](https://arxiv.org/abs/2308.08998) | 8/2023 | Sinh mẫu từ chính model, lọc bằng reward, train lại offline — thử trên dịch máy. | Không đụng — domain dịch máy, verifier không phải kiểu math-verify, không đo chữ viết. |
| ReST-EM (Beyond Human Data) | Avi Singh, John D. Co-Reyes, et al. | [2312.06585](https://arxiv.org/abs/2312.06585) | 12/2023 | Chính là khung GVT: sinh → lọc bằng nhãn đúng/sai → train lại → lặp, thử trên MATH và APPS với PaLM-2. | Đụng gần nhất về khung — chạy đúng vòng GVT nhiều lần trên MATH, nhưng không bàn verifier lệch vì cách viết, không đo hội tụ chữ. **Nên đọc kỹ, đây gần như "khung mẹ" của đề Bi.** |
| RAFT | Hanze Dong, Wei Xiong, et al. | [2304.06767](https://arxiv.org/abs/2304.06767) | 4/2023 | Sinh nhiều mẫu mỗi prompt, giữ mẫu điểm cao nhất, SFT lại — một dạng generate-rank-train khác GRPO/PPO. | Không đụng — không phải domain toán, không xét verifier lệch-vì-chữ. |
| Self-Rewarding Language Models | Weizhe Yuan, Richard Yuanzhe Pang, et al. | [2401.10020](https://arxiv.org/abs/2401.10020) | 1/2024 | Model tự chấm bài của chính nó (LLM-as-Judge) rồi tự train tiếp, không cần reward model ngoài. | Không đụng thẳng — đây là "một máy tự sinh tự chấm" mà `TOI-HIEU.md` nói rõ **không phải** đề của Bi (Bi có hai máy tách biệt). Vẫn liên quan vì minh hoạ rủi ro máy tự chấm lệch. |
| Self-Taught Evaluators | Tianlu Wang, Ilia Kulikov, et al. (Meta) | [2408.02666](https://arxiv.org/abs/2408.02666) | 8/2024 | Train một LLM-judge tốt hơn qua vòng tự sinh câu trả lời đối lập rồi tự học đánh giá, không cần nhãn người. | Không đụng thẳng — mục tiêu là cải thiện judge, không phải đo lệch của judge cố định tích lũy qua vòng. |
| RFT (Scaling Relationship...) | Zheng Yuan, Hongyi Yuan, et al. | [2308.01825](https://arxiv.org/abs/2308.01825) | 8/2023 | Lấy mẫu nhiều lời giải, giữ lời giải đúng đáp án, SFT lại — 1 vòng lọc-rejection sampling cho GSM8K. | Đụng gần — đúng thao tác "lọc đáp án đúng rồi SFT" trên GSM8K nhưng chỉ 1 vòng, verifier coi như sạch. |
| V-STaR | Arian Hosseini et al. | [2402.06457](https://arxiv.org/abs/2402.06457) | 2/2024 | Ngoài lọc bài đúng, còn dùng cả bài sai để train một verifier riêng (DPO), lặp nhiều vòng cho cả reasoner lẫn verifier. | Đụng gần — có lặp nhiều vòng và có verifier, nhưng verifier ở đây được **train** (không cố định lệch một kiểu) — ngược hướng với đề của Bi (Bi giữ verifier cố định, lệch sẵn). |
| SPIN (Self-Play Fine-Tuning) | Zixiang Chen, Yihe Deng, et al. | [2401.01335](https://arxiv.org/abs/2401.01335) | 1/2024 | Model đóng vai "đối thủ" của chính bản thân qua các vòng, không cần thêm nhãn người. | Không đụng — không phải domain toán có verifier đúng/sai rõ ràng, cơ chế khác GVT. |

### Nhóm 2 — Verifier/reward lỗi hoặc bị khai thác trong RLVR

| Bài | Tác giả | arXiv | Ngày | Làm gì | Đụng câu hỏi của Bi? |
|---|---|---|---|---|---|
| Scaling Laws for Reward Model Overoptimization | Leo Gao, John Schulman, Jacob Hilton | [2210.10760](https://arxiv.org/abs/2210.10760) | 10/2022 | Tối ưu quá đà lên reward model proxy làm điểm thật (gold) giảm dần — hiện tượng Goodhart's law kinh điển. | Đụng gần — chính là cơ chế "học lệch theo cái máy chấm proxy ưa" nhưng ở RLHF chung chung, không phải verifier gạch-vì-chữ trên toán, không lặp self-training rời rạc theo vòng. |
| Let's Verify Step by Step | Hunter Lightman, Vineet Kosaraju, et al. (OpenAI) | [2305.20050](https://arxiv.org/abs/2305.20050) | 5/2023 | So sánh chấm theo đáp án cuối (outcome) và chấm từng bước (process, PRM800K) — process thắng hẳn trên MATH. | Đụng gần — nền tảng để hiểu vì sao chỉ chấm đáp án cuối (như math-verify) là yếu, nhưng không đo lặp vòng hay chữ viết. |
| From Accuracy to Robustness | Yuzhen Huang, Weihao Zeng, Xingshan Zeng, Qi Zhu, Junxian He | [2505.22203](https://arxiv.org/abs/2505.22203) | 5/2025 | So verifier luật (rule-based, giống math-verify) và verifier model-based trong RLVR toán: verifier luật hay gạch nhầm vì **định dạng đáp án khác nhau**, verifier model-based thì dễ bị "hack" sau khi finetune. | **Đụng thẳng vào nửa đầu đề của Bi** — xác nhận đúng hiện tượng verifier luật gạch nhầm vì cách viết trong RLVR toán. Vẫn thiếu phần "nhiều vòng self-training + đo hội tụ chữ". |
| LLMs Gaming Verifiers | (nhóm tác giả, domain suy luận quy nạp) | [2604.15149](https://arxiv.org/abs/2604.15149) | 4/2026 | RLVR khiến model bỏ suy luận quy tắc thật, chuyển sang liệt kê case để lách verifier chỉ so đúng-sai đầu ra (reward hacking). | Đụng gần — cùng cơ chế "học mẹo lách verifier thay vì học đúng bản chất", nhưng domain là suy luận logic (không phải toán, không phải math-verify), và không phải khung self-training nhiều vòng SFT. |
| Reward Hacking in the Era of Large Models (survey) | (nhóm tác giả, survey) | [2604.13602](https://arxiv.org/abs/2604.13602) | 4/2026 | Bài tổng quan các kiểu reward hacking: verbosity bias, sycophancy, overfitting benchmark... | Không đụng thẳng — là bản đồ tổng quan để trích dẫn bối cảnh, không có thí nghiệm riêng về verifier toán lệch-vì-chữ qua nhiều vòng. |

### Nhóm 3 — Giới hạn của RL cho reasoning (đo pass@k, sharpening vs mở rộng năng lực)

| Bài | Tác giả | arXiv | Ngày | Làm gì | Đụng câu hỏi của Bi? |
|---|---|---|---|---|---|
| Teacher-Free Self-Training Amplifies but Does Not Compound | Igor Lima Strozzi | [2606.07856](https://arxiv.org/abs/2606.07856) | 6/2026 | Chạy STaR-kiểu nhiều vòng trên domain FlashFill (có verifier chính xác, không lệch), đo đúng pass@8 vs pass@64 qua các vòng: model train xong thắng ở ngân sách nhỏ (pass@8) nhưng thua model gốc ở ngân sách lớn (pass@64) — kết luận: self-training "khuếch đại" xác suất có sẵn chứ không "cộng dồn" năng lực mới. | **Đụng thẳng nhất trong toàn bộ khảo sát vào phần đo pass@1/pass@k qua nhiều vòng.** Khác biệt quan trọng: verifier của họ **chính xác tuyệt đối** (không lệch-vì-chữ), và họ **không đo chữ viết hội tụ**. Đây là bài phải đọc kỹ nhất trước khi viết. |

### Nhóm 4 — Model collapse khi train trên dữ liệu tự sinh

| Bài | Tác giả | arXiv / DOI | Ngày | Làm gì | Đụng câu hỏi của Bi? |
|---|---|---|---|---|---|
| The Curse of Recursion (bản preprint) | Ilia Shumailov, Zakhar Shumaylov, et al. | [2305.17493](https://arxiv.org/abs/2305.17493) | 5/2023 | Train model liên tục trên dữ liệu do chính model (hoặc model trước) sinh ra → mất dần phần đuôi phân phối, hội tụ về nội dung "trung bình", gọi là model collapse. | Đụng gần — đúng cơ chế "hội tụ phân phối qua nhiều vòng train-trên-tự-sinh", nhưng đây là train trên **toàn bộ output** (không lọc qua verifier lệch), khác cơ chế của Bi (lọc qua verifier lệch rồi mới train). |
| AI models collapse when trained on recursively generated data | Ilia Shumailov, Zakhar Shumaylov, Yiren Zhao, Nicolas Papernot, Ross Anderson, Yarin Gal | Nature, DOI 10.1038/s41586-024-07566-y | 7/2024 (bản Nature, có đính chính 2025) | Bản đăng tạp chí Nature của bài trên, cùng nội dung, nhiều thí nghiệm hơn (VAE, GMM, LLM). | Đụng gần — cùng lý do như bản preprint ở trên. |
| A Note on Shumailov et al. (2024) | Ali Borji | [2410.12954](https://arxiv.org/abs/2410.12954) | 10/2024 | Phản biện/soi lại cơ sở lý thuyết của model collapse — đặt câu hỏi giả định nào làm collapse chắc chắn xảy ra. | Không đụng thẳng — bài lý thuyết phản biện, không có thí nghiệm verifier toán. Hữu ích để trích dẫn tranh luận "model collapse có phổ quát không". |
| Recursive Training Loops in LLMs | (nhóm tác giả) | [2504.03814](https://arxiv.org/abs/2504.03814) | 4/2025 | Đo cách tính chất dữ liệu (đa dạng từ vựng vs ngữ nghĩa) làm lệch phân phối nhanh/chậm khi model liên tục train trên dữ liệu tự sinh. | Đụng gần — framework đo "lệch phân phối qua nhiều vòng train-trên-tự-sinh" khá gần cách Bi định đo "chữ viết hội tụ", nhưng domain là văn bản chung, không phải toán/verifier. |

### Nhóm 5 — Nền tảng thuật toán / benchmark đang dùng

| Bài | Tác giả | arXiv | Ngày | Làm gì | Đụng câu hỏi của Bi? |
|---|---|---|---|---|---|
| DeepSeekMath | Zhihong Shao, Peiyi Wang, et al. | [2402.03300](https://arxiv.org/abs/2402.03300) | 2/2024 | Model toán 7B + đề xuất GRPO (RL rẻ hơn PPO) làm nền cho RLVR toán sau này. | Không đụng — là nguồn thuật toán nền, không bàn verifier lệch hay self-training nhiều vòng lọc SFT. |
| DeepSeek-R1 | DeepSeek-AI (nhóm tác giả) | [2501.12948](https://arxiv.org/abs/2501.12948) | 1/2025 | RL thuần (không SFT trước) trên bài có verifier đúng/sai rõ ràng vẫn dạy được reasoning mạnh — chứng minh RLVR hoạt động ở quy mô lớn. | Không đụng thẳng — chứng minh RLVR "có tác dụng" ở mức tổng, không đo lệch verifier tích luỹ hay chữ viết. |
| Training Verifiers to Solve Math Word Problems (GSM8K) | Karl Cobbe, Vineet Kosaraju, et al. (OpenAI) | [2110.14168](https://arxiv.org/abs/2110.14168) | 10/2021 | Bài gốc tạo bộ GSM8K, đề xuất train verifier riêng để chọn lời giải đúng trong nhiều lời giải ứng viên. | Không đụng thẳng — là nguồn benchmark GSM8K mà Việc 1–3 của Bi dùng, không phải nghiên cứu về lệch chữ. |
| Measuring Mathematical Problem Solving With the MATH Dataset | Dan Hendrycks, Collin Burns, et al. | [2103.03874](https://arxiv.org/abs/2103.03874) | 3/2021 | Bài gốc tạo bộ MATH (12500 bài thi toán khó, nhiều LaTeX/phân số). | Không đụng thẳng — nguồn benchmark MATH mà Việc 1 của Bi dùng để tìm bài dễ bị gạch vì cách viết. |
| Minerva (Solving Quantitative Reasoning Problems) | (nhóm tác giả, Google Research) | [2206.14858](https://arxiv.org/abs/2206.14858) | 6/2022 | Model lớn train thêm trên văn bản khoa học, dùng chain-of-thought + majority voting để giải toán mà không cần công cụ ngoài. | Không đụng — mốc benchmark/kỹ thuật lịch sử, không liên quan verifier lệch hay self-training nhiều vòng. |

### Nhóm 6 — Tìm trực tiếp: có ai đo "verifier bias tích lũy qua nhiều vòng self-training" chưa

| Bài | Tác giả | arXiv | Ngày | Làm gì | Đụng câu hỏi của Bi? |
|---|---|---|---|---|---|
| Teacher-Free Self-Training Amplifies but Does Not Compound | (đã liệt kê ở Nhóm 3) | 2606.07856 | 6/2026 | — | **Đụng thẳng nhất** (xem Kết luận ở đầu file). |
| When Good Verifiers Go Bad: Self-Improving VLMs Can Regress on New Tasks | Jianzhe Lin | [2606.14629](https://arxiv.org/abs/2606.14629) | 6/2026 | Verifier tốt trên task A (MathVista) nhưng lệch nặng trên task B (MMMU, độ chính xác verifier rơi còn 8–23%); dùng verifier lệch mà tự tin cao để train lại VLM gây tụt điểm 3.4–10.9 điểm dù loss huấn luyện vẫn giảm. | Đụng gần — đúng cơ chế "verifier lệch, càng tự tin sai càng hại nhiều", nhưng domain VLM đa nhiệm, không phải toán/math-verify, không đo pass@1/pass@k hay chữ viết. |
| Self-Authored Verification Is Unreliable in Heuristic Self-Improving Agents | Diandian Guo, Cong Cao, et al. | [2607.24300](https://arxiv.org/abs/2607.24300) | 7/2026 | Agent tự viết code + tự kiểm tra code qua nhiều vòng: điểm tự chấm cao dần nhưng hiệu năng thật khi triển khai lại giảm — gọi là "khoảng hở verifier-triển khai"; đề xuất thêm một tín hiệu chấp nhận từ bên ngoài để chặn. | Đụng gần — đúng ý "verifier tự có trong vòng lặp làm điểm giả tăng qua nhiều vòng", nhưng đây là agent code tự-sinh-tự-chấm (giống Self-Rewarding LM, không phải hai máy tách biệt như đề Bi), và verifier ở đây không lệch theo kiểu cố định (gạch-vì-chữ) mà lệch ngẫu nhiên/tự tin giả. |

### Nhóm 7 — Tra lại 2026-09-04 (bài ra sau khảo sát gốc, đã WebFetch xác nhận title + arXiv ID + ngày)

Tra lại sau khi thầy yêu cầu "kiểm lại xem có bài nào làm đúng cái mình đưa ra chưa" (buổi trước). **Vẫn không có bài nào ghép đủ 3 mảnh của đề Bi** (verifier luật lệch-vì-format thật + nhiều vòng SFT self-training + đo cả pass@1/pass@k lẫn hội tụ văn phong). Ba bài dưới đây là mới hoặc mới được cập nhật, cần biết tới:

| Bài | Tác giả | arXiv | Ngày | Làm gì | Đụng câu hỏi của Bi? |
|---|---|---|---|---|---|
| Delay, Plateau, or Collapse: Evaluating the Impact of Systematic Verification Error on RLVR | Kazuki Egashira, Mark Vero, Jasper Dekoninck, Florian E. Dörner, Robin Staab, Martin Vechev | [2605.02909](https://arxiv.org/abs/2605.02909) | 4/2026 (v1), 17/8/2026 (v2) | Phân loại lỗi verifier trong **RLVR 1 vòng** trên tác vụ số học tổng hợp: **false negative có hệ thống ≈ nhiễu ngẫu nhiên (chỉ làm chậm, không gây sụp)**; chính **false positive** mới gây plateau/collapse. Kết luận: chất lượng verifier phải hiểu vượt quá tỉ lệ lỗi mức-mẫu. | **Đụng gần và cần xử lý trong Related Work** — kết luận của họ ("FN chỉ làm chậm, không sụp") *nghe như ngược chiều* phát hiện của Bi. Nhưng: (a) họ chạy **RLVR 1 vòng**, không phải nhiều vòng SFT self-training; (b) domain là số học tổng hợp, verifier mô phỏng — không phải `math-verify` thật trên GSM8K/MATH; (c) **không đo hội tụ văn phong**; (d) cơ chế sụp của Bi là **tập huấn luyện co hẹp qua từng vòng** (chỉ tồn tại khi lặp vòng + train lại từ base), không phải nhiễu gradient trong 1 vòng RL. Bài này làm rõ hơn *vì sao* đóng góp của Bi không trùng: Bi đo đúng chế độ (multi-round SFT) mà họ không xét. |
| When Sample Selection Bias Precipitates Model Collapse | Xinbao Qiao, Xianglong Du, Wei Liu, Jingqi Zhang, Peihua Mai, Meng Zhang, Yan Pang | [2606.13732](https://arxiv.org/abs/2606.13732) | 11/6/2026 (v1), 2/7/2026 (rev) | Lý thuyết: khi bộ chọn/verifier chỉ "nhìn" được một lát cắt hẹp, lệch của phân phối đích thì **chọn lọc bằng verifier tự nó thành lệch** và *tăng tốc* model collapse, kéo theo suy giảm đa dạng theo luật lũy thừa. ICML 2026. | Không đụng thẳng — lý thuyết tổng quát, không phải toán/`math-verify`/pass@k/văn phong. **Hữu ích làm chỗ dựa lý thuyết** cho cơ chế "tập co hẹp + lệch → sụp" ở mục 5 của DRAFT: đúng ý "lọc bằng verifier lệch không cứu được collapse, chỉ đổi hình dạng nó". |
| Escaping Model Collapse via Synthetic Data Verification: Near-term Improvements and Long-term Convergence | Bingji Yi, Qiyuan Liu, Yuwei Cheng, Haifeng Xu | [2510.16657](https://arxiv.org/abs/2510.16657) | 18/10/2025 (v1), 16/7/2026 (v3) | Lý thuyết + toy (linear regression, VAE/MNIST, 1 LLM nhỏ SmolLM2-135M): thêm verifier ngoài giúp tránh collapse **trong ngắn hạn**, nhưng "trừ khi verifier hoàn hảo, lợi ích sớm sẽ chững lại và có thể đảo chiều" do lệch verifier. | Không đụng thẳng — không phải toán, không pass@k, không văn phong, model chỉ 135M. Hữu ích trích dẫn cho luận điểm chung "lọc bằng verifier không hoàn hảo → cải thiện sớm rồi đảo chiều", cùng chiều phát hiện của Bi ở quy mô/đo lường khác. |

**Chốt lại 2026-09-04:** đề tài vẫn còn đất. Bài duy nhất cần chủ động trả lời trong Related Work là **2605.02909** (vì kết luận nghe ngược chiều) — cách trả lời: nêu rõ họ xét RLVR 1 vòng + verifier mô phỏng, Bi xét multi-round SFT self-training + verifier luật thật, và cơ chế "tập huấn luyện co hẹp qua từng vòng" chỉ xuất hiện ở chế độ Bi đo.

---

## Ghi chú tra cứu

- Toàn bộ 24 bài mới (ngoài 5 bài cũ) đều được xác nhận tồn tại qua WebSearch, phần lớn WebFetch trực tiếp trang abstract arXiv để lấy đúng tiêu đề/tác giả/ngày.
- Có vài bài rất mới (nhóm 6, tháng 6–7/2026) — ngày trên arXiv là ngày nộp bản v1, không phải ngày công bố chính thức trên hội nghị (nếu có).
- Bài Shumailov: bản preprint (2305.17493, 5/2023) và bản Nature (7/2024, DOI 10.1038/s41586-024-07566-y) là **cùng một công trình**, hai mốc thời gian khác nhau — ghi cả hai để không nhầm khi trích dẫn.
- Không có bài nào trong khảo sát này phủ định claim GVT của Bi hay tuyên bố "đã đo verifier-lệch-vì-chữ tích lũy qua nhiều vòng self-training trên toán" — nếu sau này tìm thấy bài như vậy, phải cập nhật lại mục Kết luận ngay.

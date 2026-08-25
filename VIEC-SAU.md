# Việc sau / chỗ hổng (không phải bug tuần này)

List việc **cố ý chưa làm**, hoặc **không làm bằng LLM trong `rewrite.py`**.

---

## 1. List kiểu chữ không cover hết format

**Hổng.** Gold → chữ khác do **ta nghĩ ra** ~10 luật (`rewrite.py` + `registry.py`). Không hết cách viết trên đời (`eighteen`, `18.00`, `2*9`, gold `p - q`…).

**Không phải bug.** Việc 1 cố ý hẹp: giữ nguyên giá trị, chỉ đổi chữ.

**Bảng 200 MATH đã nói gì (2026-08-16)**

- Luật `\dfrac`/`\tfrac` **đủ mạnh**: 146/146 gạch, `parse_empty`. Không cần LLM để “phát hiện” lệnh này.
- Thập phân thừa số 0 (`0.50`) 13/22 `compare_false` — list đã có, giữ.
- 24 gold cô không đọc được cả khi để nguyên: `p-q`, `\text{Evelyn}`, `\sqrt{51}`, `\pi`, `\frac43` (thiếu ngoặc), `\dfrac{17}{50}` (sách đã viết dfrac), khoảng `(3,4]`, `(2,\infty)`. Đó là **format sách**, không phải chỗ tối ưu rewrite.
- Việc 2 (bài model thật) FN MATH 7.8%: phần lớn **lôi nhầm số trong bài dài**; chữ thật hay gặp thêm `\left...\right`, số phức `6+9i` vs `6 + 9i`, `11\sqrt2` vs `11\sqrt{2}`. List việc 1 không bịa hết các kiểu đó — đúng như dự kiến.

**Cấm:** nhờ model nghĩ thêm format từ gold (không chắc còn cùng số → lẫn toán với chữ).

**Làm sau, theo thứ tự**

1. ~~Chạy việc 1 đủ 200+200.~~ Xong. Đi việc 2.
2. ~~Việc 2 — bài model thật.~~ Xong. MATH 7.8% FN (8 lôi nhầm / 2 viết không nhận).
3. Nếu paper cần thêm 1–2 luật **cứng** (không LLM): tháo `\left...\right`; `\frac43` → `\frac{4}{3}`. Chỉ khi viết mục giới hạn list.
4. Paper: ghi giới hạn “list không hết format”; việc 2 đã cover một phần format thật.
5. Việc 3 đếm chữ model tự viết sau GVT — không bịa từ gold. Mac đã có đếm; số paper vẫn chờ Kaggle.

**Không làm:** tối ưu `rewrite.py` thành máy cover mọi toán.

---

## Việc khác (để trống, thêm dần)

- [ ] Điền `CAU-HOI-THAY.md`
- [x] Việc 1 đủ 200+200 — **đi việc 2**
- [x] Việc 2 FN trên bài model (GSM8K 0%, MATH 7.8%)
- [x] Việc 3 ống GVT + dry 100 đề + mlx toy (Mac, không phải số paper)
- [ ] Việc 3 số paper: Kaggle T4, Qwen 0.5B rồi 1.5B, LoRA SFT (transformers+peft+TRL, không GRPO), k=8, GSM8K+MATH, train/test tách

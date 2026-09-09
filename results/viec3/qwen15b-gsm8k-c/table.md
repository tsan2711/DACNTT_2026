# Việc 3 — vòng generate-verify-select-train

Mỗi vòng: học sinh làm k lần → cô chấm → giữ bài chịu → ôn. **Đúng** = máy chấm chịu. Mac toy ≠ số paper.

Select (dạy): preset `reward`. Exam: mọi preset trong bảng.

| Vòng | Preset | pass@1 | pass@8 | Giữ / ôn | A thêm đề | B ổn định | C mất đề |
|------|--------|--------|----------|----------|-----------|-----------|----------|
| 0 | default | 66.7% | 92.7% | 1901 | — | — | — |
| 0 | reward | 66.7% | 92.7% | 1901 | — | — | — |
| 1 | default | 66.7% | 90.7% | 1869 | 3 | 16 | 6 |
| 1 | reward | 66.7% | 90.7% | 1869 | 3 | 16 | 6 |
| 2 | default | 65.3% | 93.3% | 1769 | 6 | 18 | 2 |
| 2 | reward | 65.3% | 93.3% | 1769 | 6 | 18 | 2 |
| 3 | default | 63.3% | 90.0% | 1693 | 1 | 18 | 6 |
| 3 | reward | 63.3% | 90.0% | 1693 | 1 | 18 | 6 |
| 4 | default | 54.0% | 90.0% | 1515 | 6 | 12 | 6 |
| 4 | reward | 54.0% | 90.0% | 1515 | 6 | 12 | 6 |

## Chữ viết (đếm trên mọi lần làm)

| Vòng | n | boxed | dfrac | tfrac | frac | dollar | sentence | assignment | unit | decimal | decimal_trailing | int_float |
|------|---|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|
| 0 | 4000 | 3466 | 0 | 0 | 1685 | 1260 | 22 | 234 | 72 | 528 | 319 | 175 |
| 1 | 4000 | 3190 | 0 | 0 | 1742 | 1299 | 12 | 228 | 72 | 561 | 340 | 180 |
| 2 | 4000 | 3042 | 0 | 0 | 1791 | 1463 | 28 | 256 | 72 | 596 | 317 | 189 |
| 3 | 4000 | 2948 | 0 | 0 | 1810 | 1677 | 38 | 261 | 71 | 588 | 307 | 184 |
| 4 | 4000 | 2926 | 0 | 0 | 1823 | 1934 | 48 | 237 | 72 | 648 | 268 | 197 |

Cách đọc (TOI-HIEU): pass@1 tăng **và** pass@k đứng/giảm **và** chữ tụ một kiểu → manh mối mạnh đang học chữ cô, không học toán. Một mình một cột thì chưa đủ.

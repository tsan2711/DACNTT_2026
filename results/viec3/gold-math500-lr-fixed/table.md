# Việc 3 — vòng generate-verify-select-train

Mỗi vòng: học sinh làm k lần → cô chấm → giữ bài chịu → ôn. **Đúng** = máy chấm chịu. Mac toy ≠ số paper.

Select (dạy): preset `reward`. Exam: mọi preset trong bảng.

| Vòng | Preset | pass@1 | pass@4 | Giữ / ôn | A thêm đề | B ổn định | C mất đề |
|------|--------|--------|----------|----------|-----------|-----------|----------|
| 0 | default | 33.3% | 50.0% | 350 | — | — | — |
| 0 | reward | 33.3% | 50.0% | 350 | — | — | — |
| 1 | default | 18.0% | 33.3% | 350 | 7 | 7 | 32 |
| 1 | reward | 18.0% | 33.3% | 350 | 7 | 7 | 32 |
| 2 | default | 15.3% | 29.3% | 350 | 8 | 7 | 14 |
| 2 | reward | 15.3% | 29.3% | 350 | 8 | 7 | 14 |

## Chữ viết (đếm trên mọi lần làm)

| Vòng | n | boxed | dfrac | tfrac | frac | dollar | sentence | assignment | unit | decimal | decimal_trailing | int_float |
|------|---|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|
| 0 | 2000 | 1038 | 12 | 0 | 1115 | 103 | 6 | 481 | 0 | 230 | 24 | 5 |
| 1 | 2000 | 1712 | 25 | 11 | 1100 | 1957 | 69 | 397 | 0 | 220 | 10 | 3 |
| 2 | 2000 | 1715 | 34 | 11 | 1117 | 1968 | 72 | 420 | 0 | 195 | 12 | 5 |

Cách đọc (TOI-HIEU): pass@1 tăng **và** pass@k đứng/giảm **và** chữ tụ một kiểu → manh mối mạnh đang học chữ cô, không học toán. Một mình một cột thì chưa đủ.

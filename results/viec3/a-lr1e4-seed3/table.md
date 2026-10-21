# Việc 3 — vòng generate-verify-select-train

Mỗi vòng: học sinh làm k lần → cô chấm → giữ bài chịu → ôn. **Đúng** = máy chấm chịu. Mac toy ≠ số paper.

Select (dạy): preset `reward`. Exam: mọi preset trong bảng.

| Vòng | Preset | pass@1 | pass@4 | Giữ / ôn | A thêm đề | B ổn định | C mất đề |
|------|--------|--------|----------|----------|-----------|-----------|----------|
| 0 | default | 29.3% | 40.0% | 455 | — | — | — |
| 0 | reward | 29.3% | 40.0% | 455 | — | — | — |
| 1 | default | 26.7% | 40.0% | 397 | 6 | 8 | 6 |
| 1 | reward | 26.7% | 40.0% | 397 | 6 | 8 | 6 |
| 2 | default | 26.7% | 41.3% | 354 | 10 | 8 | 8 |
| 2 | reward | 26.7% | 41.3% | 354 | 10 | 8 | 8 |

## Chữ viết (đếm trên mọi lần làm)

| Vòng | n | boxed | dfrac | tfrac | frac | dollar | sentence | assignment | unit | decimal | decimal_trailing | int_float |
|------|---|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|
| 0 | 2000 | 1077 | 10 | 0 | 1127 | 99 | 12 | 479 | 0 | 231 | 27 | 14 |
| 1 | 2000 | 1021 | 5 | 0 | 1123 | 101 | 15 | 517 | 0 | 239 | 24 | 12 |
| 2 | 2000 | 939 | 4 | 0 | 1145 | 140 | 13 | 471 | 0 | 257 | 25 | 15 |

Cách đọc (TOI-HIEU): pass@1 tăng **và** pass@k đứng/giảm **và** chữ tụ một kiểu → manh mối mạnh đang học chữ cô, không học toán. Một mình một cột thì chưa đủ.

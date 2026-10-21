# Việc 3 — vòng generate-verify-select-train

Mỗi vòng: học sinh làm k lần → cô chấm → giữ bài chịu → ôn. **Đúng** = máy chấm chịu. Mac toy ≠ số paper.

Select (dạy): preset `reward`. Exam: mọi preset trong bảng.

| Vòng | Preset | pass@1 | pass@4 | Giữ / ôn | A thêm đề | B ổn định | C mất đề |
|------|--------|--------|----------|----------|-----------|-----------|----------|
| 0 | default | 33.3% | 50.0% | 440 | — | — | — |
| 0 | reward | 33.3% | 50.0% | 440 | — | — | — |
| 1 | default | 29.3% | 50.7% | 397 | 11 | 10 | 10 |
| 1 | reward | 29.3% | 50.7% | 397 | 11 | 10 | 10 |
| 2 | default | 34.0% | 49.3% | 352 | 9 | 16 | 11 |
| 2 | reward | 34.0% | 49.3% | 352 | 9 | 16 | 11 |

## Chữ viết (đếm trên mọi lần làm)

| Vòng | n | boxed | dfrac | tfrac | frac | dollar | sentence | assignment | unit | decimal | decimal_trailing | int_float |
|------|---|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|
| 0 | 2000 | 1038 | 12 | 0 | 1115 | 103 | 6 | 481 | 0 | 230 | 24 | 5 |
| 1 | 2000 | 1025 | 7 | 0 | 1132 | 79 | 19 | 510 | 0 | 249 | 22 | 11 |
| 2 | 2000 | 913 | 6 | 0 | 1130 | 138 | 17 | 536 | 0 | 267 | 27 | 9 |

Cách đọc (TOI-HIEU): pass@1 tăng **và** pass@k đứng/giảm **và** chữ tụ một kiểu → manh mối mạnh đang học chữ cô, không học toán. Một mình một cột thì chưa đủ.

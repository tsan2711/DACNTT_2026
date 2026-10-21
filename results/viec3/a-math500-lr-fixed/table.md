# Việc 3 — vòng generate-verify-select-train

Mỗi vòng: học sinh làm k lần → cô chấm → giữ bài chịu → ôn. **Đúng** = máy chấm chịu. Mac toy ≠ số paper.

Select (dạy): preset `reward`. Exam: mọi preset trong bảng.

| Vòng | Preset | pass@1 | pass@4 | Giữ / ôn | A thêm đề | B ổn định | C mất đề |
|------|--------|--------|----------|----------|-----------|-----------|----------|
| 0 | default | 33.3% | 50.0% | 440 | — | — | — |
| 0 | reward | 33.3% | 50.0% | 440 | — | — | — |
| 1 | default | 32.7% | 49.3% | 391 | 14 | 9 | 15 |
| 1 | reward | 32.7% | 49.3% | 391 | 14 | 9 | 15 |
| 2 | default | 23.3% | 42.7% | 326 | 8 | 8 | 18 |
| 2 | reward | 23.3% | 42.7% | 326 | 8 | 8 | 18 |

## Chữ viết (đếm trên mọi lần làm)

| Vòng | n | boxed | dfrac | tfrac | frac | dollar | sentence | assignment | unit | decimal | decimal_trailing | int_float |
|------|---|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|
| 0 | 2000 | 1038 | 12 | 0 | 1115 | 103 | 6 | 481 | 0 | 230 | 24 | 5 |
| 1 | 2000 | 1019 | 9 | 0 | 1097 | 72 | 10 | 484 | 0 | 230 | 24 | 6 |
| 2 | 2000 | 728 | 5 | 0 | 1014 | 128 | 12 | 451 | 0 | 202 | 24 | 8 |

Cách đọc (TOI-HIEU): pass@1 tăng **và** pass@k đứng/giảm **và** chữ tụ một kiểu → manh mối mạnh đang học chữ cô, không học toán. Một mình một cột thì chưa đủ.

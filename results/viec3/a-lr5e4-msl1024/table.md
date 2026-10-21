# Việc 3 — vòng generate-verify-select-train

Mỗi vòng: học sinh làm k lần → cô chấm → giữ bài chịu → ôn. **Đúng** = máy chấm chịu. Mac toy ≠ số paper.

Select (dạy): preset `reward`. Exam: mọi preset trong bảng.

| Vòng | Preset | pass@1 | pass@4 | Giữ / ôn | A thêm đề | B ổn định | C mất đề |
|------|--------|--------|----------|----------|-----------|-----------|----------|
| 0 | default | 33.3% | 50.0% | 440 | — | — | — |
| 0 | reward | 33.3% | 50.0% | 440 | — | — | — |
| 1 | default | 30.0% | 50.7% | 400 | 11 | 11 | 10 |
| 1 | reward | 30.0% | 50.7% | 400 | 11 | 11 | 10 |
| 2 | default | 32.7% | 45.3% | 320 | 8 | 14 | 16 |
| 2 | reward | 32.7% | 45.3% | 320 | 8 | 14 | 16 |

## Chữ viết (đếm trên mọi lần làm)

| Vòng | n | boxed | dfrac | tfrac | frac | dollar | sentence | assignment | unit | decimal | decimal_trailing | int_float |
|------|---|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|
| 0 | 2000 | 1038 | 12 | 0 | 1115 | 103 | 6 | 481 | 0 | 230 | 24 | 5 |
| 1 | 2000 | 1028 | 9 | 0 | 1123 | 70 | 9 | 514 | 0 | 232 | 25 | 10 |
| 2 | 2000 | 797 | 5 | 0 | 1031 | 68 | 3 | 475 | 1 | 217 | 26 | 4 |

Cách đọc (TOI-HIEU): pass@1 tăng **và** pass@k đứng/giảm **và** chữ tụ một kiểu → manh mối mạnh đang học chữ cô, không học toán. Một mình một cột thì chưa đủ.

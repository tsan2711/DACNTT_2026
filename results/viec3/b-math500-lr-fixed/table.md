# Việc 3 — vòng generate-verify-select-train

Mỗi vòng: học sinh làm k lần → cô chấm → giữ bài chịu → ôn. **Đúng** = máy chấm chịu. Mac toy ≠ số paper.

Select (dạy): preset `reward`. Exam: mọi preset trong bảng.

| Vòng | Preset | pass@1 | pass@4 | Giữ / ôn | A thêm đề | B ổn định | C mất đề |
|------|--------|--------|----------|----------|-----------|-----------|----------|
| 0 | default | 33.3% | 50.7% | 443 | — | — | — |
| 0 | reward | 33.3% | 50.7% | 443 | — | — | — |
| 1 | default | 35.3% | 50.0% | 392 | 9 | 11 | 10 |
| 1 | reward | 35.3% | 50.0% | 392 | 9 | 11 | 10 |
| 2 | default | 28.7% | 48.7% | 328 | 12 | 5 | 14 |
| 2 | reward | 28.7% | 48.7% | 328 | 12 | 5 | 14 |

## Chữ viết (đếm trên mọi lần làm)

| Vòng | n | boxed | dfrac | tfrac | frac | dollar | sentence | assignment | unit | decimal | decimal_trailing | int_float |
|------|---|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|
| 0 | 2000 | 1038 | 12 | 0 | 1115 | 103 | 6 | 481 | 0 | 230 | 24 | 5 |
| 1 | 2000 | 989 | 7 | 0 | 1125 | 86 | 7 | 490 | 0 | 260 | 26 | 8 |
| 2 | 2000 | 819 | 3 | 0 | 1036 | 112 | 5 | 490 | 0 | 233 | 23 | 11 |

Cách đọc (TOI-HIEU): pass@1 tăng **và** pass@k đứng/giảm **và** chữ tụ một kiểu → manh mối mạnh đang học chữ cô, không học toán. Một mình một cột thì chưa đủ.

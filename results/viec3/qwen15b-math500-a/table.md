# Việc 3 — vòng generate-verify-select-train

Mỗi vòng: học sinh làm k lần → cô chấm → giữ bài chịu → ôn. **Đúng** = máy chấm chịu. Mac toy ≠ số paper.

Select (dạy): preset `reward`. Exam: mọi preset trong bảng.

| Vòng | Preset | pass@1 | pass@8 | Giữ / ôn | A thêm đề | B ổn định | C mất đề |
|------|--------|--------|----------|----------|-----------|-----------|----------|
| 0 | default | 32.0% | 57.3% | 872 | — | — | — |
| 0 | reward | 32.0% | 57.3% | 872 | — | — | — |
| 1 | default | 29.3% | 56.7% | 866 | 8 | 10 | 9 |
| 1 | reward | 29.3% | 56.7% | 866 | 8 | 10 | 9 |
| 2 | default | 28.0% | 54.7% | 869 | 6 | 2 | 9 |
| 2 | reward | 28.0% | 54.7% | 869 | 6 | 2 | 9 |
| 3 | default | 29.3% | 57.3% | 858 | 9 | 6 | 5 |
| 3 | reward | 29.3% | 57.3% | 858 | 9 | 6 | 5 |
| 4 | default | 29.3% | 56.0% | 843 | 9 | 5 | 11 |
| 4 | reward | 29.3% | 56.0% | 843 | 9 | 5 | 11 |

## Chữ viết (đếm trên mọi lần làm)

| Vòng | n | boxed | dfrac | tfrac | frac | dollar | sentence | assignment | unit | decimal | decimal_trailing | int_float |
|------|---|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|
| 0 | 4000 | 2136 | 23 | 0 | 2222 | 202 | 21 | 957 | 0 | 456 | 55 | 16 |
| 1 | 4000 | 2053 | 23 | 0 | 2245 | 181 | 17 | 978 | 0 | 452 | 50 | 17 |
| 2 | 4000 | 2067 | 22 | 0 | 2220 | 227 | 22 | 962 | 0 | 456 | 49 | 22 |
| 3 | 4000 | 2034 | 21 | 0 | 2256 | 254 | 12 | 921 | 0 | 471 | 46 | 22 |
| 4 | 4000 | 1999 | 20 | 0 | 2207 | 285 | 15 | 918 | 0 | 477 | 47 | 20 |

Cách đọc (TOI-HIEU): pass@1 tăng **và** pass@k đứng/giảm **và** chữ tụ một kiểu → manh mối mạnh đang học chữ cô, không học toán. Một mình một cột thì chưa đủ.

# Việc 3 — vòng generate-verify-select-train

Mỗi vòng: học sinh làm k lần → cô chấm → giữ bài chịu → ôn. **Đúng** = máy chấm chịu. Mac toy ≠ số paper.

Select (dạy): preset `reward`. Exam: mọi preset trong bảng.

| Vòng | Preset | pass@1 | pass@8 | Giữ / ôn | A thêm đề | B ổn định | C mất đề |
|------|--------|--------|----------|----------|-----------|-----------|----------|
| 0 | default | 32.0% | 57.3% | 876 | — | — | — |
| 0 | reward | 32.0% | 57.3% | 876 | — | — | — |
| 1 | default | 28.7% | 55.3% | 870 | 8 | 9 | 11 |
| 1 | reward | 28.7% | 55.3% | 870 | 8 | 9 | 11 |
| 2 | default | 28.7% | 52.0% | 871 | 5 | 3 | 10 |
| 2 | reward | 28.7% | 52.0% | 871 | 5 | 3 | 10 |
| 3 | default | 28.7% | 57.3% | 853 | 12 | 5 | 4 |
| 3 | reward | 28.7% | 57.3% | 853 | 12 | 5 | 4 |
| 4 | default | 28.7% | 53.3% | 850 | 6 | 4 | 12 |
| 4 | reward | 28.7% | 53.3% | 850 | 6 | 4 | 12 |

## Chữ viết (đếm trên mọi lần làm)

| Vòng | n | boxed | dfrac | tfrac | frac | dollar | sentence | assignment | unit | decimal | decimal_trailing | int_float |
|------|---|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|
| 0 | 4000 | 2136 | 23 | 0 | 2222 | 202 | 21 | 957 | 0 | 456 | 55 | 16 |
| 1 | 4000 | 2055 | 23 | 0 | 2242 | 185 | 18 | 986 | 0 | 447 | 47 | 19 |
| 2 | 4000 | 2073 | 22 | 0 | 2231 | 223 | 19 | 960 | 0 | 468 | 47 | 18 |
| 3 | 4000 | 2014 | 21 | 0 | 2235 | 248 | 12 | 917 | 0 | 459 | 49 | 22 |
| 4 | 4000 | 1987 | 21 | 0 | 2213 | 280 | 14 | 929 | 0 | 473 | 46 | 19 |

Cách đọc (TOI-HIEU): pass@1 tăng **và** pass@k đứng/giảm **và** chữ tụ một kiểu → manh mối mạnh đang học chữ cô, không học toán. Một mình một cột thì chưa đủ.

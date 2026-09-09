# Việc 3 — vòng generate-verify-select-train

Mỗi vòng: học sinh làm k lần → cô chấm → giữ bài chịu → ôn. **Đúng** = máy chấm chịu. Mac toy ≠ số paper.

Select (dạy): preset `reward`. Exam: mọi preset trong bảng.

| Vòng | Preset | pass@1 | pass@8 | Giữ / ôn | A thêm đề | B ổn định | C mất đề |
|------|--------|--------|----------|----------|-----------|-----------|----------|
| 0 | default | 37.3% | 59.3% | 836 | — | — | — |
| 0 | reward | 37.3% | 59.3% | 836 | — | — | — |
| 1 | default | 32.0% | 60.7% | 811 | 10 | 7 | 8 |
| 1 | reward | 32.0% | 60.7% | 811 | 10 | 7 | 8 |
| 2 | default | 32.7% | 58.0% | 823 | 4 | 7 | 8 |
| 2 | reward | 32.7% | 58.0% | 823 | 4 | 7 | 8 |
| 3 | default | 31.3% | 58.7% | 829 | 3 | 1 | 2 |
| 3 | reward | 31.3% | 58.7% | 829 | 3 | 1 | 2 |
| 4 | default | 33.3% | 58.7% | 815 | 3 | 8 | 3 |
| 4 | reward | 33.3% | 58.7% | 815 | 3 | 8 | 3 |

## Chữ viết (đếm trên mọi lần làm)

| Vòng | n | boxed | dfrac | tfrac | frac | dollar | sentence | assignment | unit | decimal | decimal_trailing | int_float |
|------|---|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|
| 0 | 4000 | 2160 | 29 | 0 | 2215 | 190 | 29 | 975 | 0 | 459 | 50 | 9 |
| 1 | 4000 | 2070 | 23 | 0 | 2228 | 200 | 25 | 956 | 0 | 456 | 46 | 16 |
| 2 | 4000 | 2067 | 22 | 0 | 2243 | 217 | 15 | 974 | 0 | 458 | 46 | 18 |
| 3 | 4000 | 2058 | 22 | 0 | 2257 | 233 | 16 | 953 | 0 | 453 | 52 | 20 |
| 4 | 4000 | 2020 | 22 | 0 | 2232 | 264 | 11 | 923 | 0 | 462 | 51 | 22 |

Cách đọc (TOI-HIEU): pass@1 tăng **và** pass@k đứng/giảm **và** chữ tụ một kiểu → manh mối mạnh đang học chữ cô, không học toán. Một mình một cột thì chưa đủ.

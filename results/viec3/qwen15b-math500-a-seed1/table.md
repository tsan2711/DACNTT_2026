# Việc 3 — vòng generate-verify-select-train

Mỗi vòng: học sinh làm k lần → cô chấm → giữ bài chịu → ôn. **Đúng** = máy chấm chịu. Mac toy ≠ số paper.

Select (dạy): preset `reward`. Exam: mọi preset trong bảng.

| Vòng | Preset | pass@1 | pass@8 | Giữ / ôn | A thêm đề | B ổn định | C mất đề |
|------|--------|--------|----------|----------|-----------|-----------|----------|
| 0 | default | 36.7% | 58.7% | 833 | — | — | — |
| 0 | reward | 36.7% | 58.7% | 833 | — | — | — |
| 1 | default | 32.7% | 60.7% | 809 | 10 | 7 | 7 |
| 1 | reward | 32.7% | 60.7% | 809 | 10 | 7 | 7 |
| 2 | default | 32.7% | 59.3% | 813 | 6 | 7 | 8 |
| 2 | reward | 32.7% | 59.3% | 813 | 6 | 7 | 8 |
| 3 | default | 31.3% | 59.3% | 830 | 4 | 2 | 4 |
| 3 | reward | 31.3% | 59.3% | 830 | 4 | 2 | 4 |
| 4 | default | 33.3% | 58.7% | 804 | 2 | 8 | 3 |
| 4 | reward | 33.3% | 58.7% | 804 | 2 | 8 | 3 |

## Chữ viết (đếm trên mọi lần làm)

| Vòng | n | boxed | dfrac | tfrac | frac | dollar | sentence | assignment | unit | decimal | decimal_trailing | int_float |
|------|---|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|
| 0 | 4000 | 2160 | 29 | 0 | 2215 | 190 | 29 | 975 | 0 | 459 | 50 | 9 |
| 1 | 4000 | 2075 | 23 | 0 | 2241 | 201 | 21 | 958 | 0 | 466 | 43 | 19 |
| 2 | 4000 | 2067 | 22 | 0 | 2241 | 221 | 14 | 952 | 0 | 450 | 46 | 18 |
| 3 | 4000 | 2043 | 22 | 0 | 2246 | 233 | 14 | 950 | 0 | 453 | 50 | 22 |
| 4 | 4000 | 2023 | 22 | 0 | 2235 | 260 | 9 | 918 | 0 | 480 | 48 | 21 |

Cách đọc (TOI-HIEU): pass@1 tăng **và** pass@k đứng/giảm **và** chữ tụ một kiểu → manh mối mạnh đang học chữ cô, không học toán. Một mình một cột thì chưa đủ.

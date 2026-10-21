# Việc 3 — vòng generate-verify-select-train

Mỗi vòng: học sinh làm k lần → cô chấm → giữ bài chịu → ôn. **Đúng** = máy chấm chịu. Mac toy ≠ số paper.

Select (dạy): preset `reward`. Exam: mọi preset trong bảng.

| Vòng | Preset | pass@1 | pass@4 | Giữ / ôn | A thêm đề | B ổn định | C mất đề |
|------|--------|--------|----------|----------|-----------|-----------|----------|
| 0 | default | 33.3% | 50.0% | 1400 | — | — | — |
| 0 | reward | 33.3% | 50.0% | 1400 | — | — | — |
| 1 | default | 26.7% | 49.3% | 1400 | 11 | 5 | 12 |
| 1 | reward | 26.7% | 49.3% | 1400 | 11 | 5 | 12 |
| 2 | default | 27.3% | 40.7% | 1400 | 10 | 10 | 23 |
| 2 | reward | 27.3% | 40.7% | 1400 | 10 | 10 | 23 |

## Chữ viết (đếm trên mọi lần làm)

| Vòng | n | boxed | dfrac | tfrac | frac | dollar | sentence | assignment | unit | decimal | decimal_trailing | int_float |
|------|---|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|
| 0 | 2000 | 1038 | 12 | 0 | 1115 | 103 | 6 | 481 | 0 | 230 | 24 | 5 |
| 1 | 2000 | 992 | 9 | 0 | 1081 | 94 | 11 | 504 | 0 | 247 | 20 | 8 |
| 2 | 2000 | 764 | 4 | 0 | 1061 | 134 | 7 | 451 | 0 | 234 | 21 | 12 |

Cách đọc (TOI-HIEU): pass@1 tăng **và** pass@k đứng/giảm **và** chữ tụ một kiểu → manh mối mạnh đang học chữ cô, không học toán. Một mình một cột thì chưa đủ.

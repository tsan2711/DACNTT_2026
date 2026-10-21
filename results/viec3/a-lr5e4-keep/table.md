# Việc 3 — vòng generate-verify-select-train

Mỗi vòng: học sinh làm k lần → cô chấm → giữ bài chịu → ôn. **Đúng** = máy chấm chịu. Mac toy ≠ số paper.

Select (dạy): preset `reward`. Exam: mọi preset trong bảng.

| Vòng | Preset | pass@1 | pass@4 | Giữ / ôn | A thêm đề | B ổn định | C mất đề |
|------|--------|--------|----------|----------|-----------|-----------|----------|
| 0 | default | 33.3% | 50.0% | 440 | — | — | — |
| 0 | reward | 33.3% | 50.0% | 440 | — | — | — |
| 1 | default | 31.3% | 48.0% | 396 | 9 | 10 | 12 |
| 1 | reward | 31.3% | 48.0% | 396 | 9 | 10 | 12 |
| 2 | default | 25.3% | 44.0% | 349 | 8 | 11 | 14 |
| 2 | reward | 25.3% | 44.0% | 349 | 8 | 11 | 14 |

## Chữ viết (đếm trên mọi lần làm)

| Vòng | n | boxed | dfrac | tfrac | frac | dollar | sentence | assignment | unit | decimal | decimal_trailing | int_float |
|------|---|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|
| 0 | 2000 | 1038 | 12 | 0 | 1115 | 103 | 6 | 481 | 0 | 230 | 24 | 5 |
| 1 | 2000 | 1035 | 9 | 0 | 1096 | 74 | 12 | 487 | 0 | 242 | 23 | 6 |
| 2 | 2000 | 953 | 6 | 0 | 1042 | 126 | 11 | 468 | 0 | 215 | 23 | 9 |

Cách đọc (TOI-HIEU): pass@1 tăng **và** pass@k đứng/giảm **và** chữ tụ một kiểu → manh mối mạnh đang học chữ cô, không học toán. Một mình một cột thì chưa đủ.

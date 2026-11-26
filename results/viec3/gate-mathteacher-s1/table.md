# Việc 3 — vòng generate-verify-select-train

Mỗi vòng: học sinh làm k lần → cô chấm → giữ bài chịu → ôn. **Đúng** = máy chấm chịu. Mac toy ≠ số paper.

Select (dạy): preset `reward`. Exam: mọi preset trong bảng.

| Vòng | Preset | pass@1 | pass@2 | Giữ / ôn | A thêm đề | B ổn định | C mất đề |
|------|--------|--------|----------|----------|-----------|-----------|----------|
| 0 | default | 49.2% | 59.4% | 834 | — | — | — |
| 0 | reward | 49.2% | 59.4% | 834 | — | — | — |
| 1 | default | 47.6% | 58.0% | 834 | 44 | 24 | 51 |
| 1 | reward | 47.6% | 58.0% | 834 | 44 | 24 | 51 |

## Chữ viết (đếm trên mọi lần làm)

| Vòng | n | boxed | dfrac | tfrac | frac | dollar | sentence | assignment | unit | decimal | decimal_trailing | int_float |
|------|---|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|
| 0 | 1600 | 1453 | 11 | 0 | 942 | 60 | 28 | 418 | 0 | 203 | 16 | 5 |
| 1 | 1600 | 1380 | 10 | 0 | 978 | 27 | 18 | 405 | 0 | 214 | 12 | 5 |

Cách đọc (TOI-HIEU): pass@1 tăng **và** pass@k đứng/giảm **và** chữ tụ một kiểu → manh mối mạnh đang học chữ cô, không học toán. Một mình một cột thì chưa đủ.

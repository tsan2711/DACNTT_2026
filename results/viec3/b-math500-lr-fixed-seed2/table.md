# Việc 3 — vòng generate-verify-select-train

Mỗi vòng: học sinh làm k lần → cô chấm → giữ bài chịu → ôn. **Đúng** = máy chấm chịu. Mac toy ≠ số paper.

Select (dạy): preset `reward`. Exam: mọi preset trong bảng.

| Vòng | Preset | pass@1 | pass@4 | Giữ / ôn | A thêm đề | B ổn định | C mất đề |
|------|--------|--------|----------|----------|-----------|-----------|----------|
| 0 | default | 31.3% | 52.0% | 424 | — | — | — |
| 0 | reward | 31.3% | 52.0% | 424 | — | — | — |
| 1 | default | 31.3% | 44.7% | 398 | 9 | 9 | 20 |
| 1 | reward | 31.3% | 44.7% | 398 | 9 | 9 | 20 |
| 2 | default | 20.0% | 40.7% | 332 | 9 | 4 | 15 |
| 2 | reward | 20.0% | 40.7% | 332 | 9 | 4 | 15 |

## Chữ viết (đếm trên mọi lần làm)

| Vòng | n | boxed | dfrac | tfrac | frac | dollar | sentence | assignment | unit | decimal | decimal_trailing | int_float |
|------|---|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|
| 0 | 2000 | 1085 | 13 | 0 | 1114 | 98 | 8 | 495 | 0 | 236 | 21 | 9 |
| 1 | 2000 | 1004 | 7 | 0 | 1119 | 79 | 7 | 523 | 0 | 237 | 22 | 12 |
| 2 | 2000 | 764 | 4 | 0 | 1033 | 75 | 12 | 457 | 0 | 215 | 26 | 12 |

Cách đọc (TOI-HIEU): pass@1 tăng **và** pass@k đứng/giảm **và** chữ tụ một kiểu → manh mối mạnh đang học chữ cô, không học toán. Một mình một cột thì chưa đủ.

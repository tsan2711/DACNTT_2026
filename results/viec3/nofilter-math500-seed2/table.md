# Việc 3 — vòng generate-verify-select-train

Mỗi vòng: học sinh làm k lần → cô chấm → giữ bài chịu → ôn. **Đúng** = máy chấm chịu. Mac toy ≠ số paper.

Select (dạy): preset `reward`. Exam: mọi preset trong bảng.

| Vòng | Preset | pass@1 | pass@4 | Giữ / ôn | A thêm đề | B ổn định | C mất đề |
|------|--------|--------|----------|----------|-----------|-----------|----------|
| 0 | default | 31.3% | 51.3% | 1400 | — | — | — |
| 0 | reward | 31.3% | 51.3% | 1400 | — | — | — |
| 1 | default | 34.7% | 48.7% | 1400 | 11 | 9 | 15 |
| 1 | reward | 34.7% | 48.7% | 1400 | 11 | 9 | 15 |
| 2 | default | 22.7% | 39.3% | 1400 | 11 | 4 | 25 |
| 2 | reward | 22.7% | 39.3% | 1400 | 11 | 4 | 25 |

## Chữ viết (đếm trên mọi lần làm)

| Vòng | n | boxed | dfrac | tfrac | frac | dollar | sentence | assignment | unit | decimal | decimal_trailing | int_float |
|------|---|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|
| 0 | 2000 | 1085 | 13 | 0 | 1114 | 98 | 8 | 495 | 0 | 236 | 21 | 9 |
| 1 | 2000 | 1034 | 8 | 0 | 1084 | 98 | 2 | 521 | 0 | 235 | 23 | 13 |
| 2 | 2000 | 686 | 5 | 0 | 1033 | 97 | 7 | 466 | 0 | 229 | 24 | 12 |

Cách đọc (TOI-HIEU): pass@1 tăng **và** pass@k đứng/giảm **và** chữ tụ một kiểu → manh mối mạnh đang học chữ cô, không học toán. Một mình một cột thì chưa đủ.

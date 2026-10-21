# Việc 3 — vòng generate-verify-select-train

Mỗi vòng: học sinh làm k lần → cô chấm → giữ bài chịu → ôn. **Đúng** = máy chấm chịu. Mac toy ≠ số paper.

Select (dạy): preset `reward`. Exam: mọi preset trong bảng.

| Vòng | Preset | pass@1 | pass@4 | Giữ / ôn | A thêm đề | B ổn định | C mất đề |
|------|--------|--------|----------|----------|-----------|-----------|----------|
| 0 | default | 31.3% | 51.3% | 350 | — | — | — |
| 0 | reward | 31.3% | 51.3% | 350 | — | — | — |
| 1 | default | 8.7% | 28.7% | 350 | 6 | 1 | 40 |
| 1 | reward | 8.7% | 28.7% | 350 | 6 | 1 | 40 |
| 2 | default | 10.0% | 30.7% | 350 | 17 | 9 | 14 |
| 2 | reward | 10.0% | 30.7% | 350 | 17 | 9 | 14 |

## Chữ viết (đếm trên mọi lần làm)

| Vòng | n | boxed | dfrac | tfrac | frac | dollar | sentence | assignment | unit | decimal | decimal_trailing | int_float |
|------|---|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|
| 0 | 2000 | 1085 | 13 | 0 | 1114 | 98 | 8 | 495 | 0 | 236 | 21 | 9 |
| 1 | 2000 | 1703 | 33 | 12 | 1072 | 1973 | 78 | 418 | 0 | 221 | 13 | 4 |
| 2 | 2000 | 1685 | 37 | 18 | 1070 | 1968 | 64 | 417 | 0 | 224 | 15 | 1 |

Cách đọc (TOI-HIEU): pass@1 tăng **và** pass@k đứng/giảm **và** chữ tụ một kiểu → manh mối mạnh đang học chữ cô, không học toán. Một mình một cột thì chưa đủ.

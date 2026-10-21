# Việc 3 — vòng generate-verify-select-train

Mỗi vòng: học sinh làm k lần → cô chấm → giữ bài chịu → ôn. **Đúng** = máy chấm chịu. Mac toy ≠ số paper.

Select (dạy): preset `reward`. Exam: mọi preset trong bảng.

| Vòng | Preset | pass@1 | pass@4 | Giữ / ôn | A thêm đề | B ổn định | C mất đề |
|------|--------|--------|----------|----------|-----------|-----------|----------|
| 0 | default | 31.3% | 51.3% | 424 | — | — | — |
| 0 | reward | 31.3% | 51.3% | 424 | — | — | — |
| 1 | default | 34.0% | 47.3% | 412 | 10 | 10 | 16 |
| 1 | reward | 34.0% | 47.3% | 412 | 10 | 10 | 16 |
| 2 | default | 28.0% | 45.3% | 362 | 15 | 7 | 18 |
| 2 | reward | 28.0% | 45.3% | 362 | 15 | 7 | 18 |

## Chữ viết (đếm trên mọi lần làm)

| Vòng | n | boxed | dfrac | tfrac | frac | dollar | sentence | assignment | unit | decimal | decimal_trailing | int_float |
|------|---|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|
| 0 | 2000 | 1085 | 13 | 0 | 1114 | 98 | 8 | 495 | 0 | 236 | 21 | 9 |
| 1 | 2000 | 1013 | 7 | 0 | 1127 | 78 | 10 | 491 | 0 | 248 | 20 | 13 |
| 2 | 2000 | 954 | 4 | 1 | 1166 | 167 | 21 | 506 | 0 | 278 | 28 | 10 |

Cách đọc (TOI-HIEU): pass@1 tăng **và** pass@k đứng/giảm **và** chữ tụ một kiểu → manh mối mạnh đang học chữ cô, không học toán. Một mình một cột thì chưa đủ.

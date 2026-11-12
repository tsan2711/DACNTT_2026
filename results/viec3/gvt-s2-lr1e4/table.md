# Việc 3 — vòng generate-verify-select-train

Mỗi vòng: học sinh làm k lần → cô chấm → giữ bài chịu → ôn. **Đúng** = máy chấm chịu. Mac toy ≠ số paper.

Select (dạy): preset `reward`. Exam: mọi preset trong bảng.

| Vòng | Preset | pass@1 | pass@2 | Giữ / ôn | A thêm đề | B ổn định | C mất đề |
|------|--------|--------|----------|----------|-----------|-----------|----------|
| 0 | default | 46.8% | 61.0% | 303 | — | — | — |
| 0 | reward | 46.8% | 61.0% | 303 | — | — | — |
| 1 | default | 43.6% | 54.8% | 274 | 30 | 24 | 61 |
| 1 | reward | 43.6% | 54.8% | 274 | 30 | 24 | 61 |

## Chữ viết (đếm trên mọi lần làm)

| Vòng | n | boxed | dfrac | tfrac | frac | dollar | sentence | assignment | unit | decimal | decimal_trailing | int_float |
|------|---|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|
| 0 | 1600 | 1464 | 7 | 0 | 945 | 81 | 33 | 447 | 2 | 199 | 14 | 2 |
| 1 | 1600 | 1463 | 3 | 0 | 921 | 88 | 15 | 417 | 2 | 191 | 14 | 4 |

Cách đọc (TOI-HIEU): pass@1 tăng **và** pass@k đứng/giảm **và** chữ tụ một kiểu → manh mối mạnh đang học chữ cô, không học toán. Một mình một cột thì chưa đủ.

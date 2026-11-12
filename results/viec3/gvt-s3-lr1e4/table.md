# Việc 3 — vòng generate-verify-select-train

Mỗi vòng: học sinh làm k lần → cô chấm → giữ bài chịu → ôn. **Đúng** = máy chấm chịu. Mac toy ≠ số paper.

Select (dạy): preset `reward`. Exam: mọi preset trong bảng.

| Vòng | Preset | pass@1 | pass@2 | Giữ / ôn | A thêm đề | B ổn định | C mất đề |
|------|--------|--------|----------|----------|-----------|-----------|----------|
| 0 | default | 48.2% | 58.8% | 293 | — | — | — |
| 0 | reward | 48.2% | 58.8% | 293 | — | — | — |
| 1 | default | 44.0% | 53.2% | 273 | 33 | 27 | 61 |
| 1 | reward | 44.0% | 53.2% | 273 | 33 | 27 | 61 |

## Chữ viết (đếm trên mọi lần làm)

| Vòng | n | boxed | dfrac | tfrac | frac | dollar | sentence | assignment | unit | decimal | decimal_trailing | int_float |
|------|---|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|
| 0 | 1600 | 1456 | 8 | 0 | 925 | 88 | 21 | 457 | 0 | 198 | 24 | 6 |
| 1 | 1600 | 1367 | 6 | 0 | 932 | 74 | 8 | 427 | 1 | 202 | 20 | 3 |

Cách đọc (TOI-HIEU): pass@1 tăng **và** pass@k đứng/giảm **và** chữ tụ một kiểu → manh mối mạnh đang học chữ cô, không học toán. Một mình một cột thì chưa đủ.

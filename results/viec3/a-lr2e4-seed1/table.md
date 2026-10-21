# Việc 3 — vòng generate-verify-select-train

Mỗi vòng: học sinh làm k lần → cô chấm → giữ bài chịu → ôn. **Đúng** = máy chấm chịu. Mac toy ≠ số paper.

Select (dạy): preset `reward`. Exam: mọi preset trong bảng.

| Vòng | Preset | pass@1 | pass@4 | Giữ / ôn | A thêm đề | B ổn định | C mất đề |
|------|--------|--------|----------|----------|-----------|-----------|----------|
| 0 | default | 33.3% | 50.0% | 440 | — | — | — |
| 0 | reward | 33.3% | 50.0% | 440 | — | — | — |
| 1 | default | 27.3% | 46.7% | 395 | 11 | 7 | 16 |
| 1 | reward | 27.3% | 46.7% | 395 | 11 | 7 | 16 |
| 2 | default | 31.3% | 46.7% | 343 | 12 | 10 | 12 |
| 2 | reward | 31.3% | 46.7% | 343 | 12 | 10 | 12 |

## Chữ viết (đếm trên mọi lần làm)

| Vòng | n | boxed | dfrac | tfrac | frac | dollar | sentence | assignment | unit | decimal | decimal_trailing | int_float |
|------|---|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|
| 0 | 2000 | 1038 | 12 | 0 | 1115 | 103 | 6 | 481 | 0 | 230 | 24 | 5 |
| 1 | 2000 | 997 | 10 | 0 | 1116 | 77 | 8 | 520 | 0 | 240 | 25 | 12 |
| 2 | 2000 | 890 | 6 | 0 | 1109 | 129 | 23 | 494 | 0 | 225 | 30 | 12 |

Cách đọc (TOI-HIEU): pass@1 tăng **và** pass@k đứng/giảm **và** chữ tụ một kiểu → manh mối mạnh đang học chữ cô, không học toán. Một mình một cột thì chưa đủ.

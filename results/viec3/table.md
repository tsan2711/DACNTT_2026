# Việc 3 — vòng generate-verify-select-train

Mỗi vòng: học sinh làm k lần → cô chấm → giữ bài chịu → ôn. **Đúng** = máy chấm chịu. Mac toy ≠ số paper.

Select (dạy): preset `reward`. Exam: mọi preset trong bảng.

| Vòng | Preset | pass@1 | pass@4 | Giữ / ôn | A thêm đề | B ổn định | C mất đề |
|------|--------|--------|----------|----------|-----------|-----------|----------|
| 0 | default | 100.0% | 100.0% | 300 | — | — | — |
| 0 | reward | 100.0% | 100.0% | 300 | — | — | — |
| 1 | default | 100.0% | 100.0% | 300 | 0 | 0 | 0 |
| 1 | reward | 100.0% | 100.0% | 300 | 0 | 0 | 0 |

## Chữ viết (đếm trên mọi lần làm)

| Vòng | n | boxed | dfrac | tfrac | frac | dollar | sentence | assignment | unit | decimal | decimal_trailing | int_float |
|------|---|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|
| 0 | 400 | 100 | 100 | 0 | 0 | 0 | 100 | 0 | 0 | 0 | 0 | 100 |
| 1 | 400 | 100 | 100 | 0 | 0 | 0 | 100 | 0 | 0 | 0 | 0 | 100 |

Cách đọc (TOI-HIEU): pass@1 tăng **và** pass@k đứng/giảm **và** chữ tụ một kiểu → manh mối mạnh đang học chữ cô, không học toán. Một mình một cột thì chưa đủ.

# Việc 3 — vòng generate-verify-select-train

Mỗi vòng: học sinh làm k lần → cô chấm → giữ bài chịu → ôn. **Đúng** = máy chấm chịu. Mac toy ≠ số paper.

Select (dạy): preset `reward`. Exam: mọi preset trong bảng.

| Vòng | Preset | pass@1 | pass@4 | Giữ / ôn | A thêm đề | B ổn định | C mất đề |
|------|--------|--------|----------|----------|-----------|-----------|----------|
| 0 | default | 31.3% | 51.3% | 424 | — | — | — |
| 0 | reward | 31.3% | 51.3% | 424 | — | — | — |
| 1 | default | 31.3% | 46.0% | 386 | 12 | 7 | 20 |
| 1 | reward | 31.3% | 46.0% | 386 | 12 | 7 | 20 |
| 2 | default | 27.3% | 44.7% | 350 | 14 | 6 | 16 |
| 2 | reward | 27.3% | 44.7% | 350 | 14 | 6 | 16 |

## Chữ viết (đếm trên mọi lần làm)

| Vòng | n | boxed | dfrac | tfrac | frac | dollar | sentence | assignment | unit | decimal | decimal_trailing | int_float |
|------|---|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|
| 0 | 2000 | 1085 | 13 | 0 | 1114 | 98 | 8 | 495 | 0 | 236 | 21 | 9 |
| 1 | 2000 | 1009 | 7 | 0 | 1127 | 81 | 5 | 523 | 0 | 243 | 23 | 12 |
| 2 | 2000 | 735 | 6 | 0 | 1037 | 66 | 6 | 485 | 0 | 234 | 27 | 14 |

Cách đọc (TOI-HIEU): pass@1 tăng **và** pass@k đứng/giảm **và** chữ tụ một kiểu → manh mối mạnh đang học chữ cô, không học toán. Một mình một cột thì chưa đủ.

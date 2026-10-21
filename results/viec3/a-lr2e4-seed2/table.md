# Việc 3 — vòng generate-verify-select-train

Mỗi vòng: học sinh làm k lần → cô chấm → giữ bài chịu → ôn. **Đúng** = máy chấm chịu. Mac toy ≠ số paper.

Select (dạy): preset `reward`. Exam: mọi preset trong bảng.

| Vòng | Preset | pass@1 | pass@4 | Giữ / ôn | A thêm đề | B ổn định | C mất đề |
|------|--------|--------|----------|----------|-----------|-----------|----------|
| 0 | default | 31.3% | 51.3% | 424 | — | — | — |
| 0 | reward | 31.3% | 51.3% | 424 | — | — | — |
| 1 | default | 33.3% | 48.0% | 419 | 9 | 11 | 14 |
| 1 | reward | 33.3% | 48.0% | 419 | 9 | 11 | 14 |
| 2 | default | 25.3% | 45.3% | 361 | 12 | 4 | 16 |
| 2 | reward | 25.3% | 45.3% | 361 | 12 | 4 | 16 |

## Chữ viết (đếm trên mọi lần làm)

| Vòng | n | boxed | dfrac | tfrac | frac | dollar | sentence | assignment | unit | decimal | decimal_trailing | int_float |
|------|---|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|
| 0 | 2000 | 1085 | 13 | 0 | 1114 | 98 | 8 | 495 | 0 | 236 | 21 | 9 |
| 1 | 2000 | 1037 | 8 | 0 | 1150 | 80 | 7 | 492 | 0 | 242 | 25 | 9 |
| 2 | 2000 | 990 | 3 | 0 | 1080 | 151 | 16 | 484 | 0 | 243 | 25 | 10 |

Cách đọc (TOI-HIEU): pass@1 tăng **và** pass@k đứng/giảm **và** chữ tụ một kiểu → manh mối mạnh đang học chữ cô, không học toán. Một mình một cột thì chưa đủ.

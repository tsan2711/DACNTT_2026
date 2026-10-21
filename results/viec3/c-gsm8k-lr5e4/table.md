# Việc 3 — vòng generate-verify-select-train

Mỗi vòng: học sinh làm k lần → cô chấm → giữ bài chịu → ôn. **Đúng** = máy chấm chịu. Mac toy ≠ số paper.

Select (dạy): preset `reward`. Exam: mọi preset trong bảng.

| Vòng | Preset | pass@1 | pass@4 | Giữ / ôn | A thêm đề | B ổn định | C mất đề |
|------|--------|--------|----------|----------|-----------|-----------|----------|
| 0 | default | 70.7% | 86.0% | 971 | — | — | — |
| 0 | reward | 70.7% | 86.0% | 971 | — | — | — |
| 1 | default | 64.7% | 86.0% | 933 | 11 | 9 | 11 |
| 1 | reward | 64.7% | 86.0% | 933 | 11 | 9 | 11 |
| 2 | default | 48.7% | 76.7% | 813 | 4 | 8 | 18 |
| 2 | reward | 48.7% | 76.7% | 813 | 4 | 8 | 18 |

## Chữ viết (đếm trên mọi lần làm)

| Vòng | n | boxed | dfrac | tfrac | frac | dollar | sentence | assignment | unit | decimal | decimal_trailing | int_float |
|------|---|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|
| 0 | 2000 | 1719 | 0 | 0 | 852 | 629 | 10 | 128 | 36 | 262 | 167 | 86 |
| 1 | 2000 | 1571 | 0 | 0 | 882 | 666 | 9 | 135 | 36 | 266 | 158 | 87 |
| 2 | 2000 | 1488 | 0 | 0 | 867 | 915 | 14 | 109 | 36 | 291 | 129 | 96 |

Cách đọc (TOI-HIEU): pass@1 tăng **và** pass@k đứng/giảm **và** chữ tụ một kiểu → manh mối mạnh đang học chữ cô, không học toán. Một mình một cột thì chưa đủ.

# Việc 3 — vòng generate-verify-select-train

Mỗi vòng: học sinh làm k lần → cô chấm → giữ bài chịu → ôn. **Đúng** = máy chấm chịu. Mac toy ≠ số paper.

Select (dạy): preset `reward`. Exam: mọi preset trong bảng.

| Vòng | Preset | pass@1 | pass@8 | Giữ / ôn | A thêm đề | B ổn định | C mất đề |
|------|--------|--------|----------|----------|-----------|-----------|----------|
| 0 | default | 50.0% | 72.6% | 3962 | — | — | — |
| 0 | reward | 50.0% | 72.6% | 3962 | — | — | — |
| 1 | default | 46.2% | 71.5% | 3730 | 47 | 75 | 58 |
| 1 | reward | 46.2% | 71.5% | 3730 | 47 | 75 | 58 |
| 2 | default | 44.5% | 70.2% | 3395 | 53 | 88 | 66 |
| 2 | reward | 44.5% | 70.2% | 3395 | 53 | 88 | 66 |
| 3 | default | 32.4% | 63.6% | 2638 | 51 | 60 | 117 |
| 3 | reward | 32.4% | 63.6% | 2638 | 51 | 60 | 117 |
| 4 | default | 18.6% | 48.6% | 1566 | 44 | 43 | 194 |
| 4 | reward | 18.6% | 48.6% | 1566 | 44 | 43 | 194 |

## Chữ viết (đếm trên mọi lần làm)

| Vòng | n | boxed | dfrac | tfrac | frac | dollar | sentence | assignment | unit | decimal | decimal_trailing | int_float |
|------|---|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|
| 0 | 8000 | 5608 | 24 | 0 | 3916 | 1453 | 48 | 1179 | 72 | 952 | 378 | 198 |
| 1 | 8000 | 5047 | 10 | 0 | 4066 | 1577 | 58 | 1198 | 72 | 1030 | 380 | 203 |
| 2 | 8000 | 4736 | 16 | 1 | 4196 | 2095 | 111 | 1186 | 72 | 1126 | 376 | 207 |
| 3 | 8000 | 4321 | 87 | 2 | 4094 | 2998 | 107 | 1058 | 74 | 1184 | 275 | 222 |
| 4 | 8000 | 2693 | 241 | 5 | 3700 | 3406 | 40 | 795 | 73 | 1060 | 205 | 202 |

Cách đọc (TOI-HIEU): pass@1 tăng **và** pass@k đứng/giảm **và** chữ tụ một kiểu → manh mối mạnh đang học chữ cô, không học toán. Một mình một cột thì chưa đủ.

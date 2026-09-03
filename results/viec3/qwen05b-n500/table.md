# Việc 3 — vòng generate-verify-select-train

Mỗi vòng: học sinh làm k lần → cô chấm → giữ bài chịu → ôn. **Đúng** = máy chấm chịu. Mac toy ≠ số paper.

Select (dạy): preset `reward`. Exam: mọi preset trong bảng.

| Vòng | Preset | pass@1 | pass@8 | Giữ / ôn | A thêm đề | B ổn định | C mất đề |
|------|--------|--------|----------|----------|-----------|-----------|----------|
| 0 | default | 31.1% | 60.5% | 2533 | — | — | — |
| 0 | reward | 31.1% | 60.5% | 2533 | — | — | — |
| 1 | default | 31.9% | 58.9% | 2454 | 74 | 91 | 90 |
| 1 | reward | 31.9% | 58.9% | 2454 | 74 | 91 | 90 |
| 2 | default | 29.9% | 56.1% | 2339 | 65 | 74 | 93 |
| 2 | reward | 29.9% | 56.1% | 2339 | 65 | 74 | 93 |
| 3 | default | 28.9% | 55.5% | 2267 | 76 | 73 | 82 |
| 3 | reward | 28.9% | 55.5% | 2267 | 76 | 73 | 82 |
| 4 | default | 27.4% | 54.9% | 2123 | 79 | 71 | 85 |
| 4 | reward | 27.4% | 54.9% | 2123 | 79 | 71 | 85 |

## Chữ viết (đếm trên mọi lần làm)

| Vòng | n | boxed | dfrac | tfrac | frac | dollar | sentence | assignment | unit | decimal | decimal_trailing | int_float |
|------|---|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|
| 0 | 8000 | 5880 | 28 | 0 | 3940 | 1292 | 87 | 1158 | 72 | 1101 | 391 | 171 |
| 1 | 8000 | 5839 | 24 | 0 | 4057 | 1297 | 114 | 1134 | 71 | 1099 | 409 | 163 |
| 2 | 8000 | 5711 | 22 | 0 | 4120 | 1306 | 79 | 1182 | 69 | 1218 | 395 | 173 |
| 3 | 8000 | 5631 | 19 | 0 | 4219 | 1295 | 66 | 1230 | 71 | 1175 | 425 | 169 |
| 4 | 8000 | 5513 | 22 | 0 | 4250 | 1327 | 47 | 1284 | 73 | 1205 | 411 | 172 |

Cách đọc (TOI-HIEU): pass@1 tăng **và** pass@k đứng/giảm **và** chữ tụ một kiểu → manh mối mạnh đang học chữ cô, không học toán. Một mình một cột thì chưa đủ.

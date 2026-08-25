# Luật cho Claude Code trong repo này

## Dữ liệu luôn phải cào ở hiện tại, không lấy từ trí nhớ huấn luyện

Khi cần thông tin về: bài báo (tên chính xác, tác giả, ngày đăng, arXiv ID),
số liệu benchmark, phiên bản thư viện (`math-verify`, `trl`, `transformers`,
`peft`, `vllm`, `mlx-lm`), hoặc bất cứ thứ gì có thể đã đổi sau khi model được
huấn luyện — **PHẢI** dùng `WebSearch`/`WebFetch` để lấy dữ liệu thật tại thời
điểm làm việc, không được liệt kê từ trí nhớ rồi coi là xong.

Lý do: agent hay tự tin liệt kê tên bài báo / số arXiv / số bản mới nhất từ
trí nhớ huấn luyện, nhưng trí nhớ đó đông cứng ở thời điểm cắt (knowledge
cutoff) — có thể sai tên, sai số, sai ngày, hoặc bỏ sót bài mới ra sau đó.
Đề tài này (xem `TOI-HIEU.md`) đứng trên tuyên bố "chưa ai làm hướng này" —
tuyên bố đó chỉ đứng vững nếu danh sách bài đã đọc là danh sách thật, tra lại
được, không phải bịa từ trí nhớ.

Áp dụng cụ thể:
- Liệt kê/tìm bài báo liên quan: tìm trên arXiv/Google Scholar qua WebSearch,
  xác nhận tiêu đề + arXiv ID + ngày đăng trước khi đưa vào bất kỳ file nào
  trong `papers/`.
- Trước khi trích số liệu từ một bài báo (ví dụ FP/FN của verifier) vào tài
  liệu nào đó: mở bài báo thật qua WebFetch, đọc đúng bảng số, không thuật
  lại từ trí nhớ.
- Cài đặt / phiên bản thư viện (`math-verify==?`, `trl==?`...): tra
  PyPI/GitHub release hiện tại nếu cần biết bản mới nhất, đừng đoán.

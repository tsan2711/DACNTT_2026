# Đề tài — khung đã chốt (session 2026-08-16)

Sản phẩm: **một bài báo**. Không phải app, không phải model để bán.

## Đề (title + claim) — cái này mới là đề

**Title:** Self-improving small reasoning models through generate-verify-train iterations.

**Claim:** SLM **tự cải thiện reasoning** qua vòng **generate → verify → select → train**, không cần thêm human annotation.

```
generate  — SLM viết bài (máy giải)
verify    — math-verify so đáp án với sách (máy chấm)
select    — giữ bài máy chấm chịu, bỏ bài bị gạch
train     — dạy lại chính SLM bằng những bài được giữ
          — lặp
```

"Self-improving" = không người gán nhãn bài mới. **Không** phải một máy vừa sinh vừa chấm.

## Câu hỏi nghiên cứu (nằm trong đề, không thay đề)

Người ta tin vòng GVT dạy SLM **giỏi reasoning hơn**.

Máy chấm hay gạch bài đúng vì **cách viết**. Vậy sau nhiều vòng: SLM đang cải thiện reasoning, hay chỉ học **viết đúng kiểu máy chấm ưa**?

Mình **không sửa** máy chấm (đó là TinyV). Mình **chạy vòng GVT và đo** xem claim self-improve có đứng không.

`BAI-GIANG.md` = kế hoạch đo / việc 1–2–3. Không đọc nó như một đề tài khác.

## Đề bằng một chuyện (đọc khi lại rối)

Có học sinh nhỏ (SLM). Có giáo viên keo (`math-verify`): chỉ nhìn đáp án cuối, hay gạch vì chữ (`1/2` vs `0.5`).

Mỗi khóa: học sinh làm bài → giáo viên giữ bài “đúng”, bỏ bài “sai” → học sinh ôn đúng những bài được giữ → khóa sau.

Người ta đặt tên: học sinh **tự tiến bộ**, không cần gia sư chấm từng bài (không human annotation). Đó là **generate-verify-select-train**. Đó là **tên đề tài**.

Việc của bạn **không** phải thay giáo viên, cũng không phải chế học sinh giỏi hơn để bán. Việc của bạn: cho chạy vài khóa, rồi trả lời trên bài báo:

> Học sinh có giỏi toán hơn thật không, hay chỉ học chữ giáo viên ưa?

Title = vòng đó + câu chuyện “tự tiến bộ”.  
Bài giảng = cách kiểm câu chuyện đó. Một đề, không phải hai.

## Tư duy hay rẽ nhầm

Nghe “verify” → nghĩ phải **sửa máy chấm**. Đó là TinyV.  
Nghe “self-improve / nhiều lời giải đúng” → nghĩ phải **giúp model hiểu nghĩa**. Đề không làm việc đó.  
Nghe pass@k → nghĩ **nhiều cách giải**. `k` chỉ là số lần làm lại cùng đề.

Mình **chạy vòng + đo claim**. Không tối ưu hệ thống cho “tốt hơn”.

## “Reasoning” cụ thể là gì (gốc vấn đề)

Không phải “hiểu nghĩa”, không phải IQ. Trong đề này, **reasoning = các bước làm bài**, từ đề tới đáp án.

Đề: *Lan có 3 hộp, mỗi hộp 4 quả. Ăn 2 quả. Còn bao nhiêu?*

| Phần bài | Ví dụ | Máy chấm có nhìn không? |
|----------|--------|-------------------------|
| **Reasoning** (lời) | 3×4=12, 12−2=10 | **Không.** |
| **Đáp án** (chữ cuối) | `10` hoặc `\boxed{10}` | **Có.** Chỉ cái này. |

Claim GVT: sau nhiều vòng, SLM **làm các bước đúng hơn** (ít sai phép, ít nhảy bước).  
Máy chấm **không bao giờ chấm bước**. Nó chỉ so chuỗi đáp án với sách — và hay gạch vì kiểu viết.

**Gốc:** vòng khoe “cải thiện reasoning” nhưng tín hiệu học chỉ là “chữ cuối có được chịu không”.  
Vì vậy điểm một phát tăng **chưa** nói được bước làm khá hơn — có thể chỉ chữ cuối ngày càng giống sách.

Trong `BAI-GIANG.md`, “giỏi toán” = reasoning (bước). “Học chữ” = tối ưu chuỗi đáp án cho máy chấm.

---

## Hai máy — không phải một máy tự làm tự chấm

| Máy | Tên kỹ thuật | Việc của nó | Việc nó **không** làm |
|-----|--------------|-------------|------------------------|
| **Máy giải toán** | model (Qwen…) | Đọc đề, **sinh** lời giải / đáp án | Không chấm, không biết đáp án sách |
| **Máy chấm** | `math-verify` | Lôi đáp án trong bài, **so với sách** | Không sinh lời giải, không đọc lập luận |

Máy chấm **không** viết bài. Máy giải **không** tự chấm. Mình ghép hai máy thành một vòng:

```
máy giải toán viết bài
        ↓
máy chấm: đúng (so với sách) thì giữ, sai thì bỏ
        ↓
lấy những bài “đúng” dạy lại máy giải toán
        ↓
lặp lại
```

Giống học sinh làm bài, giáo viên chỉ nhìn đáp án cuối (không đọc lời). Giáo viên không soạn bài hộ học sinh.

Việc 1–2 chỉ soi **máy chấm** (chưa cần máy giải, hoặc chỉ lấy bài máy giải có sẵn trên mạng). Việc 3 mới cho máy giải học nhiều vòng.

---

## Ba số ở việc 3 (đã sửa chỗ dễ lẫn)

Cùng **một bộ đề**. `k` = số lần **làm lại cùng đề**. Không phải số dạng đề. Không phải số cách giải.

| Số | Đo gì | Không đo gì |
|----|--------|-------------|
| **pass@1** | Bấm 1 lần, máy chấm bảo đúng bao nhiêu đề | Không nói vì toán hay vì chữ |
| **pass@k** | Làm k lần, **bao nhiêu đề** có ít nhất 1 lần máy chấm chịu | Không nói k lần đó có nhiều lời giải khác nhau không |
| **Chữ viết** | Các bài có ngày càng **một kiểu** không | Không nói điểm cao hay thấp |

“Đúng” luôn là **máy chấm chịu**, không phải mình đọc tay.

pass@k tăng ≠ đa dạng lời giải. Một khuôn lặp k lần, miễn có 1 lần được chấp nhận là đề đó vẫn pass.

Hai số này **không cover hết** “giải được thêm nhiều bài hơn”. Chúng chỉ là proxy.

“Thêm bài” đúng nghĩa phải xem **từng đề đổi trạng thái thế nào**, không chỉ hai số trung bình:

| Đề | Trước | Sau | Nghĩa |
|----|--------|-----|--------|
| A | 8 lần không lần nào được chấm đúng | Có ít nhất 1 lần được chấm đúng | **Thêm đề** (theo máy chấm) |
| B | Đã thỉnh thoảng đúng, lần đầu hay sai | Vẫn cùng đề đó, lần đầu hay đúng hơn | **Ổn định hơn**, không thêm đề |
| C | Đã từng đúng trong 8 lần | 8 lần không còn lần nào đúng | **Mất đề** |

pass@1 chỉ thấy B (và một phần A nếu lần đầu cũng đúng).  
pass@k thấy A − C gộp lại thành một số: “số đề có ≥1 lần đúng”. Tăng/giảm **không nói** bao nhiêu đề mới, bao nhiêu đề mất.

Còn trống dù có cả hai số:

- Không tách A / B / C.
- `k` hữu hạn: đề chỉ đúng lần thứ 20 thì pass@8 coi như không bao giờ đúng.
- “Được chấm đúng” ≠ “biết toán” (chữ đổi là A giả).

Muốn đo “thêm bài” thật: đếm số đề loại A (và C), không chỉ nhìn pass@1 / pass@k. Việc 3 tối thiểu vẫn ghi hai số đó + chữ; nếu làm kỹ thì thêm bảng A/B/C.

---

## Bốn trường hợp — nói được tới đâu

**1. pass@1 tăng, pass@k tăng, chữ vẫn đủ kiểu**

Máy chấm thấy “đúng” nhiều đề hơn — cả một phát lẫn cho thử lại.

Không được nói “đang học toán”. Có thể biết thêm bài; cũng có thể bài cũ trước bị gạch vì chữ, giờ được nhận.

Với đề bài: **chưa chứng minh** chỉ học chữ. Cũng **chưa chứng minh** học toán.

**2. pass@1 tăng, pass@k đứng/giảm, chữ tụ một kiểu**

Một phát hay được chấm đúng hơn. Cho thử k lần **không** thêm đề. Chữ ngày càng một kiểu máy chấm ưa.

Bộ manh mối **mạnh nhất** cho câu đề muốn: đang học chữ, không học toán.

**3. Chỉ pass@1 tăng, chữ chưa tụ**

Chưa đủ. Model có thể chỉ ổn định hơn.

**4. Chỉ chữ tụ, điểm không đổi**

Chưa đủ. Đồng phục một mình không chứng minh việc học bị lệch theo điểm.

Muốn nói “học chữ, không học toán”: cần **điểm một phát tăng** + **không thêm đề khi thử lại** + **chữ tụ**. Thiếu một mảnh → chỉ được nói “chưa chắc”.

---

## Chỗ đã phân vân (giữ để khỏi quay lại)

- Đề = vòng GVT + claim self-improve. Session trước từng giảng như thể đề = “chỉ đo máy chấm / không cải thiện model” — **thiếu khung**, dễ nhầm TinyV.
- `k` không phải “đề đa dạng” và không phải số cách giải.
- Câu trong `BAI-GIANG.md` (“vẫn còn nhiều cách đúng không?”) **lỏng** — đừng dùng câu đó.
- Cả hai pass tăng **không** suy ra đang học toán / reasoning.
- pass@1 / pass@k **không cover hết** “thêm bài”. Cần tách đề loại A (mới chạm) / B (cùng đề, ổn định hơn) / C (mất).

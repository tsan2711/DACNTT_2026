# Kịch bản báo cáo kết quả (≈4 phút)

Mở `papers/latex/paper_revised.pdf` ở trang 9, Bảng 5. Kịch bản có 6 đoạn, đoạn sau nối vào câu cuối của
đoạn trước. Nếu thầy hỏi sâu thì mở `HOI-DAP.md`.

---

### Đoạn 1: Bảng 5 là gì

*[chỉ tiêu đề Bảng 5]*

> Thưa thầy, đề tài của nhóm em kiểm tra xem một model nhỏ, Qwen2.5-1.5B, có tự giỏi toán lên được không:
> model tự giải bài, máy chấm tự động lọc ra bài đúng, rồi model học lại từ chính các bài đó, lặp nhiều vòng.
> Em xin báo cáo thẳng vào kết quả. Bảng 5 gom kết quả của **mọi lần chạy** trong đề tài. Mỗi
> dòng là một lần chạy, được chấm trên 150 đề mà model chưa từng học. Bảng chia thành bốn khối theo
> learning rate, từ train nhẹ ở trên xuống train mạnh ở dưới. Mỗi ô ghi mức thay đổi điểm từ trước khi
> train đến sau vòng cuối, số âm nghĩa là giảm.

### Đoạn 2: cách đọc một ô

*[chỉ ô A, seed 1, khối 5×10⁻⁴, cột ∆sample acc.: −8,3 [−12,3; −4,5]]*

> Để đọc bảng, em lấy ô này làm ví dụ. Số −8,3 là mức giảm **đo được** trên 150 đề. Nhưng 150 đề là ít, đổi
> sang bộ đề khác thì con số sẽ xê dịch. Vì vậy nhóm bốc lại ngẫu nhiên bộ đề 10.000 lần, tính lại mỗi lần,
> rồi lấy khoảng chứa 95% kết quả. Đó là hai số trong ngoặc: biên dưới −12,3, biên trên −4,5. Vì **ngay cả
> biên trên cũng âm**, nên đây là giảm thật, không phải do may rủi. Ngược lại, nếu khoảng có cả âm lẫn
> dương, tức là chứa số 0, thì nhóm chỉ nói là chưa biết.

### Đoạn 3: kết quả chính

*[dò cột ∆pass@1 và ∆pass@k từ trên xuống]*

> Đọc theo cách đó, cả bảng cho một kết quả rõ ràng: **không có ô nào mà cả khoảng nằm trên 0**, tức là không
> lần chạy nào tiến bộ thật. Thước đo chốt trước khi chạy là pass@1, và ở pass@1 cũng vậy. Ở thước đo ít nhiễu
> hơn là độ chính xác mẫu, biên trên cao nhất chỉ là +2,2. Nghĩa là nếu model có tăng thì cũng không quá
> khoảng 2 điểm.
>
> *[chỉ khối 5×10⁻⁴]* Không những không tăng, ở mức train mạnh nhất model còn **giảm thật**: bốn run A và B
> giảm từ 4,7 đến 9,2 điểm, và cả bốn khoảng đều nằm dưới 0.

### Đoạn 4: kết quả âm này có đáng tin không

> Một kết quả âm thì phải loại được các cách giải thích khác. Nhóm đã kiểm tra năm khả năng.
>
> **Thứ nhất, có phải do train quá nhẹ không?** *[chỉ bốn khối]* Không, vì nhóm đã thử bốn mức learning
> rate cách nhau 50 lần, và không mức nào tăng.
>
> **Thứ hai, nếu không phải do train, liệu có phải do dữ liệu train không?** *[chỉ dòng No filter, Gold]*
> Ở cùng mức 5e-4, nhóm đổi dữ liệu theo hai hướng ngược nhau. Bỏ hẳn máy chấm, cho học cả bài sai, thì vẫn
> giảm 8 đến 10 điểm. Cho học lời giải mẫu do người viết, tức là dữ liệu tốt nhất có thể, thì còn giảm nặng
> nhất, khoảng 19 điểm. Đổi dữ liệu thế nào cũng không cứu được.
>
> **Thứ ba, nếu dữ liệu không phải nguyên nhân, liệu máy chấm có chấm sai lúc kiểm tra không?** Đúng là nhóm
> phát hiện máy chấm loại nhầm khoảng 1/6 lời giải đúng. Nhưng khi chấm lại năm run bằng máy chấm đã sửa,
> cả năm vẫn giảm, thậm chí giảm mạnh hơn. Ví dụ Run A ở 5e-4 giảm 10,7 và 6,0 điểm, thay vì 8,3 và 4,7.
> Như vậy lỗi máy chấm chỉ làm mức giảm trông nhỏ hơn thực tế.
>
> **Thứ tư, nếu chấm đúng mà vẫn giảm, liệu model chỉ viết dài ra rồi bị cắt ở 512 token không?** *[chỉ cột
> cuối "Finished, matched"]* Cột cuối chỉ tính các lời giải viết xong. Ở 5e-4, chính các lời giải viết xong
> cũng kém hơn model gốc 5,5 đến 9,1 điểm. Nhóm còn train lại với giới hạn 1.024 token và vẫn giảm. Vậy
> model thật sự giải sai nhiều hơn.
>
> **Cuối cùng, liệu đây chỉ là chuyện riêng của bộ đề MATH-500?** *[chỉ dòng C]* Không, vì Run C trên bộ
> GSM8K cũng giảm.

### Đoạn 5: kết luận

*[lật sang trang 12, mục 7]*

> Vì đã loại được cả năm khả năng đó, nhóm đi đến kết luận: ở quy mô 1.5B, **vòng lặp tự học không làm model
> giỏi toán hơn, còn train mạnh thì model kém đi**.

### Đoạn 6: giới hạn và tình trạng

> Kết luận này có phạm vi rõ ràng: một model 1.5B, một cách fine-tune là LoRA, một máy chấm, và phần lớn
> cấu hình chỉ có hai seed. Về tình trạng: thí nghiệm đã chạy xong và chốt, paper đã viết xong. Hướng tiếp
> theo là train lại với máy chấm đã sửa lỗi. Em xin hết, mời thầy góp ý.

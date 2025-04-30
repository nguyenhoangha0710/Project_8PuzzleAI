# **Giải bài toán 8-Puzzle**
## **Giới thiệu**
8-Puzzle Solver là 1 ứng dụng đồ họa cho phép giải quyết bài toán 8-Puzzle bằng nhiều thuật toán tìm kiếm khác nhau. Ứng dụng cung cậps giao diện trực quan để theo dõi quá trình giải quyết, so sánh hiệu suất giữa các thuật toán và xuất kết quả để phân tích.

## **Bài toán 8-Puzzle là gì?**
Bài toán 8-Puzzle là một trò chơi di chuyển các ô số trên bảng 3x3, trong đó có 8 được đánh số từ 1 - 8 và 1 ô trống. Người chơi chỉ có thể di chuyển các ô liền kề với ô trống vào vị trí của ô trống. Mục tiêu là sắp xếp các ô về trạng thái mục tiêu mà người chơi đề ra. 
Trong ứng dụng này, trạng thái đích là:

              | 1 | 2 | 3 |
              | 4 | 5 | 6 |
              | 7 | 8 | 0 |

## **Tính năng**
* **Đa dạng thuật toán:** BFS,DFS,UCS,GBFS,A*,IDA*,Hill ClimBing,Stochastic Hill Climbing, Simulated Anealing, Beam Search, And or search , Belief Enviroment Search, BackTracking
* **Giao diện trực quan:** Theo dõi các trạng thái bắt đầu, hiện tại và đích
* **Điều khiển bước giải:** Chạy từng bước, tự động chạy, quay ngược bước trước
* **Tùy chỉnh trạng thái ban đầu:** Nhập trạng thái 8-Puzzle tùy chọn
* **Thống kê chi tiết:** So sánh thời gian thực thi, số bước thực hiện, chi phí và không gian tìm kiếm giữa các thuật toán
* **Trực quan hóa dữ liệu**: Tạo biểu đồ so sánh hiệu suất giữa các thuật toán
* **Xuất kết quả:** Lưu kết quả và đường đi vào file Excel để tiện cho phân tích sau này
## **Yêu cầu hệ thống**
Môi trường Python
Các thư viện: 
  * Tkinter(GUI)
  * pandas (Xử lý dữ liệu)
  * matplotlib (Trực quan hóa)
  * Các thư viên chuẩn khác : time, copy, collections, heapq
## **Hướng dẫn sử dụng**
### **Cách thiết lập trạng thái ban đầu**
Trạng thái ban đầu (mặc định):

         | 1 | 6 | 2 |
         | 5 | 7 | 4 |
         | 8 | 3 | 0 |
1. Nhập các giá trị có giá từ 0-8 vào lưới "Start State" (0 đại diện cho ô trống hoặc không nhập gì)
2. Nhấn nút "Update Start" để cập nhật lại trạng thái ban đầu
   ![State 8-Puzzle](https://github.com/user-attachments/assets/dacc31eb-68c5-469e-8e19-a11d263a3886)
   
### **Chạy các thuật toán**
1. Chọn thuật toán từ menu dropdown (BFS,DFS,UCS,...) hoặc các thuật toán có hướng xử lý khác ở bên ngoài menu
   ![Select Algorithm](https://github.com/user-attachments/assets/0418a759-fb66-485b-8cce-b552caa83046)
   
2. Nhấn nút "Run Algorithm" để thực thi thuật toán
3. Theo dõi tiến trình giải quyết trên giao diện "Current State"
### **Điều khiển quá trình giải**
  * **Next Step:** Di chuyển đến bước tiếp theo trong giải pháp
  * **Back Step:** Quay lại bước trước đó
  * **Auto Run:** Tự động thực hiện các bước với tốc độ 1 bước/giây
  * **Stop:** Dừng chế độ tự động chạy
  ![image](https://github.com/user-attachments/assets/f4ab9ac7-f8de-4131-b7b2-3f60f2555438)

### **Phân tích kết quả**
  * **Export:** Lưu đường đi giải quyết vào file Excel
  * **Plot Graph:** Tạo biểu đồ so sánh hiệu suất giữa các thuật toán đã chạy
  ![image](https://github.com/user-attachments/assets/b0d6e37d-2974-4867-9218-a5caba657888)
### **Các thuật toán tìm kiếm**
#### **Nhóm thuật toán tìm kiếm không có thông tin (Uninformed Search/Blind Search)**
##### 1. Breadth-First Search (BFS - Tìm kiếm theo chiều rộng):
   * Cách hoạt động: Khám phá tất cả các trạng thái ở cùng một mức (level) trước khi đi sâu hơn. Sử dụng hàng đợi
   * Ưu điểm: Đảm bảo tìm được đường đi ngắn nhất (chi phí mỗi bước là như nhau) nếu bài toán có lời giải
   * Nhược điểm: Tốn nhiều bộ nhớ vì phải lưu tất cả trạng thái ở mỗi mức
##### 2. Depth-First Search (DFS - Tìm kiếm theo chiều sâu)
   * Cách hoạt động: Khám phá một nhánh đến tận cùng trước khi quay lại và thử nhánh khác
   * Ưu điểm: Tốn ít bộ nhớ hơn BFS vì chỉ lưu một nhánh tại 1 thời điểm
   * Nhược điểm: Không đảm bảo tìm được đường đi ngắn nhất, có thể bị mắc kẹt
##### 3. Uniform Cost Search (UCS - Tìm kiếm chi phí đồng nhất)
   * Cách hoạt động: Mở rộng trạng thái có tổng chi phí thấp nhất từ trạng thái ban đầu (dựa vào chi phí đường đi không dựa trên heuritic)
   * Ưu điểm: Đảm bảo tìm được đường đi tối thiểu nếu chi phí mỗi bước là  như nhau
   * Nhược điểm: Tương tự BFS, tốn nhiều bộ nhớ
   * Trong úng dụng này, chi phí của mỗi bước di chuyển là như nhau
#### **Nhóm thuật toán tìm kiếm có thông tin**
##### **Đây là nhóm thuật toán sử dụng thông tin heuristic để ưu tiên khám phá các trạng thái có khả năng dẫn đến mục tiêu nhanh hơn**
##### **Đặc điểm:**
  * Sử dụng hàm heuristic (hàm ước lượng khảng cách từ trạng thái hiện tại đến trạng thái mục tiêu) để định hướng tìm kiếm
  * Nhanh hơn các thuật toán không có thông tin nhưng không phải lúc nào cũng đảm bảo tính tối ưu
  * **Hàm heuristic** được sử dụng trong bài toán: Tổng khoảng cách Manhattan (theo hàng và cột) của mỗi ô từ vị trí hiện tại đến vị trí mục tiêu
##### 1. Greedy Best-First Search(GBFS - Tìm kiếm tham lam theo ưu tiên):
   * Cách hoạt động: Chỉ dựa vào hàm heuristic để chọn trạng thái tiếp theo (trạng thái có giá trị heuristic thấp nhất)
   * Ưu điểm: Nhanh vì chỉ tập trung vào các trạng thái "hứa hẹn" nhất
   * Nhược điểm: không đảm bảo tối ưu (có thể mắc kẹt)
##### 2. A* Search(Tìm kiếm A*)
   * Cách hoạt động: Kết hợp chi phí đã đi (g) và heuristic (h): f(n)=g(n)+h(n). Mở rộng trạng thái có giá trị f(n) thấp nhất.
   * Ưu điểm: Đảm bảo tìm được đường đi tối ưu nếu hàm heuristic là "admissible" (không bao giờ đánh giá quá cao so với thực tế).
   * Nhược điểm: Khá tốn bộ nhớ
#### 3.Iterative Deepening A (IDA* - A* lặp sâu):
  *  Cách hoạt động: Kết hợp ý tưởng của Iterative Deepening (tăng dần giới hạn độ sâu) với A*. Mỗi vòng lặp sử dụng một ngưỡng f(n) để giới hạn tìm kiếm
  *  Ưu điểm: Tốn ít bộ nhớ hơn A* vì không lưu toàn bộ
  *  Nhược điểm: Có thể lặp lại việc khám phá trạng thái, dẫn đến thời gian chạy lâu hơn A*
### **Nhóm thuật tìm kiếm toán cục bộ**
#### Đây là thuật toán không khám phá toàn bộ trạng thái mà tập trung vào việc tập trung cải thiện một trạng thái hiện tại, thường dùng cho các bài toán tối ưu
#### Đặc điểm:
  * Bắt đầu từ một trạng thái ban đầu và cải thiện dần trạng thái đó theo một tiêu chí (thường là heuristic)
  * Không đảm bảo tìm được lời giải tối ưu toàn cục, nhưng nhanh và hiệu quả ở các bài toán lớn 
  * Không lưu trữ nhiều trạng thái, chỉ làm việc với một hoặc hai trạng thái tại 1 thời điểm
#### 1.Hill ClimBing(Leo đồi)
  * Cách hoạt động: Từ trạng thái hiện tại, chọn trạng thái láng giềng có giá trị heuristic tốt nhất (giảm nhất). Lặp lại cho đến khi không thể cải thiện thêm.
  * Ưu điểm: Rất nhanh, tốn ít bộ nhớ
  * Nhược điểm: Dễ bị mắc kẹt ở "đỉnh tối ưu cục bộ" (local optima), không đảm bảo tìm được mũ tiêu
#### 2. Stochastic Hill ClimBing (Leo đôi ngẫu nhiên): 
  * Cách hoạt động: Tương tự Hill ClimBing, nhưng thay vì chọn láng giềng tốt nhất thì chọn ngẫu nhiên một láng giềng có giá trị tổt hơn
  * Ưu điểm: Giảm khả năng bị mắc kẹt ở tối ưu cục bộ so với Hill Climbing thông thường
  * Nhược điểm: Vẫn không đảm bảo được lời giải
#### 3. Simulated Annealing (Ủ nhiệt mô phỏng)
  * Cách hoạt động: Giống Hill ClimBing, nhưng trong trường tất cả các láng giềng đều có giá trị xấu hơn trạng thái hiện tại, cho phép chọn trạng thái tiếp theo với xác suất phụ thuộc vào "nhiệt độ" (temperature). Nhiệt độ giảm dần theo thời gian.
  * Ưu điểm: Có khả năng thoát khỏi tối ưu cục bộ nhờ cơ chế ngẫu nhiên
  * Nhược điểm: Cần điều chỉnh tham số (nhiệt độ ban đầu, tốc độ giảm nhiệt) để đạt được hiệu quả
#### 4. Beam Search (Tìm kiếm chùm): 
  * Cách hoạt động: Kết hợp ý tưởng của BFS và tìm kiếm cục bộ. Chỉ giữ lại một số lượng cố định (beam width) các trạng thái tổt nhất với mỗi mức.
  * Ưu điểm: Tiết kiệm bộ nhớ so với BFS, nhanh hơn nhờ giới hạn trạng thái
  * Nhược điểm: Không đảm bảo tối ưu, có thể bỏ sót trạng thái dẫn đến mục tiêu
### **Nhóm thuật toán tìm kiếm trong môi trường không xác định**
#### Nondeterministic Enviroments : Đây là nhóm thuật toán được thiết kế để xử lý các bài toán mà kết quả của một hành động không chắc chắn (có thể dẫn đến nhiều trạng thái khác nhau)
#### 1. And-or search
  * Khái niệm cơ bản:
    - Trong không gian có 2 loại nút:
      + or nodes: Đại diện cho các lựa chọn của tác nhân (agent). Tác nhân chỉ chọn 1 nhánh con để giải quyết (tương tự như các nút thông thường)
      + and nodes: Đại diện cho kết quả không xác định của 1 hành động. Tác nhân phải giải quyết tất cả các nhánh con
  * Mục tiêu:  Là xây dựng một cây giải pháp, một kế hoạch để hướng đến trạng thái mục tiêu
  * Ưu điểm:
    - Xử lý môi trường không xác định
    - Kết quả là một cây giải pháp, cho phép tác nhân chuẩn bị cho mọi kịch bản có thể xảy ra
    - Ứng dụng rộng
  * Nhược điểm:
    - Phức tạp và tốn tài nguyên: Việc xây dựng cây giải pháp yêu cầu khám phá nhiều nhánh, dẫn đến chi phí tính toán và bộ nhớ cao
    - Khó triển khai
#### 2. Belief Search(Tìm kiếm dựa trên niềm tin)
  * Cách hoạt động: Được thiết kế cho các bài toán trong môi trường không xác định hoặc nhìn thấy một phần, nơi tác nhân không biết chính xác trạng thái hiện tại của mình. Tác nhân duy trì một tập belief state (tập hợp ác trạng thái có thể xảy ra) và cập nhật niềm tin dựa trên hành động và quan sát
  * Các bước hoạt động:
      - Khởi tạo belief state ban đầu và mục tiêu: Bắt đầu với một tập hợp trạng thái có thể xảy ra (dựa vào thông tin ban đầu)
      - Thực hiện hành động
        + Chọn một hành động
        + Dựa trên mô hình chuyển đổi trạng thái, tính toán tập hợp các trạng thái có thể xảy ra sau hành động
      - Cập nhật belief state dựa trên quan sát bằng cách loại bỏ đi những trại không phù hợp
      - Trả về kế hoạch: Kế hoạch là một chuỗi hành động đảm bảo đạt được mục tiêu, bất kể trạng thái thật sự là gì
  * Ưu điểm:
    - Xử lý các bài toán mà tác nhân không biết chính xác trạng thái hiện tại
    - Linh hoạt: Có thể kết hợp với các thuật toán tìm kiếm khác (như A*,BFS,...) trên không gian belief state để tối ưu hóa kế hoạch
    - Nhiều ứng dụng thực tế
  * Nhược điểm:
    - Phức tạp tính toán
    - Tốn bộ nhớ: Belief state có thể tăng trường theo cấp số nhân, dẫn đến khó khăn trong việc lưu trữ và xử lý
    - Khó triển khai
### **Nhóm thuật toán có ràng buộc điều kiện**
#### Định nghĩa: 
  * Biến (Variables) : Các đối tượng cần giá trị (Ví dụ: các ô trong lưới 8-Puzzle)
  * Miền giá trị (Domains): Tập hợp các giá trị có thể gán (ví dụ: các số từ 0 - 8 trong bài toán 8-Puzzle)
  * Ràng buộc (Constraints): Các điều kiện mà các biến phải thỏa mãn (vú dụ: Mỗi ô trong 8-Puzzle phải là duy nhất)
  * Mục tiêu: Tìm cách gán giá trị cho tất cả các biến sao cho thỏa mãn tất cả các ràng buộc trên
#### 1. Backtracking Search (Tìm kiếm quay lui):
  * Cách hoạt động: đệ quy để thử các giá trị cho từng biến, quay lui (backtrack) khi gặp đường cụt
  * Ưu điểm:
    - Đơn giản và dễ triển khai
    - Đảm bảo tìm được lời giải nếu có
    - Tốn ít bộ nhớ
  * Nhược điểm:
    - Hiệu suất thấp: Backtracking thử tất cả các khả năng 1 cách mù quáng, dẫn đến thời gian có thể chạy rất lâu nếu không gian tìm kiếm lớn
    - Không tối ưu: không đảm bảo tìm được đường đi ngắn nhất
      




















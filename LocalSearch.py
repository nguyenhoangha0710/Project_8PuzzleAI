


def SimpleHillClimbing(DoThi,GiaTriTaiDinh,DinhBanDau): 
    Dinghientai=DinhBanDau
    GiaTriHienTai=GiaTriTaiDinh[Dinghientai]
    print(f"Đỉnh ban đầu: {Dinghientai}, Giá trị = {GiaTriHienTai}")
    while True: 
        VungLanCan=DoThi[Dinghientai]
        dinhTotNhat=Dinghientai
        GiaTriTotNhat=GiaTriHienTai

        for dinh in VungLanCan: 
            gia_tri=GiaTriTaiDinh[dinh]
            if gia_tri > GiaTriTotNhat: 
                dinhTotNhat=dinh
                GiaTriTotNhat=gia_tri
        
        #neu khong cai thien
        if dinhTotNhat==Dinghientai:
            print(f"Kết quả cuối cùng: {Dinghientai}, Giá trị = {GiaTriHienTai}")
            return Dinghientai,GiaTriHienTai
        
        Dinghientai=dinhTotNhat
        GiaTriHienTai=GiaTriTotNhat
        print(f"Di chuyển: {Dinghientai}, Giá trị = {GiaTriHienTai}")

def main(): 
    print('Nhap dinh trong do thi:')
    try: 
        so_dinh=int(input())
        if so_dinh <=0: 
            print('so dinh phai lon khong')
            return
    except ValueError: 
        print('Vui long nhap so nguyen hop le')
        return 
    # so_dinh=3
    gia_tri_dinh={}
    print('Nhap gia tri cho moi dinh: ')
    for _ in range(so_dinh): 
        try: 
            dinh, gia_tri = input().split()
            gia_tri = int(gia_tri)
            gia_tri_dinh[dinh] = gia_tri
        except ValueError:
            print('sai')
            return
    
    do_thi={dinh: [] for dinh in gia_tri_dinh}

    print("Nhập số cạnh trong đồ thị:")
    try:
        so_canh = int(input())
        if so_canh < 0:
            print("Số cạnh không thể âm!")
            return
    except ValueError:
        print("Vui lòng nhập số nguyên hợp lệ!")
        return
    
    print("Nhập các cạnh (ví dụ: 'A B' nghĩa là cạnh từ A đến B):")
    for _ in range(so_canh):
        try:
            dinh1, dinh2 = input().split()
            if dinh1 not in do_thi or dinh2 not in do_thi:
                print(f"Đỉnh {dinh1} hoặc {dinh2} không tồn tại!")
                return
            # Thêm cạnh hai chiều (đồ thị vô hướng)
            do_thi[dinh1].append(dinh2)
            do_thi[dinh2].append(dinh1)
        except ValueError:
            print("Vui lòng nhập định dạng hợp lệ (đỉnh1 đỉnh2)!")
            return
        
    print("Nhập đỉnh bắt đầu:")
    dinh_ban_dau = input().strip()
    if dinh_ban_dau not in do_thi:
        print(f"Đỉnh {dinh_ban_dau} không tồn tại trong đồ thị!")
        return


    print("\nKết quả chạy Simple Hill Climbing:")
    SimpleHillClimbing(do_thi, gia_tri_dinh, dinh_ban_dau)

if __name__ == "__main__":
    main()
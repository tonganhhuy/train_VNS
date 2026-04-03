import time
from typing import List, Generator

def log_action(func):
    """Decorator dùng để tự động ghi log mỗi khi một phương thức được gọi."""
    def wrapper(*args, **kwargs):
        print(f"[LOG - {time.strftime('%H:%M:%S')}] Đang thực thi: {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

class HRDatabase:
    """Context Manager tùy chỉnh để lưu dữ liệu an toàn."""
    def __init__(self, filename: str):
        self.filename = filename
        self.file = None

    def __enter__(self):
        print(f"\n[DB] Đang mở kết nối tới cơ sở dữ liệu: {self.filename}...")
        self.file = open(self.filename, 'a', encoding='utf-8')
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"[DB] Đang đóng kết nối cơ sở dữ liệu {self.filename}.\n")
        if self.file:
            self.file.close()

class Employee:
    """Lớp cha đại diện cho một nhân viên cơ bản."""
    def __init__(self, emp_id: str, name: str, base_salary: float):
        self.emp_id = emp_id
        self.name = name
        self.base_salary = base_salary

    def calculate_salary(self) -> float:
        """Trả về đúng mức lương nhập vào (không phụ cấp)."""
        return self.base_salary

    def __str__(self) -> str:
        # Định dạng lương có dấu phẩy ngăn cách hàng nghìn
        return f"[{self.emp_id}] {self.name.ljust(15)} - Lương nhận: {self.calculate_salary():,.0f} VND"

class Developer(Employee):
    """Lớp con kế thừa Employee."""
    def __init__(self, emp_id: str, name: str, base_salary: float, language: str):
        super().__init__(emp_id, name, base_salary)
        self.language = language

    def calculate_salary(self) -> float:
        """Ghi đè: Chỉ trả về lương cơ bản."""
        return self.base_salary

    def __str__(self) -> str:
        return super().__str__() + f" | Chức vụ: Dev ({self.language})"

class Manager(Employee):
    """Lớp con kế thừa Employee."""
    def __init__(self, emp_id: str, name: str, base_salary: float, team_size: int):
        super().__init__(emp_id, name, base_salary)
        self.team_size = team_size

    def calculate_salary(self) -> float:
        """Ghi đè: Chỉ trả về lương cơ bản."""
        return self.base_salary

    def __str__(self) -> str:
        return super().__str__() + f" | Chức vụ: Manager (Team: {self.team_size})"

class HRSystem:
    def __init__(self):
        self.employees: List[Employee] = []

    @log_action
    def add_employee(self, employee: Employee):
        self.employees.append(employee)
        print(f"  -> Đã thêm nhân viên: {employee.name}")

    @log_action
    def remove_employee(self, emp_id: str) -> bool:
        """Tìm và xóa nhân viên theo mã ID."""
        for i, emp in enumerate(self.employees):
            if emp.emp_id == emp_id:
                removed_emp = self.employees.pop(i)
                print(f"  -> ĐÃ XÓA: {removed_emp.name} (ID: {emp_id})")
                return True
        print(f"  -> THẤT BẠI: Không tìm thấy nhân viên có ID '{emp_id}'")
        return False

    @log_action
    def show_all_employees(self):
        print("\n" + "-"*65)
        print(f"{'DANH SÁCH NHÂN VIÊN':^65}")
        print("-"*65)
        if not self.employees:
            print(f"{'Chưa có dữ liệu nhân viên.':^65}")
        else:
            for emp in self.employees:
                print(emp)
        print("-"*65 + "\n")

    def get_high_earners(self, threshold: float) -> Generator[Employee, None, None]:
        for emp in self.employees:
            if emp.calculate_salary() >= threshold:
                yield emp

    @log_action
    def save_to_database(self, filename: str):
        with HRDatabase(filename) as db_file:
            for emp in self.employees:
                db_file.write(f"{emp.emp_id},{emp.name},{emp.calculate_salary():.0f}\n")
            print("  -> Đã xuất toàn bộ dữ liệu thành công!")

def main_menu():
    hr = HRSystem()
    
    while True:
        print("\n" + "="*45)
        print(f"{'HỆ THỐNG QUẢN LÝ NHÂN SỰ':^45}")
        print("="*45)
        print("1. Thêm Lập trình viên (Developer)")
        print("2. Thêm Quản lý (Manager)")
        print("3. Hiển thị danh sách nhân viên")
        print("4. Lọc nhân viên theo mức lương")
        print("5. Lưu dữ liệu xuống file")
        print("6. Xóa nhân viên theo ID")
        print("0. Thoát chương trình")
        print("="*45)
        
        choice = input("Vui lòng chọn chức năng (0-6): ")
        
        if choice == '1':
            print("\n--- THÊM LẬP TRÌNH VIÊN ---")
            emp_id = input("Mã nhân viên: ")
            name = input("Tên nhân viên: ")
            try:
                base_salary = float(input("Nhập lương nhận (VND): "))
                language = input("Ngôn ngữ lập trình: ")
                hr.add_employee(Developer(emp_id, name, base_salary, language))
            except ValueError:
                print(">> Lỗi: Lương phải là số!")

        elif choice == '2':
            print("\n--- THÊM QUẢN LÝ ---")
            emp_id = input("Mã nhân viên: ")
            name = input("Tên nhân viên: ")
            try:
                base_salary = float(input("Nhập lương nhận (VND): "))
                team_size = int(input("Số nhân viên quản lý: "))
                hr.add_employee(Manager(emp_id, name, base_salary, team_size))
            except ValueError:
                print(">> Lỗi: Dữ liệu nhập vào không hợp lệ!")
                
        elif choice == '3':
            hr.show_all_employees()
            
        elif choice == '4':
            try:
                threshold = float(input("\nNhập mức lương tối thiểu (VND): "))
                print(f"\n--- KẾT QUẢ LỌC (>= {threshold:,.0f} VND) ---")
                found = False
                for earner in hr.get_high_earners(threshold):
                    print(earner)
                    found = True
                if not found: print("Không có nhân viên nào.")
            except ValueError:
                print(">> Lỗi: Mức lương phải là số!")
                
        elif choice == '5':
            filename = input("\nTên file lưu trữ: ")
            hr.save_to_database(filename)

        elif choice == '6':
            print("\n--- XÓA NHÂN VIÊN ---")
            emp_id_to_delete = input("Nhập mã ID cần xóa: ")
            hr.remove_employee(emp_id_to_delete)
            
        elif choice == '0':
            print("\nĐã thoát chương trình. Tạm biệt!")
            break
        else:
            print("\n>> Lựa chọn không hợp lệ!")

if __name__ == "__main__":
    main_menu()
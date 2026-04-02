import time
from typing import List, Generator

def log_action(func):
    """Decorator dùng để tự động ghi log mỗi khi một phương thức được gọi."""
    def wrapper(*args, **kwargs):
        print(f"[LOG - {time.strftime('%H:%M:%S')}] Đang thực thi: {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

class HRDatabase:
    """Context Manager tùy chỉnh để lưu dữ liệu an toàn, tự động đóng file."""
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
        """Phương thức đa hình: Tính lương."""
        return self.base_salary

    def __str__(self) -> str:
        return f"[{self.emp_id}] {self.name} - Lương: {self.calculate_salary():,.0f} VND"

class Developer(Employee):
    """Lớp con kế thừa Employee, đại diện cho Lập trình viên."""
    def __init__(self, emp_id: str, name: str, base_salary: float, language: str):
        super().__init__(emp_id, name, base_salary) # Kế thừa thuộc tính lớp cha
        self.language = language

    def calculate_salary(self) -> float:
        """Ghi đè (Override): Dev có thêm phụ cấp kỹ thuật 2,000,000 VND."""
        return self.base_salary + 2000000

    def __str__(self) -> str:
        return super().__str__() + f" (Dev: {self.language})"

class Manager(Employee):
    """Lớp con kế thừa Employee, đại diện cho Quản lý."""
    def __init__(self, emp_id: str, name: str, base_salary: float, team_size: int):
        super().__init__(emp_id, name, base_salary)
        self.team_size = team_size

    def calculate_salary(self) -> float:
        """Ghi đè: Manager có phụ cấp 500,000 VND cho mỗi nhân viên quản lý."""
        return self.base_salary + (self.team_size * 500000)

    def __str__(self) -> str:
        return super().__str__() + f" (Manager - Team: {self.team_size} người)"

class HRSystem:
    def __init__(self):
        self.employees: List[Employee] = []

    @log_action
    def add_employee(self, employee: Employee):
        self.employees.append(employee)
        print(f"  -> Đã thêm nhân viên: {employee.name}")

    @log_action
    def show_all_employees(self):
        print("\n--- DANH SÁCH NHÂN VIÊN ---")
        if not self.employees:
            print("Chưa có nhân viên nào.")
            return
        for emp in self.employees:
            print(emp)
        print("---------------------------\n")

    def get_high_earners(self, threshold: float) -> Generator[Employee, None, None]:
        """Generator trả về từng nhân viên có lương >= threshold, không tốn thêm RAM."""
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
        print("\n" + "="*35)
        print("   HỆ THỐNG QUẢN LÝ NHÂN SỰ")
        print("="*35)
        print("1. Thêm Lập trình viên (Developer)")
        print("2. Thêm Quản lý (Manager)")
        print("3. Hiển thị danh sách nhân viên")
        print("4. Lọc nhân viên theo mức lương")
        print("5. Lưu dữ liệu xuống file")
        print("0. Thoát chương trình")
        print("="*35)
        
        choice = input("Vui lòng chọn chức năng (0-5): ")
        
        if choice == '1':
            print("\n--- THÊM LẬP TRÌNH VIÊN ---")
            emp_id = input("Nhập mã nhân viên: ")
            name = input("Nhập tên nhân viên: ")
            try:
                base_salary = float(input("Nhập lương cơ bản (VND): "))
            except ValueError:
                print(">> Lỗi: Lương phải là một số hợp lệ. Vui lòng thử lại!")
                continue
            language = input("Nhập ngôn ngữ lập trình: ")
            
            hr.add_employee(Developer(emp_id, name, base_salary, language))
            
        elif choice == '2':
            print("\n--- THÊM QUẢN LÝ ---")
            emp_id = input("Nhập mã nhân viên: ")
            name = input("Nhập tên nhân viên: ")
            try:
                base_salary = float(input("Nhập lương cơ bản (VND): "))
                team_size = int(input("Nhập số nhân viên đang quản lý: "))
            except ValueError:
                print(">> Lỗi: Lương và số nhân viên quản lý phải là số. Vui lòng thử lại!")
                continue
                
            hr.add_employee(Manager(emp_id, name, base_salary, team_size))
            
        elif choice == '3':
            hr.show_all_employees()
            
        elif choice == '4':
            try:
                threshold = float(input("\nNhập mức lương tối thiểu muốn lọc (VND): "))
            except ValueError:
                print(">> Lỗi: Mức lương phải là một số hợp lệ!")
                continue
                
            print(f"\n--- NHÂN VIÊN LƯƠNG >= {threshold:,.0f} VND ---")
            high_earners = hr.get_high_earners(threshold)
            found = False
            
            for earner in high_earners:
                print(earner)
                found = True
                
            if not found:
                print("Không có nhân viên nào đạt mức lương này.")
                
        elif choice == '5':
            filename = input("\nNhập tên file để lưu (VD: data.txt): ")
            hr.save_to_database(filename)
            
        elif choice == '0':
            print("\nĐã thoát chương trình. Tạm biệt!")
            break
        else:
            print("\n>> Lựa chọn không hợp lệ, vui lòng nhập số từ 0 đến 5!")
if __name__ == "__main__":
    main_menu()
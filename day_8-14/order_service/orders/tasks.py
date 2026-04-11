import time

from celery import shared_task


@shared_task
def send_order_email_task(order_id):
    """
    Giả lập việc gửi email gửi mail (tốn thời gian) khi có đơn đặt hàng mới
    """
    print(f"Bắt đầu gửi email xác nhận cho đơn hàng {order_id}...")
    time.sleep(5)  # Giả lập delay
    print(f"Gửi email xác nhận NHẬN ĐƠN HÀNG {order_id} THÀNH CÔNG!")
    return True

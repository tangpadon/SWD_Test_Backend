## Question
![](/assets/q_idempotency.png)
## Response Section
### Idempotency การทำงานซ้ำแล้วได้ผลลัพธ์เดิม 
ใน RESTful API หมายถึง คุณสมบัติของ Endpoint หรือ HTTP Method ที่ไม่ว่าจะถูกเรียกซ้ำกี่ครั้งด้วยพารามิเตอร์เดิม สถานะของระบบบนเซิร์ฟเวอร์จะยังคงเหมือนกับการเรียกใช้งานสำเร็จเพียงครั้งแรกเสมอ
### HTTP Methods
1. Idempotent
- GET: ใช้ดึงข้อมูล ไม่มีการแก้ไขสถานะบนเซิร์ฟเวอร์ เรียกกี่ครั้งผลลัพธ์บนเซิร์ฟเวอร์ก็ไม่เปลี่ยน
- PUT: เป็นการอัปเดตข้อมูลแบบแทนที่ทั้งหมด แม้ส่งข้อมูลเดิมไปบันทึกซ้ำหลายรอบ ข้อมูลปลายทางก็ยังคงเป็นค่านั้น
- DELETE: ลบข้อมูล การลบครั้งแรกทำให้ข้อมูลหายไป การสั่งลบซ้ำครั้งถัดไป ข้อมูลก็ยังคงหายไปเช่นเดิม แม้ Status Code จะเปลี่ยนจาก 200/204 เป็น 404 Not Found แต่สถานะของข้อมูลในระบบถือว่าคงที่

2. Non-Idempotent
- POST: ใช้สำหรับสร้าง Resource ใหม่การยิงคำขอซ้ำจะทำให้เกิดการสร้างข้อมูลเพิ่มขึ้นเรื่อย ๆ

### Implement
`````
from fastapi import FastAPI, Header, status
from pydantic import BaseModel
import time

app = FastAPI()
idempotency_store = {}

class PaymentRequest(BaseModel):
    amount: float

@app.post("/payments", status_code=status.HTTP_201_CREATED)
def process_payment(payload: PaymentRequest, idempotency_key: str = Header(...)):
    if idempotency_key in idempotency_store:
        record = idempotency_store[idempotency_key]
        return {**record, "duplicate": True, "message": "พบ key นี้แล้ว ไม่ตัดเงินซ้ำ"}

    result = {
        "transaction_id": f"test_{int(time.time())}",
        "amount": payload.amount,
        "status": "SUCCESS",
    }
    idempotency_store[idempotency_key] = result
    return {**result, "duplicate": False, "message": "สร้างรายการใหม่และบันทึกไว้"}

print("Server is running on http://127.0.0.1:8000/docs")
`````
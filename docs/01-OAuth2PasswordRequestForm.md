## OAuth2PasswordRequestForm ใช้สำหรับ login เพราะ:

1. OAuth2 Standard:
    - เป็นมาตรฐานที่ใช้กันทั่วโลก
    - ทำให้ระบบ auth เข้ากันได้กับ services อื่นๆ
2. Security:
    - ป้องกัน CSRF attacks ได้ดีกว่า
    - เหมาะกับการส่ง credentials
    - ไม่เก็บ credentials ใน browser history
3. Compatibility:
    - รองรับ OAuth2 clients ทั่วไป
    - ทำงานได้กับ tools เช่น Swagger UI
    - รองรับ third-party authentication
4. Best Practice:
    - แยก authentication จาก API ปกติ
    - ทำให้รู้ชัดว่า endpoint ไหนใช้สำหรับ auth
    - เป็นที่ยอมรับในวงการ security
    - ส่วน endpoints อื่นใช้ JSON เพราะเป็น data operations ปกติที่ไม่เกี่ยวกับ credentials โดยตรง
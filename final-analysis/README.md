## Data analysis steps 🦺

### - Data understanding 🌟

- ดู ประเภทข้อมูล
- ดู duplicate, missing data
- ดู outliers
- ดู การกระจายตัวข้อมูล
- ดู ความ balance ของข้อมูล
- ดู ความสัมพันธ์ของข้อมูล

### - Models 💼

- เลือกมา 4 โมเดล เพื่อทดลอง Logistic, KNN, Decision tree, Bayes

### - Data Cleansing 🔥

แบ่งข้อมูลเป็น 2 ชุด คือ Business กับ Eco แล้วทำกระบวนการเหมือนกันตามด้านล่าง

- ทำ SMOTE แก้ปัญหา imbalanced data
- ตัด outlier
- ตัด missing data

**_ทำการเปรียบเทียบ 2 รูปแบบ_**

**แบบแรก**
dummy feature ที่เป็น object
dummy feature ที่เป็น ordinal (0-5)

**แบบสอง**
dummy feature ที่เป็น object อย่างเดียว

- standardized ข้อมูล

### Test Data with Models ✅

- ทำ 10-fold CV
- ดูเวลาที่ใช้ train
- ดู correlation matrix
- ดู accuracy, precision, recall, sensitivity, specifity, - และอื่น ๆ

### เลือก Model ที่ใช้งาน 🍷

เปรียบเทียบเวลา, performance และอื่น ๆ แต่ละ model เพื่อตัดสินใจให้เข้ากับงาน

### นำไปใช้งาน ✈️

> ปล. เคยมีการทำ feature engineering แล้ว อาจจะลองเอามาใช้เปรียบเทียบด้วย แต่ตอนนี้เอาเท่านี้ให้รอดก่อน


const button = document.getElementById("generate");
const statusEl = document.getElementById("status");
const result = document.getElementById("result");
const output = document.getElementById("output");

button.addEventListener("click", async () => {
  const person = document.getElementById("person").value.trim();

  if (person.length < 2) {
    statusEl.textContent = "กรุณาใส่ชื่อบุคคลอย่างน้อย 2 ตัวอักษร";
    return;
  }

  button.disabled = true;
  button.textContent = "PREPARING...";
  statusEl.textContent = "กำลังส่งข้อมูลไปยังระบบ...";
  result.classList.add("hidden");

  try {
    const response = await fetch(
      "https://display-resale-remindful.ngrok-free.dev/api/generate",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "ngrok-skip-browser-warning": "true"
        },
        body: JSON.stringify({
          person,
          category: document.getElementById("category").value,
          tone: document.getElementById("tone").value,
          duration_seconds: 60,
          language: "ไทย"
        })
      }
    );

    if (!response.ok) {
      throw new Error("API ตอบกลับผิดพลาด: " + response.status);
    }

    const data = await response.json();

    output.textContent = JSON.stringify(data, null, 2);
    result.classList.remove("hidden");
    statusEl.textContent =
      "รับข้อมูลสำเร็จ — สร้าง Production Brief แล้ว";

  } catch (err) {
    statusEl.textContent = "เชื่อมต่อไม่ได้: " + err.message;

  } finally {
    button.disabled = false;
    button.innerHTML =
      'CREATE PRODUCTION BRIEF <span>→</span>';
  }
});

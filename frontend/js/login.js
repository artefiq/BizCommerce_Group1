function login(event) {
    event.preventDefault(); // Mencegah form melakukan submit default
  
    // Ambil nilai dari input email dan password
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const message = document.getElementById("message");
  
    // Cek email dan password (data statis untuk contoh)
    if (email === "user@example.com" && password === "password123") {
      alert("Login successful!");
      window.location.href = "index.html"; // Redirect ke halaman index setelah login berhasil
    } else {
      message.style.display = "block"; // Tampilkan pesan error jika login gagal
    }
  }
  
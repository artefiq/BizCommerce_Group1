function signup(event) {
    event.preventDefault(); // Mencegah form melakukan submit default
  
    // Ambil nilai dari input
    const name = document.getElementById("name").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const confirmPassword = document.getElementById("confirmPassword").value;
    const message = document.getElementById("message");
  
    // Validasi apakah password dan konfirmasi password cocok
    if (password === confirmPassword) {
      alert("Sign up successful!");
      window.location.href = "login.html"; // Redirect ke halaman login setelah signup berhasil
    } else {
      alert("Password not match!");
      message.style.display = "block"; // Tampilkan pesan error jika password tidak cocok
    }
  }
  
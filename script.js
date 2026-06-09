const registroForm = document.getElementById("registroForm");
const registroMensaje = document.getElementById("registroMensaje");

if (registroForm) {
  registroForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const formData = new FormData(registroForm);
    const datosRegistro = {
      nombre: formData.get("nombre").trim(),
      correo: formData.get("correo").trim(),
      telefono: formData.get("telefono").trim(),
    };

    registroMensaje.textContent = "Enviando registro...";
    registroMensaje.className = "registro-mensaje";

    try {
      const respuesta = await fetch("http://localhost:8000/registro", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(datosRegistro),
      });

      const resultado = await respuesta.json();

      if (!respuesta.ok) {
        throw new Error(resultado.detail || "No se pudo enviar el registro.");
      }

      registroMensaje.textContent = resultado.mensaje || "Registro enviado correctamente.";
      registroMensaje.className = "registro-mensaje success";
      registroForm.reset();
    } catch (error) {
      registroMensaje.textContent = `Error: ${error.message}`;
      registroMensaje.className = "registro-mensaje error";
    }
  });
}

const API_JUGADORES_URL = "http://club-uleam-backend-env.eba-ta2ibwhg.us-east-2.elasticbeanstalk.com/jugadores";

const jugadorForm = document.getElementById("jugadorForm");
const jugadorMensaje = document.getElementById("jugadorMensaje");
const jugadoresTablaBody = document.getElementById("jugadoresTablaBody");

function mostrarMensaje(texto, tipo = "") {
  if (!jugadorMensaje) {
    return;
  }

  jugadorMensaje.textContent = texto;
  jugadorMensaje.className = tipo ? `jugador-mensaje ${tipo}` : "jugador-mensaje";
}

function crearCelda(texto) {
  const celda = document.createElement("td");
  celda.textContent = texto;
  return celda;
}

async function cargarJugadores() {
  if (!jugadoresTablaBody) {
    return;
  }

  jugadoresTablaBody.innerHTML = '<tr><td colspan="4">Cargando plantilla...</td></tr>';

  try {
    const respuesta = await fetch(API_JUGADORES_URL);
    const jugadores = await respuesta.json();

    if (!respuesta.ok) {
      throw new Error(jugadores.detail || "No se pudo cargar la plantilla.");
    }

    jugadoresTablaBody.innerHTML = "";

    jugadores.forEach((jugador) => {
      const fila = document.createElement("tr");
      fila.appendChild(crearCelda(jugador.nombre));
      fila.appendChild(crearCelda(jugador.posicion));
      fila.appendChild(crearCelda(jugador.dorsal));
      fila.insertAdjacentHTML(
        "beforeend",
        `<td><button class="delete-player-btn" onclick="eliminarJugador(${jugador.dorsal})" aria-label="Eliminar jugador dorsal ${jugador.dorsal}">X</button></td>`
      );
      jugadoresTablaBody.appendChild(fila);
    });

    if (jugadores.length === 0) {
      jugadoresTablaBody.innerHTML = '<tr><td colspan="4">No hay jugadores registrados.</td></tr>';
    }
  } catch (error) {
    jugadoresTablaBody.innerHTML = `<tr><td colspan="4">Error: ${error.message}</td></tr>`;
  }
}

async function eliminarJugador(dorsal) {
  const confirmarEliminacion = confirm(`Deseas eliminar al jugador con dorsal ${dorsal}?`);

  if (!confirmarEliminacion) {
    return;
  }

  mostrarMensaje("Eliminando jugador...");

  try {
    const respuesta = await fetch(`${API_JUGADORES_URL}/${dorsal}`, {
      method: "DELETE",
    });

    const resultado = await respuesta.json();

    if (!respuesta.ok) {
      throw new Error(resultado.detail || "No se pudo eliminar el jugador.");
    }

    mostrarMensaje(resultado.mensaje || "Jugador eliminado correctamente.", "success");
    await cargarJugadores();
  } catch (error) {
    mostrarMensaje(`Error: ${error.message}`, "error");
  }
}

if (jugadorForm) {
  jugadorForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const formData = new FormData(jugadorForm);
    const nuevoJugador = {
      nombre: formData.get("nombre").trim(),
      posicion: formData.get("posicion").trim(),
      dorsal: Number(formData.get("dorsal")),
    };

    mostrarMensaje("Agregando jugador...");

    try {
      const respuesta = await fetch(API_JUGADORES_URL, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(nuevoJugador),
      });

      const resultado = await respuesta.json();

      if (!respuesta.ok) {
        throw new Error(resultado.detail || "No se pudo agregar el jugador.");
      }

      mostrarMensaje(resultado.mensaje || "Jugador agregado correctamente.", "success");
      jugadorForm.reset();
      await cargarJugadores();
    } catch (error) {
      mostrarMensaje(`Error: ${error.message}`, "error");
    }
  });
}

window.onload = cargarJugadores;

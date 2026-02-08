function cambiarEquipo() {
    const id = document.getElementById("equipoSelect").value;
    window.location.href = "/?equipo=" + id;
}

function guardarCambios() {
    const equipo_id = document.getElementById("equipoSelect").value;
    const puertos = document.querySelectorAll(".puerto");

    let cambios = [];

    puertos.forEach(p => {
        cambios.push({
            id: p.dataset.id,
            numero: p.dataset.numero,
            estado: p.querySelector(".estado").value,
            comentario: p.querySelector(".comentario").value
        });
    });

    fetch("/guardar", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            equipo_id: equipo_id,
            cambios: cambios
        })
    })
    .then(r => r.json())
    .then(() => alert("Cambios guardados correctamente"));
}

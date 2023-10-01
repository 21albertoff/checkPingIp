function actualizarEstado() {
    fetch('resultados.json').then(response => response.json()).then(data => {
        const ips = Object.keys(data);

        ips.forEach(ip => {
            const circle = document.getElementById(ip);

            if (data[ip].length > 0) {
                const ultimoResultado = data[ip][data[ip].length - 1].status;

                if (ultimoResultado === 'OK') {
                    circle.classList.remove('error');
                    circle.classList.add('ok');
                } else {
                    circle.classList.remove('ok');
                    circle.classList.add('error');
                }
            } else {
                circle.classList.remove('ok');
                circle.classList.add('error');
            }
        });
    });
}

// Actualizar el estado inicialmente
actualizarEstado();

// Actualizar el estado cada 15 segundos
setInterval(actualizarEstado, 15000);
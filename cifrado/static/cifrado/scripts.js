// Función para mostrar/ocultar instrucciones
function toggleInstructions() {
    const instructionsBox = document.getElementById('instructionsBox');
    instructionsBox.style.display = instructionsBox.style.display === 'none' || instructionsBox.style.display === '' ? 'block' : 'none';
}

// Función para cifrar o descifrar dependiendo del tipo de cifrado seleccionado
function cifrar() {
    const tipoCifrado = document.getElementById('tipoCifrado').value;
    if (tipoCifrado === 'cesar') {
        cifrarCesar();
    } else {
        cifrarEscitala();
    }
}

function descifrar() {
    const tipoCifrado = document.getElementById('tipoCifrado').value;
    if (tipoCifrado === 'cesar') {
        descifrarCesar();
    } else {
        descifrarEscitala();
    }
}

// Función de cifrado César
function cifrarCesar() {
    const texto = document.getElementById('texto').value;
    const desplazamiento = parseInt(document.getElementById('columnas').value);
    let resultado = '';
    for (let i = 0; i < texto.length; i++) {
        const charCode = texto.charCodeAt(i);
        if (charCode >= 65 && charCode <= 90) {
            resultado += String.fromCharCode(((charCode - 65 + desplazamiento) % 26) + 65);
        } else if (charCode >= 97 && charCode <= 122) {
            resultado += String.fromCharCode(((charCode - 97 + desplazamiento) % 26) + 97);
        } else {
            resultado += texto[i];
        }
    }
    document.getElementById('resultado').innerText = resultado;
}

// Función de descifrado César
function descifrarCesar() {
    const texto = document.getElementById('texto').value;
    const desplazamiento = parseInt(document.getElementById('columnas').value);
    let resultado = '';
    for (let i = 0; i < texto.length; i++) {
        const charCode = texto.charCodeAt(i);
        if (charCode >= 65 && charCode <= 90) {
            resultado += String.fromCharCode(((charCode - 65 - desplazamiento + 26) % 26) + 65);
        } else if (charCode >= 97 && charCode <= 122) {
            resultado += String.fromCharCode(((charCode - 97 - desplazamiento + 26) % 26) + 97);
        } else {
            resultado += texto[i];
        }
    }
    document.getElementById('resultado').innerText = resultado;
}

// Función de cifrado Escítala
function cifrarEscitala() {
    const mensaje = document.getElementById('texto').value.replace(/\s+/g, '');
    const columnas = parseInt(document.getElementById('columnas').value);
    if (!mensaje || columnas <= 0) {
        alert("Por favor, ingresa un texto válido y un número de columnas mayor a 0.");
        return;
    }

    const longitud = mensaje.length;
    const filas = Math.ceil(longitud / columnas);
    const matriz = Array.from({ length: filas }, () => Array(columnas).fill(''));

    // Llenar la matriz con el mensaje
    for (let i = 0; i < longitud; i++) {
        const fila = Math.floor(i / columnas);
        const columna = i % columnas;
        matriz[fila][columna] = mensaje[i];
    }

    let mensajeCifrado = '';
    for (let col = 0; col < columnas; col++) {
        for (let row = 0; row < filas; row++) {
            if (matriz[row][col] !== '') {
                mensajeCifrado += matriz[row][col];
            }
        }
    }

    document.getElementById('resultado').innerText = mensajeCifrado;
}

// Función de descifrado Escítala
function descifrarEscitala() {
    const mensajeCifrado = document.getElementById('texto').value.replace(/\s+/g, '');
    const columnas = parseInt(document.getElementById('columnas').value);
    if (!mensajeCifrado || columnas <= 0) {
        alert("Por favor, ingresa un texto válido y un número de columnas mayor a 0.");
        return;
    }

    const longitud = mensajeCifrado.length;
    const filas = Math.ceil(longitud / columnas);
    const numShortCols = columnas - (filas * columnas - longitud); // Número de columnas cortas
    const matriz = Array.from({ length: filas }, () => Array(columnas).fill(''));

    let index = 0;
    for (let col = 0; col < columnas; col++) {
        for (let row = 0; row < filas; row++) {
            // Las columnas cortas no tienen el último carácter en la última fila
            if (col >= numShortCols && row === filas - 1) continue;
            if (index < longitud) {
                matriz[row][col] = mensajeCifrado[index++];
            }
        }
    }

    let mensajeDescifrado = '';
    for (let row = 0; row < filas; row++) {
        for (let col = 0; col < columnas; col++) {
            if (matriz[row][col] !== '') {
                mensajeDescifrado += matriz[row][col];
            }
        }
    }

    document.getElementById('resultado').innerText = mensajeDescifrado;
}

// Función para copiar el resultado
function copiarResultado() {
    const resultado = document.getElementById('resultado').innerText;
    navigator.clipboard.writeText(resultado).then(() => {
        alert('Resultado copiado al portapapeles.');
    }, () => {
        alert('No se pudo copiar el resultado.');
    });
}
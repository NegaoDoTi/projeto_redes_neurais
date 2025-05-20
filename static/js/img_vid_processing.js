const socket = io();

let socketId = null;

// Recebe o socket_id emitido pelo servidor
socket.on("connect", () => {
    socketId = socket.id;
    console.log("Conectado com socket_id:", socketId);
});

// Evento de resposta de vídeo
socket.on("video_processed", (data) => {
    const videoStatus = document.getElementById("videoStatus");
    const videoResult = document.getElementById("videoResult");
    videoStatus.innerText = "Vídeo processado com sucesso!";
    if (data.url) {
    videoResult.innerHTML = `<video controls class="w-100 mt-2"><source src="${data.url}" type="video/mp4">Seu navegador não suporta vídeo.</video>`;
    }
});

// Manipula envio de imagem
document.getElementById("imageForm").addEventListener("submit", async (e) => {
    e.preventDefault();

    const imageInput = document.getElementById("imageInput");
    const imageStatus = document.getElementById("imageStatus");
    const imageResult = document.getElementById("imageResult");

    if (!imageInput.files[0]) return;

    imageStatus.innerText = "Processando imagem...";
    imageResult.innerHTML = "";

    const formData = new FormData();
    formData.append("image", imageInput.files[0]);

    try {
    const response = await fetch("/processing/image", {
        method: "POST",
        body: formData
    });

    const result = await response.json();

    if (result.url) {
        imageStatus.innerText = "Imagem processada com sucesso!";
        imageResult.innerHTML = `<img src="${result.url}" alt="Imagem processada" class="img-fluid mt-2">`;
    } else {
        imageStatus.innerText = "Erro ao processar imagem.";
    }
    } catch (error) {
    imageStatus.innerText = "Erro na comunicação com o servidor.";
    console.error(error);
    }
});

// Manipula envio de vídeo
document.getElementById("videoForm").addEventListener("submit", async (e) => {
    e.preventDefault();

    const videoInput = document.getElementById("videoInput");
    const videoStatus = document.getElementById("videoStatus");
    const videoResult = document.getElementById("videoResult");

    if (!videoInput.files[0] || !socketId) return;

    videoStatus.innerText = "Processando vídeo...";
    videoResult.innerHTML = "";

    const formData = new FormData();
    formData.append("video", videoInput.files[0]);

    try {
    const response = await fetch(`/processing/video?socket_id=${socketId}`, {
        method: "POST",
        body: formData
    });

    if (!response.ok) {
        throw new Error("Erro ao enviar vídeo.");
    }
    } catch (error) {
    videoStatus.innerText = "Erro ao enviar vídeo.";
    console.error(error);
    }
});
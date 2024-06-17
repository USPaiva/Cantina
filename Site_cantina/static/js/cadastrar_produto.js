document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('form');
    const fotoInput = document.querySelector('#foto');

    form.addEventListener('submit', function(event) {
        const fotoFiles = fotoInput.files;

        if (fotoFiles.length === 0) {
            event.preventDefault();
            alert('Por favor, selecione uma imagem para o produto.');
            return;
        }

        const fotoFile = fotoFiles[0];
        const allowedExtensions = ['png', 'jpg', 'jpeg', 'gif'];
        const fileExtension = fotoFile.name.split('.').pop().toLowerCase();

        if (!allowedExtensions.includes(fileExtension)) {
            event.preventDefault();
            alert('Tipo de arquivo não permitido. Por favor, selecione uma imagem válida (png, jpg, jpeg, gif).');
        }
    });
});
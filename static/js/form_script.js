document.addEventListener('DOMContentLoaded', function() {
    const buttons = document.querySelectorAll('.open-form-popup');

    buttons.forEach(function(button) {
        button.addEventListener('click', function() {
            const formType = button.getAttribute('data-form-type');
            const formContent = document.getElementById(`${formType}-form-popup`).innerHTML;

            let title = '';
            if (formType === 'game') {
                title = 'DODAWANIE GRY';
            } else if (formType === 'platform') {
                title = 'DODAWANIE PLATFORMY';
            } else if (formType === 'play-style') {
                title = 'DODAWANIE STYLU GRY';
            } else if (formType === 'contact') {
                title = 'DODAWANIE NOWEGO KONTAKTU';
            }

            Swal.fire({
                title: title,
                html: formContent,
                showConfirmButton: false,
                customClass: {
                    popup: 'swal__popup',
                    title: 'swal__title'
                },
                color: '#d7d7d7',
                backdrop: 'rgba(0,0,0,0.8)',
                width: '800px'
            });

            const swal__title = document.querySelector('.swal2-title');
            swal__title.style.fontSize = '3rem';
        });
    });
});
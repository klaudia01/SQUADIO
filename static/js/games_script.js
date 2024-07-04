document.getElementById('open-form-popup').addEventListener('click', function() {
    const formContent = document.getElementById('form-popup').innerHTML;
        Swal.fire({
        title: 'DODAWANIE NOWEJ GRY',
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

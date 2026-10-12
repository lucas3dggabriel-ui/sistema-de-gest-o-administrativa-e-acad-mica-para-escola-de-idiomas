document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('aluno-form');
    const listaAlunos = document.getElementById('lista-alunos');

    function carregarAlunos() {
        fetch('/api/alunos')
            .then(response => response.json())
            .then(data => {
                listaAlunos.innerHTML = '';
                data.forEach(aluno => {
                    const li = document.createElement('li');
                    li.textContent = `${aluno.nome} - Curso: ${aluno.curso} (Nota: ${aluno.nota})`;
                    listaAlunos.appendChild(li);
                });
            });
    }

    form.addEventListener('submit', (e) => {
        e.preventDefault();
        const novoAluno = {
            nome: document.getElementById('nome').value,
            curso: document.getElementById('curso').value,
            nota: parseFloat(document.getElementById('nota').value)
        };

        fetch('/api/alunos', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(novoAluno)
        })
        .then(response => response.json())
        .then(data => {
            alert(data.mensagem);
            form.reset();
            carregarAlunos();
        });
    });

    carregarAlunos();
});
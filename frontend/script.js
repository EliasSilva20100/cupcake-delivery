const API_URL = 'http://localhost:5000/api';
let carrinho = [];

// Carregar cupcakes ao iniciar
document.addEventListener('DOMContentLoaded', function() {
    carregarCupcakes();
});

async function carregarCupcakes() {
    try {
        const response = await fetch(`${API_URL}/cupcakes`);
        const cupcakes = await response.json();
        exibirCupcakes(cupcakes);
    } catch (error) {
        console.error('Erro ao carregar cupcakes:', error);
    }
}

function exibirCupcakes(cupcakes) {
    const container = document.getElementById('cupcakes-container');
    container.innerHTML = '';

    cupcakes.forEach(cupcake => {
        const card = document.createElement('div');
        card.className = 'cupcake-card';
        card.innerHTML = `
            <img src="${cupcake.imagem}" alt="${cupcake.sabor}" class="cupcake-imagem">
            <h3>${cupcake.sabor}</h3>
            <p>${cupcake.descricao}</p>
            <div class="cupcake-preco">R$ ${cupcake.preco.toFixed(2)}</div>
            <div>Estoque: ${cupcake.estoque}</div>
            <button class="btn-adicionar" onclick="adicionarAoCarrinho(${cupcake.id}, '${cupcake.sabor}', ${cupcake.preco})">
                Adicionar ao Carrinho
            </button>
        `;
        container.appendChild(card);
    });
}

function adicionarAoCarrinho(id, sabor, preco) {
    const itemExistente = carrinho.find(item => item.id === id);
    
    if (itemExistente) {
        itemExistente.quantidade++;
    } else {
        carrinho.push({
            id: id,
            sabor: sabor,
            preco: preco,
            quantidade: 1
        });
    }
    
    atualizarCarrinho();
}

function removerDoCarrinho(id) {
    carrinho = carrinho.filter(item => item.id !== id);
    atualizarCarrinho();
}

function atualizarCarrinho() {
    const container = document.getElementById('itens-carrinho');
    const totalElement = document.getElementById('total-carrinho');
    
    container.innerHTML = '';
    let total = 0;

    carrinho.forEach(item => {
        const itemTotal = item.preco * item.quantidade;
        total += itemTotal;

        const div = document.createElement('div');
        div.className = 'item-carrinho';
        div.innerHTML = `
            <strong>${item.sabor}</strong>
            <br>Qtd: ${item.quantidade} - R$ ${itemTotal.toFixed(2)}
            <button onclick="removerDoCarrinho(${item.id})" style="margin-left: 10px; color: red; border: none; background: none; cursor: pointer;">
                ❌
            </button>
        `;
        container.appendChild(div);
    });

    totalElement.textContent = total.toFixed(2);
}

function finalizarPedido() {
    if (carrinho.length === 0) {
        alert('Seu carrinho está vazio!');
        return;
    }

    document.getElementById('modal-pedido').style.display = 'block';
}

function fecharModal() {
    document.getElementById('modal-pedido').style.display = 'none';
}

document.getElementById('form-pedido').addEventListener('submit', async function(e) {
    e.preventDefault();

    const pedidoData = {
        cliente_nome: document.getElementById('cliente-nome').value,
        cliente_email: document.getElementById('cliente-email').value,
        cliente_endereco: document.getElementById('cliente-endereco').value,
        total: carrinho.reduce((total, item) => total + (item.preco * item.quantidade), 0),
        itens: carrinho.map(item => ({
            cupcake_id: item.id,
            quantidade: item.quantidade,
            preco_unitario: item.preco
        }))
    };

    try {
        const response = await fetch(`${API_URL}/pedidos`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(pedidoData)
        });

        if (response.ok) {
            alert('Pedido realizado com sucesso!');
            carrinho = [];
            atualizarCarrinho();
            fecharModal();
            document.getElementById('form-pedido').reset();
        } else {
            alert('Erro ao realizar pedido');
        }
    } catch (error) {
        console.error('Erro:', error);
        alert('Erro ao conectar com o servidor');
    }
});

function scrollToSection(sectionId) {
    document.getElementById(sectionId).scrollIntoView({ behavior: 'smooth' });
}
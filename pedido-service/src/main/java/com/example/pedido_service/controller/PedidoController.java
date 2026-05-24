package com.example.pedido_service.controller;

import com.example.pedido_service.dto.*;
import com.example.pedido_service.model.*;
import com.example.pedido_service.repository.PedidoRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.RestTemplate;
import java.util.Date;

@RestController
@RequestMapping("/pedidos")
public class PedidoController {

    @Autowired
    private PedidoRepository pedidoRepository;

    @Autowired
    private RestTemplate restTemplate;

    // Pega as URLs injetadas pelo Docker Compose
    @Value("${URL_CLIENTE}")
    private String urlClienteService;

    @Value("${URL_RESTAURANTE}")
    private String urlRestauranteService;

    @Value("${URL_PRODUTO}")
    private String urlProdutoService;

    @PostMapping
    public ResponseEntity<?> criarPedido(@RequestBody Pedido pedido) {
        try {
            // 1. Valida se Cliente existe no ClienteService (Python)
            String urlCliente = urlClienteService + "/clientes/" + pedido.getIdCliente();
            restTemplate.getForObject(urlCliente, ClienteDTO.class);

            // 2. Valida se Restaurante existe no RestauranteService (Python)
            String urlRestaurante = urlRestauranteService + "/restaurantes/" + pedido.getIdRestaurante();
            restTemplate.getForObject(urlRestaurante, RestauranteDTO.class);

            // 3. Processa itens e valida produtos no ProdutoService (Python)
            double valorTotalPedido = 0.0;
            for (ItemPedido item : pedido.getItens()) {
                String urlProduto = urlProdutoService + "/produtos/" + item.getIdProduto();
                ProdutoDTO produto = restTemplate.getForObject(urlProduto, ProdutoDTO.class);
                
                if (produto == null) {
                    return ResponseEntity.badRequest().body("Produto ID " + item.getIdProduto() + " não encontrado.");
                }

                double subTotal = produto.getVlProduto() * item.getCdQuantidade();
                item.setVlSubTotal(subTotal);
                valorTotalPedido += subTotal;
            }

            pedido.setVlTotal(valorTotalPedido);
            pedido.setDtPedido(new Date());

            Pedido pedidoSalvo = pedidoRepository.save(pedido);
            return ResponseEntity.ok(pedidoSalvo);

        } catch (Exception e) {
            return ResponseEntity.badRequest().body("Erro de comunicação ou dados inválidos: " + e.getMessage());
        }
    }
}
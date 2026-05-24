package com.example.pedido_service.dto;
import lombok.Data;

@Data
public class ProdutoDTO {
    private Integer idProduto;
    private String nmProduto;
    private Double vlProduto;
}
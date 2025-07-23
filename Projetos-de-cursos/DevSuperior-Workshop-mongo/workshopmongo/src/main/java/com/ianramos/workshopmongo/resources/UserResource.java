package com.ianramos.workshopmongo.resources;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RestController;

import com.ianramos.workshopmongo.domain.User;

@RestController
@RequestMapping(value="/users")
public class UserResource {
	
	
	//Para informar que o método vai ser o endpoint no caminho definido acima, novamente um 
	//requestmapping passando qual o método que queremos. Outra forma é usar o "@GetMapping"
	@RequestMapping(method=RequestMethod.GET)
	public ResponseEntity<List<User>> findAll(){
		User maria = new User("1", "Maria Brown", "maria@gmail.com");
		User fogosas = new User("2", "Fogosas", "casadasfogosas@gmail.com");
		//essa nova lista de usuarios instancia um array como implementação do LIST
		//pq o list é uma interface e interfaces não podem ser instanciadas
		List<User> list = new ArrayList<>();
		//agora adicionamos a maria e fogosas (objetos) na lista
		list.addAll(Arrays.asList(maria, fogosas));
		return ResponseEntity.ok().body(list);
		//o ResponseEntity é um objeto sofisticado do Spring que encapsula todas as respostas 
		//em uma estrutura com possíveis cabeçalhos, erros etc
	}
}

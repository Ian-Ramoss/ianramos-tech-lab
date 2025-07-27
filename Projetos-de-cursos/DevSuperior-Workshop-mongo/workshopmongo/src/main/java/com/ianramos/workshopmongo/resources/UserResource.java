package com.ianramos.workshopmongo.resources;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RestController;

import com.ianramos.workshopmongo.domain.User;
import com.ianramos.workshopmongo.services.UserService;

@RestController
@RequestMapping(value="/users")
public class UserResource {
	
	
	@Autowired
	private UserService service;
	
	//Para informar que o método vai ser o endpoint no caminho definido acima, novamente um 
	//requestmapping passando qual o método que queremos. Outra forma é usar o "@GetMapping"
	@RequestMapping(method=RequestMethod.GET)
	public ResponseEntity<List<User>> findAll(){
		
		List<User> list = service.findAll();
		return ResponseEntity.ok().body(list);
		//o ResponseEntity é um objeto sofisticado do Spring que encapsula todas as respostas 
		//em uma estrutura com possíveis cabeçalhos, erros etc
	}
}

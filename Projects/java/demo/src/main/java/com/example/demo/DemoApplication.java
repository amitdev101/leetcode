package com.example.demo;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

//@SpringBootApplication
//@RestController
public class DemoApplication {

	public static void main(String[] args) {
//		SpringApplication.run(DemoApplication.class, args);
		String s = "abcdab";
		Map<Character, Long> result = s.chars().mapToObj(c->(char)c).collect(Collectors.groupingBy(c->c,Collectors.counting()));
		for(Character c: result.keySet()){
			System.out.println(c + result.get(c));
		}




	}
//	@GetMapping
//	public List<String> hello(){
//		List<String> mylist = new ArrayList<>();
//		mylist.add("hello 1");
//		mylist.add("hello 2");
//		return mylist;
//	}


//	String s = "";


}
#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
	Alejandro Valeriano Fernandez - GITT
	Practica 1
	Ejercicio 18.1
	Acortadora de URLs

"""

import webapp
import urllib

class cutURL(webapp.webApp):
	
	dicc={}
	dicc_ind={}
	n = 0
	
	def parse (self,request):
		metodo = request.split(" ", 2)[0]
		if metodo == "GET":
			recurso = request.split(" ", 2)[1][1:]
		elif metodo == "POST":
			if "%3A%2F%2F" in request:
				recurso = request.split("\r\n\r\n", 1)[1].split('=')[1].replace('%3A%2F%2F', '://')
			else:
				recurso = "http://" + request.split("\r\n\r\n", 1)[1].split('=')[1]

		return(metodo, recurso)
			
	def process (self,parsedRequest):

		(metodo, recurso) = parsedRequest
		
		httpCode = 'HTTP/1.1 200 OK\r\n\r\n'
		formulario = '<form action="http://localhost:1234" method="POST">'
		formulario += 'url a acortar: <input type="text" name="url original">'
		formulario += '<input type="submit" value="Enviar">'
		formulario += '</form>'
		
		
		if metodo == 'GET':
			if recurso == '':
				htmlBody = "<html><body>Lista de URLs acortadas: " \
					+ str(self.dicc) \
					+ formulario \
					+ "</body></html>"
			else:
				if recurso in self.dicc_ind.keys():
					httpCode = "300 Redirect"
					htmlBody = "<html><head><meta http-equiv='refresh' content='0;url=" \
						+ str(self.dicc_ind[recurso]) + "'></head></html>"
				else:
					httpCode = "400 Resource not available"
					htmlBody = "Resource not available"
		elif metodo == 'POST':
			if recurso in self.dicc.keys():
				htmlBody = "<html><a href='" + str(recurso) + "'>" \
					+ str(recurso) + "</a> = " \
					+ "<a href='" + str(recurso) + "'> http://localhost:1234/" \
					+ str(self.dicc[recurso]) + "</a></html>"
			else:
				try:
					urllib.urlopen(recurso)
				except IOError:
					return("404 Page not found","<html><head>Page not found</head><body></body>")
					
				self.dicc[recurso] = self.n
				self.dicc_ind[str(self.n)] = recurso
				self.n= self.n + 1
				htmlBody = "<html><a href='" + str(recurso) + "'>" \
					+ str(recurso) + "</a> = " \
					+ "<a href='" + str(recurso) + "'> http://localhost:1234/" \
					+ str(self.dicc[recurso]) + "</a></html>"
		else:
			 htmlBody = "<html><head></head><h1>Método aún no programado</h1></body></html>"

		return (httpCode, htmlBody)
		
if __name__ == "__main__":
	testWebApp = cutURL ("localhost", 1234)

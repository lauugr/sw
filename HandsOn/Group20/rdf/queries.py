
from rdflib import Graph, Namespace, Literal, XSD
from rdflib.plugins.sparql import prepareQuery

# map, PONER AQUI LA RUTA DONDE ESTE EL parkings.ttl
DATA_FILE = "C:/Users/jzaba/OneDrive/Documentos/UPM/4 CURSO/1 Web Semantica/SW-PROYECT/rdf/parkings.ttl"

# namespaces
SCHEMA = Namespace("http://schema.org/")
MY = Namespace("https://data.smartcitymadrid.es/ontology/parking#")
DCT = Namespace("http://purl.org/dc/terms/")
GEO = Namespace("http://www.opengis.net/ont/geosparql#")
EX = Namespace("http://group20.linkeddata.es/parkings/resource/")
g = Graph()

n = g.parse(DATA_FILE, format="turtle")

print("parkings.ttl parseado")

g.bind("schema", SCHEMA)
g.bind("my", MY)
g.bind("dct", DCT)
g.bind("geo", GEO)
g.bind("ex", EX)


#print(query 1, dame los primeros 10 parkings(id,nombre,calle))

q = prepareQuery('''
SELECT ?id ?name ?street WHERE {
  ?p a schema:ParkingFacility ;
     dct:identifier ?id ;
     schema:name ?name ;
     schema:address ?pa .
  ?pa schema:streetAddress ?street .
     
}
ORDER BY ASC(?id)
LIMIT 10
''', initNs={"schema": SCHEMA, "dct": DCT})

for r in g.query(q):
    print(r.id, "   ", r.name, "    ",r.street)
    
    
# QUERY 2 - EMT parkings (true) with postal code
print()
q2 = prepareQuery('''
                 SELECT ?id ?name ?pc ?emtParking 
WHERE {
  ?p a schema:ParkingFacility ;
     dct:identifier ?id ;
     schema:name ?name ;
        schema:address ?pa .
        ?pa schema:postalCode ?pc .
        
  ?p my:isEMTParking ?emtParking .
  FILTER(?emtParking = true)
}
ORDER BY xsd:integer(?id)
LIMIT 10
                 ''',initNs={"schema": SCHEMA, "dct": DCT, "my":MY})
    
for r in g.query(q2):
    print(r.id, "   ", r.name, "    ",r.pc, "   ",r.emtParking)
    
# QUERY 3 - Total number of parkings, cities, regions and countries
print()
q3 = prepareQuery('''
SELECT ?nParkings ?numCities ?numRegions ?numCountries WHERE {
  { SELECT (COUNT(DISTINCT ?p) AS ?nParkings) WHERE { ?p a schema:ParkingFacility } }
  { SELECT (COUNT(DISTINCT ?c) AS ?numCities)  WHERE { ?c a schema:City } }
  { SELECT (COUNT(DISTINCT ?r) AS ?numRegions) WHERE { ?r a my:AutonomousCommunity } }
  { SELECT (COUNT(DISTINCT ?n) AS ?numCountries) WHERE { ?n a schema:Country } }

}
''', initNs={"schema": SCHEMA, "my": MY})
for r in g.query(q3):
    print(r.nParkings, "    ", r.numCities, "   ", r.numRegions, "  ", r.numCountries)

# QUERY 4 - Number of parkings whose address contains “plaza” (case-insensitive)
print()
q4 = prepareQuery('''
SELECT (COUNT(?p) AS ?nParkings)
WHERE {
  ?p a schema:ParkingFacility ;
     schema:address ?pa .
  ?pa schema:streetAddress ?address .
  FILTER(CONTAINS(LCASE(STR(?address)), "plaza"))
}
''', initNs={"schema": SCHEMA})
for r in g.query(q4):
    print(r.nParkings)



# QUERY 5 — nombre + long/lat convirtiendo el literal a IRI
print()

q5 = prepareQuery('''
SELECT ?name ?long ?lat
WHERE {
  ?p a schema:ParkingFacility ;
     schema:name ?name ;
     geo:hasGeometry ?geom .
  ?geom geo:long ?long ;
        geo:lat  ?lat .
}
ORDER BY ASC(?name)
LIMIT 10
''', initNs={"schema": SCHEMA, "geo": GEO})

for r in g.query(q5):
    print(r.name,"  LONG: ",r.long,"    LAT: ",r.lat)
    

# QUERY 6 — nombre + awkt point
print()
print()
q6 = prepareQuery('''
SELECT ?name ?wkt
WHERE {
  ?p a schema:ParkingFacility ;
     schema:name ?name ;
     geo:hasGeometry ?geom .
  ?geom geo:asWKT ?wkt .
}
ORDER BY ASC(?name)
LIMIT 10

''',initNs={"schema":SCHEMA,"geo":GEO}) 

for r in g.query(q6):
    # Si prefieres el literal tal cual: print(r.name, r.wkt)
    print(r.name,"  ", r.wkt)
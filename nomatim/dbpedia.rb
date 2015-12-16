require 'dbpedia'
require 'sparql/client'
require 'rdf'
require 'linkeddata'
require 'logger'
require 'active_support/all'
require_relative './place'


$prefixes = {
     cotext: "http://opendata.cs.pub.ro/context/",
     foaf: "http://xmlns.com/foaf/0.1/",
     rdfs: 'http://www.w3.org/2000/01/rdf-schema#',
     xsd: 'http://www.w3.org/2001/XMLSchema#',
     rdf: 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
     xml: 'http://www.w3.org/XML/1998/namespace',
     owl: 'http://www.w3.org/2002/07/owl#',
     sesame: 'http://www.openrdf.org/schema/sesame#',
     fn: 'http://www.w3.org/2005/xpath-functions#',
     # vcard: VCARD.to_uri,
     ns1: 'http://opendata.cs.pub.ro/property/',
     dbpo: 'http://dbpedia.org/ontology/',
     geo:  'http://www.w3.org/2003/01/geo/wgs84_pos#'
   }

$logger = Logger.new(STDOUT)

def predicate(prefix)
  RDF::URI($prefixes[prefix])
end

def sparql_query
   dbpo =  RDF::URI("http://dbpedia.org/ontology/")

  patterns = [
    [:place, RDF.type, dbpo + "Place"],
    [:place, dbpo + "country", :country]
  ]

  Dbpedia.sparql.select(:place).where(*patterns).filter("regex(?country, 'Romania')")
end

def extract_from_dbpedia
  solutions = sparql_query.solutions

  solutions.each do |sol|
    p sol
    graph = RDF::Graph.load sol.place
    place = {}
    subject = sol.place

    # names
    graph.query([subject, RDF::FOAF.name, nil]) do |statement|
      place["name_#{statement.object.language.to_s}".to_sym] = statement.object.to_s
    end

    # lat, long
    place[:lat] = graph.query([subject, predicate(:geo) + 'lat', nil]).statements.first.try(:object).to_s
    place[:long] = graph.query([subject, predicate(:geo) + 'long', nil]).statements.first.try(:object).to_s

    graph.query([subject, predicate(:dbpo) + 'abstract', nil]) do |statement|
      place["abstract_#{statement.object.language.to_s}".to_sym] = statement.object.to_s
    end

    place[:link] = graph.query([subject, RDF::FOAF.isPrimaryTopicOf, nil]).statements.first.try(:object).to_s

    place[:name] = place[:name_ro] || place[:name_en]
    $logger.info("Saving place #{place[:name_en]}")
    Place.create(place)
  end
end

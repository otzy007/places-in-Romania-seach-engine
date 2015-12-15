require 'elasticsearch/persistence/model'
Elasticsearch::Persistence.client = Elasticsearch::Client.new(host: '192.168.0.103')

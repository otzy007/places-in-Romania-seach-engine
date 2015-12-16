require_relative './config/es'

class Place
  include Elasticsearch::Persistence::Model

  attribute :id, String
  attribute :name, String
  attribute :name_en, String
  attribute :name_ro, String
  attribute :name_fr, String
  attribute :image, String
  attribute :short_description, String
  attribute :link, String
  attribute :map, String
  attribute :osm_id, String
  attribute :lat, String
  attribute :long, String
  attribute :osm_class, String
  attribute :osm_type, String
  attribute :osm_display_name, String
  attribute :address, Hash
  attribute :osm_importance, String
  attribute :alt_names, Hash
end
